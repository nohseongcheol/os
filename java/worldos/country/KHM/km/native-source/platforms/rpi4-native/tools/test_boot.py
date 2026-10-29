#!/usr/bin/env python3
"""기존 ផ្លូវ 호환 ការបញ្ចូល_ចំនុច. ដែលពិត_ទិន្នន័យ 구현: ../ឧបករណ៍/부팅시험.py"""
import importlib as 가져오기
import sys as ប្រព័ន្ធប្រតិបត្តិការណ៏_តំលៃ
from pathlib import Path as ផ្លូវ
ប្រព័ន្ធប្រតិបត្តិការណ៏_តំលៃ.path.insert(0, str(ផ្លូវ(__file__).resolve().parents[1] / 'ឧបករណ៍'))
if __name__ == '__main__':
    import runpy as កម្មវិធី_ថត_កម្មវិធី
    កម្មវិធី_ថត_កម្មវិធី.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'ណិតវឺក_សារ', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'ប្រតិបត្តិ', 'cancel': 'បោះបង់_ការវះកាត់', 'cmd_byte': 'ពាក្យបញ្ជា_បៃ', 'reply': 'ឆ្លើយតប', 'points': '지점들', 'server': 'ម៉ាស៊ីនមេ_តំលៃ', 'data': 'ទិន្នន័យ', 'prompt': 'រហ័ស', 'enter': 'បញ្ចូល_851ea840', 'imported': '들여온파일', 'send': 'ផ្ញើ', 'main': 'រត់', 'ROOT': 'បញ្ចាំង_ឬស', 'text': 'អត្ថបទ', 'first_gui': '첫화면', 'pixel': 'ចំនុចតូចៗ', 'java_class': '자바클래스', 'upload': 'បង្ហោះ_ឯកសារ', 'pixels_file': 'ចំនុចតូចៗ_ឯកសារ', 'pixels_data': 'ចំនុចតូចៗ_ទិន្នន័យ', 'edit': 'កែសម្រួល_តំលៃ', 'receive_until': '표시까지받기', 'selector': 'អ្នកជ្រើសរើស', 'size': 'ដាក់ទំហំ', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': 'ប៊ូតុង_Y_កូអរដោនេ', 'result': 'ការវាស់វែង', 'samples': '예제들', 'client': 'អតិថិជន', 'line': 'បន្ទាត់', 'report': 'សុពលភាព_រាយការណ៍', 'work': '작업경로', 'x': 'កូអរដោណេ_x', 'python_checks': '파이썬검사', 'download': 'ទាញយក', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'ដំណើរការ', 'content': 'មាតិកា_តំលៃ', 'block': 'ទិន្នន័យ_ប្លុក', 'marker': '확인표시', 'command': 'ពាក្យ_បញ្ជា', 'expected': '예상결과', 'shell': '셸', 'drawing': 'ការគូរ_ផ្លូវ', 'f': 'ឯកសារ_ការបញ្ចូល', 'transcript': '대화기록', 'offset': 'ការបែង_ភាគ_តំលៃ', 'path': 'ផ្លូវ', 'screenshot': 'រូបថតអេក្រង់', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'ស្ទ្រីម_តំលៃ', 'cmd': '명령인수', 'name': 'ឈ្មោះ', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
