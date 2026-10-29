#!/usr/bin/env python3
import hashlib,json,subprocess
from Виконати_команда import Дії_корінь

def запустити():
    КР_дані=Дії_корінь/'build/verification/stream';КР_дані.mkdir(parents=True,exist_ok=True)
    перевірка_звіт={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Дії_корінь/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(КР_дані),str(Дії_корінь/'випробування/자바/흐름시험.java')])
        дані_посада=subprocess.run(['python3',str(Дії_корінь/'інструменти/Виконати_Файл.py'),str(КР_дані/'흐름시험.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (КР_дані/'serial.log').write_bytes(дані_посада.stdout);assert дані_посада.returncode==0,дані_посада.stdout.decode('utf-8','replace')
        текст=дані_посада.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in текст,текст
        перевірка_звіт.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(КР_дані/'report.json').write_text(json.dumps(перевірка_звіт,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':запустити()
