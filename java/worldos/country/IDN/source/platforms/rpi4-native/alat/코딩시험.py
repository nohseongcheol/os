#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from Jalankan_perintah import Tugas_akar

def jalankan():
    KR_data=Tugas_akar/'build/verification/coding';KR_data.mkdir(parents=True,exist_ok=True)
    validasi_lapor={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Tugas_akar/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(Tugas_akar/'alat/Ekspor_SDK.py')])
        with tarfile.open(str(Tugas_akar/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(KR_data))
        개발꾸러미=KR_data/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(개발꾸러미/'lib/libposix-kor-user.a')]).decode()
        for Nama_2 in ('Buat_peserta','ikat_surel','자료전문보내기','자료전문받기','buat_file','파일자료읽기','tulis_file_data'):
            assert ' T '+Nama_2+'\n' in 심볼목록, Nama_2
        (KR_data/'korean-function-symbols.txt').write_text(심볼목록)
        validasi_lapor['checks'].append('real-korean-c-function-symbols')
        def Jalankan_perintah(Nama_2,jalur,argumen_ARRAY,예상결과):
            data_posisi=subprocess.run(['python3',str(Tugas_akar/'alat/Jalankan_file.py'),str(jalur)]+argumen_ARRAY,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (KR_data/(Nama_2+'.log')).write_bytes(data_posisi.stdout);assert data_posisi.returncode==0,data_posisi.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in data_posisi.stdout,data_posisi.stdout;validasi_lapor['checks'].append(Nama_2)
        for 뒷부분 in ('c','cpp'):
            실행파일=KR_data/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            Jalankan_perintah('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=KR_data/'Stream_VALUE.elf'
        subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples/Stream_VALUE.c'),'-o',str(실행파일)])
        Jalankan_perintah('c-stream-queues',실행파일,[],'C posix-kor 연결형 komunikasi PASS')
        Jalankan_perintah('korean-python',Tugas_akar/'예제/한글코딩/인사.py',['--include',str(Tugas_akar/'예제/한글코딩/Indonesia.py')],'안녕하세요 누리')
        Jalankan_perintah('guest-korean-javac',Tugas_akar/'예제/한글코딩/인사.java',[],'안녕하세요 · total_VALUE=42')
        validasi_lapor['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(KR_data/'report.json').write_text(json.dumps(validasi_lapor,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':jalankan()
