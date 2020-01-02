## １．根据config/sys_conf.yaml 建立相关文件夹
## ２．下载ASAP数据集放到dataset下　下载bert预训练模型uncased_L-12_H-768_A-12放到bert-model下
## ３．文件介绍
### 3.1 util.py 项目中需要的一些工具类函数，包括读取训练数据到标准格式（tfrecord, xgboost的训练numpy,）， Document类，封装gec的结果
### 3.2 score.py semantic score, coherence score, prompt relevant score 和 overall score的训练和测试相关内容
### 3.3 config:模型训练，推理，存储路径所用的参数配置文件
## ４．数据预处理
### 4.1 调用util.py中read_dataset_into_tfrecord方法读取ASAP数据集转换成asap_dataset.tfrecord格式
### 4.2 调用util.py,使用bert对prompt进行encode,生成prompt.npz文件
### 4.3 调用util.py,将gec_result.txt转换成xgboost所需的npz格式文件
## 5.训练 
### 5.1 python3.5 score.py -model bsp 训练basic score模型 
### 5.2 python3.5 score.py -model csp 训练coherence score模型
### 5.3 python3.5 score.py -model psp 训练prompt relevant score模型
### 5.4 python3.5 score.py -model osp 训练overall score模型

