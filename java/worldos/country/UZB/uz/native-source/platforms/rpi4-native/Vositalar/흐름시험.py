#!/usr/bin/env python3
import hashlib,json,subprocess
from bajarmoq_buyruq import Project_ildiz

def Bajarish():
    o_lchov_ma_lumotlar=Project_ildiz/'build/verification/stream';o_lchov_ma_lumotlar.mkdir(parents=True,exist_ok=True)
    tasdiq_hisobot={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_ildiz/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(o_lchov_ma_lumotlar),str(Project_ildiz/'시험/자바/흐름시험.java')])
        ma_lumotlar_holat=subprocess.run(['python3',str(Project_ildiz/'Vositalar/bajarmoq_fayl.py'),str(o_lchov_ma_lumotlar/'흐름시험.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (o_lchov_ma_lumotlar/'serial.log').write_bytes(ma_lumotlar_holat.stdout);assert ma_lumotlar_holat.returncode==0,ma_lumotlar_holat.stdout.decode('utf-8','replace')
        Matn=ma_lumotlar_holat.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in Matn,Matn
        tasdiq_hisobot.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(o_lchov_ma_lumotlar/'report.json').write_text(json.dumps(tasdiq_hisobot,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Bajarish()
