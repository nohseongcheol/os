#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from અમલ_કરો_આદેશ import પ્રોજેક્ટ_રૂટ

def ચલાવો_2():
    પરિમાણ_ડેટા=પ્રોજેક્ટ_રૂટ/'build/verification/coding';પરિમાણ_ડેટા.mkdir(parents=True,exist_ok=True)
    માન્યતા_અહેવાલ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((પ્રોજેક્ટ_રૂટ/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(પ્રોજેક્ટ_રૂટ/'ઉપકરણો/개발꾸러미내보내기.py')])
        with tarfile.open(str(પ્રોજેક્ટ_રૂટ/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(પરિમાણ_ડેટા))
        개발꾸러미=પરિમાણ_ડેટા/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(개발꾸러미/'lib/libposix-kor-user.a')]).decode()
        for નામ in ('통신종단점만들기','બાઇંડ_કરો_સરનામું','자료전문보내기','자료전문받기','બનાવો_ફાઇલ','파일자료읽기','લખો_ફાઇલ_ડેટા'):
            assert ' T '+નામ+'\n' in 심볼목록, નામ
        (પરિમાણ_ડેટા/'korean-function-symbols.txt').write_text(심볼목록)
        માન્યતા_અહેવાલ['checks'].append('real-korean-c-function-symbols')
        def અમલ_કરો_આદેશ(નામ,પથ,દલીલ_અરે,예상결과):
            ડેટા_સ્થિતિ=subprocess.run(['python3',str(પ્રોજેક્ટ_રૂટ/'ઉપકરણો/અમલ_કરો_ફાઇલ.py'),str(પથ)]+દલીલ_અરે,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (પરિમાણ_ડેટા/(નામ+'.log')).write_bytes(ડેટા_સ્થિતિ.stdout);assert ડેટા_સ્થિતિ.returncode==0,ડેટા_સ્થિતિ.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in ડેટા_સ્થિતિ.stdout,ડેટા_સ્થિતિ.stdout;માન્યતા_અહેવાલ['checks'].append(નામ)
        for 뒷부분 in ('c','cpp'):
            실행파일=પરિમાણ_ડેટા/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            અમલ_કરો_આદેશ('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=પરિમાણ_ડેટા/'સ્ટ્રીમ_મૂલ્ય.elf'
        subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples/સ્ટ્રીમ_મૂલ્ય.c'),'-o',str(실행파일)])
        અમલ_કરો_આદેશ('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        અમલ_કરો_આદેશ('korean-python',પ્રોજેક્ટ_રૂટ/'예제/한글코딩/인사.py',['--include',str(પ્રોજેક્ટ_રૂટ/'예제/한글코딩/ગુજરાતી.py')],'안녕하세요 누리')
        અમલ_કરો_આદેશ('guest-korean-javac',પ્રોજેક્ટ_રૂટ/'예제/한글코딩/인사.java',[],'안녕하세요 · 합계=42')
        માન્યતા_અહેવાલ['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(પરિમાણ_ડેટા/'report.json').write_text(json.dumps(માન્યતા_અહેવાલ,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':ચલાવો_2()
