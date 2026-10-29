#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, Ключ_ЗНАЧЕН 입력은 свой ядро_ЗНАЧЕН UART로 전달한다. localhost 전용, 단일 управление_ЗНАЧЕН 클라이언트.
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
from 실행 import команда
from local_input import create


def СОВПАД_ЗНАЧЕН(сокет_ЗНАЧЕН, Размер):
    данные = bytearray()
    while len(данные) < Размер:
        блок_ЗНАЧЕН_652d4b53 = сокет_ЗНАЧЕН.recv(Размер - len(данные))
        if not блок_ЗНАЧЕН_652d4b53: raise EOFError()
        данные.extend(блок_ЗНАЧЕН_652d4b53)
    return bytes(данные)


class клавиатура:
    def __init__(자신, написать, 입력방식알림=None):
        자신.바이트전송 = написать; 자신.клавиша_модификатор = set(); 자신.буфер_обмена_ЗНАЧЕН = b''
        자신.한글조합기 = create(написать, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.перейти_Ключ = set()
        자신.Юникод_входные_данные = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def написать(자신, данные):
        자신.한글조합기.фиксация_состав()
        자신.바이트전송(данные)

    def перейти_МОДА(자신):
        자신.한글조합기.фиксация_состав(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, Ключ_символ):
        if Ключ_символ in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.клавиша_модификатор.add(Ключ_символ)
            else: 자신.клавиша_модификатор.discard(Ключ_символ)
            return
        if not 누르는중:
            자신.перейти_Ключ.discard(Ключ_символ)
            return
        управление_Ключ = bool(자신.клавиша_модификатор & {0xffe3, 0xffe4})
        клавиша_SHIFT = bool(자신.клавиша_модификатор & {0xffe1, 0xffe2})
        if управление_Ключ and клавиша_SHIFT and Ключ_символ in (ord('u'),ord('U')):
            자신.한글조합기.фиксация_состав(); 자신.Юникод_входные_данные = ''; return
        if 자신.Юникод_входные_данные is not None:
            if Ключ_символ in (32,0xff0d):
                try:
                    ЗНАЧЕН=int(자신.Юникод_входные_данные,16)
                    if 32<=ЗНАЧЕН<=0x10ffff and not 0xd800<=ЗНАЧЕН<=0xdfff: 자신.написать(chr(ЗНАЧЕН).encode('utf-8'))
                except ValueError: pass
                자신.Юникод_входные_данные=None
            elif Ключ_символ==0xff1b: 자신.Юникод_входные_данные=None
            elif Ключ_символ==0xff08: 자신.Юникод_входные_данные=자신.Юникод_входные_данные[:-1]
            elif Ключ_символ<128 and chr(Ключ_символ) in '0123456789abcdefABCDEF' and len(자신.Юникод_входные_данные)<6: 자신.Юникод_входные_данные+=chr(Ключ_символ)
            return
        if Ключ_символ in (0xff31,0xffc6) or Ключ_символ==32 and клавиша_SHIFT and not управление_Ключ:
            if Ключ_символ not in 자신.перейти_Ключ: 자신.перейти_МОДА()
            자신.перейти_Ключ.add(Ключ_символ)
            return
        if Ключ_символ==0xff08 and 자신.한글여부 and not управление_Ключ and 자신.한글조합기.앞글자지우기(): return
        if управление_Ключ and клавиша_SHIFT and Ключ_символ in (ord('t'),ord('T')):
            자신.написать(bytes([30,2,1,0,0,0,0])); return
        if Ключ_символ==0xffc3: 자신.написать(bytes([30,2,2,0,0,0,0])); return
        if Ключ_символ==0xffc9: 자신.написать(bytes([30,2,3,0,0,0,0])); return
        if управление_Ключ and клавиша_SHIFT and Ключ_символ in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.написать(자신.буфер_обмена_ЗНАЧЕН); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if Ключ_символ in 특수글쇠: 자신.написать(특수글쇠[Ключ_символ]); return
        кодировка_символов = Ключ_символ & 0xffffff if Ключ_символ & 0xff000000 == 0x01000000 else Ключ_символ
        if кодировка_символов > 0x10ffff or 0xd800 <= кодировка_символов <= 0xdfff or Ключ_символ >= 0xff00 and Ключ_символ < 0x1000000: return
        if управление_Ключ and 0x40 <= кодировка_символов <= 0x7f: 자신.написать(bytes([кодировка_символов & 31])); return
        if кодировка_символов < 32: return
        if 자신.한글여부 and 자신.клавиша_модификатор & {0xffea,0xfe03,0xff7e} and not управление_Ключ and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.канал_Ключ(chr(кодировка_символов), altgr=True): return
        сдвиг_часть = b'\x1b' if 자신.клавиша_модификатор & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not управление_Ключ and not сдвиг_часть and 32<=кодировка_символов<127:
            символьные_данные=chr(кодировка_символов).upper() if клавиша_SHIFT else chr(кодировка_символов)
            if 자신.한글조합기.канал_Ключ(символьные_данные): return
        자신.написать(сдвиг_часть + chr(кодировка_символов).encode('utf-8'))


class Connect_компьютер:
    def __init__(자신, Процесс):
        자신.Процесс=Процесс; 자신.блокировка_ЗНАЧЕН=threading.Lock(); 자신.준비완료=False; 자신.терминал=False; 자신.시작화면=False; 자신.ИТ_службы_закрыто=False

    def написать(자신, данные):
        if not данные or 자신.ИТ_службы_закрыто: return
        with 자신.блокировка_ЗНАЧЕН:
            try: 자신.Процесс.stdin.write(данные); 자신.Процесс.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                данные=자신.Процесс.stdout.read(4096)
                if not данные: break
                sys.stdout.buffer.write(данные); sys.stdout.buffer.flush()
                끝부분=(끝부분+данные)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); ИТ_службы_закрыто=끝부분.rfind(b'TERMINAL CLOSED'); рисунок_экран=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,ИТ_службы_закрыто,рисунок_экран,종료됨)>=0:
                    자신.терминал=열림>max(ИТ_службы_закрыто,рисунок_экран,종료됨)
                    자신.시작화면=рисунок_экран>max(열림,ИТ_службы_закрыто,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.написать(b'terminal\n')
        finally: 자신.ИТ_службы_закрыто=True

    def клиент(자신, клиент, путь):
        сервер_ЗНАЧЕН=socket.socket(socket.AF_UNIX); сервер_ЗНАЧЕН.settimeout(10); клиент.settimeout(10)
        клавиатура_ввод=клавиатура(자신.написать,lambda 한글여부:자신.написать(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            сервер_ЗНАЧЕН.connect(str(путь))
            # начальное_состояние 협상은 순서대로 끝낸다. 이후 текстовыйВывод 가닥만 클라이언트에 쓴다.
            клиент.sendall(СОВПАД_ЗНАЧЕН(сервер_ЗНАЧЕН,12))
            номер_версии=СОВПАД_ЗНАЧЕН(клиент,12)
            if номер_версии not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            сервер_ЗНАЧЕН.sendall(номер_версии)
            товар_СЧЁТ=СОВПАД_ЗНАЧЕН(сервер_ЗНАЧЕН,1);клиент.sendall(товар_СЧЁТ+СОВПАД_ЗНАЧЕН(сервер_ЗНАЧЕН,товар_СЧЁТ[0]))
            Безопасность=СОВПАД_ЗНАЧЕН(клиент,1)
            if Безопасность!=b'\x01': raise ValueError('unexpected security type')
            сервер_ЗНАЧЕН.sendall(Безопасность)
            if номер_версии==b'RFB 003.008\n':клиент.sendall(СОВПАД_ЗНАЧЕН(сервер_ЗНАЧЕН,4))
            сервер_ЗНАЧЕН.sendall(СОВПАД_ЗНАЧЕН(клиент,1))
            초기값=СОВПАД_ЗНАЧЕН(сервер_ЗНАЧЕН,24)
            клиент.sendall(초기값+СОВПАД_ЗНАЧЕН(сервер_ЗНАЧЕН,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            клиент.settimeout(None);сервер_ЗНАЧЕН.settimeout(None)
            def выход():
                try:
                    while True:
                        область_ЗНАЧЕН=СОВПАД_ЗНАЧЕН(сервер_ЗНАЧЕН,1)[0]
                        if область_ЗНАЧЕН==0:
                            HEAD_ЗНАЧЕН=СОВПАД_ЗНАЧЕН(сервер_ЗНАЧЕН,3);ввод_СЧЁТ=struct.unpack('>H',HEAD_ЗНАЧЕН[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 удаленный_ЗНАЧЕН 포인터의 중복을 피한다.
                            Скрытая_ЗНАЧЕН=포인터지원
                            if Скрытая_ЗНАЧЕН:клиент.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            клиент.sendall(bytes([область_ЗНАЧЕН])+HEAD_ЗНАЧЕН)
                            for _ in range(ввод_СЧЁТ):
                                прямоугольник=СОВПАД_ЗНАЧЕН(сервер_ЗНАЧЕН,12);가로,Вертикаль_позиция,폭,높이,кодирование_ЗНАЧЕН=struct.unpack('>HHHHi',прямоугольник)
                                if кодирование_ЗНАЧЕН!=0:raise ValueError('unexpected framebuffer encoding: '+str(кодирование_ЗНАЧЕН))
                                клиент.sendall(прямоугольник)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    данные=СОВПАД_ЗНАЧЕН(сервер_ЗНАЧЕН,min(남음,65536));клиент.sendall(данные);남음-=len(данные)
                        elif область_ЗНАЧЕН==1:
                            HEAD_ЗНАЧЕН=СОВПАД_ЗНАЧЕН(сервер_ЗНАЧЕН,5);товар_СЧЁТ=struct.unpack('>H',HEAD_ЗНАЧЕН[3:])[0]
                            клиент.sendall(bytes([область_ЗНАЧЕН])+HEAD_ЗНАЧЕН+СОВПАД_ЗНАЧЕН(сервер_ЗНАЧЕН,товар_СЧЁТ*6))
                        elif область_ЗНАЧЕН==2:клиент.sendall(bytes([область_ЗНАЧЕН]))
                        elif область_ЗНАЧЕН==3:
                            HEAD_ЗНАЧЕН=СОВПАД_ЗНАЧЕН(сервер_ЗНАЧЕН,7);товар_СЧЁТ=struct.unpack('>I',HEAD_ЗНАЧЕН[3:])[0]
                            if товар_СЧЁТ>1048576:raise ValueError('server clipboard too large')
                            клиент.sendall(bytes([область_ЗНАЧЕН])+HEAD_ЗНАЧЕН+СОВПАД_ЗНАЧЕН(сервер_ЗНАЧЕН,товар_СЧЁТ))
                        else:raise ValueError('unexpected RFB server message: '+str(область_ЗНАЧЕН))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:клиент.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            фоноваяЗадача=threading.Thread(target=выход,daemon=True);фоноваяЗадача.start()
            while not 자신.ИТ_службы_закрыто:
                область_ЗНАЧЕН=СОВПАД_ЗНАЧЕН(клиент,1)[0]
                if область_ЗНАЧЕН==4:
                    основной_текст=СОВПАД_ЗНАЧЕН(клиент,7); клавиатура_ввод.누름값(основной_текст[0]!=0,struct.unpack('>I',основной_текст[3:])[0]); continue
                if область_ЗНАЧЕН==255:
                    основной_текст=СОВПАД_ЗНАЧЕН(клиент,11)
                    if основной_текст[0]!=0: raise ValueError('unsupported QEMU input extension')
                    клавиатура_ввод.누름값(struct.unpack('>H',основной_текст[1:3])[0]!=0,struct.unpack('>I',основной_текст[3:7])[0]); continue
                if область_ЗНАЧЕН==5:
                    основной_текст=СОВПАД_ЗНАЧЕН(клиент,5); 단추들,координата_X,Y_координата=struct.unpack('>BHH',основной_текст)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: клавиатура_ввод.한글조합기.фиксация_состав()
                    if 눌림&1 and 자신.시작화면 and 64<=координата_X<576 and 112<=Y_координата<372:
                        Поиск_ИНДЕКС=(Y_координата-112)//52
                        if (Y_координата-112)%52<40 and Поиск_ИНДЕКС<5: 자신.написать(bytes([ord('1')+Поиск_ИНДЕКС]))
                    else: 자신.написать(bytes([30,1,단추들,координата_X&255,координата_X>>8,Y_координата&255,Y_координата>>8]))
                    continue
                if область_ЗНАЧЕН==6:
                    основной_текст=СОВПАД_ЗНАЧЕН(клиент,7); длина_ЗНАЧЕН=struct.unpack('>i',основной_текст[3:])[0]
                    if abs(длина_ЗНАЧЕН)>65536: raise ValueError('clipboard too large')
                    текст=СОВПАД_ЗНАЧЕН(клиент,abs(длина_ЗНАЧЕН))
                    if длина_ЗНАЧЕН>=0:
                        try: клавиатура_ввод.буфер_обмена_ЗНАЧЕН=текст.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: клавиатура_ввод.буфер_обмена_ЗНАЧЕН=текст.decode('latin-1').encode('utf-8')
                        клавиатура_ввод.буфер_обмена_ЗНАЧЕН=клавиатура_ввод.буфер_обмена_ЗНАЧЕН[:65536].decode('utf-8','ignore').encode('utf-8')
                    сервер_ЗНАЧЕН.sendall(bytes([область_ЗНАЧЕН])+основной_текст+текст); continue
                if область_ЗНАЧЕН==0:
                    основной_текст=СОВПАД_ЗНАЧЕН(клиент,19)
                    if основной_текст[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=основной_текст[3]//8
                elif область_ЗНАЧЕН==2:
                    основной_текст=СОВПАД_ЗНАЧЕН(клиент,3); ввод_СЧЁТ=struct.unpack('>H',основной_текст[1:])[0]
                    if ввод_СЧЁТ>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(ввод_СЧЁТ)+'i',СОВПАД_ЗНАЧЕН(клиент,ввод_СЧЁТ*4))
                    포인터지원=-239 in 부호들
                    # 로컬 экран 중계는 значение_по_умолчанию Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    основной_текст=struct.pack('>BHi',0,1,0)
                elif область_ЗНАЧЕН in (3,150): основной_текст=СОВПАД_ЗНАЧЕН(клиент,9)
                elif область_ЗНАЧЕН==248:
                    основной_текст=СОВПАД_ЗНАЧЕН(клиент,8)
                    if основной_текст[7]>64: raise ValueError('fence too large')
                    основной_текст+=СОВПАД_ЗНАЧЕН(клиент,основной_текст[7])
                elif область_ЗНАЧЕН==250: основной_текст=СОВПАД_ЗНАЧЕН(клиент,3)
                elif область_ЗНАЧЕН==251:
                    основной_текст=СОВПАД_ЗНАЧЕН(клиент,7)
                    if основной_текст[5]>16: raise ValueError('too many screens')
                    основной_текст+=СОВПАД_ЗНАЧЕН(клиент,основной_текст[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(область_ЗНАЧЕН))
                сервер_ЗНАЧЕН.sendall(bytes([область_ЗНАЧЕН])+основной_текст)
        except (OSError,EOFError,ValueError) as ошибка:
            if str(ошибка): print('VNC client:',ошибка,file=sys.stderr,flush=True)
        finally:
            for сокет_ЗНАЧЕН in (клиент,сервер_ЗНАЧЕН):
                try: сокет_ЗНАЧЕН.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                сокет_ЗНАЧЕН.close()


def выполнить_компьютер(номер_порта=5902, сеть=False, передача_файла_номер_порта=2121, 전달규칙들=(), разрешение_ЗНАЧЕН=(640, 480), гость_АДРЕС=None, адрес_узла='127.0.0.1'):
    with ExitStack() as Ресурсы, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        мост_ввод = None
        if сеть:
            from мост_3de4fe3a import мост_3de4fe3a
            мост_ввод = Ресурсы.enter_context(мост_3de4fe3a(передача_файла_номер_порта, 전달규칙들, гость_АДРЕС=гость_АДРЕС, адрес_узла=адрес_узла))
        путь=Path(작업경로)/'display.sock'
        with socket.socket() as порт_получения:
            порт_получения.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            порт_получения.bind(('127.0.0.1',номер_порта)); порт_получения.listen(1); порт_получения.settimeout(.2)
            원격화면접속번호=порт_получения.getsockname()[1]
            if мост_ввод and (원격화면접속번호==передача_файла_номер_порта or 50000<=원격화면접속번호<=50007 or any(сеть_ABI=='tcp' and узел==원격화면접속번호 for сеть_ABI,узел,_ in мост_ввод.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Процесс=subprocess.Popen(команда(разрешение_ЗНАЧЕН)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(путь)]+(мост_ввод.전달인수() if мост_ввод else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            мост=Connect_компьютер(Процесс); Ридер=threading.Thread(target=мост.직렬입출력,daemon=True); Ридер.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(порт_получения.getsockname()[1]),flush=True)
            if мост_ввод: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(адрес_узла,передача_файла_номер_порта),flush=True)
            def завершить(신호번호,выполнение_кадр): raise KeyboardInterrupt()
            Назад=signal.signal(signal.SIGTERM,завершить)
            обработка_дело=None; 가로채기됨=False
            try:
                while Процесс.poll() is None:
                    try: клиент,_=порт_получения.accept()
                    except socket.timeout: continue
                    if обработка_дело is not None and обработка_дело.is_alive(): клиент.close(); continue
                    if not путь.exists(): клиент.close(); continue
                    обработка_дело=threading.Thread(target=мост.клиент,args=(клиент,путь),daemon=True); обработка_дело.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                мост.ИТ_службы_закрыто=True
                if мост_ввод: мост_ввод.пауза_Событие.set()
                if Процесс.poll() is None:
                    Процесс.terminate()
                    try: Процесс.wait(timeout=5)
                    except subprocess.TimeoutExpired: Процесс.kill(); Процесс.wait()
                Ридер.join(timeout=2); Процесс.stdin.close(); Процесс.stdout.close(); signal.signal(signal.SIGTERM,Назад)
            if мост_ввод and мост_ввод.ошибка: raise RuntimeError('network bridge: '+мост_ввод.ошибка)
            return 0 if 가로채기됨 else Процесс.returncode


if __name__=='__main__':
    from 실행 import чтение_разрешение
    анализатор=argparse.ArgumentParser(description=__doc__); анализатор.add_argument('--port',type=int,default=5902)
    анализатор.add_argument('--resolution',type=чтение_разрешение,default=(640,480))
    анализатор.add_argument('--network',action='store_true'); анализатор.add_argument('--ftp-port',type=int,default=2121)
    анализатор.add_argument('--forward',action='append',default=[])
    аргумент_МАССИВ=анализатор.parse_args()
    if аргумент_МАССИВ.forward and not аргумент_МАССИВ.network: анализатор.error('--forward requires --network')
    raise SystemExit(выполнить_компьютер(аргумент_МАССИВ.port,сеть=аргумент_МАССИВ.network,передача_файла_номер_порта=аргумент_МАССИВ.ftp_port,전달규칙들=аргумент_МАССИВ.forward,разрешение_ЗНАЧЕН=аргумент_МАССИВ.resolution))
