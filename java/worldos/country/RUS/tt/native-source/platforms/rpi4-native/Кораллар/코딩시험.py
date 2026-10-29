#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from үтәргә_команда import экранга_җибәрү_тамыр

def эшләтү():
    үлчәм_мәгълүмат=экранга_җибәрү_тамыр/'build/verification/coding';үлчәм_мәгълүмат.mkdir(parents=True,exist_ok=True)
    раслау_отчет={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((экранга_җибәрү_тамыр/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(экранга_җибәрү_тамыр/'Кораллар/개발꾸러미내보내기.py')])
        with tarfile.open(str(экранга_җибәрү_тамыр/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(үлчәм_мәгълүмат))
        개발꾸러미=үлчәм_мәгълүмат/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(개발꾸러미/'lib/libposix-kor-user.a')]).decode()
        for исем in ('통신종단점만들기','BIND_адрес','자료전문보내기','자료전문받기','ачу_файл','파일자료읽기','язу_файл_мәгълүмат'):
            assert ' T '+исем+'\n' in 심볼목록, исем
        (үлчәм_мәгълүмат/'korean-function-symbols.txt').write_text(심볼목록)
        раслау_отчет['checks'].append('real-korean-c-function-symbols')
        def үтәргә_команда(исем,Yul,аргумент_МАССИВ,예상결과):
            мәгълүмат_урнаштыру=subprocess.run(['python3',str(экранга_җибәрү_тамыр/'Кораллар/үтәргә_файл.py'),str(Yul)]+аргумент_МАССИВ,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (үлчәм_мәгълүмат/(исем+'.log')).write_bytes(мәгълүмат_урнаштыру.stdout);assert мәгълүмат_урнаштыру.returncode==0,мәгълүмат_урнаштыру.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in мәгълүмат_урнаштыру.stdout,мәгълүмат_урнаштыру.stdout;раслау_отчет['checks'].append(исем)
        for 뒷부분 in ('c','cpp'):
            실행파일=үлчәм_мәгълүмат/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            үтәргә_команда('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=үлчәм_мәгълүмат/'агым_VALUE.elf'
        subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples/агым_VALUE.c'),'-o',str(실행파일)])
        үтәргә_команда('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        үтәргә_команда('korean-python',экранга_җибәрү_тамыр/'예제/한글코딩/인사.py',['--include',str(экранга_җибәрү_тамыр/'예제/한글코딩/Татарча.py')],'안녕하세요 누리')
        үтәргә_команда('guest-korean-javac',экранга_җибәрү_тамыр/'예제/한글코딩/인사.java',[],'안녕하세요 · 합계=42')
        раслау_отчет['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(үлчәм_мәгълүмат/'report.json').write_text(json.dumps(раслау_отчет,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':эшләтү()
