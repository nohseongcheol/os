#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from ئىجرا_قىلىش_بۇيرۇق import كۆرسىتىش_يىلتىز

def ئىجرا_قىل_2():
    ئۆلچەم_مەلۇمات=كۆرسىتىش_يىلتىز/'build/verification/coding';ئۆلچەم_مەلۇمات.mkdir(parents=True,exist_ok=True)
    دەلىللەش_خەۋەر={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((كۆرسىتىش_يىلتىز/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(كۆرسىتىش_يىلتىز/'قوراللار/개발꾸러미내보내기.py')])
        with tarfile.open(str(كۆرسىتىش_يىلتىز/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(ئۆلچەم_مەلۇمات))
        개발꾸러미=ئۆلچەم_مەلۇمات/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(개발꾸러미/'lib/libposix-kor-user.a')]).decode()
        for ئاتى in ('통신종단점만들기','باغلاش_ئادرېس','자료전문보내기','자료전문받기','قۇرۇش_ھۆججەت','파일자료읽기','يازماق_ھۆججەت_مەلۇمات'):
            assert ' T '+ئاتى+'\n' in 심볼목록, ئاتى
        (ئۆلچەم_مەلۇمات/'korean-function-symbols.txt').write_text(심볼목록)
        دەلىللەش_خەۋەر['checks'].append('real-korean-c-function-symbols')
        def ئىجرا_قىلىش_بۇيرۇق(ئاتى,يول,دەلىل_رەت,예상결과):
            مەلۇمات_ئورۇنلاشتۇرۇش=subprocess.run(['python3',str(كۆرسىتىش_يىلتىز/'قوراللار/ئىجرا_قىلىش_ھۆججەت.py'),str(يول)]+دەلىل_رەت,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (ئۆلچەم_مەلۇمات/(ئاتى+'.log')).write_bytes(مەلۇمات_ئورۇنلاشتۇرۇش.stdout);assert مەلۇمات_ئورۇنلاشتۇرۇش.returncode==0,مەلۇمات_ئورۇنلاشتۇرۇش.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in مەلۇمات_ئورۇنلاشتۇرۇش.stdout,مەلۇمات_ئورۇنلاشتۇرۇش.stdout;دەلىللەش_خەۋەر['checks'].append(ئاتى)
        for 뒷부분 in ('c','cpp'):
            실행파일=ئۆلچەم_مەلۇمات/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            ئىجرا_قىلىش_بۇيرۇق('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=ئۆلچەم_مەلۇمات/'ئېقىم_قىممىتى.elf'
        subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples/ئېقىم_قىممىتى.c'),'-o',str(실행파일)])
        ئىجرا_قىلىش_بۇيرۇق('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        ئىجرا_قىلىش_بۇيرۇق('korean-python',كۆرسىتىش_يىلتىز/'예제/한글코딩/인사.py',['--include',str(كۆرسىتىش_يىلتىز/'예제/한글코딩/한국어.py')],'안녕하세요 누리')
        ئىجرا_قىلىش_بۇيرۇق('guest-korean-javac',كۆرسىتىش_يىلتىز/'예제/한글코딩/인사.java',[],'안녕하세요 · 합계=42')
        دەلىللەش_خەۋەر['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(ئۆلچەم_مەلۇمات/'report.json').write_text(json.dumps(دەلىللەش_خەۋەر,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':ئىجرا_قىل_2()
