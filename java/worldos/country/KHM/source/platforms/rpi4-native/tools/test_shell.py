#!/usr/bin/env python3
"""기존 ផ្លូវ 호환 ការបញ្ចូល_ចំនុច. ដែលពិត_ទិន្នន័យ 구현: ../ឧបករណ៍/셸시험.py"""
import importlib as 가져오기
import sys as ប្រព័ន្ធប្រតិបត្តិការណ៏_តំលៃ
from pathlib import Path as ផ្លូវ
ប្រព័ន្ធប្រតិបត្តិការណ៏_តំលៃ.path.insert(0, str(ផ្លូវ(__file__).resolve().parents[1] / 'ឧបករណ៍'))
if __name__ == '__main__':
    import runpy as កម្មវិធី_ថត_កម្មវិធី
    កម្មវិធី_ថត_កម្មវិធី.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'កូអរដោណេ_x', 'msg': 'ណិតវឺក_សារ', 'i': '순번', 'reply': 'ឆ្លើយតប', 'call': '호출', 'args': 'អាគុយម៉ង់_អារេ', 'chunk': '조각', 'data': 'ទិន្នន័យ', 'proc': 'ដំណើរការ', 'long_text': '긴글', 'restored': '복원자료', 'send': 'ផ្ញើ', 'file': 'ឯកសារ', 'main': 'រត់', 'found': 'រុករក_ការវាស់វែង', 'ROOT': 'បញ្ចាំង_ឬស', 'text': 'អត្ថបទ', 'marker': '확인표시', 'command': 'ពាក្យ_បញ្ជា', 'expected': '예상결과', 'pixel': 'ចំនុចតូចៗ', 'shell': '셸', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'បញ្ចប់_ការបែង_ភាគ', 'image': 'រូបថត', 'key': '누름값', 'y': 'ប៊ូតុង_Y_កូអរដោនេ', 'output': '출력결과', 'result': 'ការវាស់វែង', 'client': 'អតិថិជន', 'line': 'បន្ទាត់', 'stream': 'ស្ទ្រីម_តំលៃ', 'name': 'ឈ្មោះ', 'value': 'តំលៃ', 'receive': '수신하기', 'report': 'សុពលភាព_រាយការណ៍', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
