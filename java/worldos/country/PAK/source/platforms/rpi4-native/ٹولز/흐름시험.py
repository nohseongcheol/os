#!/usr/bin/env python3
import hashlib,json,subprocess
from نفاذ_کریں_حکم import عکس_ڈالنا_روٹ

def چلائیں():
    پیمائش_کوائف=عکس_ڈالنا_روٹ/'build/verification/stream';پیمائش_کوائف.mkdir(parents=True,exist_ok=True)
    توثیق_رپورٹ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((عکس_ڈالنا_روٹ/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(پیمائش_کوائف),str(عکس_ڈالنا_روٹ/'시험/자바/흐름시험.java')])
        کوائف_پوزیشن_ٹھیک_کریں=subprocess.run(['python3',str(عکس_ڈالنا_روٹ/'ٹولز/نفاذ_کریں_فائل.py'),str(پیمائش_کوائف/'흐름시험.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (پیمائش_کوائف/'serial.log').write_bytes(کوائف_پوزیشن_ٹھیک_کریں.stdout);assert کوائف_پوزیشن_ٹھیک_کریں.returncode==0,کوائف_پوزیشن_ٹھیک_کریں.stdout.decode('utf-8','replace')
        متن=کوائف_پوزیشن_ٹھیک_کریں.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in متن,متن
        توثیق_رپورٹ.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(پیمائش_کوائف/'report.json').write_text(json.dumps(توثیق_رپورٹ,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':چلائیں()
