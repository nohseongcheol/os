#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ import ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍

def ଚଳାନ୍ତୁ():
    ମାପ_ଡାଟା=ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'build/verification/coding';ମାପ_ଡାଟା.mkdir(parents=True,exist_ok=True)
    ବୈଧକରଣ_ରିପୋର୍ଟ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'ଉପକରଣସମୂହ/개발꾸러미내보내기.py')])
        with tarfile.open(str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(ମାପ_ଡାଟା))
        개발꾸러미=ମାପ_ଡାଟା/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(개발꾸러미/'lib/libposix-kor-user.a')]).decode()
        for ନାମ in ('통신종단점만들기','ବନ୍ଧନ_ଠିକଣା','자료전문보내기','자료전문받기','ଖୋଲିବା_ଫାଇଲ୍','파일자료읽기','ଲିଖନ_ଫାଇଲ୍_ଡାଟା'):
            assert ' T '+ନାମ+'\n' in 심볼목록, ନାମ
        (ମାପ_ଡାଟା/'korean-function-symbols.txt').write_text(심볼목록)
        ବୈଧକରଣ_ରିପୋର୍ଟ['checks'].append('real-korean-c-function-symbols')
        def ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ(ନାମ,ପଥ,ଯୁକ୍ତି_ଆରେ,예상결과):
            ଡାଟା_ସ୍ଥିତି=subprocess.run(['python3',str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'ଉପକରଣସମୂହ/ନିର୍ବାହ_କରିବା_ଫାଇଲ୍.py'),str(ପଥ)]+ଯୁକ୍ତି_ଆରେ,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (ମାପ_ଡାଟା/(ନାମ+'.log')).write_bytes(ଡାଟା_ସ୍ଥିତି.stdout);assert ଡାଟା_ସ୍ଥିତି.returncode==0,ଡାଟା_ସ୍ଥିତି.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in ଡାଟା_ସ୍ଥିତି.stdout,ଡାଟା_ସ୍ଥିତି.stdout;ବୈଧକରଣ_ରିପୋର୍ଟ['checks'].append(ନାମ)
        for 뒷부분 in ('c','cpp'):
            실행파일=ମାପ_ଡାଟା/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=ମାପ_ଡାଟା/'ଷ୍ଟ୍ରିମ୍_ମୂଲ୍ୟ.elf'
        subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples/ଷ୍ଟ୍ରିମ୍_ମୂଲ୍ୟ.c'),'-o',str(실행파일)])
        ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ('korean-python',ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'예제/한글코딩/인사.py',['--include',str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'예제/한글코딩/한국어.py')],'안녕하세요 누리')
        ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ('guest-korean-javac',ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'예제/한글코딩/인사.java',[],'안녕하세요 · 합계=42')
        ବୈଧକରଣ_ରିପୋର୍ଟ['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(ମାପ_ଡାଟା/'report.json').write_text(json.dumps(ବୈଧକରଣ_ରିପୋର୍ଟ,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':ଚଳାନ୍ତୁ()
