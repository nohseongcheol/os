#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from לבצע_פקודה import לשקף_בסיס

def הפעלה():
    תוצאה_נתונים=לשקף_בסיס/'build/verification/coding';תוצאה_נתונים.mkdir(parents=True,exist_ok=True)
    אימות_דוח={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((לשקף_בסיס/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(לשקף_בסיס/'כלים/ייצא_ערכת_פיתוח_תוכנה.py')])
        with tarfile.open(str(לשקף_בסיס/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(תוצאה_נתונים))
        ערכת_פיתוח=תוצאה_נתונים/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(ערכת_פיתוח/'lib/libposix-kor-user.a')]).decode()
        for שם in ('ליצור_משתתף','לאגד_למען','שלח_יחידת_נתונים_נתונים','לקבל_יחידת_נתונים_נתונים','פתח_קובץ','파일자료읽기','כתיבה_קובץ_נתונים'):
            assert ' T '+שם+'\n' in 심볼목록, שם
        (תוצאה_נתונים/'korean-function-symbols.txt').write_text(심볼목록)
        אימות_דוח['checks'].append('real-korean-c-function-symbols')
        def לבצע_פקודה(שם,נתיב,ארגומנט_מערך,예상결과):
            נתונים_עמדה=subprocess.run(['python3',str(לשקף_בסיס/'כלים/לבצע_קובץ.py'),str(נתיב)]+ארגומנט_מערך,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (תוצאה_נתונים/(שם+'.log')).write_bytes(נתונים_עמדה.stdout);assert נתונים_עמדה.returncode==0,נתונים_עמדה.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in נתונים_עמדה.stdout,נתונים_עמדה.stdout;אימות_דוח['checks'].append(שם)
        for 뒷부분 in ('c','cpp'):
            실행파일=תוצאה_נתונים/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(ערכת_פיתוח/'compile.py'),str(ערכת_פיתוח/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            לבצע_פקודה('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=תוצאה_נתונים/'זרם_ערך.elf'
        subprocess.check_call(['python3',str(ערכת_פיתוח/'compile.py'),str(ערכת_פיתוח/'examples/זרם_ערך.c'),'-o',str(실행파일)])
        לבצע_פקודה('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        לבצע_פקודה('korean-python',לשקף_בסיס/'예제/한글코딩/인사.py',['--include',str(לשקף_בסיס/'예제/한글코딩/עברית.py')],'안녕하세요 누리')
        לבצע_פקודה('guest-korean-javac',לשקף_בסיס/'예제/한글코딩/인사.java',[],'안녕하세요 · סך_הכל_ערך=42')
        אימות_דוח['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(תוצאה_נתונים/'report.json').write_text(json.dumps(אימות_דוח,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':הפעלה()
