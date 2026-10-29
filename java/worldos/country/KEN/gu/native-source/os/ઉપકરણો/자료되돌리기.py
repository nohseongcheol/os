#!/usr/bin/env python3
"""હોસ્ટ 루프백 주소에만 바인딩하는 UDP 시험 સર્વર_મૂલ્ય. Ctrl+C로 종료한다."""
import argparse
import socket

def અમલ_કરો_આદેશ():
    પાર્સ_કરો_મૂલ્ય = argparse.ArgumentParser(description='jkoros ઉપયોગકર્તા UDP 예제의 로컬 되돌림 સર્વર_મૂલ્ય')
    પાર્સ_કરો_મૂલ્ય.add_argument('--port', type=int, default=9000)
    પેરામીટર_દલીલ = પાર્સ_કરો_મૂલ્ય.parse_args()
    if not 1 <= પેરામીટર_દલીલ.port <= 65535: પાર્સ_કરો_મૂલ્ય.error('પૉર્ટ_મૂલ્ય 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as સર્વર_મૂલ્ય:
        સર્વર_મૂલ્ય.bind(('127.0.0.1', પેરામીટર_દલીલ.port))
        print('UDP 127.0.0.1:{} તૈયાર_કરો. Ctrl+C로 પ્રસ્થાન_એપ્લિકેશન.'.format(પેરામીટર_દલીલ.port), flush=True)
        while True:
            ડેટા, પીઅર_મૂલ્ય = સર્વર_મૂલ્ય.recvfrom(65535)
            સર્વર_મૂલ્ય.sendto(ડેટા, પીઅર_મૂલ્ય)

if __name__ == '__main__':
    try: અમલ_કરો_આદેશ()
    except KeyboardInterrupt: pass
