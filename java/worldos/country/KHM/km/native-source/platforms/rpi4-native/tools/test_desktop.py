#!/usr/bin/env python3
"""기존 ផ្លូវ 호환 ការបញ្ចូល_ចំនុច. ដែលពិត_ទិន្នន័យ 구현: ../ឧបករណ៍/바탕화면시험.py"""
import importlib as 가져오기
import sys as ប្រព័ន្ធប្រតិបត្តិការណ៏_តំលៃ
from pathlib import Path as ផ្លូវ
ប្រព័ន្ធប្រតិបត្តិការណ៏_តំលៃ.path.insert(0, str(ផ្លូវ(__file__).resolve().parents[1] / 'ឧបករណ៍'))
if __name__ == '__main__':
    import runpy as កម្មវិធី_ថត_កម្មវិធី
    កម្មវិធី_ថត_កម្មវិធី.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('바탕화면시험')
    대응 = {'x': 'កូអរដោណេ_x', 'typing': '글자입력', 'message': '알림문', 'start': 'រត់', 'down': '누르는중', 'exact': '정확한값', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'និមិត្ត_សញ្ញា', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'ដំណើរការ', 'data': 'ទិន្នន័យ', 'main': 'រត់', 'w': '너비값', 'init': '초기값', 'block': 'ទិន្នន័យ_ប្លុក', 'ROOT': 'បញ្ចាំង_ឬស', 'text': 'អត្ថបទ', 'marker': '확인표시', 'report': 'សុពលភាព_រាយការណ៍', 'until': '까지', 'clipboard': 'ឃ្លីបបត_តំលៃ', 'dst': 'ទិសដៅ_អ៊ីម៉ែល', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': 'លេខរន្ធ', 'offset': 'ការបែង_ភាគ_តំលៃ', 'h': '높이값', 'src': '원본주소', 'event': 'ព្រឹត្តិការណ៍', 'encoding': 'សំណុំតួអក្សរ', 'size': 'ដាក់ទំហំ', 'key': '누름값', 'pixels': '화소들', 'y': 'ប៊ូតុង_Y_កូអរដោនេ', 'output': '출력결과', 'symbol': 'និមិត្ត_សញ្ញា_តំលៃ', 'client': 'អតិថិជន', 'char': 'តួអក្សរ_ទិន្នន័យ', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
