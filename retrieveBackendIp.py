import requests, json, os, yaml, sys
hostFile = sys.argv[1]
with open(hostFile, 'r') as stream:
    data_loaded = yaml.load(stream)
stream.close
controller1 = [*data_loaded['all']['children']['controller']['hosts']][0]
controller2 = [*data_loaded['all']['children']['controller']['hosts']][1]
controller3 = [*data_loaded['all']['children']['controller']['hosts']][2]
print(controller1)
print(controller2)
print(controller3)
