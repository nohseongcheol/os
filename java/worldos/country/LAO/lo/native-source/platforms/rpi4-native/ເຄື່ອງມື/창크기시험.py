#!/usr/bin/env python3
"""ຕົວ_ຈິງ_ຂໍ້ມູນ QEMU/VNC에서 ເທີມີນໍ 모서리 ລາກ_ຄ່າ·ລູກສອນເມົ້າ·동적 ຕົວອັກສອນ_ຄ່າ ຊ່ອງ_ເຂົ້າໃນ·ແກ້ໄຂ_ຄ່າ ເນື້ອໃນ_ຄ່າ_cb0f2404 보존를 검사한다."""
import ftplib
import hashlib
import io
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from PIL import Image
from ເດັສທັອບ_ເບິ່ງ import 정확한값
from ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ import ໂຄງ_ການ_ເລກຮາກ


def 창크기시험(너비, 높이, ມາດຕະການ_ທາງໂຄຈອນ):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); ຫມາຍເລກພອດ = 임시.getsockname()[1]
    ຂະ_ຫນາດ_ຂໍ້ຄວາມ = '{}x{}'.format(너비, 높이)
    ຂະ_ບວນ_ການ_ຄ່າ = subprocess.Popen(['python3', str(ໂຄງ_ການ_ເລກຮາກ/'ເຄື່ອງມື/ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(ຫມາຍເລກພອດ), '--resolution', ຂະ_ຫນາດ_ຂໍ້ຄວາມ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    ຕົວ_ໃຊ້_ເລືອກ_a916db4e = selectors.DefaultSelector(); ຕົວ_ໃຊ້_ເລືອກ_a916db4e.register(ຂະ_ບວນ_ການ_ຄ່າ.stdout, selectors.EVENT_READ)
    ບັນທຶກ_ແຖວ = bytearray(); ທາງ_ໄກ_ຄ່າ = None; ໂອນ_ຄ່າ = None; ລູກສອນເມົ້າ_ເຊື່ອງໄວ້ໄດ້=[False]

    def 기다리기(ລາຍການ_ຄ່າ, ແລ່ນ=0):
        마감 = time.monotonic() + 60
        while ລາຍການ_ຄ່າ not in ບັນທຶກ_ແຖວ[ແລ່ນ:]:
            if time.monotonic() > 마감 or ຂະ_ບວນ_ການ_ຄ່າ.poll() is not None or b'HALTED' in ບັນທຶກ_ແຖວ or b'PANIC:' in ບັນທຶກ_ແຖວ:
                raise AssertionError(ບັນທຶກ_ແຖວ[ແລ່ນ:].decode('utf-8', 'replace'))
            for ງານ, _ in ຕົວ_ໃຊ້_ເລືອກ_a916db4e.select(.1):
                ຂໍ້ມູນ = ງານ.fileobj.read(65536)
                if ຂໍ້ມູນ: ບັນທຶກ_ແຖວ.extend(ຂໍ້ມູນ)
        return ບັນທຶກ_ແຖວ[ແລ່ນ:].decode('utf-8', 'replace')

    def ກົດ_ປຸ່ມ(ສັນຍາລັກ, 눌림=True): ທາງ_ໄກ_ຄ່າ.sendall(struct.pack('>BBHI', 4, int(눌림), 0, ສັນຍາລັກ))

    def ສົ່ງ_ຂໍ້ຄວາມ(ຂໍ້ຄວາມ):
        ແລ່ນ = len(ບັນທຶກ_ແຖວ)
        for ຕົວອັກສອນ_ຄ່າ in ຂໍ້ຄວາມ:
            ສັນຍາລັກ = 0xff0d if ຕົວອັກສອນ_ຄ່າ == '\n' else ord(ຕົວອັກສອນ_ຄ່າ) if ord(ຕົວອັກສອນ_ຄ່າ) < 256 else 0x1000000 | ord(ຕົວອັກສອນ_ຄ່າ)
            ກົດ_ປຸ່ມ(ສັນຍາລັກ); ກົດ_ປຸ່ມ(ສັນຍາລັກ, False)
        return ແລ່ນ

    def ເຊລ(ຂໍ້ຄວາມ): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', ສົ່ງ_ຂໍ້ຄວາມ(ຂໍ້ຄວາມ+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, ລວງຕັ້ງ_ຈັດຕໍາແຫນ່ງ, 눌림): ທາງ_ໄກ_ຄ່າ.sendall(struct.pack('>BBHH', 5, 눌림, 가로, ລວງຕັ້ງ_ຈັດຕໍາແຫນ່ງ))

    def ກົດ_ຄ່າ(가로, ລວງຕັ້ງ_ຈັດຕໍາແຫນ່ງ): 가리키기(가로, ລວງຕັ້ງ_ຈັດຕໍາແຫນ່ງ, 1); 가리키기(가로, ລວງຕັ້ງ_ຈັດຕໍາແຫນ່ງ, 0)

    def ບິດແມັບ_ຮູບ():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 ຕົວ_ຈິງ_ຂໍ້ມູນ 너비를 쓴다.
        ທາງ_ໄກ_ຄ່າ.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        ການ_ແຕ້ມ_ຄ່າ = Image.new('RGB', (너비, 높이)); ຫມວດ_ຄ່າ_9285603e = 0
        while True:
            종류 = 정확한값(ທາງ_ໄກ_ຄ່າ, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                ຄວາມຍາວ_ຄ່າ = struct.unpack('>I', 정확한값(ທາງ_ໄກ_ຄ່າ, 7)[3:])[0]; 정확한값(ທາງ_ໄກ_ຄ່າ, ຄວາມຍາວ_ຄ່າ); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(ທາງ_ໄກ_ຄ່າ, 3)[1:])[0]
            for _ in range(개수):
                가로, ລວງຕັ້ງ_ຈັດຕໍາແຫນ່ງ, 폭, ຄວາມຍາວ_ຄ່າ, ເຂົ້າລະຫັດ_ຄ່າ = struct.unpack('>HHHHi', 정확한값(ທາງ_ໄກ_ຄ່າ, 12))
                if ເຂົ້າລະຫັດ_ຄ່າ == -239:
                    assert 폭==0 and ຄວາມຍາວ_ຄ່າ==0, 'remote cursor must be hidden'
                    ລູກສອນເມົ້າ_ເຊື່ອງໄວ້ໄດ້[0]=True
                    continue
                assert ເຂົ້າລະຫັດ_ຄ່າ == 0 and 가로+폭 <= 너비 and ລວງຕັ້ງ_ຈັດຕໍາແຫນ່ງ+ຄວາມຍາວ_ຄ່າ <= 높이
                ການ_ແຕ້ມ_ຄ່າ.paste(Image.frombytes('RGB', (폭, ຄວາມຍາວ_ຄ່າ), 정확한값(ທາງ_ໄກ_ຄ່າ, 폭*ຄວາມຍາວ_ຄ່າ*4), 'raw', 'BGRX'), (가로, ລວງຕັ້ງ_ຈັດຕໍາແຫນ່ງ))
                ຫມວດ_ຄ່າ_9285603e += 폭*ຄວາມຍາວ_ຄ່າ
            if ຫມວດ_ຄ່າ_9285603e:
                assert ຫມວດ_ຄ່າ_9285603e == 너비*높이, ຫມວດ_ຄ່າ_9285603e
                return ການ_ແຕ້ມ_ຄ່າ

    def ເຊັກເງິນ_ເປ_ລ(ຈຸດປະສານ_ຄ່າ, 색):
        마감 = time.monotonic()+10
        while True:
            ການ_ແຕ້ມ_ຄ່າ = ບິດແມັບ_ຮູບ()
            if ການ_ແຕ້ມ_ຄ່າ.getpixel(ຈຸດປະສານ_ຄ່າ) == 색: return ການ_ແຕ້ມ_ຄ່າ
            if time.monotonic() > 마감: raise AssertionError((ຈຸດປະສານ_ຄ່າ, ການ_ແຕ້ມ_ຄ່າ.getpixel(ຈຸດປະສານ_ຄ່າ), 색))

    def ໂອນອອກ_ໄຟລ໌(ຊື່, ຂໍ້ມູນ): ໂອນ_ຄ່າ.storbinary('STOR '+ຊື່, io.BytesIO(ຂໍ້ມູນ))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+ຂະ_ຫນາດ_ຂໍ້ຄວາມ+' RGB32').encode() in ບັນທຶກ_ແຖວ
        print('BOOT:', ຂະ_ຫນາດ_ຂໍ້ຄວາມ, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', ບັນທຶກ_ແຖວ).group(1))
        ທາງ_ໄກ_ຄ່າ = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(ທາງ_ໄກ_ຄ່າ, 12) == b'RFB 003.008\n'; ທາງ_ໄກ_ຄ່າ.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(ທາງ_ໄກ_ຄ່າ, 정확한값(ທາງ_ໄກ_ຄ່າ, 1)[0]); ທາງ_ໄກ_ຄ່າ.sendall(b'\x01')
        assert 정확한값(ທາງ_ໄກ_ຄ່າ, 4) == b'\0'*4; ທາງ_ໄກ_ຄ່າ.sendall(b'\x01')
        초기 = 정확한값(ທາງ_ໄກ_ຄ່າ, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(ທາງ_ໄກ_ຄ່າ, struct.unpack('>I', 초기[20:])[0])
        ທາງ_ໄກ_ຄ່າ.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        ທາງ_ໄກ_ຄ່າ.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        ເຊັກເງິນ_ເປ_ລ((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for ງານ,_ in ຕົວ_ໃຊ້_ເລືອກ_a916db4e.select(.02):
                    ຂໍ້ມູນ=ງານ.fileobj.read(65536)
                    if ຂໍ້ມູນ:ບັນທຶກ_ແຖວ.extend(ຂໍ້ມູນ)
        ວິນໂດ=[12,48,568,360]
        def 크기확인():
            ຖັນ_ຄ່າ,ແຖວ_ຄ່າ=(ວິນໂດ[2]-24)//8,(ວິນໂດ[3]-56)//16
            ຂໍ້ຄວາມ=ເຊລ('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(ຖັນ_ຄ່າ,ແຖວ_ຄ່າ) in ຂໍ້ຄວາມ,ຂໍ້ຄວາມ
            # ຕົວ_ຈິງ_ຂໍ້ມູນ ວິນໂດ 테두리: 단지 ຂະ_ຫນາດ ຄິວຣີ_ຄ່າ 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            ເຊັກເງິນ_ເປ_ລ((ວິນໂດ[0],ວິນໂດ[1]),(32,80,144))
            ການ_ແຕ້ມ_ຄ່າ=ເຊັກເງິນ_ເປ_ລ((ວິນໂດ[0]+ວິນໂດ[2]-1,ວິນໂດ[1]+ວິນໂດ[3]-1),(39,49,64))
            return ການ_ແຕ້ມ_ຄ່າ
        def 모서리(방향):
            return (ວິນໂດ[0]+(3 if 방향 in (1,3) else ວິນໂດ[2]-4),ວິນໂດ[1]+(3 if 방향<=2 else ວິນໂດ[3]-4))
        def ປ່ຽນຂະຫນາດ_ລາກ(방향,차이,ປຸ່ມ=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            ເຊັກເງິນ_ເປ_ລ(흰점,(255,255,255))
            가리키기(가,세,ປຸ່ມ)
            끝가=max(0,min(너비-1,가+차이[0]));ຈົບ_ລວງຕັ້ງ=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,ຈົບ_ລວງຕັ້ງ,ປຸ່ມ);가리키기(끝가,ຈົບ_ລວງຕັ້ງ,0);숨고르기()
            if ປຸ່ມ==1:
                왼,위,폭,ຄວາມຍາວ_ຄ່າ=ວິນໂດ;오른,아래=왼+폭,위+ຄວາມຍາວ_ຄ່າ
                if 방향 in (1,3):왼=max(0,min(오른-360,왼+끝가-가))
                else:오른=max(왼+360,min(너비,오른+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+ຈົບ_ລວງຕັ້ງ-세))
                else:아래=max(위+216,min(높이,아래+ຈົບ_ລວງຕັ້ງ-세))
                ວິນໂດ[:]=[왼,위,오른-왼,아래-위]
        크기확인();assert ລູກສອນເມົ້າ_ເຊື່ອງໄວ້ໄດ້[0]
        ປ່ຽນຂະຫນາດ_ລາກ(4,(-100,-60),4);크기확인() # 오른쪽 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            ປ່ຽນຂະຫນາດ_ລາກ(방향,차이);크기확인()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        ສົ່ງ_ຂໍ້ຄວາມ("echo '"+긴글+"'");숨고르기()
        ປ່ຽນຂະຫນາດ_ລາກ(4,(-1000,-1000));assert ວິນໂດ[2:]==[360,216]
        ປ່ຽນຂະຫນາດ_ລາກ(4,(너비,높이))
        ແລ່ນ=ສົ່ງ_ຂໍ້ຄວາມ('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),ແລ່ນ);크기확인()
        # vi가 ແກ້ໄຂ_ຄ່າ 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        ເຊລ('ftpd start')
        ໂອນ_ຄ່າ=ftplib.FTP();ໂອນ_ຄ່າ.encoding='utf-8';ໂອນ_ຄ່າ.connect('127.0.0.1',ຫມາຍເລກພອດ,timeout=20);ໂອນ_ຄ່າ.login()
        기다리기(b'NORMAL',ສົ່ງ_ຂໍ້ຄວາມ('vi /크기자료.txt\n'))
        기다리기(b'INSERT',ສົ່ງ_ຂໍ້ຄວາມ('i미저장 한글 ຂໍ້ມູນ\n'));숨고르기()
        ປ່ຽນຂະຫນາດ_ລາກ(4,(-너비,-높이))
        # ANSI ແຖວ_ຄ່າ 이동에 새 ແຖວ_ຄ່າ 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((ວິນໂດ[3]-56)//16)).encode() in ບັນທຶກ_ແຖວ[-4096:]
        ສົ່ງ_ຂໍ້ຄວາມ('작은 창에서도 이어 ຂຽນ\n');숨고르기()
        ປ່ຽນຂະຫນາດ_ລາກ(4,(너비,높이))
        ສົ່ງ_ຂໍ້ຄວາມ('큰 창에서도 이어 ຂຽນ\n');숨고르기()
        ກົດ_ປຸ່ມ(0xff1b);ກົດ_ປຸ່ມ(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',ສົ່ງ_ຂໍ້ຄວາມ(':wq\n'))
        ເນື້ອໃນ_ຄ່າ_cb0f2404=bytearray();ໂອນ_ຄ່າ.retrbinary('RETR 크기자료.txt',ເນື້ອໃນ_ຄ່າ_cb0f2404.extend)
        assert ເນື້ອໃນ_ຄ່າ_cb0f2404=='미저장 한글 ຂໍ້ມູນ\n작은 창에서도 이어 ຂຽນ\n큰 창에서도 이어 ຂຽນ\n'.encode(),ເນື້ອໃນ_ຄ່າ_cb0f2404
        크기확인().save(str(ມາດຕະການ_ທາງໂຄຈອນ/(ຂະ_ຫນາດ_ຂໍ້ຄວາມ+'-large.png')))
        # 두 번째 창은 ຄ່າທີ່ກໍານົດໄວ້ແລ້ວ ຂະ_ຫນາດ, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        ແລ່ນ=len(ບັນທຶກ_ແຖວ);ກົດ_ຄ່າ(70,16);기다리기(b'TERMINAL FOCUS 2',ແລ່ນ)
        assert 'TERMINAL SIZE 68x19' in ເຊລ('terminal size')
        ແລ່ນ=len(ບັນທຶກ_ແຖວ);ກົດ_ຄ່າ(180,16);기다리기(b'TERMINAL FOCUS 1',ແລ່ນ);크기확인()
        ປ່ຽນຂະຫນາດ_ລາກ(4,(-너비,-높이));크기확인().save(str(ມາດຕະການ_ທາງໂຄຈອນ/(ຂະ_ຫນາດ_ຂໍ້ຄວາມ+'-small.png')))
        # ຂະ_ຫນາດ ປ່ຽນ_ແປງ_ຄ່າ ກັບ_ຄືນ_ຄ່າ X 닫기도 새로운 오른쪽 가장자리를 사용한다.
        ແລ່ນ=len(ບັນທຶກ_ແຖວ);ກົດ_ຄ່າ(ວິນໂດ[0]+ວິນໂດ[2]-20,ວິນໂດ[1]+15);기다리기(b'TERMINAL FOCUS 2',ແລ່ນ)
        assert 'RESIZE CLOSED' in ເຊລ('echo RESIZE CLOSED')
        print('PASS:',ຂະ_ຫນາດ_ຂໍ້ຄວາມ,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if ໂອນ_ຄ່າ:ໂອນ_ຄ່າ.close()
        if ທາງ_ໄກ_ຄ່າ:ທາງ_ໄກ_ຄ່າ.close()
        if ຂະ_ບວນ_ການ_ຄ່າ.poll() is None:
            ຂະ_ບວນ_ການ_ຄ່າ.terminate()
            try:ຂະ_ບວນ_ການ_ຄ່າ.wait(timeout=8)
            except subprocess.TimeoutExpired:ຂະ_ບວນ_ການ_ຄ່າ.kill();ຂະ_ບວນ_ການ_ຄ່າ.wait()
        ຕົວ_ໃຊ້_ເລືອກ_a916db4e.close();ຂະ_ບວນ_ການ_ຄ່າ.stdout.close();(ມາດຕະການ_ທາງໂຄຈອນ/(ຂະ_ຫນາດ_ຂໍ້ຄວາມ+'.log')).write_bytes(ບັນທຶກ_ແຖວ)


def ແລ່ນ():
    ມາດຕະການ_ທາງໂຄຈອນ=ໂຄງ_ການ_ເລກຮາກ/'build/verification/resize';ມາດຕະການ_ທາງໂຄຈອນ.mkdir(parents=True,exist_ok=True)
    ບັນທຶກ_ແຖວ={'passed':False,'kernel_sha256':hashlib.sha256((ໂຄງ_ການ_ເລກຮາກ/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,ມາດຕະການ_ທາງໂຄຈອນ);ບັນທຶກ_ແຖວ['resolutions'].append([너비,높이])
        ບັນທຶກ_ແຖວ.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(ມາດຕະການ_ທາງໂຄຈອນ/'report.json').write_text(json.dumps(ບັນທຶກ_ແຖວ,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':ແລ່ນ()
