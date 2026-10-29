#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ import 기준

def ᎠᎢᏎᏍᏗ():
    결과자료=기준/'build/verification/coding';결과자료.mkdir(parents=True,exist_ok=True)
    ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(기준/'도구/개발꾸러미내보내기.py')])
        with tarfile.open(str(기준/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(결과자료))
        개발꾸러미=결과자료/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(개발꾸러미/'lib/libposix-kor-user.a')]).decode()
        for ᏚᏙᎥᎢ in ('통신종단점만들기','BIND_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ','자료전문보내기','자료전문받기','ᎯᏍᏚᎢ_ᎠᏍᏆᏂᎪᏙᏗ','파일자료읽기','ᎪᏪᎶᏗ_ᎠᏍᏆᏂᎪᏙᏗ_ᎦᏟᏌᏅᎯ'):
            assert ' T '+ᏚᏙᎥᎢ+'\n' in 심볼목록, ᏚᏙᎥᎢ
        (결과자료/'korean-function-symbols.txt').write_text(심볼목록)
        ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ['checks'].append('real-korean-c-function-symbols')
        def ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ(ᏚᏙᎥᎢ,ᎠᏍᏓᏩᏛᏍᏗ,ᏗᏓᎦᏘᎸᏍᏗ_array,예상결과):
            자료위치=subprocess.run(['python3',str(기준/'도구/ᎠᎴᏅᏗᏱ_ᎠᏍᏆᏂᎪᏙᏗ.py'),str(ᎠᏍᏓᏩᏛᏍᏗ)]+ᏗᏓᎦᏘᎸᏍᏗ_array,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (결과자료/(ᏚᏙᎥᎢ+'.log')).write_bytes(자료위치.stdout);assert 자료위치.returncode==0,자료위치.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in 자료위치.stdout,자료위치.stdout;ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ['checks'].append(ᏚᏙᎥᎢ)
        for 뒷부분 in ('c','cpp'):
            실행파일=결과자료/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=결과자료/'ᎤᏪᎬ_ᏧᎬᏩᎶᏗᏯ.elf'
        subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples/ᎤᏪᎬ_ᏧᎬᏩᎶᏗᏯ.c'),'-o',str(실행파일)])
        ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ('korean-python',기준/'예제/한글코딩/인사.py',['--include',str(기준/'예제/한글코딩/한국어.py')],'안녕하세요 누리')
        ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ('guest-korean-javac',기준/'예제/한글코딩/인사.java',[],'안녕하세요 · 합계=42')
        ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(결과자료/'report.json').write_text(json.dumps(ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':ᎠᎢᏎᏍᏗ()
