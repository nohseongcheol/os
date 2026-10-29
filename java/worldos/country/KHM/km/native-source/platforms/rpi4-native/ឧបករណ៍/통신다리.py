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

ម៉ាស៊ីន_អ៊ីម៉ែល = bytes.fromhex('525400123456')
관문기계주소 = bytes.fromhex('52550a000202')
អាសយដ្ឋានអ៊ីនធឺណិត_តំលៃ = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class 통신다리:
    def __init__(자신, ឯកសារ_ផ្ទេរ_លេខរន្ធ=2121, 전달규칙들=(), ថត=False, ភ្ញៀវ_អ៊ីម៉ែល=None, ហូស_អ៊ីម៉ែល='127.0.0.1'):
        if not 1024 <= ឯកសារ_ផ្ទេរ_លេខរន្ធ <= 65535 or 50000 <= ឯកសារ_ផ្ទេរ_លេខរន្ធ <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.ឯកសារ_ផ្ទេរ_លេខរន្ធ = ឯកសារ_ផ្ទេរ_លេខរន្ធ
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        ភ្ញៀវ_អ៊ីម៉ែល = ភ្ញៀវ_អ៊ីម៉ែល or 자신.ip_config['IP']
        qemu_network(자신.ip_config, ភ្ញៀវ_អ៊ីម៉ែល)
        អ៊ីម៉ែល=ipaddress.IPv4Address(ភ្ញៀវ_អ៊ីម៉ែល)
        자신.ភ្ញៀវ_អ៊ីម៉ែល=str(អ៊ីម៉ែល); 자신.현재주소=អ៊ីម៉ែល.packed
        អ៊ីម៉ែល=ipaddress.IPv4Address(ហូស_អ៊ីម៉ែល)
        if អ៊ីម៉ែល.is_multicast or str(អ៊ីម៉ែល)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.ហូស_អ៊ីម៉ែល=str(អ៊ីម៉ែល)
        자신.ថត = ថត; 자신.ត្រេស_កំណត់_ហេតុ = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', ឯកសារ_ផ្ទេរ_លេខរន្ធ)} | {('tcp', ទិន្នន័យ_កំណត់ទីតាំង) for ទិន្នន័យ_កំណត់ទីតាំង in range(50000,50008)}
        for តម្រង_តំលៃ in 전달규칙들:
            ផ្លូវ_សមាសភាគ = តម្រង_តំលៃ.split(':')
            if len(ផ្លូវ_សមាសភាគ) != 3 or ផ្លូវ_សមាសភាគ[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, ហូស, ភ្ញៀវ = ផ្លូវ_សមាសភាគ[0], int(ផ្លូវ_សមាសភាគ[1]), int(ផ្លូវ_សមាសភាគ[2])
            if not 1024 <= ហូស <= 65535 or not 1 <= ភ្ញៀវ <= 65535 or (통신규약, ហូស) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + តម្រង_តំលៃ)
            사용중주소.add((통신규약, ហូស)); 자신.전달규칙들.append((통신규약, ហូស, ភ្ញៀវ))
        자신.수신창구들 = []
        for _ in range(2):
            ម៉ាស៊ីនមេ_តំលៃ = socket.socket()
            ម៉ាស៊ីនមេ_តំលៃ.bind(('127.0.0.1', 0)); ម៉ាស៊ីនមេ_តំលៃ.listen(1); ម៉ាស៊ីនមេ_តំលៃ.setblocking(False)
            자신.수신창구들.append(ម៉ាស៊ីនមេ_តំលៃ)
        자신.접속자들 = [None, None]
        자신.បច្ចេកវិទ្យាព័ត៌មាន_មិន_ទាន់_សម្រេច = [bytearray(), bytearray()]
        자신.이더넷자료 = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.បច្ចេកវិទ្យាព័ត៌មាន_មិនត្រឹមត្រូវ = False
        자신.ផ្អាក_ព្រឹត្តិការណ៍ = threading.Event(); 자신.កំហុស = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.작업가닥 = threading.Thread(target=자신.វដ្ដ_តំលៃ, daemon=True)
        자신.작업가닥.start()

    def 전달인수(자신):
        직렬접속번호, 이더넷접속번호 = [សំនុំអក្សរ_ទិន្នន័យ.getsockname()[1] for សំនុំអក្សរ_ទិន្នន័យ in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.ភ្ញៀវ_អ៊ីម៉ែល) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.ឯកសារ_ផ្ទេរ_លេខរន្ធ, 자신.ភ្ញៀវ_អ៊ីម៉ែល)
        for លេខរន្ធ in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(លេខរន្ធ, 자신.ភ្ញៀវ_អ៊ីម៉ែល)
        for 통신규약, ហូស, ភ្ញៀវ in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, ហូស, 자신.ភ្ញៀវ_អ៊ីម៉ែល, ភ្ញៀវ)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.ហូស_អ៊ីម៉ែល+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(직렬접속번호),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(이더넷접속번호),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, កញ្ចប់_ទិន្នន័យ):
        자신.បច្ចេកវិទ្យាព័ត៌មាន_មិន_ទាន់_សម្រេច[1] += struct.pack('!I', len(កញ្ចប់_ទិន្នន័យ)) + កញ្ចប់_ទិន្នន័យ

    def ត្រេស_កញ្ចប់(자신, 방향, កញ្ចប់_ទិន្នន័យ):
        if not 자신.ថត or len(កញ្ចប់_ទិន្នន័យ)<20: return
        ការបែង_ភាគ_តំលៃ=(កញ្ចប់_ទិន្នន័យ[0]&15)*4
        ការបញ្ចូល_តំលៃ={'time':time.monotonic(),'direction':방향,'bytes':len(កញ្ចប់_ទិន្នន័យ),'protocol':កញ្ចប់_ទិន្នន័យ[9]}
        if កញ្ចប់_ទិន្នន័យ[9]==6 and len(កញ្ចប់_ទិន្នន័យ)>=ការបែង_ភាគ_តំលៃ+20:
            원본자료,ទិសដៅ_ទិន្នន័យ_អ៊ីម៉ែល,순서번호,확인번호,ការរៀបចំ_សេវាកម្ម_ផ្ទេរ_ឆ្លាតវៃ_នៅ_ផ្ទៃ_ខាង_ក្រោយ,វីនដូ=struct.unpack_from('!HHIIHH',កញ្ចប់_ទិន្នន័យ,ការបែង_ភាគ_តំលៃ)
            ការបញ្ចូល_តំលៃ.update(source=원본자료,destination=ទិសដៅ_ទិន្នន័យ_អ៊ីម៉ែល,seq=순서번호,ack=확인번호,flags=ការរៀបចំ_សេវាកម្ម_ផ្ទេរ_ឆ្លាតវៃ_នៅ_ផ្ទៃ_ខាង_ក្រោយ&255,window=វីនដូ,
                        payload=len(កញ្ចប់_ទិន្នន័យ)-ការបែង_ភាគ_តំលៃ-((កញ្ចប់_ទិន្នន័យ[ការបែង_ភាគ_តំលៃ+12]>>4)*4))
        자신.ត្រេស_កំណត់_ហេតុ.append(ការបញ្ចូល_តំលៃ)
        if len(자신.ត្រេស_កំណត់_ហេតុ)>2048: del 자신.ត្រេស_កំណត់_ហេតុ[:1024]

    def 직렬전문입력(자신, ទិន្នន័យ):
        for កូដនៃតួអក្សរ in ទិន្នន័យ:
            if កូដនៃតួអក្សរ == 192:
                if 자신.직렬전문 and not 자신.បច្ចេកវិទ្យាព័ត៌មាន_មិនត្រឹមត្រូវ and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        អ៊ីម៉ែល=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(អ៊ីម៉ែល)))
                            자신.현재주소=អ៊ីម៉ែល
                        except ValueError:
                            pass
                    자신.ត្រេស_កញ្ចប់('from_guest',자신.직렬전문)
                    자신.실행틀(관문기계주소 + ម៉ាស៊ីន_អ៊ីម៉ែល + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.បច្ចេកវិទ្យាព័ត៌មាន_មិនត្រឹមត្រូវ = False
            elif កូដនៃតួអក្សរ == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if កូដនៃតួអក្សរ not in (220, 221): 자신.បច្ចេកវិទ្យាព័ត៌មាន_មិនត្រឹមត្រូវ = True
                    កូដនៃតួអក្សរ = 192 if កូដនៃតួអក្សរ == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(កូដនៃតួអក្សរ)
                else: 자신.បច្ចេកវិទ្យាព័ត៌មាន_មិនត្រឹមត្រូវ = True

    def 이더넷입력(자신, ទិន្នន័យ):
        자신.이더넷자료 += ទិន្នន័យ
        while len(자신.이더넷자료) >= 4:
            개수 = struct.unpack_from('!I', 자신.이더넷자료)[0]
            if 개수 > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.이더넷자료) < 개수 + 4: return
            실행틀 = bytes(자신.이더넷자료[4:4+개수]); del 자신.이더넷자료[:4+개수]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                អ៊ីម៉ែល_គុណភាព_បង្ហាញ_កញ្ចប់ = 실행틀[14:42]
                if អ៊ីម៉ែល_គុណភាព_បង្ហាញ_កញ្ចប់[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and អ៊ីម៉ែល_គុណភាព_បង្ហាញ_កញ្ចប់[24:28] == 자신.현재주소:
                    응답자료 = អ៊ីម៉ែល_គុណភាព_បង្ហាញ_កញ្ចប់[:6] + b'\x00\x02' + ម៉ាស៊ីន_អ៊ីម៉ែល + 자신.현재주소 + អ៊ីម៉ែល_គុណភាព_បង្ហាញ_កញ្ចប់[8:18]
                    자신.실행틀(실행틀[6:12] + ម៉ាស៊ីន_អ៊ីម៉ែល + b'\x08\x06' + 응답자료)
            elif 실행틀[12:14] == b'\x08\x00':
                កញ្ចប់_ទិន្នន័យ = 실행틀[14:]
                자신.ត្រេស_កញ្ចប់('to_guest',កញ្ចប់_ទិន្នន័យ)
                자신.បច្ចេកវិទ្យាព័ត៌មាន_មិន_ទាន់_សម្រេច[0] += b'\xc0' + កញ្ចប់_ទិន្នន័យ.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def វដ្ដ_តំលៃ(자신):
        try:
            while not 자신.ផ្អាក_ព្រឹត្តិការណ៍.is_set():
                읽기대상들 = [សំនុំអក្សរ_ទិន្នន័យ for 순번, សំនុំអក្សរ_ទិន្នន័យ in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [សំនុំអក្សរ_ទិន្នន័យ for សំនុំអក្សរ_ទិន្នន័យ in 자신.접속자들 if សំនុំអក្សរ_ទិន្នន័យ is not None]
                쓰기대상들 = [សំនុំអក្សរ_ទិន្នន័យ for 순번, សំនុំអក្សរ_ទិន្នន័យ in enumerate(자신.접속자들) if សំនុំអក្សរ_ទិន្នន័យ is not None and 자신.បច្ចេកវិទ្យាព័ត៌មាន_មិន_ទាន់_សម្រេច[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for សំនុំអក្សរ_ទិន្នន័យ in 읽을수있음:
                    if សំនុំអក្សរ_ទិន្នន័យ in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(សំនុំអក្សរ_ទិន្នន័យ); 자신.접속자들[순번], _ = សំនុំអក្សរ_ទិន្នន័យ.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(សំនុំអក្សរ_ទិន្នន័យ); ទិន្នន័យ = សំនុំអក្សរ_ទិន្នន័យ.recv(16384)
                        if not ទិន្នន័យ: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(ទិន្នន័យ)
                for សំនុំអក្សរ_ទិន្នន័យ in 쓸수있음:
                    순번 = 자신.접속자들.index(សំនុំអក្សរ_ទិន្នន័យ)
                    try: 개수 = សំនុំអក្សរ_ទិន្នន័យ.send(자신.បច្ចេកវិទ្យាព័ត៌មាន_មិន_ទាន់_សម្រេច[순번])
                    except BlockingIOError: continue
                    del 자신.បច្ចេកវិទ្យាព័ត៌មាន_មិន_ទាន់_សម្រេច[순번][:개수]
                if any(len(둘째값) > 1024 * 1024 for 둘째값 in 자신.បច្ចេកវិទ្យាព័ត៌មាន_មិន_ទាន់_សម្រេច):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.ផ្អាក_ព្រឹត្តិការណ៍.is_set(): 자신.កំហុស = str(보조항목)

    def បិទ(자신):
        자신.ផ្អាក_ព្រឹត្តិការណ៍.set(); 자신.작업가닥.join(timeout=2)
        for សំនុំអក្សរ_ទិន្នន័យ in 자신.수신창구들 + 자신.접속자들:
            if សំនុំអក្សរ_ទិន្នន័យ is not None: សំនុំអក្សរ_ទិន្នន័យ.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *អាគុយម៉ង់_អារេ): 자신.បិទ()
