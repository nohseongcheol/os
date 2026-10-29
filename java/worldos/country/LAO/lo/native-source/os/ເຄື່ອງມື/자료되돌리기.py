#!/usr/bin/env python3
"""ໂຮສ 루프백 주소에만 바인딩하는 UDP 시험 서버. Ctrl+C로 종료한다."""
import argparse
import socket

def ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ():
    ການແຈກຄໍາສັບ_ຄ່າ = argparse.ArgumentParser(description='jkoros ຜູ້ໃຊ້ UDP 예제의 로컬 되돌림 서버')
    ການແຈກຄໍາສັບ_ຄ່າ.add_argument('--port', type=int, default=9000)
    ພາຣາມິເຕີ_ຂໍ້ພິສູດ = ການແຈກຄໍາສັບ_ຄ່າ.parse_args()
    if not 1 <= ພາຣາມິເຕີ_ຂໍ້ພິສູດ.port <= 65535: ການແຈກຄໍາສັບ_ຄ່າ.error('ຜອດ_ຄ່າ 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 서버:
        서버.bind(('127.0.0.1', ພາຣາມິເຕີ_ຂໍ້ພິສູດ.port))
        print('UDP 127.0.0.1:{} ກະ_ກຽມ. Ctrl+C로 ອອກ_ແອັບ.'.format(ພາຣາມິເຕີ_ຂໍ້ພິສູດ.port), flush=True)
        while True:
            ຂໍ້ມູນ, ລຸ້ນດຽວກັນ_ຄ່າ = 서버.recvfrom(65535)
            서버.sendto(ຂໍ້ມູນ, ລຸ້ນດຽວກັນ_ຄ່າ)

if __name__ == '__main__':
    try: ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ()
    except KeyboardInterrupt: pass
