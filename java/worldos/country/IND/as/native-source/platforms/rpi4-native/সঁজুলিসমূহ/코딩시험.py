#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from নিষ্পাদন_আদেশ import 기준

def সঞ্চালন():
    পৰিমাপ_ডাটা=기준/'build/verification/coding';পৰিমাপ_ডাটা.mkdir(parents=True,exist_ok=True)
    বৈধতা_ৰিপ_ৰ্ট={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(기준/'সঁজুলিসমূহ/개발꾸러미내보내기.py')])
        with tarfile.open(str(기준/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(পৰিমাপ_ডাটা))
        개발꾸러미=পৰিমাপ_ডাটা/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(개발꾸러미/'lib/libposix-kor-user.a')]).decode()
        for নাম in ('통신종단점만들기','বান্ধক_ঠিকনা','자료전문보내기','자료전문받기','খোলক_ফাইল','파일자료읽기','লিখক_ফাইল_ডাটা'):
            assert ' T '+নাম+'\n' in 심볼목록, নাম
        (পৰিমাপ_ডাটা/'korean-function-symbols.txt').write_text(심볼목록)
        বৈধতা_ৰিপ_ৰ্ট['checks'].append('real-korean-c-function-symbols')
        def নিষ্পাদন_আদেশ(নাম,পথ,যুক্তি_শৃঙ্খলা,예상결과):
            ডাটা_স্থান_সলনি_কৰক=subprocess.run(['python3',str(기준/'সঁজুলিসমূহ/নিষ্পাদন_ফাইল.py'),str(পথ)]+যুক্তি_শৃঙ্খলা,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (পৰিমাপ_ডাটা/(নাম+'.log')).write_bytes(ডাটা_স্থান_সলনি_কৰক.stdout);assert ডাটা_স্থান_সলনি_কৰক.returncode==0,ডাটা_স্থান_সলনি_কৰক.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in ডাটা_স্থান_সলনি_কৰক.stdout,ডাটা_স্থান_সলনি_কৰক.stdout;বৈধতা_ৰিপ_ৰ্ট['checks'].append(নাম)
        for 뒷부분 in ('c','cpp'):
            실행파일=পৰিমাপ_ডাটা/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            নিষ্পাদন_আদেশ('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=পৰিমাপ_ডাটা/'ষ্ট্ৰিম_মান.elf'
        subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples/ষ্ট্ৰিম_মান.c'),'-o',str(실행파일)])
        নিষ্পাদন_আদেশ('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        নিষ্পাদন_আদেশ('korean-python',기준/'예제/한글코딩/인사.py',['--include',str(기준/'예제/한글코딩/한국어.py')],'안녕하세요 누리')
        নিষ্পাদন_আদেশ('guest-korean-javac',기준/'예제/한글코딩/인사.java',[],'안녕하세요 · 합계=42')
        বৈধতা_ৰিপ_ৰ্ট['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(পৰিমাপ_ডাটা/'report.json').write_text(json.dumps(বৈধতা_ৰিপ_ৰ্ট,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':সঞ্চালন()
