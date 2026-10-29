#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from gnìomhaich_àithne import tilg_freumh

def ruith():
    tomhas_dàta=tilg_freumh/'build/verification/coding';tomhas_dàta.mkdir(parents=True,exist_ok=True)
    dearbhadh_aithisg={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((tilg_freumh/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(tilg_freumh/'innealan/개발꾸러미내보내기.py')])
        with tarfile.open(str(tilg_freumh/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(tomhas_dàta))
        개발꾸러미=tomhas_dàta/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(개발꾸러미/'lib/libposix-kor-user.a')]).decode()
        for Ainm in ('통신종단점만들기','BIND_ADDRESS','자료전문보내기','자료전문받기','fosgail_faidhle','파일자료읽기','sgrìobh_faidhle_dàta'):
            assert ' T '+Ainm+'\n' in 심볼목록, Ainm
        (tomhas_dàta/'korean-function-symbols.txt').write_text(심볼목록)
        dearbhadh_aithisg['checks'].append('real-korean-c-function-symbols')
        def gnìomhaich_àithne(Ainm,Slighe,argamaid_ARRAY,예상결과):
            dàta_suidhich=subprocess.run(['python3',str(tilg_freumh/'innealan/gnìomhaich_faidhle.py'),str(Slighe)]+argamaid_ARRAY,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (tomhas_dàta/(Ainm+'.log')).write_bytes(dàta_suidhich.stdout);assert dàta_suidhich.returncode==0,dàta_suidhich.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in dàta_suidhich.stdout,dàta_suidhich.stdout;dearbhadh_aithisg['checks'].append(Ainm)
        for 뒷부분 in ('c','cpp'):
            실행파일=tomhas_dàta/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            gnìomhaich_àithne('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=tomhas_dàta/'sruth_VALUE.elf'
        subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples/sruth_VALUE.c'),'-o',str(실행파일)])
        gnìomhaich_àithne('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        gnìomhaich_àithne('korean-python',tilg_freumh/'예제/한글코딩/인사.py',['--include',str(tilg_freumh/'예제/한글코딩/한국어.py')],'안녕하세요 누리')
        gnìomhaich_àithne('guest-korean-javac',tilg_freumh/'예제/한글코딩/인사.java',[],'안녕하세요 · 합계=42')
        dearbhadh_aithisg['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(tomhas_dàta/'report.json').write_text(json.dumps(dearbhadh_aithisg,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':ruith()
