import numpy as np
import argparse
import cv2
from PIL import Image
import json
import os
from paddle.fluid.core import AnalysisConfig
from paddle.fluid.core import create_paddle_predictor

if __name__ == '__main__':
    #img_info
    imgname_list = ['imgs/niu.jpg', 'imgs/person.png']
    im_size = 608
    score_threshold = 0.1
    #use_gpu = True
    use_gpu = False
    
    #define infer
    #https://paddleinference.paddlepaddle.org.cn/api_reference/python_api_index.html
    config = AnalysisConfig('ppyolo_tiny_650e_coco/model.pdmodel', 'ppyolo_tiny_650e_coco/model.pdiparams')
    config.switch_use_feed_fetch_ops(False) 
    config.enable_memory_optim()
    #if use gpu
    if use_gpu:
        config.enable_use_gpu(1000, 0)
    else:
        config.set_cpu_math_library_num_threads(4)
    predictor = create_paddle_predictor(config)

    #Simulate the prediction of multiple imgs
    fout = open('detect_result.txt', 'w')
    for i in range(len(imgname_list)):
        #img preprocess  
        img = cv2.imread(imgname_list[i])
        img_origin = img.copy()
        img = cv2.resize(img, dsize=(im_size, im_size))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img.astype(np.float32)
        mean = np.array([0.485, 0.456, 0.406], np.float32)
        std = np.array([0.229, 0.224, 0.225], np.float32)
        scale = 255
        img = img / scale
        img = img - mean
        img = img / std
        img = img.transpose((2, 0, 1))
        img = img[np.newaxis, :, :, :]
        im_shape = np.array([img_origin.shape[0], img_origin.shape[1]], np.float32).reshape((1, 2))
        im_scale_factor = np.array([[1, 1]], np.float32)
        input_list = [im_shape, img, im_scale_factor]
   
        #infer
        input_names = predictor.get_input_names() 
        for i2, name in enumerate(input_names):
            input_tensor = predictor.get_input_tensor(name)
            input_tensor.reshape(input_list[i2].shape)   
            input_tensor.copy_from_cpu(input_list[i2].copy())
        predictor.zero_copy_run()
        results = []
        output_names = predictor.get_output_names()
        for i2, name in enumerate(output_names):
            output_tensor = predictor.get_output_tensor(name)
            output_data = output_tensor.copy_to_cpu()
            results.append(output_data)
        results = results[0]

        #filter_by_score_threshold
        index = 0
        for i2 in range(len(results)):
            if(results[i2, 1]<score_threshold):
                results = results[:index, :]
                break
            index += 1

        #write result
            classid2str = ['person' ,'bicycle' ,'car' ,'motorbike' ,'aeroplane' ,'bus' ,'train' ,'truck' ,'boat' \
               ,'traffic_light' ,'fire_hydrant' ,'stop_sign' ,'parking_meter' ,'bench' ,'bird' ,'cat' ,'dog' \
               ,'horse' ,'sheep' ,'cow' ,'elephant' ,'bear' ,'zebra' ,'giraffe' ,'backpack' ,'umbrella' \
               ,'handbag' ,'tie' ,'suitcase' ,'frisbee' ,'skis' ,'snowboard' ,'sports_ball' ,'kite' \
               ,'baseball_bat' ,'baseball_glove' ,'skateboard' ,'surfboard' ,'tennis_racket' ,'bottle' \
               ,'wine_glass' ,'cup' ,'fork' ,'knife' ,'spoon' ,'bowl' ,'banana' ,'apple' ,'sandwich' \
               ,'orange' ,'broccoli' ,'carrot' ,'hot_dog' ,'pizza' ,'donut' ,'cake' ,'chair' ,'sofa' \
               ,'pottedplant' ,'bed' ,'diningtable' ,'toilet' ,'tvmonitor' ,'laptop' ,'mouse' ,'remote' \
               ,'keyboard' ,'cell_phone' ,'microwave' ,'oven' ,'toaster' ,'sink' ,'refrigerator' ,'book' \
               ,'clock' ,'vase' ,'scissors' ,'teddy_bear' ,'hair_drier' ,'toothbrush'] 
        fout.write(imgname_list[i] + '\n')
        fout.write(str(len(results)) + '\n')
        for j in range(len(results)):
            this_result = results[j]
            output_dict = {'imgname':imgname_list[i], 'xmin':round(float(this_result[2]), 3), 'ymin':round(float(this_result[3]), 3), \
                'xmax':round(float(this_result[4]), 3), 'ymax':round(float(this_result[5]), 3), 'score':round(float(this_result[1]), 3), \
                'class_id':int(this_result[0]), 'class_name':classid2str[int(this_result[0])]}
            outstr = json.dumps(output_dict)
            fout.write(outstr + '\n')
    fout.close() 

    #draw
    if(not os.path.exists('drawed_result')):
        os.system('mkdir drawed_result')
    with open('detect_result.txt', 'r') as fin:
        line = fin.readline().strip()
        while(line):
            imgname = line.split('/')[-1]
            img = cv2.imread(line)
            boxnum = fin.readline().strip()
            for i in range(int(boxnum)):
                line = fin.readline().strip()
                boxinfo = json.loads(line)
                cv2.rectangle(img, (int(boxinfo['xmin']), int(boxinfo['ymin'])), (int(boxinfo['xmax']), int(boxinfo['ymax'])), (0, 255, 0), 2)
                cv2.putText(img, str(round(boxinfo['score'], 2)), (int(boxinfo['xmin']), int(boxinfo['ymax'])), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                cv2.putText(img, boxinfo['class_name'], (int(boxinfo['xmin']), int(boxinfo['ymax'] - 30)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            cv2.imwrite('drawed_result/' + imgname, img)
            line = fin.readline().strip()
