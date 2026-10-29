#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from Vykdyti_komanda import Project_šaknis

def Paleisti():
    KR_duomenys=Project_šaknis/'build/verification/coding';KR_duomenys.mkdir(parents=True,exist_ok=True)
    tikrinimas_pranešti={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_šaknis/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(Project_šaknis/'Įrankiai/eksportuoti_SDK.py')])
        with tarfile.open(str(Project_šaknis/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(KR_duomenys))
        programuotojo_rinkinys=KR_duomenys/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(programuotojo_rinkinys/'lib/libposix-kor-user.a')]).decode()
        for Pavadinimas_2 in ('kurti_dalyvis','BIND_ADDRESS','siųsti_paketų_kelio_schema_duomenys','gauti_paketų_kelio_schema_duomenys','kurti_Failas','파일자료읽기','rašymas_Failas_duomenys'):
            assert ' T '+Pavadinimas_2+'\n' in 심볼목록, Pavadinimas_2
        (KR_duomenys/'korean-function-symbols.txt').write_text(심볼목록)
        tikrinimas_pranešti['checks'].append('real-korean-c-function-symbols')
        def Vykdyti_komanda(Pavadinimas_2,KELIAS,argumentas_ARRAY,예상결과):
            duomenys_padėtis=subprocess.run(['python3',str(Project_šaknis/'Įrankiai/Vykdyti_Failas.py'),str(KELIAS)]+argumentas_ARRAY,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (KR_duomenys/(Pavadinimas_2+'.log')).write_bytes(duomenys_padėtis.stdout);assert duomenys_padėtis.returncode==0,duomenys_padėtis.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in duomenys_padėtis.stdout,duomenys_padėtis.stdout;tikrinimas_pranešti['checks'].append(Pavadinimas_2)
        for 뒷부분 in ('c','cpp'):
            실행파일=KR_duomenys/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(programuotojo_rinkinys/'compile.py'),str(programuotojo_rinkinys/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            Vykdyti_komanda('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=KR_duomenys/'Stream_VALUE.elf'
        subprocess.check_call(['python3',str(programuotojo_rinkinys/'compile.py'),str(programuotojo_rinkinys/'examples/Stream_VALUE.c'),'-o',str(실행파일)])
        Vykdyti_komanda('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        Vykdyti_komanda('korean-python',Project_šaknis/'예제/한글코딩/인사.py',['--include',str(Project_šaknis/'예제/한글코딩/Lietuvių.py')],'안녕하세요 누리')
        Vykdyti_komanda('guest-korean-javac',Project_šaknis/'예제/한글코딩/인사.java',[],'안녕하세요 · bendras_VALUE=42')
        tikrinimas_pranešti['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(KR_duomenys/'report.json').write_text(json.dumps(tikrinimas_pranešti,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Paleisti()
