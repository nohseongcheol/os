#!/usr/bin/env python3
"""Назад_товар Python 경로를 Java 미리 번역기에 연결한다. ПЕРЕВОД_источник 구현은 СредстваJava/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from компилятор import ошибка_компиляции

задача_корень = Path(__file__).resolve().parent

class компьютер_код_компилятор:
    def __init__(자신, 입력클래스들, выполнение_цель='kernel', куча_статистика=262144):
        자신.путь_Список = [данные.путь for данные in 입력클래스들]
        자신.выполнение_цель = выполнение_цель
        자신.куча_статистика = куча_статистика

    def генерировать(자신, точка_входа, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            KR_путь = Path(작업)/'generated.c'
            команда = ['sh', str(задача_корень/'미리번역.sh'), '--entry', точка_входа,
                    '--profile', 자신.выполнение_цель, '--heap-words', str(자신.куча_статистика), '-o', str(KR_путь)]
            if 범용문자표기: команда.append('--ucn')
            for Назначить_ЗНАЧЕН in 내보내기목록: команда.extend(['--export', Назначить_ЗНАЧЕН])
            команда.extend(str(путь) for путь in 자신.путь_Список)
            результат = subprocess.run(команда, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if результат.returncode: raise ошибка_компиляции(результат.stderr.decode('utf-8', 'replace'))
            return KR_путь.read_text()

def запустить():
    raise SystemExit(subprocess.call(['sh', str(задача_корень/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': запустить()
