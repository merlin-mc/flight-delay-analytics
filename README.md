航班延误分析与预测平台 (Flight Delay Analytics)

基于中国五大枢纽机场（北京首都 PEK、深圳宝安 SZX、广州白云 CAN、上海浦东 PVG、上海虹桥 SHA）1126万条航班运行数据，完成从数据清洗、探索性分析到机器学习预测的全流程

数据集
来源：Zenodo 公开数据集 (Flight Operations Data V1.0)
规模：11,723,420 行，13 个字段

技术栈
Python | pandas | scikit-learn | Matplotlib | Jupyter | Git

核心发现
1.延误分布：准点率约 41%，中重度延误（>30分钟）占比约 30%
2. 时间规律：延误呈现明显的累积效应，早 6-7 点准点率最高，晚 20-22 点平均延误飙升至 45 分钟
3. 星期规律：周五延误最严重，平均约 38 分钟，周一最低

机器学习模型
算法：随机森林（RandomForestClassifier）
特征工程：时间特征（小时、星期、月份）+ 机场 One-Hot 编码（共 882 维）
训练数据：从 1126 万条中抽样 100 万条，80% 训练，20% 测试
模型评估：召回率 (Recall) 0.62，ROC-AUC 0.6625，在无天气和空管数据情况下，该基准模型达到业务可用水平

项目结构
flight-delay-analytics/
├── data/
│   ├── raw/  原始数据，5个机场txt文件
│   └── processed/  清洗后数据及可视化结果
├── notebooks/
│   ├── 01_eda.ipynb  探索性分析，延误分布、时间规律
│   └── 02_model.ipynb  特征工程、模型训练与推理预测
├── src/
│   ├── load_all_data.py  数据读取与合并脚本      
│   └── delay_model.pkl  训练好的随机森林模型      
└── README.md
