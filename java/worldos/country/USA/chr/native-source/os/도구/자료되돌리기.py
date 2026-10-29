#!/usr/bin/env python3
"""ᎠᏁᏢᏍᎩ 루프백 주소에만 바인딩하는 UDP 시험 ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ. Ctrl+C로 종료한다."""
import argparse
import socket

def ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ():
    해석 = argparse.ArgumentParser(description='jkoros ᎬᏗᏍᎩ UDP 예제의 로컬 되돌림 ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ')
    해석.add_argument('--port', type=int, default=9000)
    인자 = 해석.parse_args()
    if not 1 <= 인자.port <= 65535: 해석.error('ᎫᏓᎸᏗ_ᏧᎬᏩᎶᏗᏯ 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ:
        ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ.bind(('127.0.0.1', 인자.port))
        print('UDP 127.0.0.1:{} ᎭᏛᏅᎢᏍᏓ. Ctrl+C로 ᎦᏅᎪᎢᏍᏗ_ᎬᏙᏗ.'.format(인자.port), flush=True)
        while True:
            ᎦᏟᏌᏅᎯ, ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ = ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ.recvfrom(65535)
            ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ.sendto(ᎦᏟᏌᏅᎯ, ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ)

if __name__ == '__main__':
    try: ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ()
    except KeyboardInterrupt: pass
