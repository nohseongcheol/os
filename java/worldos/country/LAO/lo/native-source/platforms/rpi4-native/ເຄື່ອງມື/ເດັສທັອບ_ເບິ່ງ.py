#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, ກະແຈ_ຄ່າ 입력은 자체 ແກນກາງ_ຄ່າ UART로 전달한다. localhost 전용, 단일 ຄວບຄຸມ_ຄ່າ 클라이언트.
RFB 3.8: https://www.rfc-editor.org/rfc/rfc6143.html
"""
import argparse
from contextlib import ExitStack
from pathlib import Path
import signal
import socket
import struct
import subprocess
import sys
import tempfile
import threading
import time
from ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ import ຄໍາສັ່ງ_1f12b8e2
from local_input import create


def 정확한값(소켓, ຂະ_ຫນາດ):
    ຂໍ້ມູນ = bytearray()
    while len(ຂໍ້ມູນ) < ຂະ_ຫນາດ:
        조각 = 소켓.recv(ຂະ_ຫນາດ - len(ຂໍ້ມູນ))
        if not 조각: raise EOFError()
        ຂໍ້ມູນ.extend(조각)
    return bytes(ຂໍ້ມູນ)


class ແປ້ນພິມ:
    def __init__(자신, ສົ່ງ, 입력방식알림=None):
        자신.바이트전송 = ສົ່ງ; 자신.ປຸ່ມດັດແກ້ = set(); 자신.ຄລິບບອດ_ຄ່າ = b''
        자신.한글조합기 = create(ສົ່ງ, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.ສະວິດ_ກະແຈ = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def ສົ່ງ(자신, ຂໍ້ມູນ):
        자신.한글조합기.조합확정()
        자신.바이트전송(ຂໍ້ມູນ)

    def ສະວິດ_ໂຫມດ(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, ກະແຈ_ສັນຍາລັກ):
        if ກະແຈ_ສັນຍາລັກ in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.ປຸ່ມດັດແກ້.add(ກະແຈ_ສັນຍາລັກ)
            else: 자신.ປຸ່ມດັດແກ້.discard(ກະແຈ_ສັນຍາລັກ)
            return
        if not 누르는중:
            자신.ສະວິດ_ກະແຈ.discard(ກະແຈ_ສັນຍາລັກ)
            return
        ຊີທີອາແອວ = bool(자신.ປຸ່ມດັດແກ້ & {0xffe3, 0xffe4})
        ປຸ່ມຊິບ = bool(자신.ປຸ່ມດັດແກ້ & {0xffe1, 0xffe2})
        if ຊີທີອາແອວ and ປຸ່ມຊິບ and ກະແຈ_ສັນຍາລັກ in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if ກະແຈ_ສັນຍາລັກ in (32,0xff0d):
                try:
                    ຄ່າ=int(자신.유니코드입력,16)
                    if 32<=ຄ່າ<=0x10ffff and not 0xd800<=ຄ່າ<=0xdfff: 자신.ສົ່ງ(chr(ຄ່າ).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif ກະແຈ_ສັນຍາລັກ==0xff1b: 자신.유니코드입력=None
            elif ກະແຈ_ສັນຍາລັກ==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif ກະແຈ_ສັນຍາລັກ<128 and chr(ກະແຈ_ສັນຍາລັກ) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(ກະແຈ_ສັນຍາລັກ)
            return
        if ກະແຈ_ສັນຍາລັກ in (0xff31,0xffc6) or ກະແຈ_ສັນຍາລັກ==32 and ປຸ່ມຊິບ and not ຊີທີອາແອວ:
            if ກະແຈ_ສັນຍາລັກ not in 자신.ສະວິດ_ກະແຈ: 자신.ສະວິດ_ໂຫມດ()
            자신.ສະວິດ_ກະແຈ.add(ກະແຈ_ສັນຍາລັກ)
            return
        if ກະແຈ_ສັນຍາລັກ==0xff08 and 자신.한글여부 and not ຊີທີອາແອວ and 자신.한글조합기.앞글자지우기(): return
        if ຊີທີອາແອວ and ປຸ່ມຊິບ and ກະແຈ_ສັນຍາລັກ in (ord('t'),ord('T')):
            자신.ສົ່ງ(bytes([30,2,1,0,0,0,0])); return
        if ກະແຈ_ສັນຍາລັກ==0xffc3: 자신.ສົ່ງ(bytes([30,2,2,0,0,0,0])); return
        if ກະແຈ_ສັນຍາລັກ==0xffc9: 자신.ສົ່ງ(bytes([30,2,3,0,0,0,0])); return
        if ຊີທີອາແອວ and ປຸ່ມຊິບ and ກະແຈ_ສັນຍາລັກ in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.ສົ່ງ(자신.ຄລິບບອດ_ຄ່າ); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if ກະແຈ_ສັນຍາລັກ in 특수글쇠: 자신.ສົ່ງ(특수글쇠[ກະແຈ_ສັນຍາລັກ]); return
        ຕົວອັກສອນ_ເຂົ້າລະຫັດ = ກະແຈ_ສັນຍາລັກ & 0xffffff if ກະແຈ_ສັນຍາລັກ & 0xff000000 == 0x01000000 else ກະແຈ_ສັນຍາລັກ
        if ຕົວອັກສອນ_ເຂົ້າລະຫັດ > 0x10ffff or 0xd800 <= ຕົວອັກສອນ_ເຂົ້າລະຫັດ <= 0xdfff or ກະແຈ_ສັນຍາລັກ >= 0xff00 and ກະແຈ_ສັນຍາລັກ < 0x1000000: return
        if ຊີທີອາແອວ and 0x40 <= ຕົວອັກສອນ_ເຂົ້າລະຫັດ <= 0x7f: 자신.ສົ່ງ(bytes([ຕົວອັກສອນ_ເຂົ້າລະຫັດ & 31])); return
        if ຕົວອັກສອນ_ເຂົ້າລະຫັດ < 32: return
        if 자신.한글여부 and 자신.ປຸ່ມດັດແກ້ & {0xffea,0xfe03,0xff7e} and not ຊີທີອາແອວ and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.ຟີດ_ກະແຈ(chr(ຕົວອັກສອນ_ເຂົ້າລະຫັດ), altgr=True): return
        앞부분 = b'\x1b' if 자신.ປຸ່ມດັດແກ້ & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not ຊີທີອາແອວ and not 앞부분 and 32<=ຕົວອັກສອນ_ເຂົ້າລະຫັດ<127:
            ຕົວອັກສອນ_ຂໍ້ມູນ=chr(ຕົວອັກສອນ_ເຂົ້າລະຫັດ).upper() if ປຸ່ມຊິບ else chr(ຕົວອັກສອນ_ເຂົ້າລະຫັດ)
            if 자신.한글조합기.ຟີດ_ກະແຈ(ຕົວອັກສອນ_ຂໍ້ມູນ): return
        자신.ສົ່ງ(앞부분 + chr(ຕົວອັກສອນ_ເຂົ້າລະຫັດ).encode('utf-8'))


class ເຊື່ອມຕໍ່_ເດັສທັອບ:
    def __init__(자신, ຂະ_ບວນ_ການ):
        자신.ຂະ_ບວນ_ການ=ຂະ_ບວນ_ການ; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.ເທີມີນໍ=False; 자신.시작화면=False; 자신.닫힘=False

    def ສົ່ງ(자신, ຂໍ້ມູນ):
        if not ຂໍ້ມູນ or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.ຂະ_ບວນ_ການ.stdin.write(ຂໍ້ມູນ); 자신.ຂະ_ບວນ_ການ.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                ຂໍ້ມູນ=자신.ຂະ_ບວນ_ການ.stdout.read(4096)
                if not ຂໍ້ມູນ: break
                sys.stdout.buffer.write(ຂໍ້ມູນ); sys.stdout.buffer.flush()
                끝부분=(끝부분+ຂໍ້ມູນ)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.ເທີມີນໍ=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.ສົ່ງ(b'terminal\n')
        finally: 자신.닫힘=True

    def ລູກຂ່າຍ(자신, ລູກຂ່າຍ, ທາງໂຄຈອນ):
        서버=socket.socket(socket.AF_UNIX); 서버.settimeout(10); ລູກຂ່າຍ.settimeout(10)
        ແປ້ນພິມ_ເຂົ້າໃນ=ແປ້ນພິມ(자신.ສົ່ງ,lambda 한글여부:자신.ສົ່ງ(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            서버.connect(str(ທາງໂຄຈອນ))
            # 초기 협상은 순서대로 끝낸다. 이후 출력 가닥만 클라이언트에 쓴다.
            ລູກຂ່າຍ.sendall(정확한값(서버,12))
            판번호=정확한값(ລູກຂ່າຍ,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            서버.sendall(판번호)
            개수=정확한값(서버,1);ລູກຂ່າຍ.sendall(개수+정확한값(서버,개수[0]))
            ຄວາມປອດໄພ=정확한값(ລູກຂ່າຍ,1)
            if ຄວາມປອດໄພ!=b'\x01': raise ValueError('unexpected security type')
            서버.sendall(ຄວາມປອດໄພ)
            if 판번호==b'RFB 003.008\n':ລູກຂ່າຍ.sendall(정확한값(서버,4))
            서버.sendall(정확한값(ລູກຂ່າຍ,1))
            초기값=정확한값(서버,24)
            ລູກຂ່າຍ.sendall(초기값+정확한값(서버,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            ລູກຂ່າຍ.settimeout(None);서버.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        ຫມວດ_ຄ່າ=정확한값(서버,1)[0]
                        if ຫມວດ_ຄ່າ==0:
                            머리=정확한값(서버,3);항목수=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 ທາງ_ໄກ_ຄ່າ 포인터의 중복을 피한다.
                            ເຊື່ອງໄວ້ໄດ້_ຄ່າ=포인터지원
                            if ເຊື່ອງໄວ້ໄດ້_ຄ່າ:ລູກຂ່າຍ.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            ລູກຂ່າຍ.sendall(bytes([ຫມວດ_ຄ່າ])+머리)
                            for _ in range(항목수):
                                사각형=정확한값(서버,12);가로,ລວງຕັ້ງ_ຈັດຕໍາແຫນ່ງ,폭,높이,ເຂົ້າລະຫັດ_ຄ່າ=struct.unpack('>HHHHi',사각형)
                                if ເຂົ້າລະຫັດ_ຄ່າ!=0:raise ValueError('unexpected framebuffer encoding: '+str(ເຂົ້າລະຫັດ_ຄ່າ))
                                ລູກຂ່າຍ.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    ຂໍ້ມູນ=정확한값(서버,min(남음,65536));ລູກຂ່າຍ.sendall(ຂໍ້ມູນ);남음-=len(ຂໍ້ມູນ)
                        elif ຫມວດ_ຄ່າ==1:
                            머리=정확한값(서버,5);개수=struct.unpack('>H',머리[3:])[0]
                            ລູກຂ່າຍ.sendall(bytes([ຫມວດ_ຄ່າ])+머리+정확한값(서버,개수*6))
                        elif ຫມວດ_ຄ່າ==2:ລູກຂ່າຍ.sendall(bytes([ຫມວດ_ຄ່າ]))
                        elif ຫມວດ_ຄ່າ==3:
                            머리=정확한값(서버,7);개수=struct.unpack('>I',머리[3:])[0]
                            if 개수>1048576:raise ValueError('server clipboard too large')
                            ລູກຂ່າຍ.sendall(bytes([ຫມວດ_ຄ່າ])+머리+정확한값(서버,개수))
                        else:raise ValueError('unexpected RFB server message: '+str(ຫມວດ_ຄ່າ))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:ລູກຂ່າຍ.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                ຫມວດ_ຄ່າ=정확한값(ລູກຂ່າຍ,1)[0]
                if ຫມວດ_ຄ່າ==4:
                    ເນື້ອໃນເອກະສານ=정확한값(ລູກຂ່າຍ,7); ແປ້ນພິມ_ເຂົ້າໃນ.누름값(ເນື້ອໃນເອກະສານ[0]!=0,struct.unpack('>I',ເນື້ອໃນເອກະສານ[3:])[0]); continue
                if ຫມວດ_ຄ່າ==255:
                    ເນື້ອໃນເອກະສານ=정확한값(ລູກຂ່າຍ,11)
                    if ເນື້ອໃນເອກະສານ[0]!=0: raise ValueError('unsupported QEMU input extension')
                    ແປ້ນພິມ_ເຂົ້າໃນ.누름값(struct.unpack('>H',ເນື້ອໃນເອກະສານ[1:3])[0]!=0,struct.unpack('>I',ເນື້ອໃນເອກະສານ[3:7])[0]); continue
                if ຫມວດ_ຄ່າ==5:
                    ເນື້ອໃນເອກະສານ=정확한값(ລູກຂ່າຍ,5); 단추들,ຈຸດ_ພິ_ກັດ_x,ປຸ່ມ_Y_ຈຸດປະສານ=struct.unpack('>BHH',ເນື້ອໃນເອກະສານ)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: ແປ້ນພິມ_ເຂົ້າໃນ.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=ຈຸດ_ພິ_ກັດ_x<576 and 112<=ປຸ່ມ_Y_ຈຸດປະສານ<372:
                        ຄົ້ນຫາ_ດັດຊະນີ=(ປຸ່ມ_Y_ຈຸດປະສານ-112)//52
                        if (ປຸ່ມ_Y_ຈຸດປະສານ-112)%52<40 and ຄົ້ນຫາ_ດັດຊະນີ<5: 자신.ສົ່ງ(bytes([ord('1')+ຄົ້ນຫາ_ດັດຊະນີ]))
                    else: 자신.ສົ່ງ(bytes([30,1,단추들,ຈຸດ_ພິ_ກັດ_x&255,ຈຸດ_ພິ_ກັດ_x>>8,ປຸ່ມ_Y_ຈຸດປະສານ&255,ປຸ່ມ_Y_ຈຸດປະສານ>>8]))
                    continue
                if ຫມວດ_ຄ່າ==6:
                    ເນື້ອໃນເອກະສານ=정확한값(ລູກຂ່າຍ,7); ຄວາມຍາວ_ຄ່າ=struct.unpack('>i',ເນື້ອໃນເອກະສານ[3:])[0]
                    if abs(ຄວາມຍາວ_ຄ່າ)>65536: raise ValueError('clipboard too large')
                    ຂໍ້ຄວາມ=정확한값(ລູກຂ່າຍ,abs(ຄວາມຍາວ_ຄ່າ))
                    if ຄວາມຍາວ_ຄ່າ>=0:
                        try: ແປ້ນພິມ_ເຂົ້າໃນ.ຄລິບບອດ_ຄ່າ=ຂໍ້ຄວາມ.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: ແປ້ນພິມ_ເຂົ້າໃນ.ຄລິບບອດ_ຄ່າ=ຂໍ້ຄວາມ.decode('latin-1').encode('utf-8')
                        ແປ້ນພິມ_ເຂົ້າໃນ.ຄລິບບອດ_ຄ່າ=ແປ້ນພິມ_ເຂົ້າໃນ.ຄລິບບອດ_ຄ່າ[:65536].decode('utf-8','ignore').encode('utf-8')
                    서버.sendall(bytes([ຫມວດ_ຄ່າ])+ເນື້ອໃນເອກະສານ+ຂໍ້ຄວາມ); continue
                if ຫມວດ_ຄ່າ==0:
                    ເນື້ອໃນເອກະສານ=정확한값(ລູກຂ່າຍ,19)
                    if ເນື້ອໃນເອກະສານ[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=ເນື້ອໃນເອກະສານ[3]//8
                elif ຫມວດ_ຄ່າ==2:
                    ເນື້ອໃນເອກະສານ=정확한값(ລູກຂ່າຍ,3); 항목수=struct.unpack('>H',ເນື້ອໃນເອກະສານ[1:])[0]
                    if 항목수>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(항목수)+'i',정확한값(ລູກຂ່າຍ,항목수*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 ຄ່າທີ່ກໍານົດໄວ້ແລ້ວ Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    ເນື້ອໃນເອກະສານ=struct.pack('>BHi',0,1,0)
                elif ຫມວດ_ຄ່າ in (3,150): ເນື້ອໃນເອກະສານ=정확한값(ລູກຂ່າຍ,9)
                elif ຫມວດ_ຄ່າ==248:
                    ເນື້ອໃນເອກະສານ=정확한값(ລູກຂ່າຍ,8)
                    if ເນື້ອໃນເອກະສານ[7]>64: raise ValueError('fence too large')
                    ເນື້ອໃນເອກະສານ+=정확한값(ລູກຂ່າຍ,ເນື້ອໃນເອກະສານ[7])
                elif ຫມວດ_ຄ່າ==250: ເນື້ອໃນເອກະສານ=정확한값(ລູກຂ່າຍ,3)
                elif ຫມວດ_ຄ່າ==251:
                    ເນື້ອໃນເອກະສານ=정확한값(ລູກຂ່າຍ,7)
                    if ເນື້ອໃນເອກະສານ[5]>16: raise ValueError('too many screens')
                    ເນື້ອໃນເອກະສານ+=정확한값(ລູກຂ່າຍ,ເນື້ອໃນເອກະສານ[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(ຫມວດ_ຄ່າ))
                서버.sendall(bytes([ຫມວດ_ຄ່າ])+ເນື້ອໃນເອກະສານ)
        except (OSError,EOFError,ValueError) as ຂໍ້ຜິດພາດ:
            if str(ຂໍ້ຜິດພາດ): print('VNC client:',ຂໍ້ຜິດພາດ,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (ລູກຂ່າຍ,서버):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def ແລ່ນ_ເດັສທັອບ(ຫມາຍເລກພອດ=5902, ເຄືອຂ່າຍ=False, ຟາຍ_ໂອນ_ຫມາຍເລກພອດ=2121, 전달규칙들=(), ຄວາມລະອຽດ_ຄ່າ=(640, 480), ແຂກ_ອີເມວ=None, ໂຮສ_ອີເມວ='127.0.0.1'):
    with ExitStack() as ແຫຼ່ງ_ຊັບ_ພະ_ຍາ_ກອນ, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        ເຄືອຂ່າຍ_ຕົວເຊື່ອມ_ເຂົ້າໃນ = None
        if ເຄືອຂ່າຍ:
            from ເຄືອຂ່າຍ_ຕົວເຊື່ອມ import ເຄືອຂ່າຍ_ຕົວເຊື່ອມ
            ເຄືອຂ່າຍ_ຕົວເຊື່ອມ_ເຂົ້າໃນ = ແຫຼ່ງ_ຊັບ_ພະ_ຍາ_ກອນ.enter_context(ເຄືອຂ່າຍ_ຕົວເຊື່ອມ(ຟາຍ_ໂອນ_ຫມາຍເລກພອດ, 전달규칙들, ແຂກ_ອີເມວ=ແຂກ_ອີເມວ, ໂຮສ_ອີເມວ=ໂຮສ_ອີເມວ))
        ທາງໂຄຈອນ=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',ຫມາຍເລກພອດ)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if ເຄືອຂ່າຍ_ຕົວເຊື່ອມ_ເຂົ້າໃນ and (원격화면접속번호==ຟາຍ_ໂອນ_ຫມາຍເລກພອດ or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and ໂຮສ==원격화면접속번호 for 통신규약,ໂຮສ,_ in ເຄືອຂ່າຍ_ຕົວເຊື່ອມ_ເຂົ້າໃນ.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            ຂະ_ບວນ_ການ=subprocess.Popen(ຄໍາສັ່ງ_1f12b8e2(ຄວາມລະອຽດ_ຄ່າ)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(ທາງໂຄຈອນ)]+(ເຄືອຂ່າຍ_ຕົວເຊື່ອມ_ເຂົ້າໃນ.전달인수() if ເຄືອຂ່າຍ_ຕົວເຊື່ອມ_ເຂົ້າໃນ else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            ຕົວເຊື່ອມ=ເຊື່ອມຕໍ່_ເດັສທັອບ(ຂະ_ບວນ_ການ); ຜູ້ອ່ານ=threading.Thread(target=ຕົວເຊື່ອມ.직렬입출력,daemon=True); ຜູ້ອ່ານ.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if ເຄືອຂ່າຍ_ຕົວເຊື່ອມ_ເຂົ້າໃນ: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(ໂຮສ_ອີເມວ,ຟາຍ_ໂອນ_ຫມາຍເລກພອດ),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while ຂະ_ບວນ_ການ.poll() is None:
                    try: ລູກຂ່າຍ,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): ລູກຂ່າຍ.close(); continue
                    if not ທາງໂຄຈອນ.exists(): ລູກຂ່າຍ.close(); continue
                    처리작업=threading.Thread(target=ຕົວເຊື່ອມ.ລູກຂ່າຍ,args=(ລູກຂ່າຍ,ທາງໂຄຈອນ),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                ຕົວເຊື່ອມ.닫힘=True
                if ເຄືອຂ່າຍ_ຕົວເຊື່ອມ_ເຂົ້າໃນ: ເຄືອຂ່າຍ_ຕົວເຊື່ອມ_ເຂົ້າໃນ.ຢຸດຊົ່ວຄາວ_ງານ.set()
                if ຂະ_ບວນ_ການ.poll() is None:
                    ຂະ_ບວນ_ການ.terminate()
                    try: ຂະ_ບວນ_ການ.wait(timeout=5)
                    except subprocess.TimeoutExpired: ຂະ_ບວນ_ການ.kill(); ຂະ_ບວນ_ການ.wait()
                ຜູ້ອ່ານ.join(timeout=2); ຂະ_ບວນ_ການ.stdin.close(); ຂະ_ບວນ_ການ.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if ເຄືອຂ່າຍ_ຕົວເຊື່ອມ_ເຂົ້າໃນ and ເຄືອຂ່າຍ_ຕົວເຊື່ອມ_ເຂົ້າໃນ.ຂໍ້ຜິດພາດ: raise RuntimeError('network bridge: '+ເຄືອຂ່າຍ_ຕົວເຊື່ອມ_ເຂົ້າໃນ.ຂໍ້ຜິດພາດ)
            return 0 if 가로채기됨 else ຂະ_ບວນ_ການ.returncode


if __name__=='__main__':
    from ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ import 해상도읽기
    ຕົວແຍກວິເຄາະ=argparse.ArgumentParser(description=__doc__); ຕົວແຍກວິເຄາະ.add_argument('--port',type=int,default=5902)
    ຕົວແຍກວິເຄາະ.add_argument('--resolution',type=해상도읽기,default=(640,480))
    ຕົວແຍກວິເຄາະ.add_argument('--network',action='store_true'); ຕົວແຍກວິເຄາະ.add_argument('--ftp-port',type=int,default=2121)
    ຕົວແຍກວິເຄາະ.add_argument('--forward',action='append',default=[])
    ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ=ຕົວແຍກວິເຄາະ.parse_args()
    if ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.forward and not ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.network: ຕົວແຍກວິເຄາະ.error('--forward requires --network')
    raise SystemExit(ແລ່ນ_ເດັສທັອບ(ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.port,ເຄືອຂ່າຍ=ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.network,ຟາຍ_ໂອນ_ຫມາຍເລກພອດ=ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.ftp_port,전달규칙들=ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.forward,ຄວາມລະອຽດ_ຄ່າ=ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.resolution))
