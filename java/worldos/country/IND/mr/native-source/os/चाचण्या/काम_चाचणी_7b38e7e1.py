#!/usr/bin/env python3
"""होस्ट libc 없이 연결한 मराठी C 프로그램을 वास्तविक_डेटा ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from प्रयोक्ता_संचारजाळे_चाचणी import व्हर्च्युअल_मशीन

जागा = Path(__file__).resolve().parents[1]

def आज्ञा_कार्यवाही_करा():
    मोजमाप = {}
    सर्व्हर_मूल्य = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    सर्व्हर_मूल्य.bind(('127.0.0.1', 0))
    सर्व्हर_मूल्य.settimeout(0.1)
    पोर्ट_नंबर = सर्व्हर_मूल्य.getsockname()[1]
    स्वीकारलेले_डेटा = []
    समाप्ती_राज्य = threading.Event()
    def प्रतिध्वनी_प्रत्युत्तर_द्या():
        while not समाप्ती_राज्य.is_set():
            try:
                डेटा, पत्ता = सर्व्हर_मूल्य.recvfrom(4096)
            except socket.timeout:
                continue
            स्वीकारलेले_डेटा.append(डेटा)
            सर्व्हर_मूल्य.sendto(डेटा, पत्ता)
    कार्यसूत्र_मूल्य = threading.Thread(target=प्रतिध्वनी_प्रत्युत्तर_द्या, daemon=True)
    कार्यसूत्र_मूल्य.start()
    try:
        for प्रकार_मूल्य in ('elf', 'iso'):
            मशीन = व्हर्च्युअल_मशीन(जागा / ('build/kernel.' + प्रकार_मूल्य), प्रकार_मूल्य)
            try:
                for पुनरावृत्ती_मूल्य in range(2):
                    मशीन.आदेश('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    मशीन.आदेश('run posixudp ' + str(पोर्ट_नंबर), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                सुरू_करा = len(मशीन.लॉग_नोंद)
                मशीन.अनुक्रमिक_मूल्य.sendall(b'run posixinput\n')
                मशीन.प्रतीक्षा_करा_राज्य('POSIX INPUT READY', सुरू_करा)
                मशीन.अनुक्रमिक_मूल्य.sendall(b'abcdef')
                आउटपुट = मशीन.प्रतीक्षा_करा_राज्य('jkoros> ', सुरू_करा)
                assert 'POSIX INPUT PASS' in आउटपुट and 'Exit: 0' in आउटपुट, आउटपुट
                मशीन.आदेश('javac Hello.java', ['Exit: 0'])
                मशीन.आदेश('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                मशीन.आदेश('run hello recovered', ['arg: recovered', 'Exit: 0'])
                मोजमाप[प्रकार_मूल्य] = मशीन.लॉग_नोंद.decode('utf-8', 'replace')
                print('PASS:', प्रकार_मूल्य, 'POSIX फाइल/공유 जागा/삭제 수명/पत्ता संरक्षण_मूल्य/UDP/표준 आदान_मूल्य/기존 Java', flush=True)
            finally:
                मशीन.बंद_करा()
        assert b'posix-udp' in स्वीकारलेले_डेटा and b'truncate' in स्वीकारलेले_डेटा and b'' in स्वीकारलेले_डेटा
    finally:
        समाप्ती_राज्य.set(); कार्यसूत्र_मूल्य.join(timeout=2); सर्व्हर_मूल्य.close()
    मोजमाप['host_datagrams'] = [डेटा.decode() for डेटा in स्वीकारलेले_डेटा]
    (जागा / 'build/काम_चाचणी_7b38e7e1.json').write_text(json.dumps(मोजमाप, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    आज्ञा_कार्यवाही_करा()
