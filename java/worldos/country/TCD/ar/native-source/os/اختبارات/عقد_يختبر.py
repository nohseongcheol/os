#!/usr/bin/env python3
"""مضيف libc 없이 연결한 العربية C 프로그램을 الفعلي_بيانات ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from يختبر_مستخدم_شبكة import جهاز_ظاهري

موضع = Path(__file__).resolve().parents[1]

def ينفذ_أمر():
    نتيجة = {}
    خادم_قيمة = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    خادم_قيمة.bind(('127.0.0.1', 0))
    خادم_قيمة.settimeout(0.1)
    رقم_المنفذ = خادم_قيمة.getsockname()[1]
    받은자료 = []
    끝냄 = threading.Event()
    def ارتداد_رد():
        while not 끝냄.is_set():
            try:
                بيانات, عنوان = خادم_قيمة.recvfrom(4096)
            except socket.timeout:
                continue
            받은자료.append(بيانات)
            خادم_قيمة.sendto(بيانات, عنوان)
    عامل_قيمة = threading.Thread(target=ارتداد_رد, daemon=True)
    عامل_قيمة.start()
    try:
        for 종류 in ('elf', 'iso'):
            جهاز = جهاز_ظاهري(موضع / ('build/kernel.' + 종류), 종류)
            try:
                for تكرار_قيمة in range(2):
                    جهاز.أمر('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    جهاز.أمر('run posixudp ' + str(رقم_المنفذ), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                تشغيل = len(جهاز.سجل_سجل)
                جهاز.직렬.sendall(b'run posixinput\n')
                جهاز.حالة_انتظار('POSIX INPUT READY', تشغيل)
                جهاز.직렬.sendall(b'abcdef')
                مخرجات = جهاز.حالة_انتظار('jkoros> ', تشغيل)
                assert 'POSIX INPUT PASS' in مخرجات and 'Exit: 0' in مخرجات, مخرجات
                جهاز.أمر('javac Hello.java', ['Exit: 0'])
                جهاز.أمر('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                جهاز.أمر('run hello recovered', ['arg: recovered', 'Exit: 0'])
                نتيجة[종류] = جهاز.سجل_سجل.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX ملف/공유 موضع/삭제 수명/عنوان يحمي_قيمة/UDP/표준 إدخال_قيمة/기존 Java', flush=True)
            finally:
                جهاز.إغلاق()
        assert b'posix-udp' in 받은자료 and b'truncate' in 받은자료 and b'' in 받은자료
    finally:
        끝냄.set(); عامل_قيمة.join(timeout=2); خادم_قيمة.close()
    نتيجة['host_datagrams'] = [بيانات.decode() for بيانات in 받은자료]
    (موضع / 'build/عقد_يختبر.json').write_text(json.dumps(نتيجة, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    ينفذ_أمر()
