#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from ಪೂರೈಸು_ಆದೇಶ import ಬಿಂಬಿಸು_ಮೂಲ

def ಚಲಾಯಿಸು_2():
    ಮಾಪನ_ಡೇಟಾ=ಬಿಂಬಿಸು_ಮೂಲ/'build/verification/coding';ಮಾಪನ_ಡೇಟಾ.mkdir(parents=True,exist_ok=True)
    ದೃಢೀಕರಣ_ವರದಿ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((ಬಿಂಬಿಸು_ಮೂಲ/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(ಬಿಂಬಿಸು_ಮೂಲ/'ಪರಿಕರಗಳು/개발꾸러미내보내기.py')])
        with tarfile.open(str(ಬಿಂಬಿಸು_ಮೂಲ/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(ಮಾಪನ_ಡೇಟಾ))
        개발꾸러미=ಮಾಪನ_ಡೇಟಾ/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(개발꾸러미/'lib/libposix-kor-user.a')]).decode()
        for ಹೆಸರು in ('통신종단점만들기','ಬೈಂಡ್_ಮಾಡು_ಇಮೇಲ್','자료전문보내기','자료전문받기','ರಚಿಸು_ಫೈಲ್','파일자료읽기','ಬರೆ_ಫೈಲ್_ಡೇಟಾ'):
            assert ' T '+ಹೆಸರು+'\n' in 심볼목록, ಹೆಸರು
        (ಮಾಪನ_ಡೇಟಾ/'korean-function-symbols.txt').write_text(심볼목록)
        ದೃಢೀಕರಣ_ವರದಿ['checks'].append('real-korean-c-function-symbols')
        def ಪೂರೈಸು_ಆದೇಶ(ಹೆಸರು,ಮಾರ್ಗ,ವಾದ_ಅರೇ,예상결과):
            ಡೇಟಾ_ಹುದ್ದೆ=subprocess.run(['python3',str(ಬಿಂಬಿಸು_ಮೂಲ/'ಪರಿಕರಗಳು/ಪೂರೈಸು_ಫೈಲ್.py'),str(ಮಾರ್ಗ)]+ವಾದ_ಅರೇ,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (ಮಾಪನ_ಡೇಟಾ/(ಹೆಸರು+'.log')).write_bytes(ಡೇಟಾ_ಹುದ್ದೆ.stdout);assert ಡೇಟಾ_ಹುದ್ದೆ.returncode==0,ಡೇಟಾ_ಹುದ್ದೆ.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in ಡೇಟಾ_ಹುದ್ದೆ.stdout,ಡೇಟಾ_ಹುದ್ದೆ.stdout;ದೃಢೀಕರಣ_ವರದಿ['checks'].append(ಹೆಸರು)
        for 뒷부분 in ('c','cpp'):
            실행파일=ಮಾಪನ_ಡೇಟಾ/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            ಪೂರೈಸು_ಆದೇಶ('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=ಮಾಪನ_ಡೇಟಾ/'ಸ್ಟ್ರೀಮ್_ಮೌಲ್ಯ.elf'
        subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples/ಸ್ಟ್ರೀಮ್_ಮೌಲ್ಯ.c'),'-o',str(실행파일)])
        ಪೂರೈಸು_ಆದೇಶ('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        ಪೂರೈಸು_ಆದೇಶ('korean-python',ಬಿಂಬಿಸು_ಮೂಲ/'예제/한글코딩/인사.py',['--include',str(ಬಿಂಬಿಸು_ಮೂಲ/'예제/한글코딩/ಕನ್ನಡ.py')],'안녕하세요 누리')
        ಪೂರೈಸು_ಆದೇಶ('guest-korean-javac',ಬಿಂಬಿಸು_ಮೂಲ/'예제/한글코딩/인사.java',[],'안녕하세요 · 합계=42')
        ದೃಢೀಕರಣ_ವರದಿ['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(ಮಾಪನ_ಡೇಟಾ/'report.json').write_text(json.dumps(ದೃಢೀಕರಣ_ವರದಿ,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':ಚಲಾಯಿಸು_2()
