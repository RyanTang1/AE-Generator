#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  2 12:09:17 2018

@author: mancx111
"""
import numpy as np
import json
import argparse
from keras.models import load_model





'''
The class takes model's path and its json file's path as input
'''
class Model_Evaluator(object):
    def __init__(self, model_path, json_path, AE_path='./image_final/'):
        super(Model_Evaluator, self).__init__()
        
        #Grab the attack method using alias. Change the set below to choose which attack to evaluate
        self.set_path = ['Original', 'FGSM', 'I-FGSM', 'Mi-FGSM']
        self.AE_path = AE_path
        
        self.models = [model_path]
        
        self.class_index = json.load(open(json_path))
        self.class_set = set(self.class_index.values())  
    #Private functions that only be called by init
    def load_set(self, set_):
        my_dict = {}

        inputs = np.load(open(self.AE_path+'evaluate_input_'+set_+'.npy'))
        labels = np.load(open(self.AE_path+'evaluate_label_'+set_+'.npy'))
        for key, input_ in zip(labels, inputs):
            if key not in my_dict:
                my_dict[key] = []
            my_dict[key].append(input_)
        return my_dict
            
            
    
    #Private functions that only will be called by evaluate
    def decode_predictions(self, predict):
        argmax = np.argmax(predict, axis=1)
        confidence = np.max(predict, axis=1).sum()
        decode = []
        for label in argmax:
            decode.append(self.class_index[str(label)]) 
        return np.array(decode), confidence
        
    def evaluate(self):
        '''
        The output of this model should be accuracy
        '''
        def calculate_acc(data, model):
            '''
            data is a dictionary where y is the key and X are the value
            '''
            right, total, confidence = 0, 0, 0.0
            for key in data:
                if len(data[key]) == 0 or key not in self.class_set:
                    continue
                y = key
    
                batch = np.vstack(data[y])-127.5
                predict, con = self.decode_predictions(model.predict(batch,batch_size=10))
                right += len(predict[predict==y])
                total += len(data[y])
                confidence += con
            return float(right*100)/total, confidence*100/total
            #print clean_predict.shape
        
        
        
        result = None
        #The deployment should only have one model in self.models
        for model_path in self.models:
            degrade, score_list = 0.0, []
            result = {'robustness':None,'details':[]}
            for path in self.set_path:
                inputs = self.load_set(path)
                score = {}
                acc,confidence = calculate_acc(inputs,load_model(model_path)) ##Need change after deployment
                score['attack_method'] = path.upper()
                score['accuracy'] = str(acc)+'%'
                score['confidence'] = str(confidence)+'%'
                result['details'].append(score)
                score_list.append(acc)
                
                if len(score_list) > 1:
                    degrade += score_list[-1]
            result['robustness'] = str(100*(score_list[0]-degrade/(len(score_list)-1))/score_list[0])

      
        return result
        
            


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", help="model path", default='.')
    parser.add_argument("--index", help="index path", default='./imagenet_class_index.json')
    parser.add_argument("--AE_path", help="Directory of adversarial example", default="./image_final/")
    args = parser.parse_args()               

    model = Model_Evaluator(args.model, args.index, args.AE_path)
    result = model.evaluate()
    print(result)

        
    