#!/usr/bin/env python3
import hashlib,json,subprocess
from ดําเนินการ_คําสั่ง import แสดง_ราก

def เรียกใช้งาน():
    เมตริก_ข้อมูล=แสดง_ราก/'build/verification/stream';เมตริก_ข้อมูล.mkdir(parents=True,exist_ok=True)
    การตรวจสอบความถูกต้อง_รายงาน={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((แสดง_ราก/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(เมตริก_ข้อมูล),str(แสดง_ราก/'시험/자바/การทดสอบ_สตรีม.java')])
        ข้อมูล_ตําแหน่ง=subprocess.run(['python3',str(แสดง_ราก/'เครื่องมือ/ดําเนินการ_แฟ้ม.py'),str(เมตริก_ข้อมูล/'การทดสอบ_สตรีม.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (เมตริก_ข้อมูล/'serial.log').write_bytes(ข้อมูล_ตําแหน่ง.stdout);assert ข้อมูล_ตําแหน่ง.returncode==0,ข้อมูล_ตําแหน่ง.stdout.decode('utf-8','replace')
        ข้อความ=ข้อมูล_ตําแหน่ง.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in ข้อความ,ข้อความ
        การตรวจสอบความถูกต้อง_รายงาน.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(เมตริก_ข้อมูล/'report.json').write_text(json.dumps(การตรวจสอบความถูกต้อง_รายงาน,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':เรียกใช้งาน()
