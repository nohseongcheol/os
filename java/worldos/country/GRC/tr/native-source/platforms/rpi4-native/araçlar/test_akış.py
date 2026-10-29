#!/usr/bin/env python3
import hashlib,json,subprocess
from yürütmek_komut import işlem_kök

def çalıştır():
    KR_veri=işlem_kök/'build/verification/stream';KR_veri.mkdir(parents=True,exist_ok=True)
    doğrulama_Rapor={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((işlem_kök/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(KR_veri),str(işlem_kök/'sınamalar/자바/test_akış.java')])
        veri_konum=subprocess.run(['python3',str(işlem_kök/'araçlar/yürütmek_Dosya.py'),str(KR_veri/'test_akış.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (KR_veri/'serial.log').write_bytes(veri_konum.stdout);assert veri_konum.returncode==0,veri_konum.stdout.decode('utf-8','replace')
        metin=veri_konum.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in metin,metin
        doğrulama_Rapor.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(KR_veri/'report.json').write_text(json.dumps(doğrulama_Rapor,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':çalıştır()
