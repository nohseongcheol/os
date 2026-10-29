#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from bajarmoq_buyruq import Project_ildiz

def Bajarish():
    o_lchov_ma_lumotlar=Project_ildiz/'build/verification/coding';o_lchov_ma_lumotlar.mkdir(parents=True,exist_ok=True)
    tasdiq_hisobot={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_ildiz/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(Project_ildiz/'Vositalar/개발꾸러미내보내기.py')])
        with tarfile.open(str(Project_ildiz/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(o_lchov_ma_lumotlar))
        개발꾸러미=o_lchov_ma_lumotlar/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(개발꾸러미/'lib/libposix-kor-user.a')]).decode()
        for Nomi in ('통신종단점만들기','BOG_LAMOQ_manzil','자료전문보내기','자료전문받기','ochmoq_fayl','파일자료읽기','yozmoq_fayl_ma_lumotlar'):
            assert ' T '+Nomi+'\n' in 심볼목록, Nomi
        (o_lchov_ma_lumotlar/'korean-function-symbols.txt').write_text(심볼목록)
        tasdiq_hisobot['checks'].append('real-korean-c-function-symbols')
        def bajarmoq_buyruq(Nomi,yo_l,dalil_ARRAY,예상결과):
            ma_lumotlar_holat=subprocess.run(['python3',str(Project_ildiz/'Vositalar/bajarmoq_fayl.py'),str(yo_l)]+dalil_ARRAY,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (o_lchov_ma_lumotlar/(Nomi+'.log')).write_bytes(ma_lumotlar_holat.stdout);assert ma_lumotlar_holat.returncode==0,ma_lumotlar_holat.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in ma_lumotlar_holat.stdout,ma_lumotlar_holat.stdout;tasdiq_hisobot['checks'].append(Nomi)
        for 뒷부분 in ('c','cpp'):
            실행파일=o_lchov_ma_lumotlar/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            bajarmoq_buyruq('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=o_lchov_ma_lumotlar/'oqim_VALUE.elf'
        subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples/oqim_VALUE.c'),'-o',str(실행파일)])
        bajarmoq_buyruq('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        bajarmoq_buyruq('korean-python',Project_ildiz/'예제/한글코딩/인사.py',['--include',str(Project_ildiz/'예제/한글코딩/한국어.py')],'안녕하세요 누리')
        bajarmoq_buyruq('guest-korean-javac',Project_ildiz/'예제/한글코딩/인사.java',[],'안녕하세요 · 합계=42')
        tasdiq_hisobot['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(o_lchov_ma_lumotlar/'report.json').write_text(json.dumps(tasdiq_hisobot,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Bajarish()
