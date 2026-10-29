#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, ឃី_តំលៃ 입력은 자체 ខឺណេល_តំលៃ UART로 전달한다. localhost 전용, 단일 អង្គបញ្ជា_តំលៃ 클라이언트.
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
from អនុវត្ត_ពាក្យបញ្ជា import ពាក្យ_បញ្ជា
from local_input import create


def 정확한값(소켓, ដាក់ទំហំ):
    ទិន្នន័យ = bytearray()
    while len(ទិន្នន័យ) < ដាក់ទំហំ:
        조각 = 소켓.recv(ដាក់ទំហំ - len(ទិន្នន័យ))
        if not 조각: raise EOFError()
        ទិន្នន័យ.extend(조각)
    return bytes(ទិន្នន័យ)


class ឃីបត:
    def __init__(자신, ផ្ញើ, 입력방식알림=None):
        자신.바이트전송 = ផ្ញើ; 자신.ឃីផ្លាស់ប្តូរ = set(); 자신.ឃ្លីបបត_តំលៃ = b''
        자신.한글조합기 = create(ផ្ញើ, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.ប្ដូរ_ឃី = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def ផ្ញើ(자신, ទិន្នន័យ):
        자신.한글조합기.조합확정()
        자신.바이트전송(ទិន្នន័យ)

    def ប្ដូរ_ម៉ូដ(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, ឃី_និមិត្ត_សញ្ញា):
        if ឃី_និមិត្ត_សញ្ញា in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.ឃីផ្លាស់ប្តូរ.add(ឃី_និមិត្ត_សញ្ញា)
            else: 자신.ឃីផ្លាស់ប្តូរ.discard(ឃី_និមិត្ត_សញ្ញា)
            return
        if not 누르는중:
            자신.ប្ដូរ_ឃី.discard(ឃី_និមិត្ត_សញ្ញា)
            return
        ឃី_CTRL = bool(자신.ឃីផ្លាស់ប្តូរ & {0xffe3, 0xffe4})
        ឃី_SHIFT = bool(자신.ឃីផ្លាស់ប្តូរ & {0xffe1, 0xffe2})
        if ឃី_CTRL and ឃី_SHIFT and ឃី_និមិត្ត_សញ្ញា in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if ឃី_និមិត្ត_សញ្ញា in (32,0xff0d):
                try:
                    តំលៃ=int(자신.유니코드입력,16)
                    if 32<=តំលៃ<=0x10ffff and not 0xd800<=តំលៃ<=0xdfff: 자신.ផ្ញើ(chr(តំលៃ).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif ឃី_និមិត្ត_សញ្ញា==0xff1b: 자신.유니코드입력=None
            elif ឃី_និមិត្ត_សញ្ញា==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif ឃី_និមិត្ត_សញ្ញា<128 and chr(ឃី_និមិត្ត_សញ្ញា) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(ឃី_និមិត្ត_សញ្ញា)
            return
        if ឃី_និមិត្ត_សញ្ញា in (0xff31,0xffc6) or ឃី_និមិត្ត_សញ្ញា==32 and ឃី_SHIFT and not ឃី_CTRL:
            if ឃី_និមិត្ត_សញ្ញា not in 자신.ប្ដូរ_ឃី: 자신.ប្ដូរ_ម៉ូដ()
            자신.ប្ដូរ_ឃី.add(ឃី_និមិត្ត_សញ្ញា)
            return
        if ឃី_និមិត្ត_សញ្ញា==0xff08 and 자신.한글여부 and not ឃី_CTRL and 자신.한글조합기.앞글자지우기(): return
        if ឃី_CTRL and ឃី_SHIFT and ឃី_និមិត្ត_សញ្ញា in (ord('t'),ord('T')):
            자신.ផ្ញើ(bytes([30,2,1,0,0,0,0])); return
        if ឃី_និមិត្ត_សញ្ញា==0xffc3: 자신.ផ្ញើ(bytes([30,2,2,0,0,0,0])); return
        if ឃី_និមិត្ត_សញ្ញា==0xffc9: 자신.ផ្ញើ(bytes([30,2,3,0,0,0,0])); return
        if ឃី_CTRL and ឃី_SHIFT and ឃី_និមិត្ត_សញ្ញា in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.ផ្ញើ(자신.ឃ្លីបបត_តំលៃ); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if ឃី_និមិត្ត_សញ្ញា in 특수글쇠: 자신.ផ្ញើ(특수글쇠[ឃី_និមិត្ត_សញ្ញា]); return
        តួអក្សរ_ការបំលែងកូដ = ឃី_និមិត្ត_សញ្ញា & 0xffffff if ឃី_និមិត្ត_សញ្ញា & 0xff000000 == 0x01000000 else ឃី_និមិត្ត_សញ្ញា
        if តួអក្សរ_ការបំលែងកូដ > 0x10ffff or 0xd800 <= តួអក្សរ_ការបំលែងកូដ <= 0xdfff or ឃី_និមិត្ត_សញ្ញា >= 0xff00 and ឃី_និមិត្ត_សញ្ញា < 0x1000000: return
        if ឃី_CTRL and 0x40 <= តួអក្សរ_ការបំលែងកូដ <= 0x7f: 자신.ផ្ញើ(bytes([តួអក្សរ_ការបំលែងកូដ & 31])); return
        if តួអក្សរ_ការបំលែងកូដ < 32: return
        if 자신.한글여부 and 자신.ឃីផ្លាស់ប្តូរ & {0xffea,0xfe03,0xff7e} and not ឃី_CTRL and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.ហ្វីដ_ឃី(chr(តួអក្សរ_ការបំលែងកូដ), altgr=True): return
        앞부분 = b'\x1b' if 자신.ឃីផ្លាស់ប្តូរ & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not ឃី_CTRL and not 앞부분 and 32<=តួអក្សរ_ការបំលែងកូដ<127:
            តួអក្សរ_ទិន្នន័យ=chr(តួអក្សរ_ការបំលែងកូដ).upper() if ឃី_SHIFT else chr(តួអក្សរ_ការបំលែងកូដ)
            if 자신.한글조합기.ហ្វីដ_ឃី(តួអក្សរ_ទិន្នន័យ): return
        자신.ផ្ញើ(앞부분 + chr(តួអក្សរ_ការបំលែងកូដ).encode('utf-8'))


class ភ្ជាប់_ដែសថប:
    def __init__(자신, ដំណើរការ):
        자신.ដំណើរការ=ដំណើរការ; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.ស្ថានីយ=False; 자신.시작화면=False; 자신.닫힘=False

    def ផ្ញើ(자신, ទិន្នន័យ):
        if not ទិន្នន័យ or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.ដំណើរការ.stdin.write(ទិន្នន័យ); 자신.ដំណើរការ.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                ទិន្នន័យ=자신.ដំណើរការ.stdout.read(4096)
                if not ទិន្នន័យ: break
                sys.stdout.buffer.write(ទិន្នន័យ); sys.stdout.buffer.flush()
                끝부분=(끝부분+ទិន្នន័យ)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.ស្ថានីយ=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.ផ្ញើ(b'terminal\n')
        finally: 자신.닫힘=True

    def អតិថិជន(자신, អតិថិជន, ផ្លូវ):
        ម៉ាស៊ីនមេ_តំលៃ=socket.socket(socket.AF_UNIX); ម៉ាស៊ីនមេ_តំលៃ.settimeout(10); អតិថិជន.settimeout(10)
        ឃីបត_ការបញ្ចូល=ឃីបត(자신.ផ្ញើ,lambda 한글여부:자신.ផ្ញើ(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            ម៉ាស៊ីនមេ_តំលៃ.connect(str(ផ្លូវ))
            # 초기 협상은 순서대로 끝낸다. 이후 លទ្ធផល 가닥만 클라이언트에 쓴다.
            អតិថិជន.sendall(정확한값(ម៉ាស៊ីនមេ_តំលៃ,12))
            판번호=정확한값(អតិថិជន,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            ម៉ាស៊ីនមេ_តំលៃ.sendall(판번호)
            개수=정확한값(ម៉ាស៊ីនមេ_តំលៃ,1);អតិថិជន.sendall(개수+정확한값(ម៉ាស៊ីនមេ_តំលៃ,개수[0]))
            សុវត្ថិភាព=정확한값(អតិថិជន,1)
            if សុវត្ថិភាព!=b'\x01': raise ValueError('unexpected security type')
            ម៉ាស៊ីនមេ_តំលៃ.sendall(សុវត្ថិភាព)
            if 판번호==b'RFB 003.008\n':អតិថិជន.sendall(정확한값(ម៉ាស៊ីនមេ_តំលៃ,4))
            ម៉ាស៊ីនមេ_តំលៃ.sendall(정확한값(អតិថិជន,1))
            초기값=정확한값(ម៉ាស៊ីនមេ_តំលៃ,24)
            អតិថិជន.sendall(초기값+정확한값(ម៉ាស៊ីនមេ_តំលៃ,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            អតិថិជន.settimeout(None);ម៉ាស៊ីនមេ_តំលៃ.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        ប្រភេទ_តំលៃ=정확한값(ម៉ាស៊ីនមេ_តំលៃ,1)[0]
                        if ប្រភេទ_តំលៃ==0:
                            머리=정확한값(ម៉ាស៊ីនមេ_តំលៃ,3);항목수=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 ពីចម្ងាយ_តំលៃ 포인터의 중복을 피한다.
                            ដែលលាក់_តំលៃ=포인터지원
                            if ដែលលាក់_តំលៃ:អតិថិជន.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            អតិថិជន.sendall(bytes([ប្រភេទ_តំលៃ])+머리)
                            for _ in range(항목수):
                                사각형=정확한값(ម៉ាស៊ីនមេ_តំលៃ,12);가로,បញ្ឈរ_កំណត់ទីតាំង,폭,높이,ការបំលែងកូដ_តំលៃ=struct.unpack('>HHHHi',사각형)
                                if ការបំលែងកូដ_តំលៃ!=0:raise ValueError('unexpected framebuffer encoding: '+str(ការបំលែងកូដ_តំលៃ))
                                អតិថិជន.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    ទិន្នន័យ=정확한값(ម៉ាស៊ីនមេ_តំលៃ,min(남음,65536));អតិថិជន.sendall(ទិន្នន័យ);남음-=len(ទិន្នន័យ)
                        elif ប្រភេទ_តំលៃ==1:
                            머리=정확한값(ម៉ាស៊ីនមេ_តំលៃ,5);개수=struct.unpack('>H',머리[3:])[0]
                            អតិថិជន.sendall(bytes([ប្រភេទ_តំលៃ])+머리+정확한값(ម៉ាស៊ីនមេ_តំលៃ,개수*6))
                        elif ប្រភេទ_តំលៃ==2:អតិថិជន.sendall(bytes([ប្រភេទ_តំលៃ]))
                        elif ប្រភេទ_តំលៃ==3:
                            머리=정확한값(ម៉ាស៊ីនមេ_តំលៃ,7);개수=struct.unpack('>I',머리[3:])[0]
                            if 개수>1048576:raise ValueError('server clipboard too large')
                            អតិថិជន.sendall(bytes([ប្រភេទ_តំលៃ])+머리+정확한값(ម៉ាស៊ីនមេ_តំលៃ,개수))
                        else:raise ValueError('unexpected RFB server message: '+str(ប្រភេទ_តំលៃ))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:អតិថិជន.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                ប្រភេទ_តំលៃ=정확한값(អតិថិជន,1)[0]
                if ប្រភេទ_តំលៃ==4:
                    តួអត្ថបទ=정확한값(អតិថិជន,7); ឃីបត_ការបញ្ចូល.누름값(តួអត្ថបទ[0]!=0,struct.unpack('>I',តួអត្ថបទ[3:])[0]); continue
                if ប្រភេទ_តំលៃ==255:
                    តួអត្ថបទ=정확한값(អតិថិជន,11)
                    if តួអត្ថបទ[0]!=0: raise ValueError('unsupported QEMU input extension')
                    ឃីបត_ការបញ្ចូល.누름값(struct.unpack('>H',តួអត្ថបទ[1:3])[0]!=0,struct.unpack('>I',តួអត្ថបទ[3:7])[0]); continue
                if ប្រភេទ_តំលៃ==5:
                    តួអត្ថបទ=정확한값(អតិថិជន,5); 단추들,កូអរដោណេ_x,ប៊ូតុង_Y_កូអរដោនេ=struct.unpack('>BHH',តួអត្ថបទ)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: ឃីបត_ការបញ្ចូល.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=កូអរដោណេ_x<576 and 112<=ប៊ូតុង_Y_កូអរដោនេ<372:
                        រុករក_សន្ទស្សន៏=(ប៊ូតុង_Y_កូអរដោនេ-112)//52
                        if (ប៊ូតុង_Y_កូអរដោនេ-112)%52<40 and រុករក_សន្ទស្សន៏<5: 자신.ផ្ញើ(bytes([ord('1')+រុករក_សន្ទស្សន៏]))
                    else: 자신.ផ្ញើ(bytes([30,1,단추들,កូអរដោណេ_x&255,កូអរដោណេ_x>>8,ប៊ូតុង_Y_កូអរដោនេ&255,ប៊ូតុង_Y_កូអរដោនេ>>8]))
                    continue
                if ប្រភេទ_តំលៃ==6:
                    តួអត្ថបទ=정확한값(អតិថិជន,7); ប្រវែង_តំលៃ=struct.unpack('>i',តួអត្ថបទ[3:])[0]
                    if abs(ប្រវែង_តំលៃ)>65536: raise ValueError('clipboard too large')
                    អត្ថបទ=정확한값(អតិថិជន,abs(ប្រវែង_តំលៃ))
                    if ប្រវែង_តំលៃ>=0:
                        try: ឃីបត_ការបញ្ចូល.ឃ្លីបបត_តំលៃ=អត្ថបទ.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: ឃីបត_ការបញ្ចូល.ឃ្លីបបត_តំលៃ=អត្ថបទ.decode('latin-1').encode('utf-8')
                        ឃីបត_ការបញ្ចូល.ឃ្លីបបត_តំលៃ=ឃីបត_ការបញ្ចូល.ឃ្លីបបត_តំលៃ[:65536].decode('utf-8','ignore').encode('utf-8')
                    ម៉ាស៊ីនមេ_តំលៃ.sendall(bytes([ប្រភេទ_តំលៃ])+តួអត្ថបទ+អត្ថបទ); continue
                if ប្រភេទ_តំលៃ==0:
                    តួអត្ថបទ=정확한값(អតិថិជន,19)
                    if តួអត្ថបទ[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=តួអត្ថបទ[3]//8
                elif ប្រភេទ_តំលៃ==2:
                    តួអត្ថបទ=정확한값(អតិថិជន,3); 항목수=struct.unpack('>H',តួអត្ថបទ[1:])[0]
                    if 항목수>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(항목수)+'i',정확한값(អតិថិជន,항목수*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 តំលៃស្វ័យប្រវត្តិ Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    តួអត្ថបទ=struct.pack('>BHi',0,1,0)
                elif ប្រភេទ_តំលៃ in (3,150): តួអត្ថបទ=정확한값(អតិថិជន,9)
                elif ប្រភេទ_តំលៃ==248:
                    តួអត្ថបទ=정확한값(អតិថិជន,8)
                    if តួអត្ថបទ[7]>64: raise ValueError('fence too large')
                    តួអត្ថបទ+=정확한값(អតិថិជន,តួអត្ថបទ[7])
                elif ប្រភេទ_តំលៃ==250: តួអត្ថបទ=정확한값(អតិថិជន,3)
                elif ប្រភេទ_តំលៃ==251:
                    តួអត្ថបទ=정확한값(អតិថិជន,7)
                    if តួអត្ថបទ[5]>16: raise ValueError('too many screens')
                    តួអត្ថបទ+=정확한값(អតិថិជន,តួអត្ថបទ[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(ប្រភេទ_តំលៃ))
                ម៉ាស៊ីនមេ_តំលៃ.sendall(bytes([ប្រភេទ_តំលៃ])+តួអត្ថបទ)
        except (OSError,EOFError,ValueError) as កំហុស:
            if str(កំហុស): print('VNC client:',កំហុស,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (អតិថិជន,ម៉ាស៊ីនមេ_តំលៃ):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def ដំណើរការ_ដែសថប(លេខរន្ធ=5902, ណិតវឺក=False, ឯកសារ_ផ្ទេរ_លេខរន្ធ=2121, 전달규칙들=(), គុណភាព_បង្ហាញ_តំលៃ=(640, 480), ភ្ញៀវ_អ៊ីម៉ែល=None, ហូស_អ៊ីម៉ែល='127.0.0.1'):
    with ExitStack() as ធនធាន, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        통신다리항목 = None
        if ណិតវឺក:
            from 통신다리 import 통신다리
            통신다리항목 = ធនធាន.enter_context(통신다리(ឯកសារ_ផ្ទេរ_លេខរន្ធ, 전달규칙들, ភ្ញៀវ_អ៊ីម៉ែល=ភ្ញៀវ_អ៊ីម៉ែល, ហូស_អ៊ីម៉ែល=ហូស_អ៊ីម៉ែល))
        ផ្លូវ=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',លេខរន្ធ)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if 통신다리항목 and (원격화면접속번호==ឯកសារ_ផ្ទេរ_លេខរន្ធ or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and ហូស==원격화면접속번호 for 통신규약,ហូស,_ in 통신다리항목.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            ដំណើរការ=subprocess.Popen(ពាក្យ_បញ្ជា(គុណភាព_បង្ហាញ_តំលៃ)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(ផ្លូវ)]+(통신다리항목.전달인수() if 통신다리항목 else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            연결다리=ភ្ជាប់_ដែសថប(ដំណើរការ); អ្នកអាន=threading.Thread(target=연결다리.직렬입출력,daemon=True); អ្នកអាន.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if 통신다리항목: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(ហូស_អ៊ីម៉ែល,ឯកសារ_ផ្ទេរ_លេខរន្ធ),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while ដំណើរការ.poll() is None:
                    try: អតិថិជន,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): អតិថិជន.close(); continue
                    if not ផ្លូវ.exists(): អតិថិជន.close(); continue
                    처리작업=threading.Thread(target=연결다리.អតិថិជន,args=(អតិថិជន,ផ្លូវ),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                연결다리.닫힘=True
                if 통신다리항목: 통신다리항목.ផ្អាក_ព្រឹត្តិការណ៍.set()
                if ដំណើរការ.poll() is None:
                    ដំណើរការ.terminate()
                    try: ដំណើរការ.wait(timeout=5)
                    except subprocess.TimeoutExpired: ដំណើរការ.kill(); ដំណើរការ.wait()
                អ្នកអាន.join(timeout=2); ដំណើរការ.stdin.close(); ដំណើរការ.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if 통신다리항목 and 통신다리항목.កំហុស: raise RuntimeError('network bridge: '+통신다리항목.កំហុស)
            return 0 if 가로채기됨 else ដំណើរការ.returncode


if __name__=='__main__':
    from អនុវត្ត_ពាក្យបញ្ជា import 해상도읽기
    មុខងារ_ញែក=argparse.ArgumentParser(description=__doc__); មុខងារ_ញែក.add_argument('--port',type=int,default=5902)
    មុខងារ_ញែក.add_argument('--resolution',type=해상도읽기,default=(640,480))
    មុខងារ_ញែក.add_argument('--network',action='store_true'); មុខងារ_ញែក.add_argument('--ftp-port',type=int,default=2121)
    មុខងារ_ញែក.add_argument('--forward',action='append',default=[])
    អាគុយម៉ង់_អារេ=មុខងារ_ញែក.parse_args()
    if អាគុយម៉ង់_អារេ.forward and not អាគុយម៉ង់_អារេ.network: មុខងារ_ញែក.error('--forward requires --network')
    raise SystemExit(ដំណើរការ_ដែសថប(អាគុយម៉ង់_អារេ.port,ណិតវឺក=អាគុយម៉ង់_អារេ.network,ឯកសារ_ផ្ទេរ_លេខរន្ធ=អាគុយម៉ង់_អារេ.ftp_port,전달규칙들=អាគុយម៉ង់_អារេ.forward,គុណភាព_បង្ហាញ_តំលៃ=អាគុយម៉ង់_អារេ.resolution))
