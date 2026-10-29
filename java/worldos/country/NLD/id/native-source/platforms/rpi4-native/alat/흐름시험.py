#!/usr/bin/env python3
import hashlib,json,subprocess
from Jalankan_perintah import Tugas_akar

def jalankan():
    KR_data=Tugas_akar/'build/verification/stream';KR_data.mkdir(parents=True,exist_ok=True)
    validasi_lapor={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Tugas_akar/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(KR_data),str(Tugas_akar/'pengujian/자바/흐름시험.java')])
        data_posisi=subprocess.run(['python3',str(Tugas_akar/'alat/Jalankan_file.py'),str(KR_data/'흐름시험.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (KR_data/'serial.log').write_bytes(data_posisi.stdout);assert data_posisi.returncode==0,data_posisi.stdout.decode('utf-8','replace')
        teks=data_posisi.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in teks,teks
        validasi_lapor.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(KR_data/'report.json').write_text(json.dumps(validasi_lapor,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':jalankan()
