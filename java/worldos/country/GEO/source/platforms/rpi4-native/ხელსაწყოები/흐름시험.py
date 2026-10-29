#!/usr/bin/env python3
import hashlib,json,subprocess
from შესრულება_ბრძანება import პროეცირება_ფესვი

def გაშვება():
    გაზომვა_მონაცემები=პროეცირება_ფესვი/'build/verification/stream';გაზომვა_მონაცემები.mkdir(parents=True,exist_ok=True)
    გადამოწმება_ანგარიში={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((პროეცირება_ფესვი/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(გაზომვა_მონაცემები),str(პროეცირება_ფესვი/'시험/자바/흐름시험.java')])
        მონაცემები_პოზიცია=subprocess.run(['python3',str(პროეცირება_ფესვი/'ხელსაწყოები/შესრულება_ფაილი.py'),str(გაზომვა_მონაცემები/'흐름시험.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (გაზომვა_მონაცემები/'serial.log').write_bytes(მონაცემები_პოზიცია.stdout);assert მონაცემები_პოზიცია.returncode==0,მონაცემები_პოზიცია.stdout.decode('utf-8','replace')
        ტექსტი=მონაცემები_პოზიცია.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in ტექსტი,ტექსტი
        გადამოწმება_ანგარიში.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(გაზომვა_მონაცემები/'report.json').write_text(json.dumps(გადამოწმება_ანგარიში,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':გაშვება()
