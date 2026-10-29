#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from կատարել_հրաման import արձակել_արմատ

def Գործարկել():
    չափ_տվյալ=արձակել_արմատ/'build/verification/coding';չափ_տվյալ.mkdir(parents=True,exist_ok=True)
    վավերացում_զեկույց={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((արձակել_արմատ/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(արձակել_արմատ/'Գործիքներ/개발꾸러미내보내기.py')])
        with tarfile.open(str(արձակել_արմատ/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(չափ_տվյալ))
        개발꾸러미=չափ_տվյալ/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(개발꾸러미/'lib/libposix-kor-user.a')]).decode()
        for Անուն in ('통신종단점만들기','կապել_հասցե','자료전문보내기','자료전문받기','բացել_նիշք','파일자료읽기','գրել_նիշք_տվյալ'):
            assert ' T '+Անուն+'\n' in 심볼목록, Անուն
        (չափ_տվյալ/'korean-function-symbols.txt').write_text(심볼목록)
        վավերացում_զեկույց['checks'].append('real-korean-c-function-symbols')
        def կատարել_հրաման(Անուն,Ճանապարհ,արգումենտ_ԶԱՆԳՎԱԾ,예상결과):
            տվյալ_դիրք=subprocess.run(['python3',str(արձակել_արմատ/'Գործիքներ/կատարել_նիշք.py'),str(Ճանապարհ)]+արգումենտ_ԶԱՆԳՎԱԾ,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (չափ_տվյալ/(Անուն+'.log')).write_bytes(տվյալ_դիրք.stdout);assert տվյալ_դիրք.returncode==0,տվյալ_դիրք.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in տվյալ_դիրք.stdout,տվյալ_դիրք.stdout;վավերացում_զեկույց['checks'].append(Անուն)
        for 뒷부분 in ('c','cpp'):
            실행파일=չափ_տվյալ/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            կատարել_հրաման('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=չափ_տվյալ/'հոսք_արժեք.elf'
        subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples/հոսք_արժեք.c'),'-o',str(실행파일)])
        կատարել_հրաման('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        կատարել_հրաման('korean-python',արձակել_արմատ/'예제/한글코딩/인사.py',['--include',str(արձակել_արմատ/'예제/한글코딩/한국어.py')],'안녕하세요 누리')
        կատարել_հրաման('guest-korean-javac',արձակել_արմատ/'예제/한글코딩/인사.java',[],'안녕하세요 · 합계=42')
        վավերացում_զեկույց['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(չափ_տվյալ/'report.json').write_text(json.dumps(վավերացում_զեկույց,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Գործարկել()
