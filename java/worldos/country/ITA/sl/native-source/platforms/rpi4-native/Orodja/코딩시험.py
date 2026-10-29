#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from Izvedi_ukaz import pobuda_koren

def Zaženi():
    KR_podatki=pobuda_koren/'build/verification/coding';KR_podatki.mkdir(parents=True,exist_ok=True)
    preverjanje_veljavnosti_prijavi={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((pobuda_koren/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(pobuda_koren/'Orodja/izvoziti_komplet_za_razvoj_programske_opreme.py')])
        with tarfile.open(str(pobuda_koren/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(KR_podatki))
        razvijalski_komplet=KR_podatki/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(razvijalski_komplet/'lib/libposix-kor-user.a')]).decode()
        for Ime in ('Ustvari_končna_točka','BIND_naslov','poslati_datagram_podatki','sprejeti_sprejemati_prejeti_prejemati_datagram_podatki','odprto_Datoteka','파일자료읽기','pisati_Datoteka_podatki'):
            assert ' T '+Ime+'\n' in 심볼목록, Ime
        (KR_podatki/'korean-function-symbols.txt').write_text(심볼목록)
        preverjanje_veljavnosti_prijavi['checks'].append('real-korean-c-function-symbols')
        def Izvedi_ukaz(Ime,POT,argument_ARRAY,예상결과):
            podatki_položaj=subprocess.run(['python3',str(pobuda_koren/'Orodja/Izvedi_Datoteka.py'),str(POT)]+argument_ARRAY,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (KR_podatki/(Ime+'.log')).write_bytes(podatki_položaj.stdout);assert podatki_položaj.returncode==0,podatki_položaj.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in podatki_položaj.stdout,podatki_položaj.stdout;preverjanje_veljavnosti_prijavi['checks'].append(Ime)
        for 뒷부분 in ('c','cpp'):
            실행파일=KR_podatki/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(razvijalski_komplet/'compile.py'),str(razvijalski_komplet/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            Izvedi_ukaz('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=KR_podatki/'tok_VALUE.elf'
        subprocess.check_call(['python3',str(razvijalski_komplet/'compile.py'),str(razvijalski_komplet/'examples/tok_VALUE.c'),'-o',str(실행파일)])
        Izvedi_ukaz('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        Izvedi_ukaz('korean-python',pobuda_koren/'예제/한글코딩/인사.py',['--include',str(pobuda_koren/'예제/한글코딩/slovenščina.py')],'안녕하세요 누리')
        Izvedi_ukaz('guest-korean-javac',pobuda_koren/'예제/한글코딩/인사.java',[],'안녕하세요 · skupaj_VALUE=42')
        preverjanje_veljavnosti_prijavi['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(KR_podatki/'report.json').write_text(json.dumps(preverjanje_veljavnosti_prijavi,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Zaženi()
