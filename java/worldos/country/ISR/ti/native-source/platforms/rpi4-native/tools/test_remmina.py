#!/usr/bin/env python3
"""기존 መገዲ 호환 ምእታው_ነጥቢ. ትኽክለኛ_ሓበሬታ 구현: ../መሳርሒታት/원격한글시험.py"""
import importlib as 가져오기
import sys as ስርዓት_ስርሒት_ዋጋ
from pathlib import Path as መገዲ
ስርዓት_ስርሒት_ዋጋ.path.insert(0, str(መገዲ(__file__).resolve().parents[1] / 'መሳርሒታት'))
if __name__ == '__main__':
    import runpy as መተግበሪ_ተመዛዚ_መተግበሪ
    መተግበሪ_ተመዛዚ_መተግበሪ.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'ኣኺድ', 'profile': 'መግለጺ_መንነት', 'focused': 'ዝተቶኮረ', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'ኣገልጋሊ_ዋጋ', 'log': 'ምዝጉብ_ሪጋ', 'args': 'ሓባሪ_ቁጽሪ_ተርታ', 'deadline': '마감시각', 'data': 'ሓበሬታ', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'ኣኺድ', 'ready': '준비완료', 'found': '찾은결과', 'guest': '커널실행', 'ROOT': '기준', 'marker': '확인표시', 'text': 'ጽሑፍ', 'out': '결과자료', 'env': '환경', 'f': 'ፋይል_ምእታው', 'port': '접속번호', 'offset': 'ሽፋን_ዋጋ', 'version': '판번호', 'p': '자료위치', 'selector': 'መራፂ', 'xvfb': 'መሳሊ_መርኣዪ', 'display': 'መርኣዪ', 'n': '개수', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'ሽም', 'window': 'መስኮት', 'report': 'ምርግጋፅ_ጸብጻብ', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
