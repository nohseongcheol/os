#!/usr/bin/env python3
import hashlib,json,subprocess
from laksanakan_perintah import projek_akar

def Jalan():
    ukuran_data=projek_akar/'build/verification/stream';ukuran_data.mkdir(parents=True,exist_ok=True)
    pensahihan_lapor={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((projek_akar/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(ukuran_data),str(projek_akar/'ujian/자바/ujian_strim.java')])
        data_jawatan=subprocess.run(['python3',str(projek_akar/'alat/laksanakan_fail.py'),str(ukuran_data/'ujian_strim.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (ukuran_data/'serial.log').write_bytes(data_jawatan.stdout);assert data_jawatan.returncode==0,data_jawatan.stdout.decode('utf-8','replace')
        Teks=data_jawatan.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in Teks,Teks
        pensahihan_lapor.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(ukuran_data/'report.json').write_text(json.dumps(pensahihan_lapor,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Jalan()
