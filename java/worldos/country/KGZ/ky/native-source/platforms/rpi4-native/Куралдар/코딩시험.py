#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from аткаруу_буйрук import 기준

def Жүргүзүү():
    결과자료=기준/'build/verification/coding';결과자료.mkdir(parents=True,exist_ok=True)
    ырастоо_отчет={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(기준/'Куралдар/개발꾸러미내보내기.py')])
        with tarfile.open(str(기준/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(결과자료))
        개발꾸러미=결과자료/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(개발꾸러미/'lib/libposix-kor-user.a')]).decode()
        for Аты in ('통신종단점만들기','байланыштыруу_дарек','자료전문보내기','자료전문받기','ачуу_файл','파일자료읽기','жазуу_файл_берилмелер'):
            assert ' T '+Аты+'\n' in 심볼목록, Аты
        (결과자료/'korean-function-symbols.txt').write_text(심볼목록)
        ырастоо_отчет['checks'].append('real-korean-c-function-symbols')
        def аткаруу_буйрук(Аты,ЖОЛ,аргумент_МАССИВ,예상결과):
            자료위치=subprocess.run(['python3',str(기준/'Куралдар/аткаруу_файл.py'),str(ЖОЛ)]+аргумент_МАССИВ,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (결과자료/(Аты+'.log')).write_bytes(자료위치.stdout);assert 자료위치.returncode==0,자료위치.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in 자료위치.stdout,자료위치.stdout;ырастоо_отчет['checks'].append(Аты)
        for 뒷부분 in ('c','cpp'):
            실행파일=결과자료/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            аткаруу_буйрук('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=결과자료/'агым_маани.elf'
        subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples/агым_маани.c'),'-o',str(실행파일)])
        аткаруу_буйрук('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        аткаруу_буйрук('korean-python',기준/'예제/한글코딩/인사.py',['--include',str(기준/'예제/한글코딩/한국어.py')],'안녕하세요 누리')
        аткаруу_буйрук('guest-korean-javac',기준/'예제/한글코딩/인사.java',[],'안녕하세요 · 합계=42')
        ырастоо_отчет['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(결과자료/'report.json').write_text(json.dumps(ырастоо_отчет,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Жүргүзүү()
