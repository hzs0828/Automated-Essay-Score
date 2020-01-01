import numpy as np
import yaml
import os


# 加载打分系统配置， 主要是系列模型文件的路径
with open("config/sys_conf.yaml", encoding="utf-8") as conf_reader:
    sys_conf = yaml.load(conf_reader.read())
    print("加载完成")


xgboost_train_file_path = os.path.join(sys_conf["data_dir"], "train_set_gec.npz")
features = np.load(xgboost_train_file_path)["features"][()]

print(features)
