#!/usr/bin/env python3
"""အိမ်ရှင် libc 없이 연결한 မြန်မာ C 프로그램을 တကယ့်ဒေတာ ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from သုံးစွဲဆက်သွယ်စမ်းသပ် import စက်တု

နေရာ = Path(__file__).resolve().parents[1]

def စက်မောင်း():
    ရလဒ် = {}
    ဝန်ဆောင်စက်တန်ဖိုး = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ဝန်ဆောင်စက်တန်ဖိုး.bind(('127.0.0.1', 0))
    ဝန်ဆောင်စက်တန်ဖိုး.settimeout(0.1)
    ဆက်သွယ်ပေါက်ကိန်း = ဝန်ဆောင်စက်တန်ဖိုး.getsockname()[1]
    ရရှိဒေတာ = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                ဒေတာ, လိပ်စာ = ဝန်ဆောင်စက်တန်ဖိုး.recvfrom(4096)
            except socket.timeout:
                continue
            ရရှိဒေတာ.append(ဒေတာ)
            ဝန်ဆောင်စက်တန်ဖိုး.sendto(ဒေတာ, လိပ်စာ)
    အလုပ်သမားတန်ဖိုး = threading.Thread(target=되보내기, daemon=True)
    အလုပ်သမားတန်ဖိုး.start()
    try:
        for အမျိုးအစားတန်ဖိုး in ('elf', 'iso'):
            စက် = စက်တု(နေရာ / ('build/kernel.' + အမျိုးအစားတန်ဖိုး), အမျိုးအစားတန်ဖိုး)
            try:
                for 반복 in range(2):
                    စက်.အမိန့်('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    စက်.အမိန့်('run posixudp ' + str(ဆက်သွယ်ပေါက်ကိန်း), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                လုပ်ဆောင် = len(စက်.မှတ်တမ်းမှတ်တမ်းတစ်ခု)
                စက်.အစဉ်ဆက်တန်ဖိုး.sendall(b'run posixinput\n')
                စက်.အခြေအနေစောင့်('POSIX INPUT READY', လုပ်ဆောင်)
                စက်.အစဉ်ဆက်တန်ဖိုး.sendall(b'abcdef')
                အထွက် = စက်.အခြေအနေစောင့်('jkoros> ', လုပ်ဆောင်)
                assert 'POSIX INPUT PASS' in အထွက် and 'Exit: 0' in အထွက်, အထွက်
                စက်.အမိန့်('javac Hello.java', ['Exit: 0'])
                စက်.အမိန့်('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                စက်.အမိန့်('run hello recovered', ['arg: recovered', 'Exit: 0'])
                ရလဒ်[အမျိုးအစားတန်ဖိုး] = စက်.မှတ်တမ်းမှတ်တမ်းတစ်ခု.decode('utf-8', 'replace')
                print('PASS:', အမျိုးအစားတန်ဖိုး, 'POSIX ဖိုင်/공유 နေရာ/삭제 수명/လိပ်စာ တန်ဖိုးကာကွယ်/UDP/표준 ဝင်ဒေတာ/기존 Java', flush=True)
            finally:
                စက်.ပိတ်()
        assert b'posix-udp' in ရရှိဒေတာ and b'truncate' in ရရှိဒေတာ and b'' in ရရှိဒေတာ
    finally:
        끝냄.set(); အလုပ်သမားတန်ဖိုး.join(timeout=2); ဝန်ဆောင်စက်တန်ဖိုး.close()
    ရလဒ်['host_datagrams'] = [ဒေတာ.decode() for ဒေတာ in ရရှိဒေတာ]
    (နေရာ / 'build/စည်းမျဉ်းစမ်းသပ်.json').write_text(json.dumps(ရလဒ်, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    စက်မောင်း()
