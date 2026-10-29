#!/usr/bin/env python3
"""기존 path 호환 entryPoint. actualData implementation: ../tools/createImage.py"""
import importlib as takeValue
import sys as operatingSystemValue
from pathlib import Path as path
operatingSystemValue.path.insert(0, str(path(__file__).resolve().parents[1] / 'tools'))
if __name__ == '__main__':
    import runpy as ProgramLauncher
    ProgramLauncher.run_module('createImage', run_name='__main__', alter_sys=True)
else:
    implementation = takeValue.import_module('createImage')
    mappingValue = {'total': 'totalCapacity', 'start': 'run', 'firmware': 'firmwareValue', 'files': 'fileList', 'archive_base': 'archiveBase', 'partition': 'partitionFile', 'archive': 'archive', 'main': 'run', 'block': 'dataBlock', 'ROOT': 'projectRoot', 'boot': 'bootPath', 'stage': 'stageValue', 'out': 'resultData', 'expected': 'expected', 'f': 'fileEntry', 'src': 'originalAddress', 'path': 'path', 'p': 'dataPosition', 'extracted': 'extracted', 'member': 'member', 'mbr': 'MasterBootRecord', 'image': 'image', 'sector_count': 'sectorCount', 'dist': 'distributionPath', 'sha': 'calculateHash', 'license_': 'license_', 'source': 'originalData', 'name': 'name', 'value': 'value', 'manifest': 'bundleManifest', 'dest': 'destinationValuePosition', 'work': 'workingPath'}
    for previousItem, currentItem in mappingValue.items():
        if hasattr(implementation, currentItem): globals()[previousItem] = getattr(implementation, currentItem)
