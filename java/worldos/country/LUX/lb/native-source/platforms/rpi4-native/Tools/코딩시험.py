#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from ausféieren_Befeel import projezéieren_Racinn

def Laf():
    Mooss_Daten=projezéieren_Racinn/'build/verification/coding';Mooss_Daten.mkdir(parents=True,exist_ok=True)
    Validatioun_mellen={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((projezéieren_Racinn/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(projezéieren_Racinn/'Tools/개발꾸러미내보내기.py')])
        with tarfile.open(str(projezéieren_Racinn/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(Mooss_Daten))
        개발꾸러미=Mooss_Daten/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(개발꾸러미/'lib/libposix-kor-user.a')]).decode()
        for Numm in ('통신종단점만들기','BANNEN_Adress','자료전문보내기','자료전문받기','ariichten_Fichier','파일자료읽기','schreiwen_Fichier_Daten'):
            assert ' T '+Numm+'\n' in 심볼목록, Numm
        (Mooss_Daten/'korean-function-symbols.txt').write_text(심볼목록)
        Validatioun_mellen['checks'].append('real-korean-c-function-symbols')
        def ausféieren_Befeel(Numm,Wee,Argument_ARRAY,예상결과):
            Daten_positionéieren=subprocess.run(['python3',str(projezéieren_Racinn/'Tools/ausféieren_Fichier.py'),str(Wee)]+Argument_ARRAY,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (Mooss_Daten/(Numm+'.log')).write_bytes(Daten_positionéieren.stdout);assert Daten_positionéieren.returncode==0,Daten_positionéieren.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in Daten_positionéieren.stdout,Daten_positionéieren.stdout;Validatioun_mellen['checks'].append(Numm)
        for 뒷부분 in ('c','cpp'):
            실행파일=Mooss_Daten/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            ausféieren_Befeel('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=Mooss_Daten/'Stream_VALUE.elf'
        subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples/Stream_VALUE.c'),'-o',str(실행파일)])
        ausféieren_Befeel('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        ausféieren_Befeel('korean-python',projezéieren_Racinn/'예제/한글코딩/인사.py',['--include',str(projezéieren_Racinn/'예제/한글코딩/한국어.py')],'안녕하세요 누리')
        ausféieren_Befeel('guest-korean-javac',projezéieren_Racinn/'예제/한글코딩/인사.java',[],'안녕하세요 · 합계=42')
        Validatioun_mellen['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(Mooss_Daten/'report.json').write_text(json.dumps(Validatioun_mellen,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Laf()
