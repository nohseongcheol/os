#!/usr/bin/env python3
"""기존 ផ្លូវ 호환 ការបញ្ចូល_ចំនុច. ដែលពិត_ទិន្នន័យ 구현: ../ឧបករណ៍/예제시험.py"""
import importlib as 가져오기
import sys as ប្រព័ន្ធប្រតិបត្តិការណ៏_តំលៃ
from pathlib import Path as ផ្លូវ
ប្រព័ន្ធប្រតិបត្តិការណ៏_តំលៃ.path.insert(0, str(ផ្លូវ(__file__).resolve().parents[1] / 'ឧបករណ៍'))
if __name__ == '__main__':
    import runpy as កម្មវិធី_ថត_កម្មវិធី
    កម្មវិធី_ថត_កម្មវិធី.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제시험')
    대응 = {'count': '항목수', 'exact': '정확한값', 'expected_file': '예상파일', 'ftp_port': 'ឯកសារ_ផ្ទេរ_លេខរន្ធ', 'data': 'ទិន្នន័យ', 'graphics_command': 'ក្រាហ្វិក_ពាក្យបញ្ជា', 'main': 'រត់', 'row': 'ជួរដេក_កំណត់ទីតាំង', 'init': '초기값', 'target': 'គោលដៅ', 'ROOT': 'បញ្ចាំង_ឬស', 'text': 'អត្ថបទ', 'binary': 'គោលពីរ', 'out': 'ការវាស់វែង_ទិន្នន័យ', 'entry': 'ការបញ្ចូល_ចំនុច', 'got': '받은수', 'port': 'លេខរន្ធ', 'graphics_start': 'ផ្តើម_ការគូរ', 'col': 'ជួរឈរ_កំណត់ទីតាំង', 'begin': 'ផ្តើម_ការបែង_ភាគ', 'kind': 'ប្រភេទ_តំលៃ', 'selector': 'អ្នកជ្រើសរើស', 'n': '개수', 'key': '누름값', 'y': 'ប៊ូតុង_Y_កូអរដោនេ', 'client': 'អតិថិជន', 'line': 'បន្ទាត់', 'report': 'សុពលភាព_រាយការណ៍', 'language': 'ភាសា', 'x': 'កូអរដោណេ_x', 'start': 'រត់', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'ផ្ញើ_បញ្ជី', 'payload': 'ទិន្នន័យដែលផ្ទុក_ទិន្នន័យ', 'proc': 'ដំណើរការ', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'ឈ្មោះ_តារាង', 'content': 'មាតិកា_តំលៃ', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'ឯកសារ_ការបញ្ចូល_ឈ្មោះ', 'shell': '셸', 'color': '색상', 'transcript': '대화기록', 'offset': 'ការបែង_ភាគ_តំលៃ', 'h': '높이값', 'run': 'អនុវត្ត_ពាក្យបញ្ជា', 'c': 'កូដនៃតួអក្សរ', 'path': 'ផ្លូវ', 'encoding': 'សំណុំតួអក្សរ', 'end': 'បញ្ចប់_ការបែង_ភាគ', 'ftp': 'ឯកសារ_ផ្ទេរ_ការភ្ជាប់', 'pixels': '화소들', 'symbol': 'និមិត្ត_សញ្ញា_តំលៃ', 'source': '원본자료', 'name': 'ឈ្មោះ', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
