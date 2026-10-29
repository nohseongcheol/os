#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from thựcThiLệnh import gốcCâyDựÁn,lệnh

def chạy():
    vịTríGiáTrịĐích=gốcCâyDựÁn/'build/verification/windows';vịTríGiáTrịĐích.mkdir(parents=True,exist_ok=True)
    báoCáoViệcThẩmĐịnh={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((gốcCâyDựÁn/'build/kernel8.img').read_bytes()).hexdigest()};bảnGhiNhậtKý=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as đườngDẫnĐangLàmViệc:
        kếtNốiĐiềuKhiểnGiảLập=Path(đườngDẫnĐangLàmViệc)/'qmp.sock'
        vịTríDữLiệu=subprocess.Popen(lệnh()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(kếtNốiĐiềuKhiểnGiảLập)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        BộChọn=selectors.DefaultSelector();BộChọn.register(vịTríDữLiệu.stdout,selectors.EVENT_READ)
        def sựKiệnThẻXửLý(đơnVịGiây=.1):
            for giáTrịĐãNhấn,_ in BộChọn.select(đơnVịGiây):
                giáTrịThứHai=giáTrịĐãNhấn.fileobj.read(65536)
                if giáTrịThứHai:bảnGhiNhậtKý.extend(giáTrịThứHai)
            assert b'PANIC:' not in bảnGhiNhậtKý and b'HALTED' not in bảnGhiNhậtKý,bảnGhiNhậtKý[-2048:]
        def đợi(dấuMốc,vịTríHiệnTại,đơnVịGiây=50):
            độLệchKếtThúc=time.monotonic()+đơnVịGiây
            while dấuMốc not in bảnGhiNhậtKý[vịTríHiệnTại:]:
                if time.monotonic()>độLệchKếtThúc or vịTríDữLiệu.poll() is not None:raise AssertionError(bảnGhiNhậtKý[vịTríHiệnTại:].decode('utf-8','replace'))
                sựKiệnThẻXửLý()
            return bytes(bảnGhiNhậtKý[vịTríHiệnTại:])
        def gửi(giáTrịThứHai,dấuMốc=b'jkoros-native> '):
            vịTríHiệnTại=len(bảnGhiNhậtKý);vịTríDữLiệu.stdin.write(giáTrịThứHai);vịTríDữLiệu.stdin.flush();return đợi(dấuMốc,vịTríHiệnTại)
        def vỏLệnh(dữLiệuChuỗi):return gửi((dữLiệuChuỗi+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def giáTrịLốiTắt(chỉSốThứBa):return bytes([30,2,chỉSốThứBa,0,0,0,0])
        def nútNhấnChuột(tọaĐộX,tọaĐộY):return bytes([30,1,1,tọaĐộX&255,tọaĐộX>>8,tọaĐộY&255,tọaĐộY>>8,30,1,0,tọaĐộX&255,tọaĐộX>>8,tọaĐộY&255,tọaĐộY>>8])
        def chếĐộLệnh():
            vịTríDữLiệu.stdin.write(b'\x1b');vịTríDữLiệu.stdin.flush();độLệchKếtThúc=time.monotonic()+.2
            while time.monotonic()<độLệchKếtThúc:sựKiệnThẻXửLý(.03)
        try:
            đợi(b'jkoros-native> ',0)
            vỏLệnh('terminal');sựKiệnThẻXửLý(.3)
            vỏLệnh('mkdir first; cd first; export NAME=one')
            gửi('vi thứBậcĐầuTiên.py\n'.encode(),b'NORMAL')
            gửi('i값 = 21\nprint(giáTrị * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            độLệchKếtThúc=time.monotonic()+3
            while time.monotonic()<độLệchKếtThúc:sựKiệnThẻXửLý(.1)
            gửi(giáTrịLốiTắt(1),b'TERMINAL FOCUS 2');sựKiệnThẻXửLý(.2)
            assert b'/\r\n' in vỏLệnh('pwd')
            vỏLệnh('export NAME=two')
            gửi('vi thứBậcThứHai.txt\n'.encode(),b'NORMAL')
            gửi('i두 번째 cửaSổ\n'.encode(),b'INSERT')
            gửi(nútNhấnChuột(180,12),b'TERMINAL FOCUS 1');sựKiệnThẻXửLý(.2)
            chếĐộLệnh();gửi(b':wq\r')
            assert b'one:/first' in vỏLệnh('echo "$NAME:$PWD"')
            assert 'giáTrị = 21\r\nprint(giáTrị * 2)'.encode() in vỏLệnh('cat thứBậcĐầuTiên.py')
            kếtQuả=vỏLệnh('python thứBậcĐầuTiên.py');assert b'42\r\n' in kếtQuả,kếtQuả
            # Close the first shell with its actual title-bar X; second editor resumes.
            gửi(nútNhấnChuột(560,63),b'TERMINAL FOCUS 2');sựKiệnThẻXửLý(.2)
            chếĐộLệnh();gửi(b':wq\r')
            assert b'two:/' in vỏLệnh('echo "$NAME:$PWD"')
            assert '두 번째 cửaSổ'.encode() in vỏLệnh('cat thứBậcThứHai.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            gửi('vi thứBậcThứHai.txt\n'.encode(),b'NORMAL');gửi(b'xu',b'NORMAL')
            gửi(b'iX',b'INSERT');chếĐộLệnh();gửi(b':q\r',b'Unsaved')
            gửi(b':q!\r');assert '두 번째 cửaSổ'.encode() in vỏLệnh('cat thứBậcThứHai.txt')
            gửi(giáTrịLốiTắt(1),b'TERMINAL FOCUS 1');sựKiệnThẻXửLý(.2)
            gửi(giáTrịLốiTắt(1),b'TERMINAL FOCUS 3');sựKiệnThẻXửLý(.2)
            gửi(giáTrịLốiTắt(1),b'TERMINAL FOCUS 4');sựKiệnThẻXửLý(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            vịTríDữLiệu.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));vịTríDữLiệu.stdin.flush()
            vỏLệnh('echo DRAGGED_OK')
            gửi('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            gửi('i저장하지 않은 DữLiệu'.encode(),b'INSERT')
            gửi(nútNhấnChuột(578,97),b'TERMINAL FOCUS 3');sựKiệnThẻXửLý(.2)
            assert '버릴문서.txt'.encode() not in vỏLệnh('ls')
            gửi(giáTrịLốiTắt(1),b'TERMINAL FOCUS 4');sựKiệnThẻXửLý(.2)
            vỏLệnh('echo REUSED_WINDOW_OK')
            lượngĐãHoànTất=bảnGhiNhậtKý.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            đợi(b'jkoros-native> ',lượngĐãHoànTất)
            # UART completion precedes the next QEMU display refresh.
            độLệchKếtThúc=time.monotonic()+.3
            while time.monotonic()<độLệchKếtThúc:sựKiệnThẻXửLý(.05)
            with socket.socket(socket.AF_UNIX) as mãKýTự:
                mãKýTự.settimeout(10);mãKýTự.connect(str(kếtNốiĐiềuKhiểnGiảLập))
                with mãKýTự.makefile('rwb') as mụcTệp:
                    json.loads(mụcTệp.readline())
                    for giáTrịYêuCầu in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(vịTríGiáTrịĐích/'four-terminals.png'),'format':'png'}}):
                        mụcTệp.write((json.dumps(giáTrịYêuCầu)+'\n').encode());mụcTệp.flush()
                        while True:
                            giáTrịĐãTrảVề=json.loads(mụcTệp.readline())
                            if 'error' in giáTrịĐãTrảVề:raise AssertionError(giáTrịĐãTrảVề)
                            if 'return' in giáTrịĐãTrảVề:break
            from PIL import Image
            danhSáchCácĐiểmẢnh=Image.open(str(vịTríGiáTrịĐích/'four-terminals.png')).convert('RGB')
            for cặpTọaĐộ,màuĐiểmẢnh in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert danhSáchCácĐiểmẢnh.getpixel(cặpTọaĐộ)==màuĐiểmẢnh,(cặpTọaĐộ,danhSáchCácĐiểmẢnh.getpixel(cặpTọaĐộ))
            vỏLệnh('echo FOUR_WINDOWS_OK')
            báoCáoViệcThẩmĐịnh.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if vịTríDữLiệu.poll() is None:vịTríDữLiệu.terminate()
            try:vịTríDữLiệu.wait(timeout=5)
            except subprocess.TimeoutExpired:vịTríDữLiệu.kill();vịTríDữLiệu.wait()
            BộChọn.close();vịTríDữLiệu.stdin.close();vịTríDữLiệu.stdout.close();(vịTríGiáTrịĐích/'serial.log').write_bytes(bảnGhiNhậtKý);(vịTríGiáTrịĐích/'report.json').write_text(json.dumps(báoCáoViệcThẩmĐịnh,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':chạy()
