#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from exekutatu_komando import Project_erro

def Exekutatu_2():
    neurria_datuak=Project_erro/'build/verification/coding';neurria_datuak.mkdir(parents=True,exist_ok=True)
    balidazio_txosten={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_erro/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(Project_erro/'Tresnak/개발꾸러미내보내기.py')])
        with tarfile.open(str(Project_erro/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(neurria_datuak))
        개발꾸러미=neurria_datuak/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(개발꾸러미/'lib/libposix-kor-user.a')]).decode()
        for Izena in ('sortu_amaiera_puntu','lotu_helbide','자료전문보내기','자료전문받기','ireki_fitxategi','파일자료읽기','idatzi_fitxategi_datuak'):
            assert ' T '+Izena+'\n' in 심볼목록, Izena
        (neurria_datuak/'korean-function-symbols.txt').write_text(심볼목록)
        balidazio_txosten['checks'].append('real-korean-c-function-symbols')
        def exekutatu_komando(Izena,Bide_izena,arg_matrize,예상결과):
            datuak_kargu=subprocess.run(['python3',str(Project_erro/'Tresnak/exekutatu_fitxategi.py'),str(Bide_izena)]+arg_matrize,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (neurria_datuak/(Izena+'.log')).write_bytes(datuak_kargu.stdout);assert datuak_kargu.returncode==0,datuak_kargu.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in datuak_kargu.stdout,datuak_kargu.stdout;balidazio_txosten['checks'].append(Izena)
        for 뒷부분 in ('c','cpp'):
            실행파일=neurria_datuak/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            exekutatu_komando('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=neurria_datuak/'Stream_balio.elf'
        subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples/Stream_balio.c'),'-o',str(실행파일)])
        exekutatu_komando('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        exekutatu_komando('korean-python',Project_erro/'예제/한글코딩/인사.py',['--include',str(Project_erro/'예제/한글코딩/Euskara.py')],'안녕하세요 누리')
        exekutatu_komando('guest-korean-javac',Project_erro/'예제/한글코딩/인사.java',[],'안녕하세요 · 합계=42')
        balidazio_txosten['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(neurria_datuak/'report.json').write_text(json.dumps(balidazio_txosten,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Exekutatu_2()
