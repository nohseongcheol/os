#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from نفاذ_کریں_حکم import عکس_ڈالنا_روٹ

def چلائیں():
    پیمائش_کوائف=عکس_ڈالنا_روٹ/'build/verification/coding';پیمائش_کوائف.mkdir(parents=True,exist_ok=True)
    توثیق_رپورٹ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((عکس_ڈالنا_روٹ/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(عکس_ڈالنا_روٹ/'ٹولز/개발꾸러미내보내기.py')])
        with tarfile.open(str(عکس_ڈالنا_روٹ/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(پیمائش_کوائف))
        개발꾸러미=پیمائش_کوائف/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(개발꾸러미/'lib/libposix-kor-user.a')]).decode()
        for نام in ('통신종단점만들기','باندھیں_پتہ','자료전문보내기','자료전문받기','بنائیں_فائل','파일자료읽기','لکھیں_فائل_کوائف'):
            assert ' T '+نام+'\n' in 심볼목록, نام
        (پیمائش_کوائف/'korean-function-symbols.txt').write_text(심볼목록)
        توثیق_رپورٹ['checks'].append('real-korean-c-function-symbols')
        def نفاذ_کریں_حکم(نام,راستہ_2,دلائل_لڑی,예상결과):
            کوائف_پوزیشن_ٹھیک_کریں=subprocess.run(['python3',str(عکس_ڈالنا_روٹ/'ٹولز/نفاذ_کریں_فائل.py'),str(راستہ_2)]+دلائل_لڑی,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (پیمائش_کوائف/(نام+'.log')).write_bytes(کوائف_پوزیشن_ٹھیک_کریں.stdout);assert کوائف_پوزیشن_ٹھیک_کریں.returncode==0,کوائف_پوزیشن_ٹھیک_کریں.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in کوائف_پوزیشن_ٹھیک_کریں.stdout,کوائف_پوزیشن_ٹھیک_کریں.stdout;توثیق_رپورٹ['checks'].append(نام)
        for 뒷부분 in ('c','cpp'):
            실행파일=پیمائش_کوائف/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            نفاذ_کریں_حکم('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=پیمائش_کوائف/'بہاؤ_قدر.elf'
        subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples/بہاؤ_قدر.c'),'-o',str(실행파일)])
        نفاذ_کریں_حکم('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        نفاذ_کریں_حکم('korean-python',عکس_ڈالنا_روٹ/'예제/한글코딩/인사.py',['--include',str(عکس_ڈالنا_روٹ/'예제/한글코딩/اردو.py')],'안녕하세요 누리')
        نفاذ_کریں_حکم('guest-korean-javac',عکس_ڈالنا_روٹ/'예제/한글코딩/인사.java',[],'안녕하세요 · 합계=42')
        توثیق_رپورٹ['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(پیمائش_کوائف/'report.json').write_text(json.dumps(توثیق_رپورٹ,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':چلائیں()
