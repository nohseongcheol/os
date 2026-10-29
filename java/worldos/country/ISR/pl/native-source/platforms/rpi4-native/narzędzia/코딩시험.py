#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from Wykonaj_polecenie import Project_korzeń

def Uruchom_2():
    KR_dane=Project_korzeń/'build/verification/coding';KR_dane.mkdir(parents=True,exist_ok=True)
    walidacja_Raport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_korzeń/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(Project_korzeń/'narzędzia/eksportować_SDK.py')])
        with tarfile.open(str(Project_korzeń/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(KR_dane))
        zestaw_deweloperski=KR_dane/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(zestaw_deweloperski/'lib/libposix-kor-user.a')]).decode()
        for Nazwa in ('Twórca_uczestnik','BIND_ADRES','wysłać_datagram_dane','odbierać_datagram_dane','otwarty_Plik','파일자료읽기','zapis_Plik_dane'):
            assert ' T '+Nazwa+'\n' in 심볼목록, Nazwa
        (KR_dane/'korean-function-symbols.txt').write_text(심볼목록)
        walidacja_Raport['checks'].append('real-korean-c-function-symbols')
        def Wykonaj_polecenie(Nazwa,ścieżka_2,argument_TABLICA,예상결과):
            dane_stanowisko=subprocess.run(['python3',str(Project_korzeń/'narzędzia/Wykonaj_Plik.py'),str(ścieżka_2)]+argument_TABLICA,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (KR_dane/(Nazwa+'.log')).write_bytes(dane_stanowisko.stdout);assert dane_stanowisko.returncode==0,dane_stanowisko.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in dane_stanowisko.stdout,dane_stanowisko.stdout;walidacja_Raport['checks'].append(Nazwa)
        for 뒷부분 in ('c','cpp'):
            plik_wykonywalny=KR_dane/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(zestaw_deweloperski/'compile.py'),str(zestaw_deweloperski/'examples'/('인사.'+뒷부분)),'-o',str(plik_wykonywalny)])
            Wykonaj_polecenie('korean-'+뒷부분,plik_wykonywalny,[],'posix-kor 호출')
        plik_wykonywalny=KR_dane/'Stream_WARTOŚĆ.elf'
        subprocess.check_call(['python3',str(zestaw_deweloperski/'compile.py'),str(zestaw_deweloperski/'examples/Stream_WARTOŚĆ.c'),'-o',str(plik_wykonywalny)])
        Wykonaj_polecenie('c-stream-queues',plik_wykonywalny,[],'C posix-kor 연결형 komunikacja PASS')
        Wykonaj_polecenie('korean-python',Project_korzeń/'예제/한글코딩/인사.py',['--include',str(Project_korzeń/'예제/한글코딩/polski.py')],'안녕하세요 누리')
        Wykonaj_polecenie('guest-korean-javac',Project_korzeń/'예제/한글코딩/인사.java',[],'안녕하세요 · suma_WARTOŚĆ=42')
        walidacja_Raport['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(KR_dane/'report.json').write_text(json.dumps(walidacja_Raport,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Uruchom_2()
