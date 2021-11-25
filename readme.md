请注意：本仓库是纯个人仓库。
attention: this repo is a purely personal repo.

### 一
发起本仓库的出发点是paddledetection源码只开源了代码、模型参数，并没有开源导出的inference_model。  
(1)如果使用模型参数+ppdet代码进行预测，会导致代码过于庞大，无法拷贝走并部署。  
(2)如果使用代码自带的deploy/python/infer.py预测脚本，虽然能够使用inference_model模型、脱离ppdet代码，但是infer.py代码太长，依赖不够简单，对于初级开发人员来说依然无法简单的拷走并部署。  
(3)虽然paddledetection给出了导出模型的方法，但是导出模型仍然是一个不大不小的步骤，会依赖一些环境，比如不太好安装的pycocotools  
(4)本方法的唯一缺点是导出的模型在运行时需要依赖于导出时的环境，如果预测库更新太大，模型可能无法运行。但我认为这都是小问题，当下好用才是王道。  

### 二
本代码会只使用opencv，numpy等初级新手也会的库，和一些所必须的paddle api，完成一个预测demo，使得用户能够极快的上手。  

### 三
本仓库放一个较小的模型，其他模型存到百度云，以链接的方式给出  
本仓库文件解释：  
run.sh 启动预测的脚本，假如环境合适，可直接执行sh run.sh  
infer.py 预测脚本，默认不适用gpu，需要修改请打开文件，注释第16行，取消注释第15行；输入图片列表在第12行的imgname_list变量中。用户可自行修改成其他输入方式  
ppyolo_tiny_650e_coco 存放导出的inference model  
imgs 存放输入图片  
drawed_result 存放预测完成后画了矩形框的图，用户尝试执行sh run.sh时，建议先删除本文件夹下的两张图。如果执行run.sh后本文件夹下存下了图，可证明预测成功  
detect_resul.txt 以文本形式存放了预测结果  

### 四
导出环境：本代码使用了paddledetection2.3版本，python3.6。  

### 五
运行环境：paddlepaddle 2.1.1版本，gpu版和cpu版都行。高阶用户可以使用TensorRT等加速库部署。  

### 其他预测模型：
#### ppyolo tiny：链接: https://pan.baidu.com/s/1yNq0KrE70WarcqcRrM-cKg 提取码: i5qm 
#### yolov3 r34：链接: https://pan.baidu.com/s/1Xw2pQk15Ldfn2yA3iVeesA 提取码: a2c7
