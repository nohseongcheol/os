#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼ import ਪ੍ਰੋਜੈਕਟ_ਰੂਟ

def ਚਲਾਓ_2():
    ਮਾਪ_ਸਮੱਗਰੀ=ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'build/verification/coding';ਮਾਪ_ਸਮੱਗਰੀ.mkdir(parents=True,exist_ok=True)
    ਮਾਨਤਾ_ਵਿਵਰਨ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'ਸਾਧਨ/개발꾸러미내보내기.py')])
        with tarfile.open(str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(ਮਾਪ_ਸਮੱਗਰੀ))
        개발꾸러미=ਮਾਪ_ਸਮੱਗਰੀ/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(개발꾸러미/'lib/libposix-kor-user.a')]).decode()
        for ਨਾਂ in ('통신종단점만들기','ਜ਼ਿਲਦਬੰਦੀ_ਪਤਾ','자료전문보내기','자료전문받기','ਖੋਲੋ_ਲਿਖਤ_ਪੱਤਰ','파일자료읽기','ਲਿੱਖੋ_ਲਿਖਤ_ਪੱਤਰ_ਸਮੱਗਰੀ'):
            assert ' T '+ਨਾਂ+'\n' in 심볼목록, ਨਾਂ
        (ਮਾਪ_ਸਮੱਗਰੀ/'korean-function-symbols.txt').write_text(심볼목록)
        ਮਾਨਤਾ_ਵਿਵਰਨ['checks'].append('real-korean-c-function-symbols')
        def ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼(ਨਾਂ,ਮਾਰਗ,ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ,예상결과):
            ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ=subprocess.run(['python3',str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'ਸਾਧਨ/ਅਮਲ_ਕਰੋ_ਲਿਖਤ_ਪੱਤਰ.py'),str(ਮਾਰਗ)]+ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (ਮਾਪ_ਸਮੱਗਰੀ/(ਨਾਂ+'.log')).write_bytes(ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.stdout);assert ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.returncode==0,ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.stdout,ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.stdout;ਮਾਨਤਾ_ਵਿਵਰਨ['checks'].append(ਨਾਂ)
        for 뒷부분 in ('c','cpp'):
            실행파일=ਮਾਪ_ਸਮੱਗਰੀ/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=ਮਾਪ_ਸਮੱਗਰੀ/'ਸਟ੍ਰੀਮ_ਕੀਮਤ.elf'
        subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples/ਸਟ੍ਰੀਮ_ਕੀਮਤ.c'),'-o',str(실행파일)])
        ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼('korean-python',ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'예제/한글코딩/인사.py',['--include',str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'예제/한글코딩/ਪੰਜਾਬੀ.py')],'안녕하세요 누리')
        ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼('guest-korean-javac',ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'예제/한글코딩/인사.java',[],'안녕하세요 · 합계=42')
        ਮਾਨਤਾ_ਵਿਵਰਨ['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(ਮਾਪ_ਸਮੱਗਰੀ/'report.json').write_text(json.dumps(ਮਾਨਤਾ_ਵਿਵਰਨ,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':ਚਲਾਓ_2()
