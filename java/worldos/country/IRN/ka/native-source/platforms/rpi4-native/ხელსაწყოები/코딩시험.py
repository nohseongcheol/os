#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from შესრულება_ბრძანება import პროეცირება_ფესვი

def გაშვება():
    გაზომვა_მონაცემები=პროეცირება_ფესვი/'build/verification/coding';გაზომვა_მონაცემები.mkdir(parents=True,exist_ok=True)
    გადამოწმება_ანგარიში={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((პროეცირება_ფესვი/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(პროეცირება_ფესვი/'ხელსაწყოები/개발꾸러미내보내기.py')])
        with tarfile.open(str(პროეცირება_ფესვი/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(გაზომვა_მონაცემები))
        개발꾸러미=გაზომვა_მონაცემები/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(개발꾸러미/'lib/libposix-kor-user.a')]).decode()
        for სახელი in ('통신종단점만들기','მიბმა_მისამართი','자료전문보내기','자료전문받기','გახსნა_ფაილი','파일자료읽기','ჩაწერა_ფაილი_მონაცემები'):
            assert ' T '+სახელი+'\n' in 심볼목록, სახელი
        (გაზომვა_მონაცემები/'korean-function-symbols.txt').write_text(심볼목록)
        გადამოწმება_ანგარიში['checks'].append('real-korean-c-function-symbols')
        def შესრულება_ბრძანება(სახელი,გეზი,არგუმენტი_მასივი,예상결과):
            მონაცემები_პოზიცია=subprocess.run(['python3',str(პროეცირება_ფესვი/'ხელსაწყოები/შესრულება_ფაილი.py'),str(გეზი)]+არგუმენტი_მასივი,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (გაზომვა_მონაცემები/(სახელი+'.log')).write_bytes(მონაცემები_პოზიცია.stdout);assert მონაცემები_პოზიცია.returncode==0,მონაცემები_პოზიცია.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in მონაცემები_პოზიცია.stdout,მონაცემები_პოზიცია.stdout;გადამოწმება_ანგარიში['checks'].append(სახელი)
        for 뒷부분 in ('c','cpp'):
            실행파일=გაზომვა_მონაცემები/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            შესრულება_ბრძანება('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=გაზომვა_მონაცემები/'ნაკადი_მნიშვნელობა.elf'
        subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples/ნაკადი_მნიშვნელობა.c'),'-o',str(실행파일)])
        შესრულება_ბრძანება('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        შესრულება_ბრძანება('korean-python',პროეცირება_ფესვი/'예제/한글코딩/인사.py',['--include',str(პროეცირება_ფესვი/'예제/한글코딩/한국어.py')],'안녕하세요 누리')
        შესრულება_ბრძანება('guest-korean-javac',პროეცირება_ფესვი/'예제/한글코딩/인사.java',[],'안녕하세요 · 합계=42')
        გადამოწმება_ანგარიში['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(გაზომვა_მონაცემები/'report.json').write_text(json.dumps(გადამოწმება_ანგარიში,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':გაშვება()
