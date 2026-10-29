#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. மொழியாக்கம்_மூலம் 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from 컴파일러 import 컴파일오류

திட்டப்பணி_மூலம் = Path(__file__).resolve().parent

class 기계어번역기:
    def __init__(자신, 입력클래스들, 실행대상='kernel', குவியல்_சொல்_எண்ணிக்கை=262144):
        자신.பாதை_பட்டியல் = [தரவு.பாதை_2 for தரவு in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.குவியல்_சொல்_எண்ணிக்கை = குவியல்_சொல்_எண்ணிக்கை

    def உருவாக்குக(자신, நுழைவுப்_புள்ளி, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            அளவிடக்கூடியது_பாதை = Path(작업)/'generated.c'
            கட்டளை = ['sh', str(திட்டப்பணி_மூலம்/'미리번역.sh'), '--entry', நுழைவுப்_புள்ளி,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.குவியல்_சொல்_எண்ணிக்கை), '-o', str(அளவிடக்கூடியது_பாதை)]
            if 범용문자표기: கட்டளை.append('--ucn')
            for ஒதுக்கு_மதிப்பு in 내보내기목록: கட்டளை.extend(['--export', ஒதுக்கு_மதிப்பு])
            கட்டளை.extend(str(பாதை_2) for பாதை_2 in 자신.பாதை_பட்டியல்)
            அளவிடக்கூடியது = subprocess.run(கட்டளை, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if அளவிடக்கூடியது.returncode: raise 컴파일오류(அளவிடக்கூடியது.stderr.decode('utf-8', 'replace'))
            return அளவிடக்கூடியது_பாதை.read_text()

def செயல்படுத்துக():
    raise SystemExit(subprocess.call(['sh', str(திட்டப்பணி_மூலம்/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': செயல்படுத்துக()
