#!/usr/bin/env python3
import hashlib,json,subprocess
from לבצע_פקודה import לשקף_בסיס

def הפעלה():
    תוצאה_נתונים=לשקף_בסיס/'build/verification/stream';תוצאה_נתונים.mkdir(parents=True,exist_ok=True)
    אימות_דוח={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((לשקף_בסיס/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(תוצאה_נתונים),str(לשקף_בסיס/'시험/자바/נסה_זרם.java')])
        נתונים_עמדה=subprocess.run(['python3',str(לשקף_בסיס/'כלים/לבצע_קובץ.py'),str(תוצאה_נתונים/'נסה_זרם.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (תוצאה_נתונים/'serial.log').write_bytes(נתונים_עמדה.stdout);assert נתונים_עמדה.returncode==0,נתונים_עמדה.stdout.decode('utf-8','replace')
        טקסט=נתונים_עמדה.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in טקסט,טקסט
        אימות_דוח.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(תוצאה_נתונים/'report.json').write_text(json.dumps(אימות_דוח,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':הפעלה()
