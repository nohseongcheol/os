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

ማሽን_አድራሻ = bytes.fromhex('525400123456')
관문기계주소 = bytes.fromhex('52550a000202')
የበይነመረብ_አድራሻ_እሴት = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class መረብ_ድልድይ:
    def __init__(자신, ፋይል_ትልልፍ_የወደብ_ቁጥር=2121, 전달규칙들=(), መያዝ=False, እንግዳ_አድራሻ=None, አዘጋጅ_አድራሻ='127.0.0.1'):
        if not 1024 <= ፋይል_ትልልፍ_የወደብ_ቁጥር <= 65535 or 50000 <= ፋይል_ትልልፍ_የወደብ_ቁጥር <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.ፋይል_ትልልፍ_የወደብ_ቁጥር = ፋይል_ትልልፍ_የወደብ_ቁጥር
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        እንግዳ_አድራሻ = እንግዳ_አድራሻ or 자신.ip_config['IP']
        qemu_network(자신.ip_config, እንግዳ_አድራሻ)
        አድራሻ=ipaddress.IPv4Address(እንግዳ_አድራሻ)
        자신.እንግዳ_አድራሻ=str(አድራሻ); 자신.현재주소=አድራሻ.packed
        አድራሻ=ipaddress.IPv4Address(አዘጋጅ_አድራሻ)
        if አድራሻ.is_multicast or str(አድራሻ)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.አዘጋጅ_አድራሻ=str(አድራሻ)
        자신.መያዝ = መያዝ; 자신.ዱካ_መዝግብ = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', ፋይል_ትልልፍ_የወደብ_ቁጥር)} | {('tcp', ውሂብ_በቦታ_አስቀመጠ) for ውሂብ_በቦታ_አስቀመጠ in range(50000,50008)}
        for ደንብ_እሴት in 전달규칙들:
            ዱካ_አካል = ደንብ_እሴት.split(':')
            if len(ዱካ_አካል) != 3 or ዱካ_አካል[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, አዘጋጅ_b78e430d, እንግዳ = ዱካ_አካል[0], int(ዱካ_አካል[1]), int(ዱካ_አካል[2])
            if not 1024 <= አዘጋጅ_b78e430d <= 65535 or not 1 <= እንግዳ <= 65535 or (통신규약, አዘጋጅ_b78e430d) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + ደንብ_እሴት)
            사용중주소.add((통신규약, አዘጋጅ_b78e430d)); 자신.전달규칙들.append((통신규약, አዘጋጅ_b78e430d, እንግዳ))
        자신.수신창구들 = []
        for _ in range(2):
            አገልጋይ_እሴት = socket.socket()
            አገልጋይ_እሴት.bind(('127.0.0.1', 0)); አገልጋይ_እሴት.listen(1); አገልጋይ_እሴት.setblocking(False)
            자신.수신창구들.append(አገልጋይ_እሴት)
        자신.접속자들 = [None, None]
        자신.የመረጃ_ቴክኖሎጂ_ተጠባባቂ = [bytearray(), bytearray()]
        자신.ኢተርኔት = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.የመረጃ_ቴክኖሎጂ_ልክ_ያልኾነ = False
        자신.ላፍታ_አቁም_ፍጻሜ = threading.Event(); 자신.ስህተት = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.작업가닥 = threading.Thread(target=자신.ዑደት_እሴት, daemon=True)
        자신.작업가닥.start()

    def 전달인수(자신):
        직렬접속번호, ኢተርኔት_ወደብ = [ኅብረቁምፊ_ውሂብ.getsockname()[1] for ኅብረቁምፊ_ውሂብ in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.እንግዳ_አድራሻ) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.ፋይል_ትልልፍ_የወደብ_ቁጥር, 자신.እንግዳ_አድራሻ)
        for የወደብ_ቁጥር in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(የወደብ_ቁጥር, 자신.እንግዳ_አድራሻ)
        for 통신규약, አዘጋጅ_b78e430d, እንግዳ in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, አዘጋጅ_b78e430d, 자신.እንግዳ_አድራሻ, እንግዳ)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.አዘጋጅ_አድራሻ+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(직렬접속번호),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(ኢተርኔት_ወደብ),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, ፓኬት_ውሂብ):
        자신.የመረጃ_ቴክኖሎጂ_ተጠባባቂ[1] += struct.pack('!I', len(ፓኬት_ውሂብ)) + ፓኬት_ውሂብ

    def ዱካ_ፓኬት(자신, 방향, ፓኬት_ውሂብ):
        if not 자신.መያዝ or len(ፓኬት_ውሂብ)<20: return
        ዝንፍ_እሴት=(ፓኬት_ውሂብ[0]&15)*4
        ምዝግብ_እሴት={'time':time.monotonic(),'direction':방향,'bytes':len(ፓኬት_ውሂብ),'protocol':ፓኬት_ውሂብ[9]}
        if ፓኬት_ውሂብ[9]==6 and len(ፓኬት_ውሂብ)>=ዝንፍ_እሴት+20:
            원본자료,መድረሻ_ውሂብ_አድራሻ,순서번호,확인번호,ውቅረት_የበስተጀርባ_ብልህ_የማስተላለፍ_አገልግሎት,መስኮት=struct.unpack_from('!HHIIHH',ፓኬት_ውሂብ,ዝንፍ_እሴት)
            ምዝግብ_እሴት.update(source=원본자료,destination=መድረሻ_ውሂብ_አድራሻ,seq=순서번호,ack=확인번호,flags=ውቅረት_የበስተጀርባ_ብልህ_የማስተላለፍ_አገልግሎት&255,window=መስኮት,
                        payload=len(ፓኬት_ውሂብ)-ዝንፍ_እሴት-((ፓኬት_ውሂብ[ዝንፍ_እሴት+12]>>4)*4))
        자신.ዱካ_መዝግብ.append(ምዝግብ_እሴት)
        if len(자신.ዱካ_መዝግብ)>2048: del 자신.ዱካ_መዝግብ[:1024]

    def 직렬전문입력(자신, ውሂብ):
        for የቁምፊ_ኮድ in ውሂብ:
            if የቁምፊ_ኮድ == 192:
                if 자신.직렬전문 and not 자신.የመረጃ_ቴክኖሎጂ_ልክ_ያልኾነ and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        አድራሻ=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(አድራሻ)))
                            자신.현재주소=አድራሻ
                        except ValueError:
                            pass
                    자신.ዱካ_ፓኬት('from_guest',자신.직렬전문)
                    자신.실행틀(관문기계주소 + ማሽን_አድራሻ + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.የመረጃ_ቴክኖሎጂ_ልክ_ያልኾነ = False
            elif የቁምፊ_ኮድ == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if የቁምፊ_ኮድ not in (220, 221): 자신.የመረጃ_ቴክኖሎጂ_ልክ_ያልኾነ = True
                    የቁምፊ_ኮድ = 192 if የቁምፊ_ኮድ == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(የቁምፊ_ኮድ)
                else: 자신.የመረጃ_ቴክኖሎጂ_ልክ_ያልኾነ = True

    def 이더넷입력(자신, ውሂብ):
        자신.ኢተርኔት += ውሂብ
        while len(자신.ኢተርኔት) >= 4:
            개수 = struct.unpack_from('!I', 자신.ኢተርኔት)[0]
            if 개수 > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.ኢተርኔት) < 개수 + 4: return
            실행틀 = bytes(자신.ኢተርኔት[4:4+개수]); del 자신.ኢተርኔት[:4+개수]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                አድራሻ_ጥራት_ፓኬት = 실행틀[14:42]
                if አድራሻ_ጥራት_ፓኬት[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and አድራሻ_ጥራት_ፓኬት[24:28] == 자신.현재주소:
                    응답자료 = አድራሻ_ጥራት_ፓኬት[:6] + b'\x00\x02' + ማሽን_አድራሻ + 자신.현재주소 + አድራሻ_ጥራት_ፓኬት[8:18]
                    자신.실행틀(실행틀[6:12] + ማሽን_አድራሻ + b'\x08\x06' + 응답자료)
            elif 실행틀[12:14] == b'\x08\x00':
                ፓኬት_ውሂብ = 실행틀[14:]
                자신.ዱካ_ፓኬት('to_guest',ፓኬት_ውሂብ)
                자신.የመረጃ_ቴክኖሎጂ_ተጠባባቂ[0] += b'\xc0' + ፓኬት_ውሂብ.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def ዑደት_እሴት(자신):
        try:
            while not 자신.ላፍታ_አቁም_ፍጻሜ.is_set():
                읽기대상들 = [ኅብረቁምፊ_ውሂብ for 순번, ኅብረቁምፊ_ውሂብ in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [ኅብረቁምፊ_ውሂብ for ኅብረቁምፊ_ውሂብ in 자신.접속자들 if ኅብረቁምፊ_ውሂብ is not None]
                쓰기대상들 = [ኅብረቁምፊ_ውሂብ for 순번, ኅብረቁምፊ_ውሂብ in enumerate(자신.접속자들) if ኅብረቁምፊ_ውሂብ is not None and 자신.የመረጃ_ቴክኖሎጂ_ተጠባባቂ[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for ኅብረቁምፊ_ውሂብ in 읽을수있음:
                    if ኅብረቁምፊ_ውሂብ in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(ኅብረቁምፊ_ውሂብ); 자신.접속자들[순번], _ = ኅብረቁምፊ_ውሂብ.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(ኅብረቁምፊ_ውሂብ); ውሂብ = ኅብረቁምፊ_ውሂብ.recv(16384)
                        if not ውሂብ: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(ውሂብ)
                for ኅብረቁምፊ_ውሂብ in 쓸수있음:
                    순번 = 자신.접속자들.index(ኅብረቁምፊ_ውሂብ)
                    try: 개수 = ኅብረቁምፊ_ውሂብ.send(자신.የመረጃ_ቴክኖሎጂ_ተጠባባቂ[순번])
                    except BlockingIOError: continue
                    del 자신.የመረጃ_ቴክኖሎጂ_ተጠባባቂ[순번][:개수]
                if any(len(둘째값) > 1024 * 1024 for 둘째값 in 자신.የመረጃ_ቴክኖሎጂ_ተጠባባቂ):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.ላፍታ_አቁም_ፍጻሜ.is_set(): 자신.ስህተት = str(보조항목)

    def መዝጊያ(자신):
        자신.ላፍታ_አቁም_ፍጻሜ.set(); 자신.작업가닥.join(timeout=2)
        for ኅብረቁምፊ_ውሂብ in 자신.수신창구들 + 자신.접속자들:
            if ኅብረቁምፊ_ውሂብ is not None: ኅብረቁምፊ_ውሂብ.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *ነጋሪ_እሴት_ድርድር): 자신.መዝጊያ()
