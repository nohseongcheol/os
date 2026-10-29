#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from thựcThiLệnh import gốcCâyDựÁn,lệnh

def chạy():
    vịTríGiáTrịĐích=gốcCâyDựÁn/'build/verification/swing';vịTríGiáTrịĐích.mkdir(parents=True,exist_ok=True)
    đườngDẫnLớp=gốcCâyDựÁn/'build/verification/new-java';đườngDẫnLớp.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(gốcCâyDựÁn/'dist/jkoros-native-korean.jar'),'-d',str(đườngDẫnLớp),str(gốcCâyDựÁn/'KiểmThử/Java/ThửSwing.java'),str(gốcCâyDựÁn/'KiểmThử/Java/thửCửaSổHangul.java')])
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
            DữLiệu=(gốcCâyDựÁn/'build/verification/new-java/ThửSwing.class').read_bytes()
            gửi('load ThửSwing.class\n'.encode(),b'hex> ')
            for chỉSốThứBậc in range(0,len(DữLiệu),64):gửi(DữLiệu[chỉSốThứBậc:chỉSốThứBậc+64].hex().encode()+b'\n',b'hex> ')
            gửi(b'.\n')
            gửi('java ThửSwing\n'.encode(),b'SWING READY')
            độLệchKếtThúc=time.monotonic()+3
            while time.monotonic()<độLệchKếtThúc:sựKiệnThẻXửLý(.1)
            # JFrame centered at (120,100), content at y=130.
            gửi(nútNhấnChuột(200,210),b'',)  # focus JTextField
            vịTríDữLiệu.stdin.write('누리'.encode());vịTríDữLiệu.stdin.flush()
            độLệchKếtThúc=time.monotonic()+.3
            while time.monotonic()<độLệchKếtThúc:sựKiệnThẻXửLý(.05)
            kếtQuả=gửi(nútNhấnChuột(200,255),'SWING CLICK 이름누리'.encode())
            đợi(b'true',len(bảnGhiNhậtKý)-len(kếtQuả))
            gửi(giáTrịLốiTắt(1),b'TERMINAL FOCUS 2')
            kếtQuả=vỏLệnh('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in kếtQuả
            gửi(nútNhấnChuột(180,12),b'TERMINAL FOCUS 1')
            độLệchKếtThúc=time.monotonic()+.3
            while time.monotonic()<độLệchKếtThúc:sựKiệnThẻXửLý(.05)
            with socket.socket(socket.AF_UNIX) as mãKýTự:
                mãKýTự.settimeout(10);mãKýTự.connect(str(kếtNốiĐiềuKhiểnGiảLập))
                with mãKýTự.makefile('rwb') as mụcTệp:
                    json.loads(mụcTệp.readline())
                    for giáTrịYêuCầu in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(vịTríGiáTrịĐích/'native-swing.png'),'format':'png'}}):
                        mụcTệp.write((json.dumps(giáTrịYêuCầu)+'\n').encode());mụcTệp.flush()
                        while True:
                            giáTrịĐãTrảVề=json.loads(mụcTệp.readline())
                            if 'error' in giáTrịĐãTrảVề:raise AssertionError(giáTrịĐãTrảVề)
                            if 'return' in giáTrịĐãTrảVề:break
            gửi(nútNhấnChuột(505,115))
            vỏLệnh('echo SWING_CLOSED_OK')
            DữLiệu=(đườngDẫnLớp/'thửCửaSổHangul.class').read_bytes()
            gửi('load thửCửaSổHangul.class\n'.encode(),b'hex> ')
            for chỉSốThứBậc in range(0,len(DữLiệu),64):gửi(DữLiệu[chỉSốThứBậc:chỉSốThứBậc+64].hex().encode()+b'\n',b'hex> ')
            gửi(b'.\n')
            gửi('java thửCửaSổHangul\n'.encode(),b'KOREAN SWING READY')
            gửi(nútNhấnChuột(200,255),'KOREAN SWING CLICK tên'.encode())
            gửi(nútNhấnChuột(505,115))
            vỏLệnh('echo KOREAN_SWING_CLOSED_OK')
            báoCáoViệcThẩmĐịnh.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','tiếngViệt cửaSổ/nút/ThôngBáoHànhĐộng/HàngĐợiSựKiện directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if vịTríDữLiệu.poll() is None:vịTríDữLiệu.terminate()
            try:vịTríDữLiệu.wait(timeout=5)
            except subprocess.TimeoutExpired:vịTríDữLiệu.kill();vịTríDữLiệu.wait()
            BộChọn.close();vịTríDữLiệu.stdin.close();vịTríDữLiệu.stdout.close();(vịTríGiáTrịĐích/'serial.log').write_bytes(bảnGhiNhậtKý);(vịTríGiáTrịĐích/'report.json').write_text(json.dumps(báoCáoViệcThẩmĐịnh,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':chạy()
