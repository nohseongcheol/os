#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from изпълнявам_команда import проект_корен

def Стартиране():
    мярка_данни=проект_корен/'build/verification/coding';мярка_данни.mkdir(parents=True,exist_ok=True)
    проверка_отчет={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((проект_корен/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(проект_корен/'Инструменти/експортирам_софтуерен_развоен_пакет.py')])
        with tarfile.open(str(проект_корен/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(мярка_данни))
        развоен_пакет=мярка_данни/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(развоен_пакет/'lib/libposix-kor-user.a')]).decode()
        for Име in ('Създаване_участник','обвързвам_адрес','изпращам_дейтаграма_данни','получавам_дейтаграма_данни','отварям_Файл','파일자료읽기','записване_Файл_данни'):
            assert ' T '+Име+'\n' in 심볼목록, Име
        (мярка_данни/'korean-function-symbols.txt').write_text(심볼목록)
        проверка_отчет['checks'].append('real-korean-c-function-symbols')
        def изпълнявам_команда(Име,ПЪТ,аргумент_масив,예상결과):
            данни_позиция=subprocess.run(['python3',str(проект_корен/'Инструменти/изпълнявам_Файл.py'),str(ПЪТ)]+аргумент_масив,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (мярка_данни/(Име+'.log')).write_bytes(данни_позиция.stdout);assert данни_позиция.returncode==0,данни_позиция.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in данни_позиция.stdout,данни_позиция.stdout;проверка_отчет['checks'].append(Име)
        for 뒷부분 in ('c','cpp'):
            실행파일=мярка_данни/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(развоен_пакет/'compile.py'),str(развоен_пакет/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            изпълнявам_команда('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=мярка_данни/'поток_стойност.elf'
        subprocess.check_call(['python3',str(развоен_пакет/'compile.py'),str(развоен_пакет/'examples/поток_стойност.c'),'-o',str(실행파일)])
        изпълнявам_команда('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        изпълнявам_команда('korean-python',проект_корен/'예제/한글코딩/인사.py',['--include',str(проект_корен/'예제/한글코딩/Български.py')],'안녕하세요 누리')
        изпълнявам_команда('guest-korean-javac',проект_корен/'예제/한글코딩/인사.java',[],'안녕하세요 · общо_стойност=42')
        проверка_отчет['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(мярка_данни/'report.json').write_text(json.dumps(проверка_отчет,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Стартиране()
