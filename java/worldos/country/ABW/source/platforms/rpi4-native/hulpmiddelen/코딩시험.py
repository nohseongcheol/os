#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from Uitvoeren_opdracht import Taken_wortel

def starten():
    HR_gegevens=Taken_wortel/'build/verification/coding';HR_gegevens.mkdir(parents=True,exist_ok=True)
    validatie_Rapport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Taken_wortel/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(Taken_wortel/'hulpmiddelen/exporteren_SDK.py')])
        with tarfile.open(str(Taken_wortel/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(HR_gegevens))
        Development_Kit=HR_gegevens/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(Development_Kit/'lib/libposix-kor-user.a')]).decode()
        for Naam in ('maken_eindpunt','BIND_ADRES','e_mailen_datagram_gegevens','ontvangen_datagram_gegevens','open_Bestand','파일자료읽기','schrijven_Bestand_gegevens'):
            assert ' T '+Naam+'\n' in 심볼목록, Naam
        (HR_gegevens/'korean-function-symbols.txt').write_text(심볼목록)
        validatie_Rapport['checks'].append('real-korean-c-function-symbols')
        def Uitvoeren_opdracht(Naam,pad,argument_MATRIX,예상결과):
            gegevens_functie=subprocess.run(['python3',str(Taken_wortel/'hulpmiddelen/Uitvoeren_Bestand.py'),str(pad)]+argument_MATRIX,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (HR_gegevens/(Naam+'.log')).write_bytes(gegevens_functie.stdout);assert gegevens_functie.returncode==0,gegevens_functie.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in gegevens_functie.stdout,gegevens_functie.stdout;validatie_Rapport['checks'].append(Naam)
        for 뒷부분 in ('c','cpp'):
            uitvoerbaar_bestand=HR_gegevens/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(Development_Kit/'compile.py'),str(Development_Kit/'examples'/('인사.'+뒷부분)),'-o',str(uitvoerbaar_bestand)])
            Uitvoeren_opdracht('korean-'+뒷부분,uitvoerbaar_bestand,[],'posix-kor 호출')
        uitvoerbaar_bestand=HR_gegevens/'Stream_WAARDE.elf'
        subprocess.check_call(['python3',str(Development_Kit/'compile.py'),str(Development_Kit/'examples/Stream_WAARDE.c'),'-o',str(uitvoerbaar_bestand)])
        Uitvoeren_opdracht('c-stream-queues',uitvoerbaar_bestand,[],'C posix-kor 연결형 communicatie PASS')
        Uitvoeren_opdracht('korean-python',Taken_wortel/'예제/한글코딩/인사.py',['--include',str(Taken_wortel/'예제/한글코딩/Nederlands.py')],'안녕하세요 누리')
        Uitvoeren_opdracht('guest-korean-javac',Taken_wortel/'예제/한글코딩/인사.java',[],'안녕하세요 · totaal_WAARDE=42')
        validatie_Rapport['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(HR_gegevens/'report.json').write_text(json.dumps(validatie_Rapport,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':starten()
