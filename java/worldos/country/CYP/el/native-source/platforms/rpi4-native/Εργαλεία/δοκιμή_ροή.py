#!/usr/bin/env python3
import hashlib,json,subprocess
from εκτελώ_εντολή import έργο_ρίζα

def Εκτέλεση_2():
    μέτρηση_δεδομένα=έργο_ρίζα/'build/verification/stream';μέτρηση_δεδομένα.mkdir(parents=True,exist_ok=True)
    επικύρωση_έκθεση={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((έργο_ρίζα/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(μέτρηση_δεδομένα),str(έργο_ρίζα/'시험/자바/δοκιμή_ροή.java')])
        δεδομένα_θέση=subprocess.run(['python3',str(έργο_ρίζα/'Εργαλεία/εκτελώ_Αρχείο.py'),str(μέτρηση_δεδομένα/'δοκιμή_ροή.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (μέτρηση_δεδομένα/'serial.log').write_bytes(δεδομένα_θέση.stdout);assert δεδομένα_θέση.returncode==0,δεδομένα_θέση.stdout.decode('utf-8','replace')
        Κείμενο=δεδομένα_θέση.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in Κείμενο,Κείμενο
        επικύρωση_έκθεση.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(μέτρηση_δεδομένα/'report.json').write_text(json.dumps(επικύρωση_έκθεση,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Εκτέλεση_2()
