#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from uitvoer_bevel import Project_wortel

def Loop():
    maatreël_data=Project_wortel/'build/verification/coding';maatreël_data.mkdir(parents=True,exist_ok=True)
    validering_verslag={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_wortel/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(Project_wortel/'Nutsmiddels/개발꾸러미내보내기.py')])
        with tarfile.open(str(Project_wortel/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(maatreël_data))
        개발꾸러미=maatreël_data/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(개발꾸러미/'lib/libposix-kor-user.a')]).decode()
        for Naam in ('통신종단점만들기','BIND_adres','자료전문보내기','자료전문받기','skep_lêer','파일자료읽기','skryf_lêer_data'):
            assert ' T '+Naam+'\n' in 심볼목록, Naam
        (maatreël_data/'korean-function-symbols.txt').write_text(심볼목록)
        validering_verslag['checks'].append('real-korean-c-function-symbols')
        def uitvoer_bevel(Naam,Pad,argument_ARRAY,예상결과):
            data_plaas=subprocess.run(['python3',str(Project_wortel/'Nutsmiddels/uitvoer_lêer.py'),str(Pad)]+argument_ARRAY,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (maatreël_data/(Naam+'.log')).write_bytes(data_plaas.stdout);assert data_plaas.returncode==0,data_plaas.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in data_plaas.stdout,data_plaas.stdout;validering_verslag['checks'].append(Naam)
        for 뒷부분 in ('c','cpp'):
            실행파일=maatreël_data/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            uitvoer_bevel('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=maatreël_data/'Stream_VALUE.elf'
        subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples/Stream_VALUE.c'),'-o',str(실행파일)])
        uitvoer_bevel('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        uitvoer_bevel('korean-python',Project_wortel/'예제/한글코딩/인사.py',['--include',str(Project_wortel/'예제/한글코딩/한국어.py')],'안녕하세요 누리')
        uitvoer_bevel('guest-korean-javac',Project_wortel/'예제/한글코딩/인사.java',[],'안녕하세요 · 합계=42')
        validering_verslag['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(maatreël_data/'report.json').write_text(json.dumps(validering_verslag,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Loop()
