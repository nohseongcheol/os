#!/usr/bin/env python3
"""기존 ផ្លូវ 호환 ការបញ្ចូល_ចំនុច. ដែលពិត_ទិន្នន័យ 구현: ../ឧបករណ៍/ដែសថប_ការមើល.py"""
import importlib as 가져오기
import sys as ប្រព័ន្ធប្រតិបត្តិការណ៏_តំលៃ
from pathlib import Path as ផ្លូវ
ប្រព័ន្ធប្រតិបត្តិការណ៏_តំលៃ.path.insert(0, str(ផ្លូវ(__file__).resolve().parents[1] / 'ឧបករណ៍'))
if __name__ == '__main__':
    import runpy as កម្មវិធី_ថត_កម្មវិធី
    កម្មវិធី_ថត_កម្មវិធី.run_module('ដែសថប_ការមើល', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ដែសថប_ការមើល')
    대응 = {'count': '항목수', 'special': '특수글쇠', 'error': 'កំហុស', 'exact': '정확한값', 'network': 'ណិតវឺក', 'closed': '닫힘', 'length': 'ប្រវែង_តំលៃ', 'opened': '열림', 'ftp_port': 'ឯកសារ_ផ្ទេរ_លេខរន្ធ', 'server': 'ម៉ាស៊ីនមេ_តំលៃ', 'resources': 'ធនធាន', 'data': 'ទិន្នន័យ', 'shift': 'ឃី_SHIFT', 'send': 'ផ្ញើ', 'run_desktop': 'ដំណើរការ_ដែសថប', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'ហូស', 'text': 'អត្ថបទ', 'korean': '한글여부', 'port': 'លេខរន្ធ', 'signum': '신호번호', 'version': '판번호', 'parser': 'មុខងារ_ញែក', 'bridge': '연결다리', 'kind': 'ប្រភេទ_តំលៃ', 'tail': '끝부분', 'size': 'ដាក់ទំហំ', 'previous_buttons': '이전단추', 'key': '누름값', 'y': 'ប៊ូតុង_Y_កូអរដោនេ', 'prefix': '앞부분', 'client': 'អតិថិជន', 'char': 'តួអក្សរ_ទិន្នន័យ', 'work': '작업경로', 'Keyboard': 'ឃីបត', 'x': 'កូអរដោណេ_x', 'down': '누르는중', 'net': '통신다리항목', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'អាគុយម៉ង់_អារេ', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'ដំណើរការ', 'Desktop': 'ភ្ជាប់_ដែសថប', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'ប្ដូរ_ម៉ូដ', 'command': 'ពាក្យ_បញ្ជា', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'ឃី_CTRL', 'path': 'ផ្លូវ', 'cp': 'តួអក្សរ_ការបំលែងកូដ', 'terminate': '종료시키기', 'security': 'សុវត្ថិភាព', 'vnc_port': '원격화면접속번호', 'body': 'តួអត្ថបទ', 'index': 'រុករក_សន្ទស្សន៏', 'exited': '종료됨', 'keysym': 'ឃី_និមិត្ត_សញ្ញា', 'output': '출력결과', 'keyboard': 'ឃីបត_ការបញ្ចូល', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'អ្នកអាន', 'NetworkBridge': '통신다리', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
