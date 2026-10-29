#!/usr/bin/env python3
import hashlib,json,subprocess
from executeCommand import projectRoot

def run():
    resultData=projectRoot/'build/verification/stream';resultData.mkdir(parents=True,exist_ok=True)
    validationReport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((projectRoot/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(resultData),str(projectRoot/'tests/Java/testStream.java')])
        dataPosition=subprocess.run(['python3',str(projectRoot/'tools/executeFile.py'),str(resultData/'testStream.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (resultData/'serial.log').write_bytes(dataPosition.stdout);assert dataPosition.returncode==0,dataPosition.stdout.decode('utf-8','replace')
        text=dataPosition.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 limitValue\nDNS isUnsupported\nSTREAM PASS\nexit 0\n' in text,text
        validationReport.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(resultData/'report.json').write_text(json.dumps(validationReport,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':run()
