#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from 실행 import задача_корень

def запустить():
    KR_данные=задача_корень/'build/verification/coding';KR_данные.mkdir(parents=True,exist_ok=True)
    проверка_Отчет={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((задача_корень/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(задача_корень/'инструменты/экспортировать_пакет_SDK.py')])
        with tarfile.open(str(задача_корень/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(KR_данные))
        комплект_SDK=KR_данные/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(комплект_SDK/'lib/libposix-kor-user.a')]).decode()
        for Название in ('Create_участник','BIND_АДРЕС','написать_датаграмма_данные','получить_датаграмма_данные','открыть_файл','чтение_файл_данные','запись_файл_данные'):
            assert ' T '+Название+'\n' in 심볼목록, Название
        (KR_данные/'korean-function-symbols.txt').write_text(심볼목록)
        проверка_Отчет['checks'].append('real-korean-c-function-symbols')
        def 실행(Название,путь,аргумент_МАССИВ,예상결과):
            данные_позиция=subprocess.run(['python3',str(задача_корень/'инструменты/Выполнить_файл.py'),str(путь)]+аргумент_МАССИВ,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (KR_данные/(Название+'.log')).write_bytes(данные_позиция.stdout);assert данные_позиция.returncode==0,данные_позиция.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in данные_позиция.stdout,данные_позиция.stdout;проверка_Отчет['checks'].append(Название)
        for 뒷부분 in ('c','cpp'):
            исполняемый_файл=KR_данные/('приветствие_ae353e94-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(комплект_SDK/'compile.py'),str(комплект_SDK/'examples'/('приветствие_ae353e94.'+뒷부분)),'-o',str(исполняемый_файл)])
            실행('korean-'+뒷부분,исполняемый_файл,[],'posix-kor 호출')
        исполняемый_файл=KR_данные/'поток_ЗНАЧЕН.elf'
        subprocess.check_call(['python3',str(комплект_SDK/'compile.py'),str(комплект_SDK/'examples/поток_ЗНАЧЕН.c'),'-o',str(исполняемый_файл)])
        실행('c-stream-queues',исполняемый_файл,[],'C posix-kor 연결형 коммуникация PASS')
        실행('korean-python',задача_корень/'예제/한글코딩/приветствие_ae353e94.py',['--include',str(задача_корень/'예제/한글코딩/русский.py')],'안녕하세요 누리')
        실행('guest-korean-javac',задача_корень/'예제/한글코딩/приветствие_ae353e94.java',[],'안녕하세요 · итог_ЗНАЧЕН=42')
        проверка_Отчет['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(KR_данные/'report.json').write_text(json.dumps(проверка_Отчет,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':запустить()
