#!/usr/bin/env python3
"""기존 መተላለፊያ 호환 ምዝግብ_ቦታ. ትክክለኛ_ውሂብ 구현: ../መሳሪያዎች/원격한글시험.py"""
import importlib as 가져오기
import sys as ስርዓተ_ክወና_እሴት
from pathlib import Path as መተላለፊያ
ስርዓተ_ክወና_እሴት.path.insert(0, str(መተላለፊያ(__file__).resolve().parents[1] / 'መሳሪያዎች'))
if __name__ == '__main__':
    import runpy as ፕሮግራም_የመተግበሪያ_መሳቢያ
    ፕሮግራም_የመተግበሪያ_መሳቢያ.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'ማስኬጃ', 'profile': 'መገለጫ', 'focused': 'የተተኮረ', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'አገልጋይ_እሴት', 'log': 'መዝግብ_ረድፍ', 'args': 'ነጋሪ_እሴት_ድርድር', 'deadline': '마감시각', 'data': 'ውሂብ', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'ማስኬጃ', 'ready': '준비완료', 'found': 'ፈልግ_ልኬት', 'guest': 'እንግዳ', 'ROOT': 'አሳይ_ስር', 'marker': '확인표시', 'text': 'ጽሁፍ', 'out': 'ልኬት_ውሂብ', 'env': '환경', 'f': 'ፋይል_ምዝግብ', 'port': 'የወደብ_ቁጥር', 'offset': 'ዝንፍ_እሴት', 'version': '판번호', 'p': 'ውሂብ_በቦታ_አስቀመጠ', 'selector': 'መራጭ', 'xvfb': 'ምናባዊ_ማሳያ', 'display': 'ማሳያ', 'n': '개수', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'ስም', 'window': 'መስኮት', 'report': 'ማረጋገጥ_ዘገባ', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
