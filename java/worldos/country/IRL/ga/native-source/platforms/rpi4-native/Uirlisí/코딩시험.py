#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from Rith_ordú import teilgean_fréamh

def Rith_2():
    tomhas_sonraí=teilgean_fréamh/'build/verification/coding';tomhas_sonraí.mkdir(parents=True,exist_ok=True)
    bailíochtú_tuairisc={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((teilgean_fréamh/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(teilgean_fréamh/'Uirlisí/easportáil_SDK.py')])
        with tarfile.open(str(teilgean_fréamh/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(tomhas_sonraí))
        개발꾸러미=tomhas_sonraí/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(개발꾸러미/'lib/libposix-kor-user.a')]).decode()
        for Ainm in ('통신종단점만들기','BIND_ADDRESS','자료전문보내기','자료전문받기','oscail_comhad','파일자료읽기','scríobh_comhad_sonraí'):
            assert ' T '+Ainm+'\n' in 심볼목록, Ainm
        (tomhas_sonraí/'korean-function-symbols.txt').write_text(심볼목록)
        bailíochtú_tuairisc['checks'].append('real-korean-c-function-symbols')
        def Rith_ordú(Ainm,CONAIR,argóint_ARRAY,예상결과):
            sonraí_suíomh=subprocess.run(['python3',str(teilgean_fréamh/'Uirlisí/Rith_comhad.py'),str(CONAIR)]+argóint_ARRAY,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (tomhas_sonraí/(Ainm+'.log')).write_bytes(sonraí_suíomh.stdout);assert sonraí_suíomh.returncode==0,sonraí_suíomh.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in sonraí_suíomh.stdout,sonraí_suíomh.stdout;bailíochtú_tuairisc['checks'].append(Ainm)
        for 뒷부분 in ('c','cpp'):
            실행파일=tomhas_sonraí/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            Rith_ordú('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=tomhas_sonraí/'sruth_VALUE.elf'
        subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples/sruth_VALUE.c'),'-o',str(실행파일)])
        Rith_ordú('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        Rith_ordú('korean-python',teilgean_fréamh/'예제/한글코딩/인사.py',['--include',str(teilgean_fréamh/'예제/한글코딩/Gaeilge.py')],'안녕하세요 누리')
        Rith_ordú('guest-korean-javac',teilgean_fréamh/'예제/한글코딩/인사.java',[],'안녕하세요 · 합계=42')
        bailíochtú_tuairisc['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(tomhas_sonraí/'report.json').write_text(json.dumps(bailíochtú_tuairisc,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Rith_2()
