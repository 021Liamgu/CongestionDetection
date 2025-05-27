# 交通拥堵检测分析

## 项目概述
本研究对比分析了两个主要城市区域的交通拥堵情况：洛杉矶（METR-LA）和旧金山湾区（PEMS-BAY）。通过处理和分析大规模交通传感器数据，我们深入了解了这两个地区的交通拥堵模式和特征。

## 数据集
由于数据文件较大，未包含在代码仓库中。您需要单独下载数据文件：

### METR-LA 数据集
- 覆盖区域：洛杉矶都会区
- 时间范围：2012年3月1日至2012年6月27日
- 传感器数量：207个
- 数据文件：
  - metr-la.csv (69.43 MB)
  - metr-la.h5 (54.40 MB)

### PEMS-BAY 数据集
- 覆盖区域：旧金山湾区
- 时间范围：2017年1月1日至2017年6月30日
- 传感器数量：325个
- 数据文件：
  - pems-bay.h5 (129.63 MB)

### 数据获取
请联系项目维护者以获取数据文件访问权限。获取后，请按以下结构放置数据文件：

```
HKU_CD/
├── data/
│   ├── metr_la/
│   │   ├── metr-la.csv
│   │   └── metr-la.h5
│   └── pems_bay/
│       └── pems-bay.h5
```

## 安装和运行

1. 克隆仓库：
```bash
git clone https://github.com/021Liamgu/CongestionDetection.git
cd CongestionDetection
```

2. 创建数据目录：
```bash
mkdir -p data/metr_la
mkdir -p data/pems_bay
```

3. 下载并放置数据文件

4. 安装依赖：
```bash
pip install -r requirements.txt
```

5. 运行分析：
```bash
python congestion_detection.py
```

## 主要发现

1. **区域差异**：
   - METR-LA整体拥堵率：10.78%
   - PEMS-BAY整体拥堵率：1.03%

2. **最严重拥堵位置**：
   - METR-LA最高：42.42%（传感器12）
   - PEMS-BAY最高：13.77%（传感器121）

3. **拥堵分布特征**：
   - METR-LA：拥堵分布不均匀，存在明显热点
   - PEMS-BAY：拥堵分布相对均匀

## 可视化结果
运行代码后将生成拥堵分析可视化结果：
- 24小时拥堵模式对比
- 传感器拥堵分布对比

## 联系方式
如需获取数据文件或有任何问题，请联系项目维护者。 