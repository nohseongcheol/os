#!/usr/bin/env python3
"""dữLiệuThựcTế QEMU/VNC에서 thiếtBịCuối giáTrịGóc giáTrịKéo·conTrỏ·동적 giáTrịKýTự mụcÔ·giáTrịSửa giáTrịNộiDung 보존를 검사한다."""
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
from khungNhìnMànLàmViệc import giáTrịChínhXác
from thựcThiLệnh import gốcCâyDựÁn


def thửĐangĐổiCỡCửaSổ(giáTrịRộng, giáTrịCao, đườngDẫnKếtQuả):
    with socket.socket() as giáTrịTạm:
        giáTrịTạm.bind(('127.0.0.1', 0)); sốCổng = giáTrịTạm.getsockname()[1]
    vănBảnCỡ = '{}x{}'.format(giáTrịRộng, giáTrịCao)
    giáTrịTiếnTrình = subprocess.Popen(['python3', str(gốcCâyDựÁn/'CôngCụ/thựcThiLệnh.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(sốCổng), '--resolution', vănBảnCỡ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    BộChọn = selectors.DefaultSelector(); BộChọn.register(giáTrịTiếnTrình.stdout, selectors.EVENT_READ)
    bảnGhiNhậtKý = bytearray(); giáTrịTừXa = None; giáTrịChuyểnGiao = None; ẩnConTrỏ=[False]

    def đợi(hiệnGiáTrị, chạy=0):
        giáTrịHạnChót = time.monotonic() + 60
        while hiệnGiáTrị not in bảnGhiNhậtKý[chạy:]:
            if time.monotonic() > giáTrịHạnChót or giáTrịTiếnTrình.poll() is not None or b'HALTED' in bảnGhiNhậtKý or b'PANIC:' in bảnGhiNhậtKý:
                raise AssertionError(bảnGhiNhậtKý[chạy:].decode('utf-8', 'replace'))
            for sựKiện, _ in BộChọn.select(.1):
                DữLiệu = sựKiện.fileobj.read(65536)
                if DữLiệu: bảnGhiNhậtKý.extend(DữLiệu)
        return bảnGhiNhậtKý[chạy:].decode('utf-8', 'replace')

    def nútNhấnChuột(kýHiệu, làĐãNhấn=True): giáTrịTừXa.sendall(struct.pack('>BBHI', 4, int(làĐãNhấn), 0, kýHiệu))

    def gửiVănBản(vănBản):
        chạy = len(bảnGhiNhậtKý)
        for giáTrịKýTự in vănBản:
            kýHiệu = 0xff0d if giáTrịKýTự == '\n' else ord(giáTrịKýTự) if ord(giáTrịKýTự) < 256 else 0x1000000 | ord(giáTrịKýTự)
            nútNhấnChuột(kýHiệu); nútNhấnChuột(kýHiệu, False)
        return chạy

    def vỏLệnh(vănBản): return đợi(b'\r\n__RESIZE_DONE__\r\n', gửiVănBản(vănBản+'; echo __RESIZE_DONE__\n'))

    def tạiĐiểm(vịTríNgang, vịTríDọc, làĐãNhấn): giáTrịTừXa.sendall(struct.pack('>BBHH', 5, làĐãNhấn, vịTríNgang, vịTríDọc))

    def giáTrịNhấnChuột(vịTríNgang, vịTríDọc): tạiĐiểm(vịTríNgang, vịTríDọc, 1); tạiĐiểm(vịTríNgang, vịTríDọc, 0)

    def ảnhBảnĐồBit():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 dữLiệuThựcTế 너비를 쓴다.
        giáTrịTừXa.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, giáTrịRộng, giáTrịCao))
        HìnhVẽ = Image.new('RGB', (giáTrịRộng, giáTrịCao)); giáTrịVùng = 0
        while True:
            giáTrịLoại = giáTrịChínhXác(giáTrịTừXa, 1)[0]
            if giáTrịLoại == 2: continue
            if giáTrịLoại == 3:
                độDài = struct.unpack('>I', giáTrịChínhXác(giáTrịTừXa, 7)[3:])[0]; giáTrịChínhXác(giáTrịTừXa, độDài); continue
            assert giáTrịLoại == 0, giáTrịLoại
            sốLượngPhầnMục = struct.unpack('>H', giáTrịChínhXác(giáTrịTừXa, 3)[1:])[0]
            for _ in range(sốLượngPhầnMục):
                vịTríNgang, vịTríDọc, khoảngTrảiRộng, độDài, giáTrịBảngMã = struct.unpack('>HHHHi', giáTrịChínhXác(giáTrịTừXa, 12))
                if giáTrịBảngMã == -239:
                    assert khoảngTrảiRộng==0 and độDài==0, 'remote cursor must be hidden'
                    ẩnConTrỏ[0]=True
                    continue
                assert giáTrịBảngMã == 0 and vịTríNgang+khoảngTrảiRộng <= giáTrịRộng and vịTríDọc+độDài <= giáTrịCao
                HìnhVẽ.paste(Image.frombytes('RGB', (khoảngTrảiRộng, độDài), giáTrịChínhXác(giáTrịTừXa, khoảngTrảiRộng*độDài*4), 'raw', 'BGRX'), (vịTríNgang, vịTríDọc))
                giáTrịVùng += khoảngTrảiRộng*độDài
            if giáTrịVùng:
                assert giáTrịVùng == giáTrịRộng*giáTrịCao, giáTrịVùng
                return HìnhVẽ

    def kiểmTraĐiểmẢnh(giáTrịTọaĐộ, giáTrịMàu):
        giáTrịHạnChót = time.monotonic()+10
        while True:
            HìnhVẽ = ảnhBảnĐồBit()
            if HìnhVẽ.getpixel(giáTrịTọaĐộ) == giáTrịMàu: return HìnhVẽ
            if time.monotonic() > giáTrịHạnChót: raise AssertionError((giáTrịTọaĐộ, HìnhVẽ.getpixel(giáTrịTọaĐộ), giáTrịMàu))

    def cácTệpTảiLên(tên, DữLiệu): giáTrịChuyểnGiao.storbinary('STOR '+tên, io.BytesIO(DữLiệu))

    try:
        đợi(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+vănBảnCỡ+' RGB32').encode() in bảnGhiNhậtKý
        print('BOOT:', vănBảnCỡ, flush=True)
        sốTừXa = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', bảnGhiNhậtKý).group(1))
        giáTrịTừXa = socket.create_connection(('127.0.0.1', sốTừXa), timeout=20)
        assert giáTrịChínhXác(giáTrịTừXa, 12) == b'RFB 003.008\n'; giáTrịTừXa.sendall(b'RFB 003.008\n')
        assert 1 in giáTrịChínhXác(giáTrịTừXa, giáTrịChínhXác(giáTrịTừXa, 1)[0]); giáTrịTừXa.sendall(b'\x01')
        assert giáTrịChínhXác(giáTrịTừXa, 4) == b'\0'*4; giáTrịTừXa.sendall(b'\x01')
        trạngTháiBanĐầu = giáTrịChínhXác(giáTrịTừXa, 24); assert struct.unpack('>HH', trạngTháiBanĐầu[:4]) == (giáTrịRộng, giáTrịCao)
        giáTrịChínhXác(giáTrịTừXa, struct.unpack('>I', trạngTháiBanĐầu[20:])[0])
        giáTrịTừXa.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        giáTrịTừXa.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        kiểmTraĐiểmẢnh((giáTrịRộng-1, giáTrịCao-1), (24, 32, 48))
        def ngắnTạmDừng(giáTrịGiây=.25):
            phầnKết=time.monotonic()+giáTrịGiây
            while time.monotonic()<phầnKết:
                for sựKiện,_ in BộChọn.select(.02):
                    DữLiệu=sựKiện.fileobj.read(65536)
                    if DữLiệu:bảnGhiNhậtKý.extend(DữLiệu)
        cửaSổ=[12,48,568,360]
        def xácMinhCỡ():
            giáTrịCột,giáTrịHàng=(cửaSổ[2]-24)//8,(cửaSổ[3]-56)//16
            vănBản=vỏLệnh('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(giáTrịCột,giáTrịHàng) in vănBản,vănBản
            # dữLiệuThựcTế cửaSổ 테두리: 단지 cỡ giáTrịTruyVấn 값만 바뀐 것이 아닌지 확인한다.
            tạiĐiểm(giáTrịRộng-1,10,0);ngắnTạmDừng()
            kiểmTraĐiểmẢnh((cửaSổ[0],cửaSổ[1]),(32,80,144))
            HìnhVẽ=kiểmTraĐiểmẢnh((cửaSổ[0]+cửaSổ[2]-1,cửaSổ[1]+cửaSổ[3]-1),(39,49,64))
            return HìnhVẽ
        def giáTrịGóc(hướng):
            return (cửaSổ[0]+(3 if hướng in (1,3) else cửaSổ[2]-4),cửaSổ[1]+(3 if hướng<=2 else cửaSổ[3]-4))
        def kéoĐổiCỡ(hướng,giáTrịKhácBiệt,nút=1):
            toánHạngĐầuTiên,giáTrịBa=giáTrịGóc(hướng);tạiĐiểm(toánHạngĐầuTiên,giáTrịBa,0);ngắnTạmDừng()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            điểmẢnhTrắng=(toánHạngĐầuTiên-7 if hướng in (1,4) else toánHạngĐầuTiên+7,giáTrịBa-7)
            kiểmTraĐiểmẢnh(điểmẢnhTrắng,(255,255,255))
            tạiĐiểm(toánHạngĐầuTiên,giáTrịBa,nút)
            ngangKếtThúc=max(0,min(giáTrịRộng-1,toánHạngĐầuTiên+giáTrịKhácBiệt[0]));dọcKếtThúc=max(0,min(giáTrịCao-1,giáTrịBa+giáTrịKhácBiệt[1]))
            tạiĐiểm(ngangKếtThúc,dọcKếtThúc,nút);tạiĐiểm(ngangKếtThúc,dọcKếtThúc,0);ngắnTạmDừng()
            if nút==1:
                giáTrịTrái,giáTrịĐỉnh,khoảngTrảiRộng,độDài=cửaSổ;giáTrịPhải,giáTrịĐáy=giáTrịTrái+khoảngTrảiRộng,giáTrịĐỉnh+độDài
                if hướng in (1,3):giáTrịTrái=max(0,min(giáTrịPhải-360,giáTrịTrái+ngangKếtThúc-toánHạngĐầuTiên))
                else:giáTrịPhải=max(giáTrịTrái+360,min(giáTrịRộng,giáTrịPhải+ngangKếtThúc-toánHạngĐầuTiên))
                if hướng<=2:giáTrịĐỉnh=max(34,min(giáTrịĐáy-216,giáTrịĐỉnh+dọcKếtThúc-giáTrịBa))
                else:giáTrịĐáy=max(giáTrịĐỉnh+216,min(giáTrịCao,giáTrịĐáy+dọcKếtThúc-giáTrịBa))
                cửaSổ[:]=[giáTrịTrái,giáTrịĐỉnh,giáTrịPhải-giáTrịTrái,giáTrịĐáy-giáTrịĐỉnh]
        xácMinhCỡ();assert ẩnConTrỏ[0]
        kéoĐổiCỡ(4,(-100,-60),4);xácMinhCỡ() # phải 버튼은 크기를 바꾸지 않는다.
        for hướng,giáTrịKhácBiệt in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            kéoĐổiCỡ(hướng,giáTrịKhácBiệt);xácMinhCỡ()
        # giáTrịVào 중인 긴 vănBảnHangul 명령은 xuốngDòng/vịTríNgang 스크롤과 무관하게 그대로 실행된다.
        vănBảnDài='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        gửiVănBản("echo '"+vănBảnDài+"'");ngắnTạmDừng()
        kéoĐổiCỡ(4,(-1000,-1000));assert cửaSổ[2:]==[360,216]
        kéoĐổiCỡ(4,(giáTrịRộng,giáTrịCao))
        chạy=gửiVănBản('\n');đợi(('\r\n'+vănBảnDài+'\r\n').encode(),chạy);xácMinhCỡ()
        # vi가 giáTrịSửa 중에 MànHình 크기를 giáTrịThửLại 읽고, 저장하지 않은 한글도 유지한다.
        vỏLệnh('ftpd start')
        giáTrịChuyểnGiao=ftplib.FTP();giáTrịChuyểnGiao.encoding='utf-8';giáTrịChuyểnGiao.connect('127.0.0.1',sốCổng,timeout=20);giáTrịChuyểnGiao.login()
        đợi(b'NORMAL',gửiVănBản('vi /크기자료.txt\n'))
        đợi(b'INSERT',gửiVănBản('i미저장 한글 DữLiệu\n'));ngắnTạmDừng()
        kéoĐổiCỡ(4,(-giáTrịRộng,-giáTrịCao))
        # ANSI giáTrịHàng 이동에 새 giáTrịHàng 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((cửaSổ[3]-56)//16)).encode() in bảnGhiNhậtKý[-4096:]
        gửiVănBản('작은 창에서도 giáTrịSựTiếpDiễn ghi\n');ngắnTạmDừng()
        kéoĐổiCỡ(4,(giáTrịRộng,giáTrịCao))
        gửiVănBản('큰 창에서도 giáTrịSựTiếpDiễn ghi\n');ngắnTạmDừng()
        nútNhấnChuột(0xff1b);nútNhấnChuột(0xff1b,False);ngắnTạmDừng()
        đợi(b'jkoros-native> ',gửiVănBản(':wq\n'))
        giáTrịNộiDung=bytearray();giáTrịChuyểnGiao.retrbinary('RETR 크기자료.txt',giáTrịNộiDung.extend)
        assert giáTrịNộiDung=='미저장 한글 DữLiệu\n작은 창에서도 giáTrịSựTiếpDiễn ghi\n큰 창에서도 giáTrịSựTiếpDiễn ghi\n'.encode(),giáTrịNộiDung
        xácMinhCỡ().save(str(đườngDẫnKếtQuả/(vănBảnCỡ+'-large.png')))
        # 두 번째 창은 giáTrịMặcĐịnh cỡ, giáTrịThửLại phầnMụcĐầuTiên 창을 고르면 앞에서 바꾼 크기가 유지된다.
        chạy=len(bảnGhiNhậtKý);giáTrịNhấnChuột(70,16);đợi(b'TERMINAL FOCUS 2',chạy)
        assert 'TERMINAL SIZE 68x19' in vỏLệnh('terminal size')
        chạy=len(bảnGhiNhậtKý);giáTrịNhấnChuột(180,16);đợi(b'TERMINAL FOCUS 1',chạy);xácMinhCỡ()
        kéoĐổiCỡ(4,(-giáTrịRộng,-giáTrịCao));xácMinhCỡ().save(str(đườngDẫnKếtQuả/(vănBảnCỡ+'-small.png')))
        # cỡ đổiGiáTrị giáTrịLùi X 닫기도 새로운 phải 가장자리를 사용한다.
        chạy=len(bảnGhiNhậtKý);giáTrịNhấnChuột(cửaSổ[0]+cửaSổ[2]-20,cửaSổ[1]+15);đợi(b'TERMINAL FOCUS 2',chạy)
        assert 'RESIZE CLOSED' in vỏLệnh('echo RESIZE CLOSED')
        print('PASS:',vănBảnCỡ,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if giáTrịChuyểnGiao:giáTrịChuyểnGiao.close()
        if giáTrịTừXa:giáTrịTừXa.close()
        if giáTrịTiếnTrình.poll() is None:
            giáTrịTiếnTrình.terminate()
            try:giáTrịTiếnTrình.wait(timeout=8)
            except subprocess.TimeoutExpired:giáTrịTiếnTrình.kill();giáTrịTiếnTrình.wait()
        BộChọn.close();giáTrịTiếnTrình.stdout.close();(đườngDẫnKếtQuả/(vănBảnCỡ+'.log')).write_bytes(bảnGhiNhậtKý)


def chạy():
    đườngDẫnKếtQuả=gốcCâyDựÁn/'build/verification/resize';đườngDẫnKếtQuả.mkdir(parents=True,exist_ok=True)
    bảnGhiNhậtKý={'passed':False,'kernel_sha256':hashlib.sha256((gốcCâyDựÁn/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for giáTrịRộng,giáTrịCao in ((640,480),(1920,1080)):
            thửĐangĐổiCỡCửaSổ(giáTrịRộng,giáTrịCao,đườngDẫnKếtQuả);bảnGhiNhậtKý['resolutions'].append([giáTrịRộng,giáTrịCao])
        bảnGhiNhậtKý.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(đườngDẫnKếtQuả/'report.json').write_text(json.dumps(bảnGhiNhậtKý,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':chạy()
