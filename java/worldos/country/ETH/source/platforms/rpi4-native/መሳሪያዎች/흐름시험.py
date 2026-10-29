#!/usr/bin/env python3
import hashlib,json,subprocess
from ፈጽም_ትእዛዝ import አሳይ_ስር

def ማስኬጃ():
    ልኬት_ውሂብ=አሳይ_ስር/'build/verification/stream';ልኬት_ውሂብ.mkdir(parents=True,exist_ok=True)
    ማረጋገጥ_ዘገባ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((አሳይ_ስር/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(ልኬት_ውሂብ),str(አሳይ_ስር/'시험/자바/흐름시험.java')])
        ውሂብ_በቦታ_አስቀመጠ=subprocess.run(['python3',str(አሳይ_ስር/'መሳሪያዎች/ፈጽም_ፋይል.py'),str(ልኬት_ውሂብ/'흐름시험.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (ልኬት_ውሂብ/'serial.log').write_bytes(ውሂብ_በቦታ_አስቀመጠ.stdout);assert ውሂብ_በቦታ_አስቀመጠ.returncode==0,ውሂብ_በቦታ_አስቀመጠ.stdout.decode('utf-8','replace')
        ጽሁፍ=ውሂብ_በቦታ_አስቀመጠ.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in ጽሁፍ,ጽሁፍ
        ማረጋገጥ_ዘገባ.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(ልኬት_ውሂብ/'report.json').write_text(json.dumps(ማረጋገጥ_ዘገባ,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':ማስኬጃ()
