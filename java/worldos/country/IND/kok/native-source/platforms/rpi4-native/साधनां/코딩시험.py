#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from पाळो_दिवचो_आदेश import प्रॉजॅक्ट_रूट

def चलोवप():
    मेजप_डेटा=प्रॉजॅक्ट_रूट/'build/verification/coding';मेजप_डेटा.mkdir(parents=True,exist_ok=True)
    वैधताय_अहवाल={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((प्रॉजॅक्ट_रूट/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(प्रॉजॅक्ट_रूट/'साधनां/개발꾸러미내보내기.py')])
        with tarfile.open(str(प्रॉजॅक्ट_रूट/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(मेजप_डेटा))
        개발꾸러미=मेजप_डेटा/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(개발꾸러미/'lib/libposix-kor-user.a')]).decode()
        for नांव in ('통신종단점만들기','BIND_नामो','자료전문보내기','자료전문받기','उगडचें_फायल','파일자료읽기','बरोवचें_फायल_डेटा'):
            assert ' T '+नांव+'\n' in 심볼목록, नांव
        (मेजप_डेटा/'korean-function-symbols.txt').write_text(심볼목록)
        वैधताय_अहवाल['checks'].append('real-korean-c-function-symbols')
        def पाळो_दिवचो_आदेश(नांव,पाथ,युक्तीवाद_क्रम,예상결과):
            डेटा_स्थिती=subprocess.run(['python3',str(प्रॉजॅक्ट_रूट/'साधनां/पाळो_दिवचो_फायल.py'),str(पाथ)]+युक्तीवाद_क्रम,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (मेजप_डेटा/(नांव+'.log')).write_bytes(डेटा_स्थिती.stdout);assert डेटा_स्थिती.returncode==0,डेटा_स्थिती.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in डेटा_स्थिती.stdout,डेटा_स्थिती.stdout;वैधताय_अहवाल['checks'].append(नांव)
        for 뒷부분 in ('c','cpp'):
            실행파일=मेजप_डेटा/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            पाळो_दिवचो_आदेश('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=मेजप_डेटा/'Stream_मोल.elf'
        subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples/Stream_मोल.c'),'-o',str(실행파일)])
        पाळो_दिवचो_आदेश('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        पाळो_दिवचो_आदेश('korean-python',प्रॉजॅक्ट_रूट/'예제/한글코딩/인사.py',['--include',str(प्रॉजॅक्ट_रूट/'예제/한글코딩/한국어.py')],'안녕하세요 누리')
        पाळो_दिवचो_आदेश('guest-korean-javac',प्रॉजॅक्ट_रूट/'예제/한글코딩/인사.java',[],'안녕하세요 · 합계=42')
        वैधताय_अहवाल['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(मेजप_डेटा/'report.json').write_text(json.dumps(वैधताय_अहवाल,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':चलोवप()
