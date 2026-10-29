#!/usr/bin/env python3
"""기존 ផ្លូវ 호환 ការបញ្ចូល_ចំនុច. ដែលពិត_ទិន្នន័យ 구현: ../ឧបករណ៍/អនុវត្ត_ពាក្យបញ្ជា.py"""
import importlib as 가져오기
import sys as ប្រព័ន្ធប្រតិបត្តិការណ៏_តំលៃ
from pathlib import Path as ផ្លូវ
ប្រព័ន្ធប្រតិបត្តិការណ៏_តំលៃ.path.insert(0, str(ផ្លូវ(__file__).resolve().parents[1] / 'ឧបករណ៍'))
if __name__ == '__main__':
    import runpy as កម្មវិធី_ថត_កម្មវិធី
    កម្មវិធី_ថត_កម្មវិធី.run_module('អនុវត្ត_ពាក្យបញ្ជា', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('អនុវត្ត_ពាក្យបញ្ជា')
    대응 = {'supported': '지원목록', 'parser': 'មុខងារ_ញែក', 'qemu': '모의기계', 'run_desktop': 'ដំណើរការ_ដែសថប', 'main': 'រត់', 'host': 'ហូស', 'status': 'ភាព_តំលៃ', 'NetworkBridge': '통신다리', 'ROOT': 'បញ្ចាំង_ឬស', 'bridge': '연결다리', 'loader': '적재기', 'base': 'គំរូដែសថប_តំលៃ', 'options': 'ជំរើស', 'binary': 'គោលពីរ', 'args': 'អាគុយម៉ង់_អារេ', 'command': 'ពាក្យ_បញ្ជា'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
