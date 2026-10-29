#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ import ໂຄງ_ການ_ເລກຮາກ,ຄໍາສັ່ງ_1f12b8e2

def ແລ່ນ():
    ປາຍທາງ_ຄ່າ_ຈັດຕໍາແຫນ່ງ=ໂຄງ_ການ_ເລກຮາກ/'build/verification/windows';ປາຍທາງ_ຄ່າ_ຈັດຕໍາແຫນ່ງ.mkdir(parents=True,exist_ok=True)
    ໃຊ້ໄດ້_ລາຍງານ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((ໂຄງ_ການ_ເລກຮາກ/'build/kernel8.img').read_bytes()).hexdigest()};ບັນທຶກ_ແຖວ=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ=subprocess.Popen(ຄໍາສັ່ງ_1f12b8e2()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        ຕົວ_ໃຊ້_ເລືອກ_a916db4e=selectors.DefaultSelector();ຕົວ_ໃຊ້_ເລືອກ_a916db4e.register(ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ.stdout,selectors.EVENT_READ)
        def ຈັດ_ການ_ງານ(초단위=.1):
            for 누름값,_ in ຕົວ_ໃຊ້_ເລືອກ_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:ບັນທຶກ_ແຖວ.extend(둘째값)
            assert b'PANIC:' not in ບັນທຶກ_ແຖວ and b'HALTED' not in ບັນທຶກ_ແຖວ,ບັນທຶກ_ແຖວ[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            ຈົບ_ອອບເຊັດ=time.monotonic()+초단위
            while 확인표시 not in ບັນທຶກ_ແຖວ[현재위치:]:
                if time.monotonic()>ຈົບ_ອອບເຊັດ or ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ.poll() is not None:raise AssertionError(ບັນທຶກ_ແຖວ[현재위치:].decode('utf-8','replace'))
                ຈັດ_ການ_ງານ()
            return bytes(ບັນທຶກ_ແຖວ[현재위치:])
        def ສົ່ງ(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(ບັນທຶກ_ແຖວ);ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ.stdin.write(둘째값);ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ.stdin.flush();return 기다리기(확인표시,현재위치)
        def ເຊລ(ສະຕຣິງ_ຂໍ້ມູນ):return ສົ່ງ((ສະຕຣິງ_ຂໍ້ມູນ+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def ທາງລັດ_ຄ່າ(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def ກົດ_ປຸ່ມ(ຈຸດ_ພິ_ກັດ_x,ປຸ່ມ_Y_ຈຸດປະສານ):return bytes([30,1,1,ຈຸດ_ພິ_ກັດ_x&255,ຈຸດ_ພິ_ກັດ_x>>8,ປຸ່ມ_Y_ຈຸດປະສານ&255,ປຸ່ມ_Y_ຈຸດປະສານ>>8,30,1,0,ຈຸດ_ພິ_ກັດ_x&255,ຈຸດ_ພິ_ກັດ_x>>8,ປຸ່ມ_Y_ຈຸດປະສານ&255,ປຸ່ມ_Y_ຈຸດປະສານ>>8])
        def ຄໍາສັ່ງ_ໂຫມດ():
            ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ.stdin.write(b'\x1b');ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ.stdin.flush();ຈົບ_ອອບເຊັດ=time.monotonic()+.2
            while time.monotonic()<ຈົບ_ອອບເຊັດ:ຈັດ_ການ_ງານ(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            ເຊລ('terminal');ຈັດ_ການ_ງານ(.3)
            ເຊລ('mkdir first; cd first; export NAME=one')
            ສົ່ງ('vi 첫째.py\n'.encode(),b'NORMAL')
            ສົ່ງ('i값 = 21\nprint(ຄ່າ * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            ຈົບ_ອອບເຊັດ=time.monotonic()+3
            while time.monotonic()<ຈົບ_ອອບເຊັດ:ຈັດ_ການ_ງານ(.1)
            ສົ່ງ(ທາງລັດ_ຄ່າ(1),b'TERMINAL FOCUS 2');ຈັດ_ການ_ງານ(.2)
            assert b'/\r\n' in ເຊລ('pwd')
            ເຊລ('export NAME=two')
            ສົ່ງ('vi 둘째.txt\n'.encode(),b'NORMAL')
            ສົ່ງ('i두 번째 ວິນໂດ\n'.encode(),b'INSERT')
            ສົ່ງ(ກົດ_ປຸ່ມ(180,12),b'TERMINAL FOCUS 1');ຈັດ_ການ_ງານ(.2)
            ຄໍາສັ່ງ_ໂຫມດ();ສົ່ງ(b':wq\r')
            assert b'one:/first' in ເຊລ('echo "$NAME:$PWD"')
            assert 'ຄ່າ = 21\r\nprint(ຄ່າ * 2)'.encode() in ເຊລ('cat 첫째.py')
            ມາດຕະການ=ເຊລ('python 첫째.py');assert b'42\r\n' in ມາດຕະການ,ມາດຕະການ
            # Close the first shell with its actual title-bar X; second editor resumes.
            ສົ່ງ(ກົດ_ປຸ່ມ(560,63),b'TERMINAL FOCUS 2');ຈັດ_ການ_ງານ(.2)
            ຄໍາສັ່ງ_ໂຫມດ();ສົ່ງ(b':wq\r')
            assert b'two:/' in ເຊລ('echo "$NAME:$PWD"')
            assert '두 번째 ວິນໂດ'.encode() in ເຊລ('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            ສົ່ງ('vi 둘째.txt\n'.encode(),b'NORMAL');ສົ່ງ(b'xu',b'NORMAL')
            ສົ່ງ(b'iX',b'INSERT');ຄໍາສັ່ງ_ໂຫມດ();ສົ່ງ(b':q\r',b'Unsaved')
            ສົ່ງ(b':q!\r');assert '두 번째 ວິນໂດ'.encode() in ເຊລ('cat 둘째.txt')
            ສົ່ງ(ທາງລັດ_ຄ່າ(1),b'TERMINAL FOCUS 1');ຈັດ_ການ_ງານ(.2)
            ສົ່ງ(ທາງລັດ_ຄ່າ(1),b'TERMINAL FOCUS 3');ຈັດ_ການ_ງານ(.2)
            ສົ່ງ(ທາງລັດ_ຄ່າ(1),b'TERMINAL FOCUS 4');ຈັດ_ການ_ງານ(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ.stdin.flush()
            ເຊລ('echo DRAGGED_OK')
            ສົ່ງ('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            ສົ່ງ('i저장하지 않은 ຂໍ້ມູນ'.encode(),b'INSERT')
            ສົ່ງ(ກົດ_ປຸ່ມ(578,97),b'TERMINAL FOCUS 3');ຈັດ_ການ_ງານ(.2)
            assert '버릴문서.txt'.encode() not in ເຊລ('ls')
            ສົ່ງ(ທາງລັດ_ຄ່າ(1),b'TERMINAL FOCUS 4');ຈັດ_ການ_ງານ(.2)
            ເຊລ('echo REUSED_WINDOW_OK')
            완료량=ບັນທຶກ_ແຖວ.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            ຈົບ_ອອບເຊັດ=time.monotonic()+.3
            while time.monotonic()<ຈົບ_ອອບເຊັດ:ຈັດ_ການ_ງານ(.05)
            with socket.socket(socket.AF_UNIX) as ຈຸດ_ລະ_ຫັດ:
                ຈຸດ_ລະ_ຫັດ.settimeout(10);ຈຸດ_ລະ_ຫັດ.connect(str(모의제어접속))
                with ຈຸດ_ລະ_ຫັດ.makefile('rwb') as ຟາຍ_ເຂົ້າໃນ:
                    json.loads(ຟາຍ_ເຂົ້າໃນ.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(ປາຍທາງ_ຄ່າ_ຈັດຕໍາແຫນ່ງ/'four-terminals.png'),'format':'png'}}):
                        ຟາຍ_ເຂົ້າໃນ.write((json.dumps(요청값)+'\n').encode());ຟາຍ_ເຂົ້າໃນ.flush()
                        while True:
                            반환값=json.loads(ຟາຍ_ເຂົ້າໃນ.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(ປາຍທາງ_ຄ່າ_ຈັດຕໍາແຫນ່ງ/'four-terminals.png')).convert('RGB')
            for ຕົວປະສານຄູ່,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(ຕົວປະສານຄູ່)==색상,(ຕົວປະສານຄູ່,화소들.getpixel(ຕົວປະສານຄູ່))
            ເຊລ('echo FOUR_WINDOWS_OK')
            ໃຊ້ໄດ້_ລາຍງານ.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ.poll() is None:ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ.terminate()
            try:ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ.wait(timeout=5)
            except subprocess.TimeoutExpired:ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ.kill();ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ.wait()
            ຕົວ_ໃຊ້_ເລືອກ_a916db4e.close();ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ.stdin.close();ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ.stdout.close();(ປາຍທາງ_ຄ່າ_ຈັດຕໍາແຫນ່ງ/'serial.log').write_bytes(ບັນທຶກ_ແຖວ);(ປາຍທາງ_ຄ່າ_ຈັດຕໍາແຫນ່ງ/'report.json').write_text(json.dumps(ໃຊ້ໄດ້_ລາຍງານ,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':ແລ່ນ()
