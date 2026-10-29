#!/usr/bin/env python3
"""tựThân 커널의 vỏLệnh, 프로세스 đầuRaĐầuVào, Unicode GUI 터미널을 dữLiệuThựcTế raspi4b에서 KiểmThử."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from thựcThiLệnh import gốcCâyDựÁn, lệnh


def chạy():
    đầuRa = gốcCâyDựÁn / 'build/verification/shell'; đầuRa.mkdir(parents=True, exist_ok=True)
    báoCáoViệcThẩmĐịnh = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((gốcCâyDựÁn / 'build/kernel8.img').read_bytes()).hexdigest()}
    bảnGhiDiễnTiến = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as đườngDẫnĐangLàmViệc:
        kếtNốiĐiềuKhiểnGiảLập = Path(đườngDẫnĐangLàmViệc) / 'qmp.sock'
        tiếnTrình = subprocess.Popen(lệnh()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(kếtNốiĐiềuKhiểnGiảLập)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        bộGiámSátSựSẵnSàng=selectors.DefaultSelector(); bộGiámSátSựSẵnSàng.register(tiếnTrình.stdout,selectors.EVENT_READ)
        def nhậnThôngĐiệp(dấuMốc, hếtGiờViệcThựcThi=45):
            DữLiệu=bytearray(); độLệchKếtThúc=time.monotonic()+hếtGiờViệcThựcThi
            while dấuMốc not in DữLiệu:
                if time.monotonic()>độLệchKếtThúc or tiếnTrình.poll() is not None: raise AssertionError('UART timeout/exit: '+DữLiệu.decode('utf-8','replace'))
                for giáTrịĐãNhấn,_ in bộGiámSátSựSẵnSàng.select(.1):
                    giáTrịĐoạn=giáTrịĐãNhấn.fileobj.read(4096)
                    if giáTrịĐoạn: DữLiệu.extend(giáTrịĐoạn); bảnGhiDiễnTiến.extend(giáTrịĐoạn)
                if b'PANIC:' in DữLiệu or b'FAIL ' in DữLiệu: raise AssertionError(DữLiệu)
            return DữLiệu.decode('utf-8','replace').replace('\r\n','\n')
        def gửi(DữLiệu, dấuMốc=b'jkoros-native> '):
            tiếnTrình.stdin.write(DữLiệu); tiếnTrình.stdin.flush(); return nhậnThôngĐiệp(dấuMốc)
        def vỏLệnh(dòng, *dựKiến):
            kếtQuả=gửi(dòng.encode()+b'\n')
            for giáTrị in dựKiến: assert giáTrị in kếtQuả, (dòng,giáTrị,kếtQuả)
            return kếtQuả
        def Tệp(tên):
            vănBản=vỏLệnh('hex '+tên,'HEX BEGIN','HEX END'); tìmKiếmKếtQuả=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',vănBản,re.S)
            DữLiệu=bytes.fromhex(''.join(tìmKiếmKếtQuả.group(2).split())); assert len(DữLiệu)==int(tìmKiếmKếtQuả.group(1)); return DữLiệu
        try:
            nhậnThôngĐiệp(b'jkoros-native> ')
            vỏLệnh('mkdir TácVụ; cd TácVụ; pwd','/TácVụ')
            vỏLệnh('mkdir 하위; echo "한글 DữLiệu 😀" > LờiChào.txt')
            assert Tệp('LờiChào.txt')=='한글 DữLiệu 😀\n'.encode()
            vỏLệnh('cp LờiChào.txt saoChépGiáTrị.txt; mv saoChépGiáTrị.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 DữLiệu 😀')
            vỏLệnh('cd 하위; cat ../LờiChào.txt; cat /TácVụ/LờiChào.txt; pwd','한글 DữLiệu 😀','/TácVụ/하위')
            vỏLệnh('cd ..; rmdir 하위; echo $?','1\n')
            vỏLệnh('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            vỏLệnh('cp LờiChào.txt LờiChào.txt; echo $?','1\n'); assert Tệp('LờiChào.txt')=='한글 DữLiệu 😀\n'.encode()
            vỏLệnh('export LờiChào=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/TácVụ','GOOD')
            assert b'BAD\n' not in Tệp('LờiChào.txt')
            vỏLệnh("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert Tệp('리터럴')=='$인사\n누리\n'.encode()
            vỏLệnh('echo one > giáTrịCâuLệnh; echo two >> giáTrịCâuLệnh; echo three >> giáTrịCâuLệnh')
            vỏLệnh('cat < giáTrịCâuLệnh | grep t | tee 추림 | wc -l','2\n'); assert Tệp('추림')==b'two\nthree\n'
            vỏLệnh('head -n 1 giáTrịCâuLệnh > giáTrịPhíaTrước; tail -n 1 giáTrịCâuLệnh > giáTrịLùi'); assert Tệp('앞')==b'one\n'; assert Tệp('뒤')==b'three\n'
            vỏLệnh('grep absent giáTrịCâuLệnh; echo $?','1\n')
            vỏLệnh('echo untouched > bảoVệGiáTrị')
            vỏLệnh('echo destroyed > bảoVệGiáTrị |','명령이 빠졌습니다'); assert Tệp('bảoVệGiáTrị')==b'untouched\n'
            vỏLệnh('echo "oops','따옴표가 닫히지 않았습니다')
            vỏLệnh('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            vỏLệnh('echo bad 2> bảoVệGiáTrị','번호를 지정한 Tệp mụcBộMôTả đầuRaĐầuVào chếĐộChuyển'); assert Tệp('bảoVệGiáTrị')==b'untouched\n'
            vỏLệnh('rm 빈파일 리터럴 giáTrịCâuLệnh 추림 giáTrịPhíaTrước giáTrịLùi bảoVệGiáTrị')
            báoCáoViệcThẩmĐịnh['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            vỏLệnh("python -c 'print(123)' | wc -c",'4\n')
            vỏLệnh("python -c 'print(456)' > ChươngTrình.txt"); assert Tệp('ChươngTrình.txt')==b'456\n'
            vỏLệnh("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            vỏLệnh("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < ChươngTrình.txt", "b'456\\n'", "b''")
            vỏLệnh("python -c 'print(\"x\"*17000)' | wc -c", 'lỗi -28')
            vỏLệnh('echo recovered | wc -c','10\n')
            vỏLệnh("python -c 'import jkoros; print(jkoros.read("+'"/TácVụ/ChươngTrình.txt"'+"))'",'456','exit 0')
            vỏLệnh('cd /; javac Hello.java','Compiled:','exit 0')
            vỏLệnh('java Hello > /TácVụ/Java.txt'); assert '안녕하세요'.encode() in Tệp('/TácVụ/Java.txt')
            vỏLệnh('cd TácVụ; echo "echo script > kếtQuảViệcThựcThi" > lệnh.sh; echo "false || echo recovered >> kếtQuảViệcThựcThi" >> lệnh.sh; sh lệnh.sh')
            assert Tệp('kếtQuảViệcThựcThi')==b'script\nrecovered\n'
            vỏLệnh('rm kếtQuảViệcThựcThi; echo "exit 7" > chươngTrìnhRa.sh; sh chươngTrìnhRa.sh; echo $?','7\n')
            vỏLệnh('rm chươngTrìnhRa.sh lệnh.sh ChươngTrình.txt Java.txt LờiChào.txt; cd /; rmdir TácVụ')
            báoCáoViệcThẩmĐịnh['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            vỏLệnh('echo history-proof','history-proof')
            kếtQuả=gửi(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert kếtQuả.count('history-proof')>=2, kếtQuả
            gửi(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            kếtQuả=gửi(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in kếtQuả, kếtQuả
            kếtQuả=gửi(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in kếtQuả,kếtQuả
            kếtQuả=gửi('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in kếtQuả,kếtQuả
            vănBảnDài='한글'*50
            kếtQuả=gửi(('echo '+vănBảnDài+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+vănBảnDài+'\r\njkoros-native> ').encode()); assert '\n'+vănBảnDài+'\n' in kếtQuả
            vỏLệnh('terminal','TERMINAL READY')
            vỏLệnh('clear')
            vỏLệnh('echo "한글 thiếtBịCuối ABC xyz 012 😀"','한글 thiếtBịCuối ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as máyKhách:
                máyKhách.settimeout(10); máyKhách.connect(str(kếtNốiĐiềuKhiểnGiảLập))
                with máyKhách.makefile('rwb') as giáTrịLuồng:
                    json.loads(giáTrịLuồng.readline())
                    def gọiThựcHiện(tên,mảngĐốiSố=None):
                        thôngĐiệpMạng={'execute':tên}
                        if mảngĐốiSố: thôngĐiệpMạng['arguments']=mảngĐốiSố
                        giáTrịLuồng.write((json.dumps(thôngĐiệpMạng)+'\n').encode()); giáTrịLuồng.flush()
                        while True:
                            lờiĐáp=json.loads(giáTrịLuồng.readline())
                            if 'error' in lờiĐáp: raise AssertionError(lờiĐáp)
                            if 'return' in lờiĐáp: return lờiĐáp['return']
                    gọiThựcHiện('qmp_capabilities')
                    ảnh=đầuRa/'terminal.ppm'; gọiThựcHiện('screendump',{'filename':str(ảnh),'format':'ppm'})
                    gọiThựcHiện('screendump',{'filename':str(đầuRa/'terminal.png'),'format':'png'})
                    DữLiệu=ảnh.read_bytes().split(b'\n',3)[3]
                    def điểmẢnh(tọaĐộX,tọaĐộY): return tuple(DữLiệu[(tọaĐộY*640+tọaĐộX)*3:(tọaĐộY*640+tọaĐộX)*3+3])
                    assert điểmẢnh(12,48)==(32,80,144),điểmẢnh(12,48)
                    assert len(set(điểmẢnh(tọaĐộX,tọaĐộY) for tọaĐộY in range(100,116) for tọaĐộX in range(24,56)))>1,'Hangul glyphs missing'
                    vỏLệnh('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    vỏLệnh("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    gọiThựcHiện('screendump',{'filename':str(ảnh),'format':'ppm'})
                    dữLiệuĐãPhụcHồi=ảnh.read_bytes().split(b'\n',3)[3]
                    assert tuple(dữLiệuĐãPhụcHồi[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    vỏLệnh('echo test > visible.txt; cat visible.txt','test')
                    for chỉSốThứBậc in range(27): vỏLệnh('echo scroll-'+str(chỉSốThứBậc),'scroll-'+str(chỉSốThứBậc))
                    gửi(b'\x1b[5~\x1b[6~\n')
                    gọiThựcHiện('screendump',{'filename':str(đầuRa/'terminal-scroll.png'),'format':'png'})
                    kếtQuả=gửi(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in kếtQuả,kếtQuả
                    vỏLệnh('rm visible.txt')
                    gọiThựcHiện('quit')
            tiếnTrình.wait(timeout=5)
            báoCáoViệcThẩmĐịnh['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            báoCáoViệcThẩmĐịnh['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if tiếnTrình.poll() is None:
                tiếnTrình.terminate()
                try: tiếnTrình.wait(timeout=5)
                except subprocess.TimeoutExpired: tiếnTrình.kill(); tiếnTrình.wait()
            bộGiámSátSựSẵnSàng.close(); tiếnTrình.stdin.close(); tiếnTrình.stdout.close()
            (đầuRa/'serial.log').write_bytes(bảnGhiDiễnTiến)
            (đầuRa/'report.json').write_text(json.dumps(báoCáoViệcThẩmĐịnh,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': chạy()
