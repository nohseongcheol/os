#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from అమలు_చేయి_ఆదేశం import ప్రొజెక్ట్_మూలం

def నడుపుము():
    ప్రమాణం_డేటా=ప్రొజెక్ట్_మూలం/'build/verification/coding';ప్రమాణం_డేటా.mkdir(parents=True,exist_ok=True)
    నిర్ధారణ_నివేదిక={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((ప్రొజెక్ట్_మూలం/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(ప్రొజెక్ట్_మూలం/'ఉపకరణాలు/개발꾸러미내보내기.py')])
        with tarfile.open(str(ప్రొజెక్ట్_మూలం/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(ప్రమాణం_డేటా))
        개발꾸러미=ప్రమాణం_డేటా/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(개발꾸러미/'lib/libposix-kor-user.a')]).decode()
        for పేరు in ('통신종단점만들기','బైండ్_చేయి_ఇమెయిల్','자료전문보내기','자료전문받기','తెరువు_ఫైలు','파일자료읽기','వ్రాయి_ఫైలు_డేటా'):
            assert ' T '+పేరు+'\n' in 심볼목록, పేరు
        (ప్రమాణం_డేటా/'korean-function-symbols.txt').write_text(심볼목록)
        నిర్ధారణ_నివేదిక['checks'].append('real-korean-c-function-symbols')
        def అమలు_చేయి_ఆదేశం(పేరు,పాత్,కారకం_శ్రేణి,예상결과):
            డేటా_స్థాయి=subprocess.run(['python3',str(ప్రొజెక్ట్_మూలం/'ఉపకరణాలు/అమలు_చేయి_ఫైలు.py'),str(పాత్)]+కారకం_శ్రేణి,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (ప్రమాణం_డేటా/(పేరు+'.log')).write_bytes(డేటా_స్థాయి.stdout);assert డేటా_స్థాయి.returncode==0,డేటా_స్థాయి.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in డేటా_స్థాయి.stdout,డేటా_స్థాయి.stdout;నిర్ధారణ_నివేదిక['checks'].append(పేరు)
        for 뒷부분 in ('c','cpp'):
            실행파일=ప్రమాణం_డేటా/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            అమలు_చేయి_ఆదేశం('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=ప్రమాణం_డేటా/'ధార_మూల్యం.elf'
        subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples/ధార_మూల్యం.c'),'-o',str(실행파일)])
        అమలు_చేయి_ఆదేశం('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        అమలు_చేయి_ఆదేశం('korean-python',ప్రొజెక్ట్_మూలం/'예제/한글코딩/인사.py',['--include',str(ప్రొజెక్ట్_మూలం/'예제/한글코딩/한국어.py')],'안녕하세요 누리')
        అమలు_చేయి_ఆదేశం('guest-korean-javac',ప్రొజెక్ట్_మూలం/'예제/한글코딩/인사.java',[],'안녕하세요 · 합계=42')
        నిర్ధారణ_నివేదిక['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(ప్రమాణం_డేటా/'report.json').write_text(json.dumps(నిర్ధారణ_నివేదిక,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':నడుపుము()
