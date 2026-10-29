#!/usr/bin/env python3
"""sauka libc 없이 연결한 한국어 C 프로그램을 Na_hakika_Tarin_bayani ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import Mai_alaka_da_aikin_na_ura_na_boye_na_ura_mai_kwakwalwa

위치 = Path(__file__).resolve().parents[1]

def gudanar_Umarni():
    결과 = {}
    Saba_Daraja = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    Saba_Daraja.bind(('127.0.0.1', 0))
    Saba_Daraja.settimeout(0.1)
    lambar_kafa = Saba_Daraja.getsockname()[1]
    받은자료 = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                Tarin_bayani, imel = Saba_Daraja.recvfrom(4096)
            except socket.timeout:
                continue
            받은자료.append(Tarin_bayani)
            Saba_Daraja.sendto(Tarin_bayani, imel)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            na_ura_mai_kwakwalwa = Mai_alaka_da_aikin_na_ura_na_boye_na_ura_mai_kwakwalwa(위치 / ('build/kernel.' + 종류), 종류)
            try:
                for sifirint_Daraja in range(2):
                    na_ura_mai_kwakwalwa.Umarni('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    na_ura_mai_kwakwalwa.Umarni('run posixudp ' + str(lambar_kafa), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                Tafiyar_da = len(na_ura_mai_kwakwalwa.logu_naɗa)
                na_ura_mai_kwakwalwa.직렬.sendall(b'run posixinput\n')
                na_ura_mai_kwakwalwa.jira_Matsayi('POSIX INPUT READY', Tafiyar_da)
                na_ura_mai_kwakwalwa.직렬.sendall(b'abcdef')
                출력 = na_ura_mai_kwakwalwa.jira_Matsayi('jkoros> ', Tafiyar_da)
                assert 'POSIX INPUT PASS' in 출력 and 'Exit: 0' in 출력, 출력
                na_ura_mai_kwakwalwa.Umarni('javac Hello.java', ['Exit: 0'])
                na_ura_mai_kwakwalwa.Umarni('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                na_ura_mai_kwakwalwa.Umarni('run hello recovered', ['arg: recovered', 'Exit: 0'])
                결과[종류] = na_ura_mai_kwakwalwa.logu_naɗa.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX Fayil/공유 위치/삭제 수명/imel Kare_Daraja/UDP/표준 입력/기존 Java', flush=True)
            finally:
                na_ura_mai_kwakwalwa.Rufe()
        assert b'posix-udp' in 받은자료 and b'truncate' in 받은자료 and b'' in 받은자료
    finally:
        끝냄.set(); 일꾼.join(timeout=2); Saba_Daraja.close()
    결과['host_datagrams'] = [Tarin_bayani.decode() for Tarin_bayani in 받은자료]
    (위치 / 'build/규약시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    gudanar_Umarni()
