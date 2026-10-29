#!/usr/bin/env python3
"""ארח libc 없이 연결한 עברית C 프로그램을 בפועל_נתונים ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from נסה_משתמש_רשת import מחשב_וירטואלי

מיקום = Path(__file__).resolve().parents[1]

def לבצע_פקודה():
    תוצאה = {}
    שרת_ערך = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    שרת_ערך.bind(('127.0.0.1', 0))
    שרת_ערך.settimeout(0.1)
    מספר_יציאה = שרת_ערך.getsockname()[1]
    받은자료 = []
    끝냄 = threading.Event()
    def הד_מענה():
        while not 끝냄.is_set():
            try:
                נתונים, למען = שרת_ערך.recvfrom(4096)
            except socket.timeout:
                continue
            받은자료.append(נתונים)
            שרת_ערך.sendto(נתונים, למען)
    עובד_ערך = threading.Thread(target=הד_מענה, daemon=True)
    עובד_ערך.start()
    try:
        for 종류 in ('elf', 'iso'):
            מחשב = מחשב_וירטואלי(מיקום / ('build/kernel.' + 종류), 종류)
            try:
                for סבב_ערך in range(2):
                    מחשב.פקודה('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    מחשב.פקודה('run posixudp ' + str(מספר_יציאה), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                הפעלה = len(מחשב.לרשום_שיא)
                מחשב.직렬.sendall(b'run posixinput\n')
                מחשב.מצב_המתנה('POSIX INPUT READY', הפעלה)
                מחשב.직렬.sendall(b'abcdef')
                פלטטקסט = מחשב.מצב_המתנה('jkoros> ', הפעלה)
                assert 'POSIX INPUT PASS' in פלטטקסט and 'Exit: 0' in פלטטקסט, פלטטקסט
                מחשב.פקודה('javac Hello.java', ['Exit: 0'])
                מחשב.פקודה('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                מחשב.פקודה('run hello recovered', ['arg: recovered', 'Exit: 0'])
                תוצאה[종류] = מחשב.לרשום_שיא.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX קובץ/공유 מיקום/삭제 수명/למען הגן_ערך/UDP/표준 קלט_ערך/기존 Java', flush=True)
            finally:
                מחשב.סגירה()
        assert b'posix-udp' in 받은자료 and b'truncate' in 받은자료 and b'' in 받은자료
    finally:
        끝냄.set(); עובד_ערך.join(timeout=2); שרת_ערך.close()
    תוצאה['host_datagrams'] = [נתונים.decode() for נתונים in 받은자료]
    (מיקום / 'build/חוזה_נסה.json').write_text(json.dumps(תוצאה, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    לבצע_פקודה()
