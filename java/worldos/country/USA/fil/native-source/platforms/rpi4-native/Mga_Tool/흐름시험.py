#!/usr/bin/env python3
import hashlib,json,subprocess
from Mag_execute_utos import Project_root

def run():
    sukat_data=Project_root/'build/verification/stream';sukat_data.mkdir(parents=True,exist_ok=True)
    pagpapatibay_ulat={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_root/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(sukat_data),str(Project_root/'시험/자바/흐름시험.java')])
        data_posisyon=subprocess.run(['python3',str(Project_root/'Mga_Tool/Mag_execute_file.py'),str(sukat_data/'흐름시험.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (sukat_data/'serial.log').write_bytes(data_posisyon.stdout);assert data_posisyon.returncode==0,data_posisyon.stdout.decode('utf-8','replace')
        SMS=data_posisyon.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in SMS,SMS
        pagpapatibay_ulat.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(sukat_data/'report.json').write_text(json.dumps(pagpapatibay_ulat,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':run()
