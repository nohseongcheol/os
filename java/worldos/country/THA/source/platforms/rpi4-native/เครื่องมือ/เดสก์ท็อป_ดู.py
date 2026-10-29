#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, คีย์_ค่า 입력은 เอง เคอร์เนล_ค่า UART로 전달한다. localhost 전용, 단일 ควบคุม_ค่า 클라이언트.
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
from ดําเนินการ_คําสั่ง import คําสั่ง
from local_input import create


def 정확한값(소켓, ขนาด):
    ข้อมูล = bytearray()
    while len(ข้อมูล) < ขนาด:
        조각 = 소켓.recv(ขนาด - len(ข้อมูล))
        if not 조각: raise EOFError()
        ข้อมูล.extend(조각)
    return bytes(ข้อมูล)


class คีย์บอร์ด:
    def __init__(자신, ส่ง, 입력방식알림=None):
        자신.바이트전송 = ส่ง; 자신.แป้นปรับค่า = set(); 자신.คลิปบอร์ด_ค่า = b''
        자신.한글조합기 = create(ส่ง, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.สลับ_คีย์ = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def ส่ง(자신, ข้อมูล):
        자신.한글조합기.조합확정()
        자신.바이트전송(ข้อมูล)

    def สลับ_โหมด(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, คีย์_สัญลักษณ์):
        if คีย์_สัญลักษณ์ in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.แป้นปรับค่า.add(คีย์_สัญลักษณ์)
            else: 자신.แป้นปรับค่า.discard(คีย์_สัญลักษณ์)
            return
        if not 누르는중:
            자신.สลับ_คีย์.discard(คีย์_สัญลักษณ์)
            return
        ควบคุม_คีย์ = bool(자신.แป้นปรับค่า & {0xffe3, 0xffe4})
        เลื่อน_คีย์ = bool(자신.แป้นปรับค่า & {0xffe1, 0xffe2})
        if ควบคุม_คีย์ and เลื่อน_คีย์ and คีย์_สัญลักษณ์ in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if คีย์_สัญลักษณ์ in (32,0xff0d):
                try:
                    ค่า=int(자신.유니코드입력,16)
                    if 32<=ค่า<=0x10ffff and not 0xd800<=ค่า<=0xdfff: 자신.ส่ง(chr(ค่า).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif คีย์_สัญลักษณ์==0xff1b: 자신.유니코드입력=None
            elif คีย์_สัญลักษณ์==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif คีย์_สัญลักษณ์<128 and chr(คีย์_สัญลักษณ์) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(คีย์_สัญลักษณ์)
            return
        if คีย์_สัญลักษณ์ in (0xff31,0xffc6) or คีย์_สัญลักษณ์==32 and เลื่อน_คีย์ and not ควบคุม_คีย์:
            if คีย์_สัญลักษณ์ not in 자신.สลับ_คีย์: 자신.สลับ_โหมด()
            자신.สลับ_คีย์.add(คีย์_สัญลักษณ์)
            return
        if คีย์_สัญลักษณ์==0xff08 and 자신.한글여부 and not ควบคุม_คีย์ and 자신.한글조합기.앞글자지우기(): return
        if ควบคุม_คีย์ and เลื่อน_คีย์ and คีย์_สัญลักษณ์ in (ord('t'),ord('T')):
            자신.ส่ง(bytes([30,2,1,0,0,0,0])); return
        if คีย์_สัญลักษณ์==0xffc3: 자신.ส่ง(bytes([30,2,2,0,0,0,0])); return
        if คีย์_สัญลักษณ์==0xffc9: 자신.ส่ง(bytes([30,2,3,0,0,0,0])); return
        if ควบคุม_คีย์ and เลื่อน_คีย์ and คีย์_สัญลักษณ์ in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.ส่ง(자신.คลิปบอร์ด_ค่า); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if คีย์_สัญลักษณ์ in 특수글쇠: 자신.ส่ง(특수글쇠[คีย์_สัญลักษณ์]); return
        อักขระ_การเข้ารหัส = คีย์_สัญลักษณ์ & 0xffffff if คีย์_สัญลักษณ์ & 0xff000000 == 0x01000000 else คีย์_สัญลักษณ์
        if อักขระ_การเข้ารหัส > 0x10ffff or 0xd800 <= อักขระ_การเข้ารหัส <= 0xdfff or คีย์_สัญลักษณ์ >= 0xff00 and คีย์_สัญลักษณ์ < 0x1000000: return
        if ควบคุม_คีย์ and 0x40 <= อักขระ_การเข้ารหัส <= 0x7f: 자신.ส่ง(bytes([อักขระ_การเข้ารหัส & 31])); return
        if อักขระ_การเข้ารหัส < 32: return
        if 자신.한글여부 and 자신.แป้นปรับค่า & {0xffea,0xfe03,0xff7e} and not ควบคุม_คีย์ and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.ฟีด_คีย์(chr(อักขระ_การเข้ารหัส), altgr=True): return
        앞부분 = b'\x1b' if 자신.แป้นปรับค่า & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not ควบคุม_คีย์ and not 앞부분 and 32<=อักขระ_การเข้ารหัส<127:
            ข้อมูลอักขระ=chr(อักขระ_การเข้ารหัส).upper() if เลื่อน_คีย์ else chr(อักขระ_การเข้ารหัส)
            if 자신.한글조합기.ฟีด_คีย์(ข้อมูลอักขระ): return
        자신.ส่ง(앞부분 + chr(อักขระ_การเข้ารหัส).encode('utf-8'))


class เชื่อมต่อ_เดสก์ท็อป:
    def __init__(자신, โพรเซส):
        자신.โพรเซส=โพรเซส; 자신.ล็อก_ค่า=threading.Lock(); 자신.준비완료=False; 자신.เทอร์มินัล=False; 자신.시작화면=False; 자신.เทคโนโลยีสารสนเทศ_ปิด=False

    def ส่ง(자신, ข้อมูล):
        if not ข้อมูล or 자신.เทคโนโลยีสารสนเทศ_ปิด: return
        with 자신.ล็อก_ค่า:
            try: 자신.โพรเซส.stdin.write(ข้อมูล); 자신.โพรเซส.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                ข้อมูล=자신.โพรเซส.stdout.read(4096)
                if not ข้อมูล: break
                sys.stdout.buffer.write(ข้อมูล); sys.stdout.buffer.flush()
                끝부분=(끝부분+ข้อมูล)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); เทคโนโลยีสารสนเทศ_ปิด=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,เทคโนโลยีสารสนเทศ_ปิด,그림화면,종료됨)>=0:
                    자신.เทอร์มินัล=열림>max(เทคโนโลยีสารสนเทศ_ปิด,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,เทคโนโลยีสารสนเทศ_ปิด,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.ส่ง(b'terminal\n')
        finally: 자신.เทคโนโลยีสารสนเทศ_ปิด=True

    def ไคลเอ็นต์(자신, ไคลเอ็นต์, เส้นทาง):
        เซิร์ฟเวอร์_ค่า=socket.socket(socket.AF_UNIX); เซิร์ฟเวอร์_ค่า.settimeout(10); ไคลเอ็นต์.settimeout(10)
        คีย์บอร์ด_รายการ=คีย์บอร์ด(자신.ส่ง,lambda 한글여부:자신.ส่ง(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            เซิร์ฟเวอร์_ค่า.connect(str(เส้นทาง))
            # สภาวะเริ่มต้น 협상은 순서대로 끝낸다. 이후 ข้อความออก 가닥만 클라이언트에 쓴다.
            ไคลเอ็นต์.sendall(정확한값(เซิร์ฟเวอร์_ค่า,12))
            หมายเลขรุ่น=정확한값(ไคลเอ็นต์,12)
            if หมายเลขรุ่น not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            เซิร์ฟเวอร์_ค่า.sendall(หมายเลขรุ่น)
            개수=정확한값(เซิร์ฟเวอร์_ค่า,1);ไคลเอ็นต์.sendall(개수+정확한값(เซิร์ฟเวอร์_ค่า,개수[0]))
            ความปลอดภัย=정확한값(ไคลเอ็นต์,1)
            if ความปลอดภัย!=b'\x01': raise ValueError('unexpected security type')
            เซิร์ฟเวอร์_ค่า.sendall(ความปลอดภัย)
            if หมายเลขรุ่น==b'RFB 003.008\n':ไคลเอ็นต์.sendall(정확한값(เซิร์ฟเวอร์_ค่า,4))
            เซิร์ฟเวอร์_ค่า.sendall(정확한값(ไคลเอ็นต์,1))
            초기값=정확한값(เซิร์ฟเวอร์_ค่า,24)
            ไคลเอ็นต์.sendall(초기값+정확한값(เซิร์ฟเวอร์_ค่า,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            ไคลเอ็นต์.settimeout(None);เซิร์ฟเวอร์_ค่า.settimeout(None)
            def ผลผลิต():
                try:
                    while True:
                        ประเภท_ค่า=정확한값(เซิร์ฟเวอร์_ค่า,1)[0]
                        if ประเภท_ค่า==0:
                            머리=정확한값(เซิร์ฟเวอร์_ค่า,3);항목수=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 ระยะไกล_ค่า 포인터의 중복을 피한다.
                            ที่ซ่อน_ค่า=포인터지원
                            if ที่ซ่อน_ค่า:ไคลเอ็นต์.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            ไคลเอ็นต์.sendall(bytes([ประเภท_ค่า])+머리)
                            for _ in range(항목수):
                                สี่เหลี่ยมผืนผ้า=정확한값(เซิร์ฟเวอร์_ค่า,12);가로,แนวตั้ง_ตําแหน่ง,폭,높이,การเข้ารหัส_ค่า=struct.unpack('>HHHHi',สี่เหลี่ยมผืนผ้า)
                                if การเข้ารหัส_ค่า!=0:raise ValueError('unexpected framebuffer encoding: '+str(การเข้ารหัส_ค่า))
                                ไคลเอ็นต์.sendall(สี่เหลี่ยมผืนผ้า)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    ข้อมูล=정확한값(เซิร์ฟเวอร์_ค่า,min(남음,65536));ไคลเอ็นต์.sendall(ข้อมูล);남음-=len(ข้อมูล)
                        elif ประเภท_ค่า==1:
                            머리=정확한값(เซิร์ฟเวอร์_ค่า,5);개수=struct.unpack('>H',머리[3:])[0]
                            ไคลเอ็นต์.sendall(bytes([ประเภท_ค่า])+머리+정확한값(เซิร์ฟเวอร์_ค่า,개수*6))
                        elif ประเภท_ค่า==2:ไคลเอ็นต์.sendall(bytes([ประเภท_ค่า]))
                        elif ประเภท_ค่า==3:
                            머리=정확한값(เซิร์ฟเวอร์_ค่า,7);개수=struct.unpack('>I',머리[3:])[0]
                            if 개수>1048576:raise ValueError('server clipboard too large')
                            ไคลเอ็นต์.sendall(bytes([ประเภท_ค่า])+머리+정확한값(เซิร์ฟเวอร์_ค่า,개수))
                        else:raise ValueError('unexpected RFB server message: '+str(ประเภท_ค่า))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:ไคลเอ็นต์.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            งานเบื้องหลัง=threading.Thread(target=ผลผลิต,daemon=True);งานเบื้องหลัง.start()
            while not 자신.เทคโนโลยีสารสนเทศ_ปิด:
                ประเภท_ค่า=정확한값(ไคลเอ็นต์,1)[0]
                if ประเภท_ค่า==4:
                    เนื้อความ=정확한값(ไคลเอ็นต์,7); คีย์บอร์ด_รายการ.누름값(เนื้อความ[0]!=0,struct.unpack('>I',เนื้อความ[3:])[0]); continue
                if ประเภท_ค่า==255:
                    เนื้อความ=정확한값(ไคลเอ็นต์,11)
                    if เนื้อความ[0]!=0: raise ValueError('unsupported QEMU input extension')
                    คีย์บอร์ด_รายการ.누름값(struct.unpack('>H',เนื้อความ[1:3])[0]!=0,struct.unpack('>I',เนื้อความ[3:7])[0]); continue
                if ประเภท_ค่า==5:
                    เนื้อความ=정확한값(ไคลเอ็นต์,5); 단추들,พิกัดแกน_x,세로좌표=struct.unpack('>BHH',เนื้อความ)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: คีย์บอร์ด_รายการ.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=พิกัดแกน_x<576 and 112<=세로좌표<372:
                        การค้นหา_ดัชนี=(세로좌표-112)//52
                        if (세로좌표-112)%52<40 and การค้นหา_ดัชนี<5: 자신.ส่ง(bytes([ord('1')+การค้นหา_ดัชนี]))
                    else: 자신.ส่ง(bytes([30,1,단추들,พิกัดแกน_x&255,พิกัดแกน_x>>8,세로좌표&255,세로좌표>>8]))
                    continue
                if ประเภท_ค่า==6:
                    เนื้อความ=정확한값(ไคลเอ็นต์,7); 길이=struct.unpack('>i',เนื้อความ[3:])[0]
                    if abs(길이)>65536: raise ValueError('clipboard too large')
                    ข้อความ=정확한값(ไคลเอ็นต์,abs(길이))
                    if 길이>=0:
                        try: คีย์บอร์ด_รายการ.คลิปบอร์ด_ค่า=ข้อความ.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: คีย์บอร์ด_รายการ.คลิปบอร์ด_ค่า=ข้อความ.decode('latin-1').encode('utf-8')
                        คีย์บอร์ด_รายการ.คลิปบอร์ด_ค่า=คีย์บอร์ด_รายการ.คลิปบอร์ด_ค่า[:65536].decode('utf-8','ignore').encode('utf-8')
                    เซิร์ฟเวอร์_ค่า.sendall(bytes([ประเภท_ค่า])+เนื้อความ+ข้อความ); continue
                if ประเภท_ค่า==0:
                    เนื้อความ=정확한값(ไคลเอ็นต์,19)
                    if เนื้อความ[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=เนื้อความ[3]//8
                elif ประเภท_ค่า==2:
                    เนื้อความ=정확한값(ไคลเอ็นต์,3); 항목수=struct.unpack('>H',เนื้อความ[1:])[0]
                    if 항목수>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(항목수)+'i',정확한값(ไคลเอ็นต์,항목수*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 ค่าเริ่มต้น Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    เนื้อความ=struct.pack('>BHi',0,1,0)
                elif ประเภท_ค่า in (3,150): เนื้อความ=정확한값(ไคลเอ็นต์,9)
                elif ประเภท_ค่า==248:
                    เนื้อความ=정확한값(ไคลเอ็นต์,8)
                    if เนื้อความ[7]>64: raise ValueError('fence too large')
                    เนื้อความ+=정확한값(ไคลเอ็นต์,เนื้อความ[7])
                elif ประเภท_ค่า==250: เนื้อความ=정확한값(ไคลเอ็นต์,3)
                elif ประเภท_ค่า==251:
                    เนื้อความ=정확한값(ไคลเอ็นต์,7)
                    if เนื้อความ[5]>16: raise ValueError('too many screens')
                    เนื้อความ+=정확한값(ไคลเอ็นต์,เนื้อความ[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(ประเภท_ค่า))
                เซิร์ฟเวอร์_ค่า.sendall(bytes([ประเภท_ค่า])+เนื้อความ)
        except (OSError,EOFError,ValueError) as ข้อผิดพลาด:
            if str(ข้อผิดพลาด): print('VNC client:',ข้อผิดพลาด,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (ไคลเอ็นต์,เซิร์ฟเวอร์_ค่า):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def ใช้งาน_เดสก์ท็อป(หมายเลขพอร์ต=5902, เครือข่าย_9b2e3222=False, การถ่ายโอนแฟ้ม_หมายเลขพอร์ต=2121, 전달규칙들=(), ความละเอียด_ค่า=(640, 480), ผู้เยี่ยมชม_อีเมล=None, โฮสต์_อีเมล='127.0.0.1'):
    with ExitStack() as แหล่งข้อมูล, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        บริดจ์_รายการ = None
        if เครือข่าย_9b2e3222:
            from บริดจ์_3de4fe3a import บริดจ์_3de4fe3a
            บริดจ์_รายการ = แหล่งข้อมูล.enter_context(บริดจ์_3de4fe3a(การถ่ายโอนแฟ้ม_หมายเลขพอร์ต, 전달규칙들, ผู้เยี่ยมชม_อีเมล=ผู้เยี่ยมชม_อีเมล, โฮสต์_อีเมล=โฮสต์_อีเมล))
        เส้นทาง=Path(작업경로)/'display.sock'
        with socket.socket() as รับ_แปลง:
            รับ_แปลง.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            รับ_แปลง.bind(('127.0.0.1',หมายเลขพอร์ต)); รับ_แปลง.listen(1); รับ_แปลง.settimeout(.2)
            원격화면접속번호=รับ_แปลง.getsockname()[1]
            if บริดจ์_รายการ and (원격화면접속번호==การถ่ายโอนแฟ้ม_หมายเลขพอร์ต or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and โฮสต์==원격화면접속번호 for 통신규약,โฮสต์,_ in บริดจ์_รายการ.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            โพรเซส=subprocess.Popen(คําสั่ง(ความละเอียด_ค่า)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(เส้นทาง)]+(บริดจ์_รายการ.전달인수() if บริดจ์_รายการ else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            บริดจ์=เชื่อมต่อ_เดสก์ท็อป(โพรเซส); ผู้อ่าน=threading.Thread(target=บริดจ์.직렬입출력,daemon=True); ผู้อ่าน.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(รับ_แปลง.getsockname()[1]),flush=True)
            if บริดจ์_รายการ: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(โฮสต์_อีเมล,การถ่ายโอนแฟ้ม_หมายเลขพอร์ต),flush=True)
            def สิ้นสุด(สัญญาณ_หมายเลข,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,สิ้นสุด)
            การประมวลผล_งาน=None; 가로채기됨=False
            try:
                while โพรเซส.poll() is None:
                    try: ไคลเอ็นต์,_=รับ_แปลง.accept()
                    except socket.timeout: continue
                    if การประมวลผล_งาน is not None and การประมวลผล_งาน.is_alive(): ไคลเอ็นต์.close(); continue
                    if not เส้นทาง.exists(): ไคลเอ็นต์.close(); continue
                    การประมวลผล_งาน=threading.Thread(target=บริดจ์.ไคลเอ็นต์,args=(ไคลเอ็นต์,เส้นทาง),daemon=True); การประมวลผล_งาน.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                บริดจ์.เทคโนโลยีสารสนเทศ_ปิด=True
                if บริดจ์_รายการ: บริดจ์_รายการ.หยุดชั่วคราว_กิจกรรม.set()
                if โพรเซส.poll() is None:
                    โพรเซส.terminate()
                    try: โพรเซส.wait(timeout=5)
                    except subprocess.TimeoutExpired: โพรเซส.kill(); โพรเซส.wait()
                ผู้อ่าน.join(timeout=2); โพรเซส.stdin.close(); โพรเซส.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if บริดจ์_รายการ and บริดจ์_รายการ.ข้อผิดพลาด: raise RuntimeError('network bridge: '+บริดจ์_รายการ.ข้อผิดพลาด)
            return 0 if 가로채기됨 else โพรเซส.returncode


if __name__=='__main__':
    from ดําเนินการ_คําสั่ง import 해상도읽기
    ตัวแยกวิเคราะห์=argparse.ArgumentParser(description=__doc__); ตัวแยกวิเคราะห์.add_argument('--port',type=int,default=5902)
    ตัวแยกวิเคราะห์.add_argument('--resolution',type=해상도읽기,default=(640,480))
    ตัวแยกวิเคราะห์.add_argument('--network',action='store_true'); ตัวแยกวิเคราะห์.add_argument('--ftp-port',type=int,default=2121)
    ตัวแยกวิเคราะห์.add_argument('--forward',action='append',default=[])
    อาร์กิวเมนต์_อาร์เรย์=ตัวแยกวิเคราะห์.parse_args()
    if อาร์กิวเมนต์_อาร์เรย์.forward and not อาร์กิวเมนต์_อาร์เรย์.network: ตัวแยกวิเคราะห์.error('--forward requires --network')
    raise SystemExit(ใช้งาน_เดสก์ท็อป(อาร์กิวเมนต์_อาร์เรย์.port,เครือข่าย_9b2e3222=อาร์กิวเมนต์_อาร์เรย์.network,การถ่ายโอนแฟ้ม_หมายเลขพอร์ต=อาร์กิวเมนต์_อาร์เรย์.ftp_port,전달규칙들=อาร์กิวเมนต์_อาร์เรย์.forward,ความละเอียด_ค่า=อาร์กิวเมนต์_อาร์เรย์.resolution))
