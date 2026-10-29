#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from இயக்கு_கட்டளை import திட்டப்பணி_மூலம்

def செயல்படுத்துக():
    அளவிடக்கூடியது_தரவு=திட்டப்பணி_மூலம்/'build/verification/coding';அளவிடக்கூடியது_தரவு.mkdir(parents=True,exist_ok=True)
    செல்லுபடியாக்கம்_அறிக்கை={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((திட்டப்பணி_மூலம்/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(திட்டப்பணி_மூலம்/'கருவிகள்/개발꾸러미내보내기.py')])
        with tarfile.open(str(திட்டப்பணி_மூலம்/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(அளவிடக்கூடியது_தரவு))
        개발꾸러미=அளவிடக்கூடியது_தரவு/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(개발꾸러미/'lib/libposix-kor-user.a')]).decode()
        for பெயர் in ('உருவாக்கு_முடிவுப்_புள்ளி','கட்டு_முகவரி','자료전문보내기','자료전문받기','திற_கோப்பு','파일자료읽기','எழுது_கோப்பு_தரவு'):
            assert ' T '+பெயர்+'\n' in 심볼목록, பெயர்
        (அளவிடக்கூடியது_தரவு/'korean-function-symbols.txt').write_text(심볼목록)
        செல்லுபடியாக்கம்_அறிக்கை['checks'].append('real-korean-c-function-symbols')
        def இயக்கு_கட்டளை(பெயர்,பாதை_2,மதிப்புரு_கோவை,예상결과):
            தரவு_நிலை=subprocess.run(['python3',str(திட்டப்பணி_மூலம்/'கருவிகள்/இயக்கு_கோப்பு.py'),str(பாதை_2)]+மதிப்புரு_கோவை,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (அளவிடக்கூடியது_தரவு/(பெயர்+'.log')).write_bytes(தரவு_நிலை.stdout);assert தரவு_நிலை.returncode==0,தரவு_நிலை.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in தரவு_நிலை.stdout,தரவு_நிலை.stdout;செல்லுபடியாக்கம்_அறிக்கை['checks'].append(பெயர்)
        for 뒷부분 in ('c','cpp'):
            செயல்படுத்தக்கூடிய_கோப்பு=அளவிடக்கூடியது_தரவு/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples'/('인사.'+뒷부분)),'-o',str(செயல்படுத்தக்கூடிய_கோப்பு)])
            இயக்கு_கட்டளை('korean-'+뒷부분,செயல்படுத்தக்கூடிய_கோப்பு,[],'posix-kor 호출')
        செயல்படுத்தக்கூடிய_கோப்பு=அளவிடக்கூடியது_தரவு/'தொடரோடி_மதிப்பு.elf'
        subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples/தொடரோடி_மதிப்பு.c'),'-o',str(செயல்படுத்தக்கூடிய_கோப்பு)])
        இயக்கு_கட்டளை('c-stream-queues',செயல்படுத்தக்கூடிய_கோப்பு,[],'C posix-kor 연결형 통신 PASS')
        இயக்கு_கட்டளை('korean-python',திட்டப்பணி_மூலம்/'예제/한글코딩/인사.py',['--include',str(திட்டப்பணி_மூலம்/'예제/한글코딩/தமிழ்.py')],'안녕하세요 누리')
        இயக்கு_கட்டளை('guest-korean-javac',திட்டப்பணி_மூலம்/'예제/한글코딩/인사.java',[],'안녕하세요 · 합계=42')
        செல்லுபடியாக்கம்_அறிக்கை['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(அளவிடக்கூடியது_தரவு/'report.json').write_text(json.dumps(செல்லுபடியாக்கம்_அறிக்கை,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':செயல்படுத்துக()
