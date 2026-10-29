#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from ක්_රියාත්මක_කරන්න_විධානය import 기준

def ක්_රියාත්මක_කරන්න_2():
    결과자료=기준/'build/verification/coding';결과자료.mkdir(parents=True,exist_ok=True)
    වලංගුකරණය_වාර්තාව={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(기준/'මෙවලම්/개발꾸러미내보내기.py')])
        with tarfile.open(str(기준/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(결과자료))
        개발꾸러미=결과자료/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(개발꾸러미/'lib/libposix-kor-user.a')]).decode()
        for නම in ('통신종단점만들기','බඳින්න_යොමුව','자료전문보내기','자료전문받기','සාදන්න_ගොනුව','파일자료읽기','ලියන්න_ගොනුව_දත්ත'):
            assert ' T '+නම+'\n' in 심볼목록, නම
        (결과자료/'korean-function-symbols.txt').write_text(심볼목록)
        වලංගුකරණය_වාර්තාව['checks'].append('real-korean-c-function-symbols')
        def ක්_රියාත්මක_කරන්න_විධානය(නම,මාර්_ගය,විස්තාරකය_ආරා_ව,예상결과):
            자료위치=subprocess.run(['python3',str(기준/'මෙවලම්/ක්_රියාත්මක_කරන්න_ගොනුව.py'),str(මාර්_ගය)]+විස්තාරකය_ආරා_ව,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (결과자료/(නම+'.log')).write_bytes(자료위치.stdout);assert 자료위치.returncode==0,자료위치.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in 자료위치.stdout,자료위치.stdout;වලංගුකරණය_වාර්තාව['checks'].append(නම)
        for 뒷부분 in ('c','cpp'):
            실행파일=결과자료/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            ක්_රියාත්මක_කරන්න_විධානය('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=결과자료/'දහර_අගය.elf'
        subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples/දහර_අගය.c'),'-o',str(실행파일)])
        ක්_රියාත්මක_කරන්න_විධානය('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        ක්_රියාත්මක_කරන්න_විධානය('korean-python',기준/'예제/한글코딩/인사.py',['--include',str(기준/'예제/한글코딩/한국어.py')],'안녕하세요 누리')
        ක්_රියාත්මක_කරන්න_විධානය('guest-korean-javac',기준/'예제/한글코딩/인사.java',[],'안녕하세요 · 합계=42')
        වලංගුකරණය_වාර්තාව['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(결과자료/'report.json').write_text(json.dumps(වලංගුකරණය_වාර්තාව,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':ක්_රියාත්මක_කරන්න_2()
