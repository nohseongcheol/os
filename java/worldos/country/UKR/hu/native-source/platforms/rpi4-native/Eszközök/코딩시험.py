#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from végrehajt_parancs import teendő_gyök

def Futtatás():
    KR_adat=teendő_gyök/'build/verification/coding';KR_adat.mkdir(parents=True,exist_ok=True)
    ellenőrzés_jelent={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((teendő_gyök/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(teendő_gyök/'Eszközök/exportál_SDK.py')])
        with tarfile.open(str(teendő_gyök/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(KR_adat))
        fejlesztőkészlet=KR_adat/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(fejlesztőkészlet/'lib/libposix-kor-user.a')]).decode()
        for Név in ('készít_végpont','BIND_CÍM','küld_datagram_adat','fogad_datagram_adat','készít_Fájl','파일자료읽기','ír_Fájl_adat'):
            assert ' T '+Név+'\n' in 심볼목록, Név
        (KR_adat/'korean-function-symbols.txt').write_text(심볼목록)
        ellenőrzés_jelent['checks'].append('real-korean-c-function-symbols')
        def végrehajt_parancs(Név,ÚTVONAL,argumentum_TÖMB,예상결과):
            adat_pozíció=subprocess.run(['python3',str(teendő_gyök/'Eszközök/végrehajt_Fájl.py'),str(ÚTVONAL)]+argumentum_TÖMB,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (KR_adat/(Név+'.log')).write_bytes(adat_pozíció.stdout);assert adat_pozíció.returncode==0,adat_pozíció.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in adat_pozíció.stdout,adat_pozíció.stdout;ellenőrzés_jelent['checks'].append(Név)
        for 뒷부분 in ('c','cpp'):
            végrehajtható_Fájl=KR_adat/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(fejlesztőkészlet/'compile.py'),str(fejlesztőkészlet/'examples'/('인사.'+뒷부분)),'-o',str(végrehajtható_Fájl)])
            végrehajt_parancs('korean-'+뒷부분,végrehajtható_Fájl,[],'posix-kor 호출')
        végrehajtható_Fájl=KR_adat/'Stream_ÉRTÉK.elf'
        subprocess.check_call(['python3',str(fejlesztőkészlet/'compile.py'),str(fejlesztőkészlet/'examples/Stream_ÉRTÉK.c'),'-o',str(végrehajtható_Fájl)])
        végrehajt_parancs('c-stream-queues',végrehajtható_Fájl,[],'C posix-kor 연결형 kommunikáció PASS')
        végrehajt_parancs('korean-python',teendő_gyök/'예제/한글코딩/인사.py',['--include',str(teendő_gyök/'예제/한글코딩/magyar.py')],'안녕하세요 누리')
        végrehajt_parancs('guest-korean-javac',teendő_gyök/'예제/한글코딩/인사.java',[],'안녕하세요 · összesen_ÉRTÉK=42')
        ellenőrzés_jelent['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(KR_adat/'report.json').write_text(json.dumps(ellenőrzés_jelent,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Futtatás()
