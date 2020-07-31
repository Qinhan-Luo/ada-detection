# -*- encoding: utf-8 -*-
'''
@Time : 2020/6/28 9:31 
@Author : qinhanluo
@File : envs.py 
@Software: PyCharm
@Description ： TODO
'''
import os
from datetime import datetime
import logging

# individual packages
from .fileproc import safeMakeDirs
from .cfg_parser import getConfig

def setLogging(log_dir, stdout_flag):
    safeMakeDirs(log_dir)
    dt = datetime.now()
    log_name = dt.strftime('%Y-%m-%d_%H_%M_%S') + '.log'

    log_fp = os.path.join(log_dir, log_name)

    if stdout_flag:
        logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)
    else:
        logging.basicConfig(filename=log_fp, format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)

def combineConfig(cur_cfg, train_flag):
    ret_cfg = {}
    for k, v in cur_cfg.items():
        if k == 'train' or k == 'test' or k == 'speed':
            continue
        ret_cfg[k] = v
    if train_flag == 1:
        key = 'train'
    elif train_flag == 2:
        key = 'test'
    else:
        key = 'speed'
    for k, v in cur_cfg[key].items():
        ret_cfg[k] = v
    return ret_cfg


def initEnv(train_flag, model_name):
    cfgs_root = 'cfgs'
    cur_cfg = getConfig(cfgs_root, model_name)

    root_dir = cur_cfg['output_root']
    cur_cfg['model_name'] = model_name
    version = cur_cfg['output_version']
    work_dir = os.path.join(root_dir, model_name, version)

    backup_name = cur_cfg['backup_name']
    log_name = cur_cfg['log_name']
    backup_dir = os.path.join(work_dir, backup_name)
    log_dir = os.path.join(work_dir, log_name)

    if train_flag == 1:
        safeMakeDirs(backup_dir)
        stdout_flag = cur_cfg['train']['stdout']
        setLogging(log_dir, stdout_flag)
        cur_cfg['train']['backup_dir'] = backup_dir
    elif train_flag == 2:
        pass
    ret_cfg = combineConfig(cur_cfg, train_flag)
    return ret_cfg

if __name__ == '__main__':
    pass