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

машина_дарек = bytes.fromhex('525400123456')
관문기계주소 = bytes.fromhex('52550a000202')
Интернет_дарек_маани = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class 통신다리:
    def __init__(자신, 파일전송접속번호=2121, 전달규칙들=(), тартуу_жаздыруу=False, 게스트주소=None, кабылдоо_дарек='127.0.0.1'):
        if not 1024 <= 파일전송접속번호 <= 65535 or 50000 <= 파일전송접속번호 <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.파일전송접속번호 = 파일전송접속번호
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        게스트주소 = 게스트주소 or 자신.ip_config['IP']
        qemu_network(자신.ip_config, 게스트주소)
        дарек=ipaddress.IPv4Address(게스트주소)
        자신.게스트주소=str(дарек); 자신.현재주소=дарек.packed
        дарек=ipaddress.IPv4Address(кабылдоо_дарек)
        if дарек.is_multicast or str(дарек)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.кабылдоо_дарек=str(дарек)
        자신.тартуу_жаздыруу = тартуу_жаздыруу; 자신.추적기록 = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', 파일전송접속번호)} | {('tcp', 자료위치) for 자료위치 in range(50000,50008)}
        for чыпка_маани in 전달규칙들:
            жол_курамдык_бөлүк = чыпка_маани.split(':')
            if len(жол_курамдык_бөлүк) != 3 or жол_курамдык_бөлүк[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, кабылдоо, 커널실행 = жол_курамдык_бөлүк[0], int(жол_курамдык_бөлүк[1]), int(жол_курамдык_бөлүк[2])
            if not 1024 <= кабылдоо <= 65535 or not 1 <= 커널실행 <= 65535 or (통신규약, кабылдоо) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + чыпка_маани)
            사용중주소.add((통신규약, кабылдоо)); 자신.전달규칙들.append((통신규약, кабылдоо, 커널실행))
        자신.수신창구들 = []
        for _ in range(2):
            сервер_маани = socket.socket()
            сервер_маани.bind(('127.0.0.1', 0)); сервер_маани.listen(1); сервер_маани.setblocking(False)
            자신.수신창구들.append(сервер_маани)
        자신.접속자들 = [None, None]
        자신.대기중 = [bytearray(), bytearray()]
        자신.이더넷자료 = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.잘못됨 = False
        자신.пауза_окуя = threading.Event(); 자신.Ката = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.작업가닥 = threading.Thread(target=자신.Айлампа_маани, daemon=True)
        자신.작업가닥.start()

    def 전달인수(자신):
        직렬접속번호, 이더넷접속번호 = [сап_берилмелер.getsockname()[1] for сап_берилмелер in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.게스트주소) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.파일전송접속번호, 자신.게스트주소)
        for 접속번호 in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(접속번호, 자신.게스트주소)
        for 통신규약, кабылдоо, 커널실행 in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, кабылдоо, 자신.게스트주소, 커널실행)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.кабылдоо_дарек+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(직렬접속번호),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(이더넷접속번호),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, пакет_берилмелер):
        자신.대기중[1] += struct.pack('!I', len(пакет_берилмелер)) + пакет_берилмелер

    def 전문추적(자신, 방향, пакет_берилмелер):
        if not 자신.тартуу_жаздыруу or len(пакет_берилмелер)<20: return
        Жылбышуу_маани=(пакет_берилмелер[0]&15)*4
        киргизме_жазуу_маани={'time':time.monotonic(),'direction':방향,'bytes':len(пакет_берилмелер),'protocol':пакет_берилмелер[9]}
        if пакет_берилмелер[9]==6 and len(пакет_берилмелер)>=Жылбышуу_маани+20:
            원본자료,көздөө_жайы_берилмелер_дарек,순서번호,확인번호,설정비트,терезе=struct.unpack_from('!HHIIHH',пакет_берилмелер,Жылбышуу_маани)
            киргизме_жазуу_маани.update(source=원본자료,destination=көздөө_жайы_берилмелер_дарек,seq=순서번호,ack=확인번호,flags=설정비트&255,window=терезе,
                        payload=len(пакет_берилмелер)-Жылбышуу_маани-((пакет_берилмелер[Жылбышуу_маани+12]>>4)*4))
        자신.추적기록.append(киргизме_жазуу_маани)
        if len(자신.추적기록)>2048: del 자신.추적기록[:1024]

    def 직렬전문입력(자신, берилмелер):
        for символ_коду in берилмелер:
            if символ_коду == 192:
                if 자신.직렬전문 and not 자신.잘못됨 and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        дарек=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(дарек)))
                            자신.현재주소=дарек
                        except ValueError:
                            pass
                    자신.전문추적('from_guest',자신.직렬전문)
                    자신.실행틀(관문기계주소 + машина_дарек + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.잘못됨 = False
            elif символ_коду == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if символ_коду not in (220, 221): 자신.잘못됨 = True
                    символ_коду = 192 if символ_коду == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(символ_коду)
                else: 자신.잘못됨 = True

    def 이더넷입력(자신, берилмелер):
        자신.이더넷자료 += берилмелер
        while len(자신.이더넷자료) >= 4:
            개수 = struct.unpack_from('!I', 자신.이더넷자료)[0]
            if 개수 > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.이더넷자료) < 개수 + 4: return
            실행틀 = bytes(자신.이더넷자료[4:4+개수]); del 자신.이더넷자료[:4+개수]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                дарек_чечим_пакет = 실행틀[14:42]
                if дарек_чечим_пакет[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and дарек_чечим_пакет[24:28] == 자신.현재주소:
                    응답자료 = дарек_чечим_пакет[:6] + b'\x00\x02' + машина_дарек + 자신.현재주소 + дарек_чечим_пакет[8:18]
                    자신.실행틀(실행틀[6:12] + машина_дарек + b'\x08\x06' + 응답자료)
            elif 실행틀[12:14] == b'\x08\x00':
                пакет_берилмелер = 실행틀[14:]
                자신.전문추적('to_guest',пакет_берилмелер)
                자신.대기중[0] += b'\xc0' + пакет_берилмелер.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def Айлампа_маани(자신):
        try:
            while not 자신.пауза_окуя.is_set():
                읽기대상들 = [сап_берилмелер for 순번, сап_берилмелер in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [сап_берилмелер for сап_берилмелер in 자신.접속자들 if сап_берилмелер is not None]
                쓰기대상들 = [сап_берилмелер for 순번, сап_берилмелер in enumerate(자신.접속자들) if сап_берилмелер is not None and 자신.대기중[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for сап_берилмелер in 읽을수있음:
                    if сап_берилмелер in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(сап_берилмелер); 자신.접속자들[순번], _ = сап_берилмелер.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(сап_берилмелер); берилмелер = сап_берилмелер.recv(16384)
                        if not берилмелер: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(берилмелер)
                for сап_берилмелер in 쓸수있음:
                    순번 = 자신.접속자들.index(сап_берилмелер)
                    try: 개수 = сап_берилмелер.send(자신.대기중[순번])
                    except BlockingIOError: continue
                    del 자신.대기중[순번][:개수]
                if any(len(둘째값) > 1024 * 1024 for 둘째값 in 자신.대기중):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.пауза_окуя.is_set(): 자신.Ката = str(보조항목)

    def Жабуу(자신):
        자신.пауза_окуя.set(); 자신.작업가닥.join(timeout=2)
        for сап_берилмелер in 자신.수신창구들 + 자신.접속자들:
            if сап_берилмелер is not None: сап_берилмелер.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *аргумент_МАССИВ): 자신.Жабуу()
