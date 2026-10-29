#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from اجرا_فرمان import نمایش_دادن_جذر

def اجرا_2():
    سنجش_داده_ها=نمایش_دادن_جذر/'build/verification/coding';سنجش_داده_ها.mkdir(parents=True,exist_ok=True)
    اعتبارسنجی_گزارش={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((نمایش_دادن_جذر/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(نمایش_دادن_جذر/'ابزارها/개발꾸러미내보내기.py')])
        with tarfile.open(str(نمایش_دادن_جذر/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(سنجش_داده_ها))
        개발꾸러미=سنجش_داده_ها/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(개발꾸러미/'lib/libposix-kor-user.a')]).decode()
        for نام in ('통신종단점만들기','مرتبط_سازی_آدرس','자료전문보내기','자료전문받기','ایجاد_فایل','파일자료읽기','نوشتن_فایل_داده_ها'):
            assert ' T '+نام+'\n' in 심볼목록, نام
        (سنجش_داده_ها/'korean-function-symbols.txt').write_text(심볼목록)
        اعتبارسنجی_گزارش['checks'].append('real-korean-c-function-symbols')
        def اجرا_فرمان(نام,مسیر,آرگومان_آرايه,예상결과):
            داده_ها_مرتب_کردن=subprocess.run(['python3',str(نمایش_دادن_جذر/'ابزارها/اجرا_فایل.py'),str(مسیر)]+آرگومان_آرايه,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (سنجش_داده_ها/(نام+'.log')).write_bytes(داده_ها_مرتب_کردن.stdout);assert داده_ها_مرتب_کردن.returncode==0,داده_ها_مرتب_کردن.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in داده_ها_مرتب_کردن.stdout,داده_ها_مرتب_کردن.stdout;اعتبارسنجی_گزارش['checks'].append(نام)
        for 뒷부분 in ('c','cpp'):
            실행파일=سنجش_داده_ها/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            اجرا_فرمان('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=سنجش_داده_ها/'جریان_مقدار.elf'
        subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples/جریان_مقدار.c'),'-o',str(실행파일)])
        اجرا_فرمان('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        اجرا_فرمان('korean-python',نمایش_دادن_جذر/'예제/한글코딩/인사.py',['--include',str(نمایش_دادن_جذر/'예제/한글코딩/فارسی.py')],'안녕하세요 누리')
        اجرا_فرمان('guest-korean-javac',نمایش_دادن_جذر/'예제/한글코딩/인사.java',[],'안녕하세요 · 합계=42')
        اعتبارسنجی_گزارش['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(سنجش_داده_ها/'report.json').write_text(json.dumps(اعتبارسنجی_گزارش,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':اجرا_2()
