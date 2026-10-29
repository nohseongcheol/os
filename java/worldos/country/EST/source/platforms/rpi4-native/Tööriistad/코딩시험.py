#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from Täida_käsk import Project_juur

def Käivita_2():
    näitaja_andmed=Project_juur/'build/verification/coding';näitaja_andmed.mkdir(parents=True,exist_ok=True)
    kinnitamine_aruanne={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_juur/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(Project_juur/'Tööriistad/eksportima_SDK.py')])
        with tarfile.open(str(Project_juur/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(näitaja_andmed))
        arenduskomplekt=näitaja_andmed/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(arenduskomplekt/'lib/libposix-kor-user.a')]).decode()
        for Nimi_2 in ('avama_osaleja','BIND_ADDRESS','saatma_datagramm_andmed','saama_datagramm_andmed','avama_Fail','파일자료읽기','kirjutamine_Fail_andmed'):
            assert ' T '+Nimi_2+'\n' in 심볼목록, Nimi_2
        (näitaja_andmed/'korean-function-symbols.txt').write_text(심볼목록)
        kinnitamine_aruanne['checks'].append('real-korean-c-function-symbols')
        def Täida_käsk(Nimi_2,RADA,argument_ARRAY,예상결과):
            andmed_ametikoht=subprocess.run(['python3',str(Project_juur/'Tööriistad/Täida_Fail.py'),str(RADA)]+argument_ARRAY,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (näitaja_andmed/(Nimi_2+'.log')).write_bytes(andmed_ametikoht.stdout);assert andmed_ametikoht.returncode==0,andmed_ametikoht.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in andmed_ametikoht.stdout,andmed_ametikoht.stdout;kinnitamine_aruanne['checks'].append(Nimi_2)
        for 뒷부분 in ('c','cpp'):
            실행파일=näitaja_andmed/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(arenduskomplekt/'compile.py'),str(arenduskomplekt/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            Täida_käsk('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=näitaja_andmed/'voog_VALUE.elf'
        subprocess.check_call(['python3',str(arenduskomplekt/'compile.py'),str(arenduskomplekt/'examples/voog_VALUE.c'),'-o',str(실행파일)])
        Täida_käsk('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        Täida_käsk('korean-python',Project_juur/'예제/한글코딩/인사.py',['--include',str(Project_juur/'예제/한글코딩/Eesti.py')],'안녕하세요 누리')
        Täida_käsk('guest-korean-javac',Project_juur/'예제/한글코딩/인사.java',[],'안녕하세요 · kokku_VALUE=42')
        kinnitamine_aruanne['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(näitaja_andmed/'report.json').write_text(json.dumps(kinnitamine_aruanne,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Käivita_2()
