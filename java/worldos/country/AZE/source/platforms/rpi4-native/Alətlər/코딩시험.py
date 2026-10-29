#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from icra_etmək_əmr import Project_kök

def İcra_Et():
    ölçü_verilənlər=Project_kök/'build/verification/coding';ölçü_verilənlər.mkdir(parents=True,exist_ok=True)
    yoxlama_hesabat={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_kök/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(Project_kök/'Alətlər/ixrac_etmək_SDK.py')])
        with tarfile.open(str(Project_kök/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(ölçü_verilənlər))
        개발꾸러미=ölçü_verilənlər/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(개발꾸러미/'lib/libposix-kor-user.a')]).decode()
        for Ad in ('통신종단점만들기','BIND_ünvan','자료전문보내기','자료전문받기','açmaq_fayl','파일자료읽기','yazmaq_fayl_verilənlər'):
            assert ' T '+Ad+'\n' in 심볼목록, Ad
        (ölçü_verilənlər/'korean-function-symbols.txt').write_text(심볼목록)
        yoxlama_hesabat['checks'].append('real-korean-c-function-symbols')
        def icra_etmək_əmr(Ad,Cığır,arqument_ARRAY,예상결과):
            verilənlər_yerinə_qoymaq=subprocess.run(['python3',str(Project_kök/'Alətlər/icra_etmək_fayl.py'),str(Cığır)]+arqument_ARRAY,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (ölçü_verilənlər/(Ad+'.log')).write_bytes(verilənlər_yerinə_qoymaq.stdout);assert verilənlər_yerinə_qoymaq.returncode==0,verilənlər_yerinə_qoymaq.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in verilənlər_yerinə_qoymaq.stdout,verilənlər_yerinə_qoymaq.stdout;yoxlama_hesabat['checks'].append(Ad)
        for 뒷부분 in ('c','cpp'):
            실행파일=ölçü_verilənlər/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            icra_etmək_əmr('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=ölçü_verilənlər/'axın_VALUE.elf'
        subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples/axın_VALUE.c'),'-o',str(실행파일)])
        icra_etmək_əmr('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        icra_etmək_əmr('korean-python',Project_kök/'예제/한글코딩/인사.py',['--include',str(Project_kök/'예제/한글코딩/한국어.py')],'안녕하세요 누리')
        icra_etmək_əmr('guest-korean-javac',Project_kök/'예제/한글코딩/인사.java',[],'안녕하세요 · 합계=42')
        yoxlama_hesabat['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(ölçü_verilənlər/'report.json').write_text(json.dumps(yoxlama_hesabat,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':İcra_Et()
