#!/usr/bin/env python3
"""sauka 루프백 주소에만 바인딩하는 UDP 시험 Saba_Daraja. Ctrl+C로 종료한다."""
import argparse
import socket

def gudanar_Umarni():
    Daddatse_Daraja = argparse.ArgumentParser(description='jkoros Mai_anfani_da_kwamfuta UDP 예제의 로컬 되돌림 Saba_Daraja')
    Daddatse_Daraja.add_argument('--port', type=int, default=9000)
    maaunin_Tubalin_aiki = Daddatse_Daraja.parse_args()
    if not 1 <= maaunin_Tubalin_aiki.port <= 65535: Daddatse_Daraja.error('fot_Daraja 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as Saba_Daraja:
        Saba_Daraja.bind(('127.0.0.1', maaunin_Tubalin_aiki.port))
        print('UDP 127.0.0.1:{} Shirya. Ctrl+C로 Mafita_Shiri.'.format(maaunin_Tubalin_aiki.port), flush=True)
        while True:
            Tarin_bayani, Fiya_Daraja = Saba_Daraja.recvfrom(65535)
            Saba_Daraja.sendto(Tarin_bayani, Fiya_Daraja)

if __name__ == '__main__':
    try: gudanar_Umarni()
    except KeyboardInterrupt: pass
