#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from কার্যকর_করুন_আদেশ import প্রকল্প_মূল

def চালনা():
    পরিমাপ_ডাটা=প্রকল্প_মূল/'build/verification/coding';পরিমাপ_ডাটা.mkdir(parents=True,exist_ok=True)
    বৈধকরণ_রিপোর্ট={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((প্রকল্প_মূল/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(প্রকল্প_মূল/'সরঞ্জামগুলি/개발꾸러미내보내기.py')])
        with tarfile.open(str(প্রকল্প_মূল/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(পরিমাপ_ডাটা))
        개발꾸러미=পরিমাপ_ডাটা/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(개발꾸러미/'lib/libposix-kor-user.a')]).decode()
        for নাম in ('통신종단점만들기','বন্ধন_করা_ইমেইল','자료전문보내기','자료전문받기','খোলা_ফাইল','파일자료읽기','লেখা_ফাইল_ডাটা'):
            assert ' T '+নাম+'\n' in 심볼목록, নাম
        (পরিমাপ_ডাটা/'korean-function-symbols.txt').write_text(심볼목록)
        বৈধকরণ_রিপোর্ট['checks'].append('real-korean-c-function-symbols')
        def কার্যকর_করুন_আদেশ(নাম,পথ_2,যুক্তি_অ্যারে,예상결과):
            ডাটা_পদ=subprocess.run(['python3',str(প্রকল্প_মূল/'সরঞ্জামগুলি/কার্যকর_করুন_ফাইল.py'),str(পথ_2)]+যুক্তি_অ্যারে,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (পরিমাপ_ডাটা/(নাম+'.log')).write_bytes(ডাটা_পদ.stdout);assert ডাটা_পদ.returncode==0,ডাটা_পদ.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in ডাটা_পদ.stdout,ডাটা_পদ.stdout;বৈধকরণ_রিপোর্ট['checks'].append(নাম)
        for 뒷부분 in ('c','cpp'):
            실행파일=পরিমাপ_ডাটা/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            কার্যকর_করুন_আদেশ('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=পরিমাপ_ডাটা/'প্রবাহ_মান.elf'
        subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples/প্রবাহ_মান.c'),'-o',str(실행파일)])
        কার্যকর_করুন_আদেশ('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        কার্যকর_করুন_আদেশ('korean-python',প্রকল্প_মূল/'예제/한글코딩/인사.py',['--include',str(প্রকল্প_মূল/'예제/한글코딩/বাংলা.py')],'안녕하세요 누리')
        কার্যকর_করুন_আদেশ('guest-korean-javac',প্রকল্প_মূল/'예제/한글코딩/인사.java',[],'안녕하세요 · 합계=42')
        বৈধকরণ_রিপোর্ট['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(পরিমাপ_ডাটা/'report.json').write_text(json.dumps(বৈধকরণ_রিপোর্ট,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':চালনা()
