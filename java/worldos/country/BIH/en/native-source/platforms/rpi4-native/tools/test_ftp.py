#!/usr/bin/env python3
"""기존 path 호환 entryPoint. actualData implementation: ../tools/testFtp.py"""
import importlib as takeValue
import sys as operatingSystemValue
from pathlib import Path as path
operatingSystemValue.path.insert(0, str(path(__file__).resolve().parents[1] / 'tools'))
if __name__ == '__main__':
    import runpy as ProgramLauncher
    ProgramLauncher.run_module('testFtp', run_name='__main__', alter_sys=True)
else:
    implementation = takeValue.import_module('testFtp')
    mappingValue = {'timeout': 'executionTimeout', 'payload': 'payloadData', 'broken': 'broken', 'linux_example': 'linuxExample', 'chunk': 'fragmentValue', 'data': 'data', 'proc': 'process', 'code': 'instructionSequence', 'linux': 'linuxFile', 'archive': 'archive', 'main': 'run', 'net_source': 'netSource', 'temporary': 'temporary', 'static_source': 'staticSource', 'java_source': 'javaSource', 'echo': 'echoServerEntry', 'ROOT': 'projectRoot', 'text': 'text', 'marker': 'marker', 'EchoFixture': 'EchoFixture', 'command': 'command', 'out': 'resultData', 'expected': 'expected', 'server_source': 'serverSource', 'shell': 'shell', 'upload': 'uploadFiles', 'transcript': 'transcript', 'port': 'portNumber', 'native': 'native', 'elf': 'executableFile', 'server_udp_port': 'serverDatagramPort', 'packed': 'packed', 'bridge': 'bridge', 'selector': 'selector', 'end': 'endOffset', 'e': 'auxiliaryEntry', 'ftp': 'fileTransferConnection', 'key': 'pressedValue', 'bytecode': 'bytecode', 'peer': 'peerValue', 'result': 'result', 'unchanged': 'preservedData', 'line': 'line', 'server_tcp_port': 'serverStreamPort', 'source': 'originalData', 'NetworkBridge': 'networkBridge', 'jar': 'javaBundle', 'receive': 'receiveMessage', 'report': 'validationReport'}
    for previousItem, currentItem in mappingValue.items():
        if hasattr(implementation, currentItem): globals()[previousItem] = getattr(implementation, currentItem)
