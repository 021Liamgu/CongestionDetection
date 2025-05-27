import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sns
import h5py

class CongestionDetector:
    def __init__(self, data_path, dataset_name, speed_threshold=20):
        """
        Initialize the congestion detector
        :param data_path: Path to the data file
        :param dataset_name: Name of the dataset (for display purposes)
        :param speed_threshold: Speed threshold for congestion (in mph)
        """
        self.data_path = data_path
        self.dataset_name = dataset_name
        self.speed_threshold = speed_threshold
        self.data = None
        self.congestion_matrix = None
        self.timestamps = None
        
    def load_h5_data(self, h5_file, group_name):
        """Load data from H5 file with specific group structure"""
        group = h5_file[group_name]
        values = np.array(group['block0_values'])
        return values
        
    def load_data(self):
        """Load data from file (CSV or H5)"""
        if self.data_path.endswith('.csv'):
            df = pd.read_csv(self.data_path)
            self.timestamps = pd.to_datetime(df['Unnamed: 0'])
            self.data = df.drop('Unnamed: 0', axis=1).values
        else:  # H5 file
            with h5py.File(self.data_path, 'r') as f:
                # Check which group structure we have
                if 'speed' in f:
                    self.data = self.load_h5_data(f, 'speed')
                else:
                    self.data = self.load_h5_data(f, 'df')
                
                # Create timestamps (5-minute intervals)
                if self.dataset_name == 'PEMS-BAY':
                    start_time = pd.Timestamp('2017-01-01')
                else:
                    start_time = pd.Timestamp('2012-03-01')
                self.timestamps = pd.date_range(start=start_time, periods=self.data.shape[0], freq='5min')
    
    def detect_congestion(self):
        """
        Detect congestion based on speed threshold
        Returns a boolean matrix where True indicates congestion
        """
        if self.data is None:
            self.load_data()
        self.congestion_matrix = self.data < self.speed_threshold
        return self.congestion_matrix
    
    def get_congestion_statistics(self):
        """Calculate congestion statistics"""
        if self.congestion_matrix is None:
            self.detect_congestion()
            
        total_points = np.prod(self.congestion_matrix.shape)
        congested_points = np.sum(self.congestion_matrix)
        congestion_ratio = congested_points / total_points
        
        # Extract hour from timestamps
        if isinstance(self.timestamps, pd.Series):
            hours = self.timestamps.dt.hour
        else:
            hours = self.timestamps.hour
        
        # Calculate hourly congestion
        hourly_congestion = []
        for hour in range(24):
            hour_mask = hours == hour
            hour_congestion = np.mean(self.congestion_matrix[hour_mask, :])
            hourly_congestion.append(hour_congestion)
            
        # Calculate congestion by sensor
        sensor_congestion = np.mean(self.congestion_matrix, axis=0)
        most_congested_sensors = np.argsort(sensor_congestion)[-5:]  # Top 5 most congested
        
        # Get time span
        if isinstance(self.timestamps, pd.Series):
            start_date = self.timestamps.iloc[0].strftime('%Y-%m-%d')
            end_date = self.timestamps.iloc[-1].strftime('%Y-%m-%d')
        else:
            start_date = self.timestamps[0].strftime('%Y-%m-%d')
            end_date = self.timestamps[-1].strftime('%Y-%m-%d')
        
        return {
            'overall_congestion_ratio': congestion_ratio,
            'hourly_congestion': hourly_congestion,
            'sensor_congestion': sensor_congestion,
            'most_congested_sensors': most_congested_sensors,
            'num_sensors': self.data.shape[1],
            'time_span': f"{start_date} to {end_date}"
        }
    
    def plot_congestion_patterns(self, ax1, ax2):
        """Plot congestion patterns on given axes"""
        stats = self.get_congestion_statistics()
        
        # Plot 1: Hourly congestion pattern
        ax1.plot(range(24), stats['hourly_congestion'], marker='o', linewidth=2, label=self.dataset_name)
        ax1.set_title('Average Congestion by Hour of Day')
        ax1.set_xlabel('Hour of Day')
        ax1.set_ylabel('Congestion Ratio')
        ax1.grid(True)
        ax1.legend()
        
        # Plot 2: Sensor congestion distribution
        sns.histplot(stats['sensor_congestion'], bins=30, ax=ax2, label=self.dataset_name, alpha=0.5)
        ax2.set_title('Distribution of Congestion Across Sensors')
        ax2.set_xlabel('Congestion Ratio')
        ax2.set_ylabel('Number of Sensors')
        ax2.legend()

def analyze_datasets():
    # Initialize detectors for both datasets
    detectors = [
        CongestionDetector('data/metr_la/metr-la.csv', 'METR-LA'),
        CongestionDetector('data/pems_bay/pems-bay.h5', 'PEMS-BAY')
    ]
    
    # Create figure for comparison plots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12))
    
    # Analyze each dataset
    for detector in detectors:
        # Detect congestion
        detector.detect_congestion()
        
        # Get and print statistics
        stats = detector.get_congestion_statistics()
        print(f"\nResults for {detector.dataset_name}:")
        print(f"Time span: {stats['time_span']}")
        print(f"Number of sensors: {stats['num_sensors']}")
        print(f"Overall congestion ratio: {stats['overall_congestion_ratio']:.2%}")
        print("\nTop 5 most congested sensor locations (sensor IDs):")
        for sensor_idx in stats['most_congested_sensors']:
            congestion_ratio = stats['sensor_congestion'][sensor_idx]
            print(f"Sensor {sensor_idx}: {congestion_ratio:.2%}")
        
        # Add to comparison plots
        detector.plot_congestion_patterns(ax1, ax2)
    
    plt.tight_layout()
    plt.savefig('congestion_comparison.png')
    plt.close()
    print("\nCongestion comparison has been saved to 'congestion_comparison.png'")

if __name__ == "__main__":
    analyze_datasets() 