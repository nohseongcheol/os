"""Layer-2/SLIP bridge. TCP, UDP and FTP are processed by the guest, not Python.

QEMU's user network supplies NAT/host forwarding. raspi4b has no emulated GENET,
so a second UART carries IPv4 packets to the guest's lwIP stack.
"""
import select
import socket
import struct
import threading
import time
import ipaddress
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, qemu_network

ເຄື່ອງຈັກ_ອີເມວ = bytes.fromhex('525400123456')
관문기계주소 = bytes.fromhex('52550a000202')
ທີ່ຢູ່ອິນເຕີເນັດ_ຄ່າ = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class ເຄືອຂ່າຍ_ຕົວເຊື່ອມ:
    def __init__(자신, ຟາຍ_ໂອນ_ຫມາຍເລກພອດ=2121, 전달규칙들=(), ບັນທຶກ_ba7b8054=False, ແຂກ_ອີເມວ=None, ໂຮສ_ອີເມວ='127.0.0.1'):
        if not 1024 <= ຟາຍ_ໂອນ_ຫມາຍເລກພອດ <= 65535 or 50000 <= ຟາຍ_ໂອນ_ຫມາຍເລກພອດ <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.ຟາຍ_ໂອນ_ຫມາຍເລກພອດ = ຟາຍ_ໂອນ_ຫມາຍເລກພອດ
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        ແຂກ_ອີເມວ = ແຂກ_ອີເມວ or 자신.ip_config['IP']
        qemu_network(자신.ip_config, ແຂກ_ອີເມວ)
        ອີເມວ=ipaddress.IPv4Address(ແຂກ_ອີເມວ)
        자신.ແຂກ_ອີເມວ=str(ອີເມວ); 자신.현재주소=ອີເມວ.packed
        ອີເມວ=ipaddress.IPv4Address(ໂຮສ_ອີເມວ)
        if ອີເມວ.is_multicast or str(ອີເມວ)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.ໂຮສ_ອີເມວ=str(ອີເມວ)
        자신.ບັນທຶກ_ba7b8054 = ບັນທຶກ_ba7b8054; 자신.추적기록 = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', ຟາຍ_ໂອນ_ຫມາຍເລກພອດ)} | {('tcp', ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ) for ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ in range(50000,50008)}
        for ລະບຽບ_ຄ່າ in 전달규칙들:
            ທາງໂຄຈອນ_ອົງປະກອບ = ລະບຽບ_ຄ່າ.split(':')
            if len(ທາງໂຄຈອນ_ອົງປະກອບ) != 3 or ທາງໂຄຈອນ_ອົງປະກອບ[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, ໂຮສ, ແຂກ = ທາງໂຄຈອນ_ອົງປະກອບ[0], int(ທາງໂຄຈອນ_ອົງປະກອບ[1]), int(ທາງໂຄຈອນ_ອົງປະກອບ[2])
            if not 1024 <= ໂຮສ <= 65535 or not 1 <= ແຂກ <= 65535 or (통신규약, ໂຮສ) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + ລະບຽບ_ຄ່າ)
            사용중주소.add((통신규약, ໂຮສ)); 자신.전달규칙들.append((통신규약, ໂຮສ, ແຂກ))
        자신.수신창구들 = []
        for _ in range(2):
            서버 = socket.socket()
            서버.bind(('127.0.0.1', 0)); 서버.listen(1); 서버.setblocking(False)
            자신.수신창구들.append(서버)
        자신.접속자들 = [None, None]
        자신.ເທັກໂນໂລຢີຂໍ້ມູນຂ່າວສານ_ລໍຖ້າດໍາເນີນການ = [bytearray(), bytearray()]
        자신.ການເຊື່ອມຕໍ່ແບບຜ່ານສາຍ = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.ເທັກໂນໂລຢີຂໍ້ມູນຂ່າວສານ_ໃຊ້ບໍ່ໄດ້ = False
        자신.ຢຸດຊົ່ວຄາວ_ງານ = threading.Event(); 자신.ຂໍ້ຜິດພາດ = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.작업가닥 = threading.Thread(target=자신.ຮອບ_ຄ່າ, daemon=True)
        자신.작업가닥.start()

    def 전달인수(자신):
        직렬접속번호, ການເຊື່ອມຕໍ່ແບບຜ່ານສາຍ_ຜອດ = [ສະຕຣິງ_ຂໍ້ມູນ.getsockname()[1] for ສະຕຣິງ_ຂໍ້ມູນ in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.ແຂກ_ອີເມວ) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.ຟາຍ_ໂອນ_ຫມາຍເລກພອດ, 자신.ແຂກ_ອີເມວ)
        for ຫມາຍເລກພອດ in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(ຫມາຍເລກພອດ, 자신.ແຂກ_ອີເມວ)
        for 통신규약, ໂຮສ, ແຂກ in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, ໂຮສ, 자신.ແຂກ_ອີເມວ, ແຂກ)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.ໂຮສ_ອີເມວ+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(직렬접속번호),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(ການເຊື່ອມຕໍ່ແບບຜ່ານສາຍ_ຜອດ),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, ແພັກເກັດ_ຂໍ້ມູນ):
        자신.ເທັກໂນໂລຢີຂໍ້ມູນຂ່າວສານ_ລໍຖ້າດໍາເນີນການ[1] += struct.pack('!I', len(ແພັກເກັດ_ຂໍ້ມູນ)) + ແພັກເກັດ_ຂໍ້ມູນ

    def 전문추적(자신, 방향, ແພັກເກັດ_ຂໍ້ມູນ):
        if not 자신.ບັນທຶກ_ba7b8054 or len(ແພັກເກັດ_ຂໍ້ມູນ)<20: return
        ອອບເຊັດ_ຄ່າ=(ແພັກເກັດ_ຂໍ້ມູນ[0]&15)*4
        ເຂົ້າໃນ_ຄ່າ={'time':time.monotonic(),'direction':방향,'bytes':len(ແພັກເກັດ_ຂໍ້ມູນ),'protocol':ແພັກເກັດ_ຂໍ້ມູນ[9]}
        if ແພັກເກັດ_ຂໍ້ມູນ[9]==6 and len(ແພັກເກັດ_ຂໍ້ມູນ)>=ອອບເຊັດ_ຄ່າ+20:
            원본자료,ປາຍທາງ_ຂໍ້ມູນ_ອີເມວ,순서번호,확인번호,ການຕັ້ງຄ່າເຊື່ອມຕໍ່_ບໍລິການໂອນຍ້າຍອັດສະລິຍະໃນພື້ນຫຼັງ,ວິນໂດ=struct.unpack_from('!HHIIHH',ແພັກເກັດ_ຂໍ້ມູນ,ອອບເຊັດ_ຄ່າ)
            ເຂົ້າໃນ_ຄ່າ.update(source=원본자료,destination=ປາຍທາງ_ຂໍ້ມູນ_ອີເມວ,seq=순서번호,ack=확인번호,flags=ການຕັ້ງຄ່າເຊື່ອມຕໍ່_ບໍລິການໂອນຍ້າຍອັດສະລິຍະໃນພື້ນຫຼັງ&255,window=ວິນໂດ,
                        payload=len(ແພັກເກັດ_ຂໍ້ມູນ)-ອອບເຊັດ_ຄ່າ-((ແພັກເກັດ_ຂໍ້ມູນ[ອອບເຊັດ_ຄ່າ+12]>>4)*4))
        자신.추적기록.append(ເຂົ້າໃນ_ຄ່າ)
        if len(자신.추적기록)>2048: del 자신.추적기록[:1024]

    def 직렬전문입력(자신, ຂໍ້ມູນ):
        for ຈຸດ_ລະ_ຫັດ in ຂໍ້ມູນ:
            if ຈຸດ_ລະ_ຫັດ == 192:
                if 자신.직렬전문 and not 자신.ເທັກໂນໂລຢີຂໍ້ມູນຂ່າວສານ_ໃຊ້ບໍ່ໄດ້ and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        ອີເມວ=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(ອີເມວ)))
                            자신.현재주소=ອີເມວ
                        except ValueError:
                            pass
                    자신.전문추적('from_guest',자신.직렬전문)
                    자신.실행틀(관문기계주소 + ເຄື່ອງຈັກ_ອີເມວ + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.ເທັກໂນໂລຢີຂໍ້ມູນຂ່າວສານ_ໃຊ້ບໍ່ໄດ້ = False
            elif ຈຸດ_ລະ_ຫັດ == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if ຈຸດ_ລະ_ຫັດ not in (220, 221): 자신.ເທັກໂນໂລຢີຂໍ້ມູນຂ່າວສານ_ໃຊ້ບໍ່ໄດ້ = True
                    ຈຸດ_ລະ_ຫັດ = 192 if ຈຸດ_ລະ_ຫັດ == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(ຈຸດ_ລະ_ຫັດ)
                else: 자신.ເທັກໂນໂລຢີຂໍ້ມູນຂ່າວສານ_ໃຊ້ບໍ່ໄດ້ = True

    def 이더넷입력(자신, ຂໍ້ມູນ):
        자신.ການເຊື່ອມຕໍ່ແບບຜ່ານສາຍ += ຂໍ້ມູນ
        while len(자신.ການເຊື່ອມຕໍ່ແບບຜ່ານສາຍ) >= 4:
            개수 = struct.unpack_from('!I', 자신.ການເຊື່ອມຕໍ່ແບບຜ່ານສາຍ)[0]
            if 개수 > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.ການເຊື່ອມຕໍ່ແບບຜ່ານສາຍ) < 개수 + 4: return
            실행틀 = bytes(자신.ການເຊື່ອມຕໍ່ແບບຜ່ານສາຍ[4:4+개수]); del 자신.ການເຊື່ອມຕໍ່ແບບຜ່ານສາຍ[:4+개수]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                ອີເມວ_ຄວາມລະອຽດ_ແພັກເກັດ = 실행틀[14:42]
                if ອີເມວ_ຄວາມລະອຽດ_ແພັກເກັດ[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and ອີເມວ_ຄວາມລະອຽດ_ແພັກເກັດ[24:28] == 자신.현재주소:
                    응답자료 = ອີເມວ_ຄວາມລະອຽດ_ແພັກເກັດ[:6] + b'\x00\x02' + ເຄື່ອງຈັກ_ອີເມວ + 자신.현재주소 + ອີເມວ_ຄວາມລະອຽດ_ແພັກເກັດ[8:18]
                    자신.실행틀(실행틀[6:12] + ເຄື່ອງຈັກ_ອີເມວ + b'\x08\x06' + 응답자료)
            elif 실행틀[12:14] == b'\x08\x00':
                ແພັກເກັດ_ຂໍ້ມູນ = 실행틀[14:]
                자신.전문추적('to_guest',ແພັກເກັດ_ຂໍ້ມູນ)
                자신.ເທັກໂນໂລຢີຂໍ້ມູນຂ່າວສານ_ລໍຖ້າດໍາເນີນການ[0] += b'\xc0' + ແພັກເກັດ_ຂໍ້ມູນ.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def ຮອບ_ຄ່າ(자신):
        try:
            while not 자신.ຢຸດຊົ່ວຄາວ_ງານ.is_set():
                읽기대상들 = [ສະຕຣິງ_ຂໍ້ມູນ for 순번, ສະຕຣິງ_ຂໍ້ມູນ in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [ສະຕຣິງ_ຂໍ້ມູນ for ສະຕຣິງ_ຂໍ້ມູນ in 자신.접속자들 if ສະຕຣິງ_ຂໍ້ມູນ is not None]
                쓰기대상들 = [ສະຕຣິງ_ຂໍ້ມູນ for 순번, ສະຕຣິງ_ຂໍ້ມູນ in enumerate(자신.접속자들) if ສະຕຣິງ_ຂໍ້ມູນ is not None and 자신.ເທັກໂນໂລຢີຂໍ້ມູນຂ່າວສານ_ລໍຖ້າດໍາເນີນການ[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for ສະຕຣິງ_ຂໍ້ມູນ in 읽을수있음:
                    if ສະຕຣິງ_ຂໍ້ມູນ in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(ສະຕຣິງ_ຂໍ້ມູນ); 자신.접속자들[순번], _ = ສະຕຣິງ_ຂໍ້ມູນ.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(ສະຕຣິງ_ຂໍ້ມູນ); ຂໍ້ມູນ = ສະຕຣິງ_ຂໍ້ມູນ.recv(16384)
                        if not ຂໍ້ມູນ: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(ຂໍ້ມູນ)
                for ສະຕຣິງ_ຂໍ້ມູນ in 쓸수있음:
                    순번 = 자신.접속자들.index(ສະຕຣິງ_ຂໍ້ມູນ)
                    try: 개수 = ສະຕຣິງ_ຂໍ້ມູນ.send(자신.ເທັກໂນໂລຢີຂໍ້ມູນຂ່າວສານ_ລໍຖ້າດໍາເນີນການ[순번])
                    except BlockingIOError: continue
                    del 자신.ເທັກໂນໂລຢີຂໍ້ມູນຂ່າວສານ_ລໍຖ້າດໍາເນີນການ[순번][:개수]
                if any(len(둘째값) > 1024 * 1024 for 둘째값 in 자신.ເທັກໂນໂລຢີຂໍ້ມູນຂ່າວສານ_ລໍຖ້າດໍາເນີນການ):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.ຢຸດຊົ່ວຄາວ_ງານ.is_set(): 자신.ຂໍ້ຜິດພາດ = str(보조항목)

    def ປິດ(자신):
        자신.ຢຸດຊົ່ວຄາວ_ງານ.set(); 자신.작업가닥.join(timeout=2)
        for ສະຕຣິງ_ຂໍ້ມູນ in 자신.수신창구들 + 자신.접속자들:
            if ສະຕຣິງ_ຂໍ້ມູນ is not None: ສະຕຣິງ_ຂໍ້ມູນ.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ): 자신.ປິດ()
