#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from орындау_пәрмен import жоба_түбір

def Орындау_2():
    өлшем_деректер=жоба_түбір/'build/verification/coding';өлшем_деректер.mkdir(parents=True,exist_ok=True)
    тексерім_есеп={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((жоба_түбір/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(жоба_түбір/'Құралдар/экспорттау_бағдарламалық_құралды_әзірлеуге_арналған_құралдар_жиынтығы.py')])
        with tarfile.open(str(жоба_түбір/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(өлшем_деректер))
        개발꾸러미=өлшем_деректер/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(개발꾸러미/'lib/libposix-kor-user.a')]).decode()
        for Аты in ('жасау_қатысушы','байланыстыру_мекенжай','자료전문보내기','자료전문받기','ашу_файл','파일자료읽기','жазу_файл_деректер'):
            assert ' T '+Аты+'\n' in 심볼목록, Аты
        (өлшем_деректер/'korean-function-symbols.txt').write_text(심볼목록)
        тексерім_есеп['checks'].append('real-korean-c-function-symbols')
        def орындау_пәрмен(Аты,Жол_2,аргумент_массив,예상결과):
            деректер_лауазым=subprocess.run(['python3',str(жоба_түбір/'Құралдар/орындау_файл.py'),str(Жол_2)]+аргумент_массив,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (өлшем_деректер/(Аты+'.log')).write_bytes(деректер_лауазым.stdout);assert деректер_лауазым.returncode==0,деректер_лауазым.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in деректер_лауазым.stdout,деректер_лауазым.stdout;тексерім_есеп['checks'].append(Аты)
        for 뒷부분 in ('c','cpp'):
            실행파일=өлшем_деректер/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            орындау_пәрмен('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=өлшем_деректер/'ағым_мән.elf'
        subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples/ағым_мән.c'),'-o',str(실행파일)])
        орындау_пәрмен('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        орындау_пәрмен('korean-python',жоба_түбір/'예제/한글코딩/인사.py',['--include',str(жоба_түбір/'예제/한글코딩/한국어.py')],'안녕하세요 누리')
        орындау_пәрмен('guest-korean-javac',жоба_түбір/'예제/한글코딩/인사.java',[],'안녕하세요 · 합계=42')
        тексерім_есеп['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(өлшем_деректер/'report.json').write_text(json.dumps(тексерім_есеп,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Орындау_2()
