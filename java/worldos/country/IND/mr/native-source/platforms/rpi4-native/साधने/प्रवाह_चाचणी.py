#!/usr/bin/env python3
import hashlib,json,subprocess
from आज्ञा_कार्यवाही_करा import प्रोजेक्ट_मूळ

def सुरू_करा():
    मोजमाप_डेटा=प्रोजेक्ट_मूळ/'build/verification/stream';मोजमाप_डेटा.mkdir(parents=True,exist_ok=True)
    पडताळणी_अहवाल={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((प्रोजेक्ट_मूळ/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(मोजमाप_डेटा),str(प्रोजेक्ट_मूळ/'चाचण्या/जावा/प्रवाह_चाचणी.java')])
        डेटा_स्थान=subprocess.run(['python3',str(प्रोजेक्ट_मूळ/'साधने/संचिका_कार्यवाही_करा.py'),str(मोजमाप_डेटा/'प्रवाह_चाचणी.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (मोजमाप_डेटा/'serial.log').write_bytes(डेटा_स्थान.stdout);assert डेटा_स्थान.returncode==0,डेटा_स्थान.stdout.decode('utf-8','replace')
        पाठ्य=डेटा_स्थान.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 मर्यादा_मूल्य\nDNS आहे_असमर्थित\nSTREAM PASS\nexit 0\n' in पाठ्य,पाठ्य
        पडताळणी_अहवाल.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(मोजमाप_डेटा/'report.json').write_text(json.dumps(पडताळणी_अहवाल,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':सुरू_करा()
