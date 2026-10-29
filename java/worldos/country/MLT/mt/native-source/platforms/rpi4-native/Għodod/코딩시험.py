#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from eżegwixxa_kmand import pprojetta_għerq

def serje():
    miżura_data=pprojetta_għerq/'build/verification/coding';miżura_data.mkdir(parents=True,exist_ok=True)
    validazzjoni_rapport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((pprojetta_għerq/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(pprojetta_għerq/'Għodod/개발꾸러미내보내기.py')])
        with tarfile.open(str(pprojetta_għerq/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(miżura_data))
        개발꾸러미=miżura_data/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(개발꾸러미/'lib/libposix-kor-user.a')]).decode()
        for isem in ('통신종단점만들기','BIND_ADDRESS','자료전문보내기','자료전문받기','fetaħ_fajl','파일자료읽기','kiteb_fajl_data'):
            assert ' T '+isem+'\n' in 심볼목록, isem
        (miżura_data/'korean-function-symbols.txt').write_text(심볼목록)
        validazzjoni_rapport['checks'].append('real-korean-c-function-symbols')
        def eżegwixxa_kmand(isem,mogħdija,argument_ARRAY,예상결과):
            data_pożizzjoni=subprocess.run(['python3',str(pprojetta_għerq/'Għodod/eżegwixxa_fajl.py'),str(mogħdija)]+argument_ARRAY,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (miżura_data/(isem+'.log')).write_bytes(data_pożizzjoni.stdout);assert data_pożizzjoni.returncode==0,data_pożizzjoni.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in data_pożizzjoni.stdout,data_pożizzjoni.stdout;validazzjoni_rapport['checks'].append(isem)
        for 뒷부분 in ('c','cpp'):
            실행파일=miżura_data/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            eżegwixxa_kmand('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=miżura_data/'Stream_VALUE.elf'
        subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples/Stream_VALUE.c'),'-o',str(실행파일)])
        eżegwixxa_kmand('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        eżegwixxa_kmand('korean-python',pprojetta_għerq/'예제/한글코딩/인사.py',['--include',str(pprojetta_għerq/'예제/한글코딩/Malti.py')],'안녕하세요 누리')
        eżegwixxa_kmand('guest-korean-javac',pprojetta_għerq/'예제/한글코딩/인사.java',[],'안녕하세요 · 합계=42')
        validazzjoni_rapport['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(miżura_data/'report.json').write_text(json.dumps(validazzjoni_rapport,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':serje()
