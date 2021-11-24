请注意：本仓库是纯个人仓库。
attention: this repo is a purely personal repo.

一：发起本仓库的出发点是paddledetection源码只开源了代码、模型参数，并没有开源导出的inference_model。
(1)如果使用模型参数+ppdet代码进行预测，会导致代码过于庞大，无法拷贝走并部署。
(2)如果使用代码自带的deploy/python/infer.py预测脚本，虽然能够使用inference_model模型、脱离ppdet代码，但是infer.py代码太长，依赖不够简单，对于初级开发人员来说依然无法简单的拷走并部署。
(3)虽然paddledetection给出了导出模型的方法，但是导出模型仍然是一个不大不小的步骤，会依赖一些环境，比如不太好安装的pycocotools
(4)本方法的唯一缺点是导出的模型在运行时需要依赖于导出时的环境，如果预测库更新太大，模型可能无法运行。但我认为这都是小问题，当下好用才是王道。

二：本代码会只使用opencv，numpy等初级新手也会的库，完成一个预测demo，使得用户能够极快的上手。

三：本仓库放一个较小的模型，其他模型存到百度云，以链接的方式给出

四：环境：paddlepaddle 2.1.1版本，gpu版和cpu版都行