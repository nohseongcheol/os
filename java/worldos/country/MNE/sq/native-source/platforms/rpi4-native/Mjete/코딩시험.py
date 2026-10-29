#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from zbatoj_komandë import Project_rrënjë

def Ekzekuto():
    llogaritje_të_dhëna=Project_rrënjë/'build/verification/coding';llogaritje_të_dhëna.mkdir(parents=True,exist_ok=True)
    miratim_raport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_rrënjë/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(Project_rrënjë/'Mjete/개발꾸러미내보내기.py')])
        with tarfile.open(str(Project_rrënjë/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(llogaritje_të_dhëna))
        개발꾸러미=llogaritje_të_dhëna/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(개발꾸러미/'lib/libposix-kor-user.a')]).decode()
        for Emër in ('통신종단점만들기','BIND_email','자료전문보내기','자료전문받기','hap_skedar','파일자료읽기','shkruaj_skedar_të_dhëna'):
            assert ' T '+Emër+'\n' in 심볼목록, Emër
        (llogaritje_të_dhëna/'korean-function-symbols.txt').write_text(심볼목록)
        miratim_raport['checks'].append('real-korean-c-function-symbols')
        def zbatoj_komandë(Emër,POZICIONI,argument_ARRAY,예상결과):
            të_dhëna_pozicioni=subprocess.run(['python3',str(Project_rrënjë/'Mjete/zbatoj_skedar.py'),str(POZICIONI)]+argument_ARRAY,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (llogaritje_të_dhëna/(Emër+'.log')).write_bytes(të_dhëna_pozicioni.stdout);assert të_dhëna_pozicioni.returncode==0,të_dhëna_pozicioni.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in të_dhëna_pozicioni.stdout,të_dhëna_pozicioni.stdout;miratim_raport['checks'].append(Emër)
        for 뒷부분 in ('c','cpp'):
            실행파일=llogaritje_të_dhëna/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            zbatoj_komandë('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=llogaritje_të_dhëna/'Stream_VALUE.elf'
        subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples/Stream_VALUE.c'),'-o',str(실행파일)])
        zbatoj_komandë('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        zbatoj_komandë('korean-python',Project_rrënjë/'예제/한글코딩/인사.py',['--include',str(Project_rrënjë/'예제/한글코딩/한국어.py')],'안녕하세요 누리')
        zbatoj_komandë('guest-korean-javac',Project_rrënjë/'예제/한글코딩/인사.java',[],'안녕하세요 · 합계=42')
        miratim_raport['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(llogaritje_të_dhëna/'report.json').write_text(json.dumps(miratim_raport,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Ekzekuto()
