#!/usr/bin/env python3
"""기존 path 호환 entryPoint. actualData implementation: ../tools/exampleEcho.py"""
import importlib as takeValue
import sys as operatingSystemValue
from pathlib import Path as path
operatingSystemValue.path.insert(0, str(path(__file__).resolve().parents[1] / 'tools'))
if __name__ == '__main__':
    import runpy as ProgramLauncher
    ProgramLauncher.run_module('exampleEcho', run_name='__main__', alter_sys=True)
else:
    implementation = takeValue.import_module('exampleEcho')
    mappingValue = {'data': 'data', 'sock': 'socketValue', 'tcp_port': 'tcpPort', 'chunk': 'fragmentValue', 'received': 'hasReceived', 'self': 'selfValue', 'UDP': 'datagramHandleRequest', 'thread': 'worker', 'echo': 'echoServerEntry', 'TCP': 'handleConnectionRequest', 'EchoServers': 'EchoServers', 'parser': 'parser', 'server': 'serverValue', 'udp_port': 'udpPort', 'args': 'argumentArray'}
    for previousItem, currentItem in mappingValue.items():
        if hasattr(implementation, currentItem): globals()[previousItem] = getattr(implementation, currentItem)
