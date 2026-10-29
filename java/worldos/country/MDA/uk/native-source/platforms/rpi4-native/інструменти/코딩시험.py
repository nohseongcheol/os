#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from Виконати_команда import Дії_корінь

def запустити():
    КР_дані=Дії_корінь/'build/verification/coding';КР_дані.mkdir(parents=True,exist_ok=True)
    перевірка_звіт={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Дії_корінь/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(Дії_корінь/'інструменти/експортувати_пакет_інструментів_розробки.py')])
        with tarfile.open(str(Дії_корінь/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(КР_дані))
        пакет_розробки=КР_дані/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(пакет_розробки/'lib/libposix-kor-user.a')]).decode()
        for Назва in ('Створення_учасник','зв_язувати_адреса','надсилати_дейтаграма_дані','отримувати_дейтаграма_дані','відкрито_Файл','파일자료읽기','записування_Файл_дані'):
            assert ' T '+Назва+'\n' in 심볼목록, Назва
        (КР_дані/'korean-function-symbols.txt').write_text(심볼목록)
        перевірка_звіт['checks'].append('real-korean-c-function-symbols')
        def Виконати_команда(Назва,шлях,аргумент_масив,예상결과):
            дані_посада=subprocess.run(['python3',str(Дії_корінь/'інструменти/Виконати_Файл.py'),str(шлях)]+аргумент_масив,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (КР_дані/(Назва+'.log')).write_bytes(дані_посада.stdout);assert дані_посада.returncode==0,дані_посада.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in дані_посада.stdout,дані_посада.stdout;перевірка_звіт['checks'].append(Назва)
        for 뒷부분 in ('c','cpp'):
            실행파일=КР_дані/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(пакет_розробки/'compile.py'),str(пакет_розробки/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            Виконати_команда('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=КР_дані/'потік_значення.elf'
        subprocess.check_call(['python3',str(пакет_розробки/'compile.py'),str(пакет_розробки/'examples/потік_значення.c'),'-o',str(실행파일)])
        Виконати_команда('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        Виконати_команда('korean-python',Дії_корінь/'예제/한글코딩/인사.py',['--include',str(Дії_корінь/'예제/한글코딩/українська.py')],'안녕하세요 누리')
        Виконати_команда('guest-korean-javac',Дії_корінь/'예제/한글코딩/인사.java',[],'안녕하세요 · усього_значення=42')
        перевірка_звіт['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(КР_дані/'report.json').write_text(json.dumps(перевірка_звіт,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':запустити()
