#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from कार्यान्वयन_गर्नुहोस्_आदेश import परियोजना_रूट

def चलाउनुहोस्():
    मापन_लगत=परियोजना_रूट/'build/verification/coding';मापन_लगत.mkdir(parents=True,exist_ok=True)
    वैधानिकता_रिपोर्ट={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((परियोजना_रूट/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(परियोजना_रूट/'उपकरणहरू/개발꾸러미내보내기.py')])
        with tarfile.open(str(परियोजना_रूट/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(मापन_लगत))
        개발꾸러미=मापन_लगत/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(개발꾸러미/'lib/libposix-kor-user.a')]).decode()
        for नाम in ('통신종단점만들기','बाँध्नु_ठेगाना','자료전문보내기','자료전문받기','सिर्जना_फाइल','파일자료읽기','लेख्नुहोस्_फाइल_लगत'):
            assert ' T '+नाम+'\n' in 심볼목록, नाम
        (मापन_लगत/'korean-function-symbols.txt').write_text(심볼목록)
        वैधानिकता_रिपोर्ट['checks'].append('real-korean-c-function-symbols')
        def कार्यान्वयन_गर्नुहोस्_आदेश(नाम,मार्ग,तर्क_विन्यास,예상결과):
            लगत_राख्नुहोस्=subprocess.run(['python3',str(परियोजना_रूट/'उपकरणहरू/कार्यान्वयन_गर्नुहोस्_फाइल.py'),str(मार्ग)]+तर्क_विन्यास,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (मापन_लगत/(नाम+'.log')).write_bytes(लगत_राख्नुहोस्.stdout);assert लगत_राख्नुहोस्.returncode==0,लगत_राख्नुहोस्.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in लगत_राख्नुहोस्.stdout,लगत_राख्नुहोस्.stdout;वैधानिकता_रिपोर्ट['checks'].append(नाम)
        for 뒷부분 in ('c','cpp'):
            실행파일=मापन_लगत/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            कार्यान्वयन_गर्नुहोस्_आदेश('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=मापन_लगत/'प्रवाह_मान.elf'
        subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples/प्रवाह_मान.c'),'-o',str(실행파일)])
        कार्यान्वयन_गर्नुहोस्_आदेश('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        कार्यान्वयन_गर्नुहोस्_आदेश('korean-python',परियोजना_रूट/'예제/한글코딩/인사.py',['--include',str(परियोजना_रूट/'예제/한글코딩/नेपाली.py')],'안녕하세요 누리')
        कार्यान्वयन_गर्नुहोस्_आदेश('guest-korean-javac',परियोजना_रूट/'예제/한글코딩/인사.java',[],'안녕하세요 · 합계=42')
        वैधानिकता_रिपोर्ट['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(मापन_लगत/'report.json').write_text(json.dumps(वैधानिकता_रिपोर्ट,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':चलाउनुहोस्()
