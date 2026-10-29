#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from Mag_execute_utos import Project_root

def run():
    sukat_data=Project_root/'build/verification/coding';sukat_data.mkdir(parents=True,exist_ok=True)
    pagpapatibay_ulat={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_root/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(Project_root/'Mga_Tool/export_SDK.py')])
        with tarfile.open(str(Project_root/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(sukat_data))
        개발꾸러미=sukat_data/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(개발꾸러미/'lib/libposix-kor-user.a')]).decode()
        for pangalan in ('통신종단점만들기','BIND_email','자료전문보내기','자료전문받기','buksan_file','파일자료읽기','sumulat_file_data'):
            assert ' T '+pangalan+'\n' in 심볼목록, pangalan
        (sukat_data/'korean-function-symbols.txt').write_text(심볼목록)
        pagpapatibay_ulat['checks'].append('real-korean-c-function-symbols')
        def Mag_execute_utos(pangalan,path,argumento_ARRAY,예상결과):
            data_posisyon=subprocess.run(['python3',str(Project_root/'Mga_Tool/Mag_execute_file.py'),str(path)]+argumento_ARRAY,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (sukat_data/(pangalan+'.log')).write_bytes(data_posisyon.stdout);assert data_posisyon.returncode==0,data_posisyon.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in data_posisyon.stdout,data_posisyon.stdout;pagpapatibay_ulat['checks'].append(pangalan)
        for 뒷부분 in ('c','cpp'):
            실행파일=sukat_data/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            Mag_execute_utos('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=sukat_data/'Stream_VALUE.elf'
        subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples/Stream_VALUE.c'),'-o',str(실행파일)])
        Mag_execute_utos('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        Mag_execute_utos('korean-python',Project_root/'예제/한글코딩/인사.py',['--include',str(Project_root/'예제/한글코딩/한국어.py')],'안녕하세요 누리')
        Mag_execute_utos('guest-korean-javac',Project_root/'예제/한글코딩/인사.java',[],'안녕하세요 · 합계=42')
        pagpapatibay_ulat['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(sukat_data/'report.json').write_text(json.dumps(pagpapatibay_ulat,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':run()
