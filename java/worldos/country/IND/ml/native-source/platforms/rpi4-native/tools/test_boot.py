#!/usr/bin/env python3
"""기존 വഴി 호환 എന്_ട്രി_പോയിന്_റ്. വാസ്തവമായ_ഡാറ്റാ 구현: ../ഉപകരണങ്ങൾ/부팅시험.py"""
import importlib as 가져오기
import sys as ഓപ്പറേറ്റിംഗ്_സിസ്റ്റം_മൂല്യം
from pathlib import Path as വഴി
ഓപ്പറേറ്റിംഗ്_സിസ്റ്റം_മൂല്യം.path.insert(0, str(വഴി(__file__).resolve().parents[1] / 'ഉപകരണങ്ങൾ'))
if __name__ == '__main__':
    import runpy as പ്രോഗ്രാം_ആപ്പ്_ഡ്രോയർ
    പ്രോഗ്രാം_ആപ്പ്_ഡ്രോയർ.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'നെറ്റ്_വർക്ക്_ഇമെയിൽ', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'പ്രവര്_ത്തിപ്പിയ്ക്കുക', 'cancel': 'റദ്ദാക്കുക_ഓപ്പറേഷൻ', 'cmd_byte': 'കമാന്_ഡ്_బైట్', 'reply': 'മറുപടി_നൽകുക', 'points': '지점들', 'server': 'സെര്_വര്_മൂല്യം', 'data': 'ഡാറ്റാ', 'prompt': 'പ്രോംപ്റ്റ്', 'enter': 'നല്_കുക', 'imported': '들여온파일', 'send': 'അയയ്ക്കുക', 'main': 'നടപ്പിലാക്കുക', 'ROOT': 'പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം', 'text': 'പദാവലി', 'first_gui': '첫화면', 'pixel': 'പെല്', 'java_class': '자바클래스', 'upload': 'അപ്_ലോഡ്_ഫയലുകൾ', 'pixels_file': 'പെല്_ഫയല്', 'pixels_data': 'പെല്_ഡാറ്റാ', 'edit': 'ചിട്ടപ്പെടുത്തല്_മൂല്യം', 'receive_until': '표시까지받기', 'selector': 'సెలక్టర్', 'size': 'വലിപ്പം', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': 'Y_ബട്ടൺ_ഏകോപനം', 'result': 'അളവ്', 'samples': '예제들', 'client': 'ക്ലയന്_റ്', 'line': 'ലൈൻ', 'report': 'నిర్ధారణ_నివేదిక', 'work': '작업경로', 'x': 'x_ഏകോപനം', 'python_checks': '파이썬검사', 'download': 'ഡൗൺലോഡ്', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'പ്രക്രിയ', 'content': 'ഉള്ളടക്കം_മൂല്യം', 'block': 'ഡാറ്റാ_തടയുക', 'marker': '확인표시', 'command': 'ആജ്ഞ', 'expected': '예상결과', 'shell': 'ഷെല്', 'drawing': 'ഡ്രോയിംഗ്_പാത', 'f': 'ഫയല്_എന്_ട്രി', 'transcript': '대화기록', 'offset': 'ഓഫ്_സെറ്റ്_മൂല്യം', 'path': 'വഴി', 'screenshot': 'സ്ക്രീൻഷോട്ട്', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'സ്ട്രീം_മൂല്യം', 'cmd': '명령인수', 'name': 'പേരു്', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
