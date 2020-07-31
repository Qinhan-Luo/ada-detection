# -*- encoding: utf-8 -*-
'''
@Time : 2020/6/28 9:22 
@Author : qinhanluo
@File : cfg_parser.py 
@Software: PyCharm
@Description ： TODO
'''
import yaml
import sys
import logging as log
import os
#TODO, ADD SOME LOGFILES

def parse(fp):
    with open(fp, 'r') as fd:
        cont = fd.read()
        y = yaml.load(cont, Loader=yaml.FullLoader)
        return y

def getConfig(cfgs_root, model_name):
    main_cfg = parse('%s/main.yml' % cfgs_root)
    if model_name not in main_cfg['cfg_dict'].keys():
        models = ', '.join(main_cfg['cfg_dict'].keys())
        print('There are models like %s\n' % models, file=sys.stderr)
        raise Exception
    cfg_fp = './' + cfgs_root + '/' + main_cfg['cfg_dict'][model_name]
    config = parse(cfg_fp)
    return config