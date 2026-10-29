#!/usr/bin/env python3
import hashlib,json,subprocess
from اجرا_فرمان import نمایش_دادن_جذر

def اجرا_2():
    سنجش_داده_ها=نمایش_دادن_جذر/'build/verification/stream';سنجش_داده_ها.mkdir(parents=True,exist_ok=True)
    اعتبارسنجی_گزارش={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((نمایش_دادن_جذر/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(سنجش_داده_ها),str(نمایش_دادن_جذر/'시험/자바/흐름시험.java')])
        داده_ها_مرتب_کردن=subprocess.run(['python3',str(نمایش_دادن_جذر/'ابزارها/اجرا_فایل.py'),str(سنجش_داده_ها/'흐름시험.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (سنجش_داده_ها/'serial.log').write_bytes(داده_ها_مرتب_کردن.stdout);assert داده_ها_مرتب_کردن.returncode==0,داده_ها_مرتب_کردن.stdout.decode('utf-8','replace')
        متن=داده_ها_مرتب_کردن.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in متن,متن
        اعتبارسنجی_گزارش.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(سنجش_داده_ها/'report.json').write_text(json.dumps(اعتبارسنجی_گزارش,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':اجرا_2()
