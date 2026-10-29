#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from kawe_tono import whakaatu_pūtake

def whakahaere():
    mēhua_raraunga=whakaatu_pūtake/'build/verification/coding';mēhua_raraunga.mkdir(parents=True,exist_ok=True)
    whakamana_pūrongo={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((whakaatu_pūtake/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(whakaatu_pūtake/'Ngā_Utauta/개발꾸러미내보내기.py')])
        with tarfile.open(str(whakaatu_pūtake/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(mēhua_raraunga))
        개발꾸러미=mēhua_raraunga/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(개발꾸러미/'lib/libposix-kor-user.a')]).decode()
        for Ingoa in ('통신종단점만들기','BIND_ADDRESS','자료전문보내기','자료전문받기','tiwhikete_kōnae','파일자료읽기','tuhi_kōnae_raraunga'):
            assert ' T '+Ingoa+'\n' in 심볼목록, Ingoa
        (mēhua_raraunga/'korean-function-symbols.txt').write_text(심볼목록)
        whakamana_pūrongo['checks'].append('real-korean-c-function-symbols')
        def kawe_tono(Ingoa,ara,tohenga_HUĀNGA,예상결과):
            raraunga_tūranga=subprocess.run(['python3',str(whakaatu_pūtake/'Ngā_Utauta/kawe_kōnae.py'),str(ara)]+tohenga_HUĀNGA,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (mēhua_raraunga/(Ingoa+'.log')).write_bytes(raraunga_tūranga.stdout);assert raraunga_tūranga.returncode==0,raraunga_tūranga.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in raraunga_tūranga.stdout,raraunga_tūranga.stdout;whakamana_pūrongo['checks'].append(Ingoa)
        for 뒷부분 in ('c','cpp'):
            실행파일=mēhua_raraunga/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            kawe_tono('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=mēhua_raraunga/'roma_uara.elf'
        subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples/roma_uara.c'),'-o',str(실행파일)])
        kawe_tono('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        kawe_tono('korean-python',whakaatu_pūtake/'예제/한글코딩/인사.py',['--include',str(whakaatu_pūtake/'예제/한글코딩/Reo_Māori.py')],'안녕하세요 누리')
        kawe_tono('guest-korean-javac',whakaatu_pūtake/'예제/한글코딩/인사.java',[],'안녕하세요 · 합계=42')
        whakamana_pūrongo['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(mēhua_raraunga/'report.json').write_text(json.dumps(whakamana_pūrongo,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':whakahaere()
