#!/usr/bin/env python3
"""기존 path 호환 entryPoint. actualData implementation: ../tools/networkBridge.py"""
import importlib as takeValue
import sys as operatingSystemValue
from pathlib import Path as path
operatingSystemValue.path.insert(0, str(path(__file__).resolve().parents[1] / 'tools'))
if __name__ == '__main__':
    import runpy as ProgramLauncher
    ProgramLauncher.run_module('networkBridge', run_name='__main__', alter_sys=True)
else:
    implementation = takeValue.import_module('networkBridge')
    mappingValue = {'response': 'response', 'parts': 'pathComponent', 's': 'stringData', 'i': 'ordinalIndex', 'close': 'close', 'forward': 'forwardingRule', 'slip_input': 'slipInput', 'self': 'selfValue', 'item': 'entryValue', 'flags': 'configurationBits', 'ftp_port': 'fileTransferPortNumber', 'args': 'argumentArray', 'server': 'serverValue', 'data': 'data', 'ethernet_input': 'ethernetInput', 'trace_packet': 'tracePacket', 'GATEWAY': 'gatewayHardwareAddress', 'rule': 'ruleValue', 'protocol': 'NetworkABI', 'forwards': 'forwardingRules', 'occupied': 'occupied', 'host': 'Host', 'ack': 'confirmationNumber', 'serial_port': 'serialPortNumber', 'readers': 'readers', 'guest': 'guest', 'destination': 'destinationDataAddress', 'ethernet_port': 'ethernetPort', 'b': 'secondValue', 'MAC': 'machineAddress', 'arp': 'addressResolutionPacket', 'writable': 'writable', 'direction': 'direction', 'seq': 'orderNumber', 'frame': 'executionFrame', 'loop': 'cycleValue', 'port': 'portNumber', 'offset': 'offsetValue', 'readable': 'canRead', 'c': 'characterCode', 'p': 'dataPosition', 'writers': 'writers', 'IP': 'internetAddressValue', 'e': 'auxiliaryEntry', 'n': 'itemCount', 'packet': 'packetData', 'arguments': 'forwardedArgument', 'source': 'originalData', 'NetworkBridge': 'networkBridge', 'window': 'window', 'capture': 'capture'}
    for previousItem, currentItem in mappingValue.items():
        if hasattr(implementation, currentItem): globals()[previousItem] = getattr(implementation, currentItem)
