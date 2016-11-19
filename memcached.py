#coding=utf-8
'''
Created on 2016年8月18日

@author: sunzhidong
'''
from elasticache_pyclient import MemcacheClient
import boto3

def memcached():
    mc = MemcacheClient('bestvapp-product.rnnzz3.cfg.cnn1.cache.amazonaws.com.cn:11211')
    res = mc.get('laravel:bestv-product-list')
    print(res)
    
#     ret = mc.set('py_test', 'asdf')
#     print(ret)
    
    ret = mc.get('py_test')
    print(ret)
    
def aws_cache():
    client = boto3.client('elasticache')
    response = client.describe_cache_clusters(
             CacheClusterId='bestvapp-product.rnnzz3.cfg.cnn1.cache.amazonaws.com.cn',
             MaxRecords=123,
             ShowCacheNodeInfo=True                               
    )

if __name__ == '__main__':
#     memcached()
    aws_cache()