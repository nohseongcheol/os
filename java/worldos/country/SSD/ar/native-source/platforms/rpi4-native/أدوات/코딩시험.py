#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from ينفذ_أمر import يعرض_جذر

def تشغيل():
    مقياس_بيانات=يعرض_جذر/'build/verification/coding';مقياس_بيانات.mkdir(parents=True,exist_ok=True)
    التحقق_من_صحة_إبلاغ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((يعرض_جذر/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(يعرض_جذر/'أدوات/تصدير_عدة_تطوير_البرامج.py')])
        with tarfile.open(str(يعرض_جذر/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(مقياس_بيانات))
        أداة_التطوير=مقياس_بيانات/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(أداة_التطوير/'lib/libposix-kor-user.a')]).decode()
        for اسم in ('فتح_المشارك','يربط_عنوان','يرسل_مخطط_بيانات_بيانات','يستلم_مخطط_بيانات_بيانات','فتح_ملف','يقرأ_ملف_بيانات','كتابة_ملف_بيانات'):
            assert ' T '+اسم+'\n' in 심볼목록, اسم
        (مقياس_بيانات/'korean-function-symbols.txt').write_text(심볼목록)
        التحقق_من_صحة_إبلاغ['checks'].append('real-korean-c-function-symbols')
        def ينفذ_أمر(اسم,مسار,وسيطة_صفيف,예상결과):
            بيانات_منصب=subprocess.run(['python3',str(يعرض_جذر/'أدوات/ينفذ_ملف.py'),str(مسار)]+وسيطة_صفيف,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (مقياس_بيانات/(اسم+'.log')).write_bytes(بيانات_منصب.stdout);assert بيانات_منصب.returncode==0,بيانات_منصب.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in بيانات_منصب.stdout,بيانات_منصب.stdout;التحقق_من_صحة_إبلاغ['checks'].append(اسم)
        for 뒷부분 in ('c','cpp'):
            실행파일=مقياس_بيانات/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(أداة_التطوير/'compile.py'),str(أداة_التطوير/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            ينفذ_أمر('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=مقياس_بيانات/'بث_قيمة.elf'
        subprocess.check_call(['python3',str(أداة_التطوير/'compile.py'),str(أداة_التطوير/'examples/بث_قيمة.c'),'-o',str(실행파일)])
        ينفذ_أمر('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        ينفذ_أمر('korean-python',يعرض_جذر/'예제/한글코딩/인사.py',['--include',str(يعرض_جذر/'예제/한글코딩/العربية.py')],'안녕하세요 누리')
        ينفذ_أمر('guest-korean-javac',يعرض_جذر/'예제/한글코딩/인사.java',[],'안녕하세요 · إجمالي_قيمة=42')
        التحقق_من_صحة_إبلاغ['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(مقياس_بيانات/'report.json').write_text(json.dumps(التحقق_من_صحة_إبلاغ,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':تشغيل()
