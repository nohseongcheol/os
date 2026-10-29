#!/usr/bin/env python3
import hashlib,json,subprocess
from thựcThiLệnh import gốcCâyDựÁn

def chạy():
    dữLiệuKếtQuả=gốcCâyDựÁn/'build/verification/stream';dữLiệuKếtQuả.mkdir(parents=True,exist_ok=True)
    báoCáoViệcThẩmĐịnh={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((gốcCâyDựÁn/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(dữLiệuKếtQuả),str(gốcCâyDựÁn/'KiểmThử/Java/thửLuồng.java')])
        vịTríDữLiệu=subprocess.run(['python3',str(gốcCâyDựÁn/'CôngCụ/thựcThiTệp.py'),str(dữLiệuKếtQuả/'thửLuồng.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (dữLiệuKếtQuả/'serial.log').write_bytes(vịTríDữLiệu.stdout);assert vịTríDữLiệu.returncode==0,vịTríDữLiệu.stdout.decode('utf-8','replace')
        vănBản=vịTríDữLiệu.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 giáTrịGiớiHạn\nDNS làKhôngHỗTrợ\nSTREAM PASS\nexit 0\n' in vănBản,vănBản
        báoCáoViệcThẩmĐịnh.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(dữLiệuKếtQuả/'report.json').write_text(json.dumps(báoCáoViệcThẩmĐịnh,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':chạy()
