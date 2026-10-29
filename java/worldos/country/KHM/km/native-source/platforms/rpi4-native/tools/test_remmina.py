#!/usr/bin/env python3
"""기존 ផ្លូវ 호환 ការបញ្ចូល_ចំនុច. ដែលពិត_ទិន្នន័យ 구현: ../ឧបករណ៍/원격한글시험.py"""
import importlib as 가져오기
import sys as ប្រព័ន្ធប្រតិបត្តិការណ៏_តំលៃ
from pathlib import Path as ផ្លូវ
ប្រព័ន្ធប្រតិបត្តិការណ៏_តំលៃ.path.insert(0, str(ផ្លូវ(__file__).resolve().parents[1] / 'ឧបករណ៍'))
if __name__ == '__main__':
    import runpy as កម្មវិធី_ថត_កម្មវិធី
    កម្មវិធី_ថត_កម្មវិធី.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'រត់', 'profile': 'ទម្រង់', 'focused': 'ដែលផ្តោត', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'ម៉ាស៊ីនមេ_តំលៃ', 'log': 'កំណត់_ហេតុ_ថត', 'args': 'អាគុយម៉ង់_អារេ', 'deadline': '마감시각', 'data': 'ទិន្នន័យ', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'រត់', 'ready': '준비완료', 'found': 'រុករក_ការវាស់វែង', 'guest': 'ភ្ញៀវ', 'ROOT': 'បញ្ចាំង_ឬស', 'marker': '확인표시', 'text': 'អត្ថបទ', 'out': 'ការវាស់វែង_ទិន្នន័យ', 'env': '환경', 'f': 'ឯកសារ_ការបញ្ចូល', 'port': 'លេខរន្ធ', 'offset': 'ការបែង_ភាគ_តំលៃ', 'version': '판번호', 'p': 'ទិន្នន័យ_កំណត់ទីតាំង', 'selector': 'អ្នកជ្រើសរើស', 'xvfb': 'និម្មិត_បង្ហាញ', 'display': 'ឧបករណ៏បង្ហាញ', 'n': '개수', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'ឈ្មោះ', 'window': 'វីនដូ', 'report': 'សុពលភាព_រាយការណ៍', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
