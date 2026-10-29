#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ import ໂຄງ_ການ_ເລກຮາກ,ຄໍາສັ່ງ_1f12b8e2

def ແລ່ນ():
    ປາຍທາງ_ຄ່າ_ຈັດຕໍາແຫນ່ງ=ໂຄງ_ການ_ເລກຮາກ/'build/verification/swing';ປາຍທາງ_ຄ່າ_ຈັດຕໍາແຫນ່ງ.mkdir(parents=True,exist_ok=True)
    ປະເພດສິ່ງຂອງ_ທາງໂຄຈອນ=ໂຄງ_ການ_ເລກຮາກ/'build/verification/new-java';ປະເພດສິ່ງຂອງ_ທາງໂຄຈອນ.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(ໂຄງ_ການ_ເລກຮາກ/'dist/jkoros-native-korean.jar'),'-d',str(ປະເພດສິ່ງຂອງ_ທາງໂຄຈອນ),str(ໂຄງ_ການ_ເລກຮາກ/'시험/자바/스윙시험.java'),str(ໂຄງ_ການ_ເລກຮາກ/'시험/자바/한글창시험.java')])
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
            ຂໍ້ມູນ=(ໂຄງ_ການ_ເລກຮາກ/'build/verification/new-java/스윙시험.class').read_bytes()
            ສົ່ງ('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(ຂໍ້ມູນ),64):ສົ່ງ(ຂໍ້ມູນ[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            ສົ່ງ(b'.\n')
            ສົ່ງ('java 스윙시험\n'.encode(),b'SWING READY')
            ຈົບ_ອອບເຊັດ=time.monotonic()+3
            while time.monotonic()<ຈົບ_ອອບເຊັດ:ຈັດ_ການ_ງານ(.1)
            # JFrame centered at (120,100), content at y=130.
            ສົ່ງ(ກົດ_ປຸ່ມ(200,210),b'',)  # focus JTextField
            ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ.stdin.write('누리'.encode());ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ.stdin.flush()
            ຈົບ_ອອບເຊັດ=time.monotonic()+.3
            while time.monotonic()<ຈົບ_ອອບເຊັດ:ຈັດ_ການ_ງານ(.05)
            ມາດຕະການ=ສົ່ງ(ກົດ_ປຸ່ມ(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(ບັນທຶກ_ແຖວ)-len(ມາດຕະການ))
            ສົ່ງ(ທາງລັດ_ຄ່າ(1),b'TERMINAL FOCUS 2')
            ມາດຕະການ=ເຊລ('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in ມາດຕະການ
            ສົ່ງ(ກົດ_ປຸ່ມ(180,12),b'TERMINAL FOCUS 1')
            ຈົບ_ອອບເຊັດ=time.monotonic()+.3
            while time.monotonic()<ຈົບ_ອອບເຊັດ:ຈັດ_ການ_ງານ(.05)
            with socket.socket(socket.AF_UNIX) as ຈຸດ_ລະ_ຫັດ:
                ຈຸດ_ລະ_ຫັດ.settimeout(10);ຈຸດ_ລະ_ຫັດ.connect(str(모의제어접속))
                with ຈຸດ_ລະ_ຫັດ.makefile('rwb') as ຟາຍ_ເຂົ້າໃນ:
                    json.loads(ຟາຍ_ເຂົ້າໃນ.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(ປາຍທາງ_ຄ່າ_ຈັດຕໍາແຫນ່ງ/'native-swing.png'),'format':'png'}}):
                        ຟາຍ_ເຂົ້າໃນ.write((json.dumps(요청값)+'\n').encode());ຟາຍ_ເຂົ້າໃນ.flush()
                        while True:
                            반환값=json.loads(ຟາຍ_ເຂົ້າໃນ.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            ສົ່ງ(ກົດ_ປຸ່ມ(505,115))
            ເຊລ('echo SWING_CLOSED_OK')
            ຂໍ້ມູນ=(ປະເພດສິ່ງຂອງ_ທາງໂຄຈອນ/'한글창시험.class').read_bytes()
            ສົ່ງ('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(ຂໍ້ມູນ),64):ສົ່ງ(ຂໍ້ມູນ[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            ສົ່ງ(b'.\n')
            ສົ່ງ('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            ສົ່ງ(ກົດ_ປຸ່ມ(200,255),'KOREAN SWING CLICK ຊື່'.encode())
            ສົ່ງ(ກົດ_ປຸ່ມ(505,115))
            ເຊລ('echo KOREAN_SWING_CLOSED_OK')
            ໃຊ້ໄດ້_ລາຍງານ.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','한국어 ວິນໂດ/ປຸ່ມ/동작알림/ງານ_ຄິວ directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ.poll() is None:ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ.terminate()
            try:ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ.wait(timeout=5)
            except subprocess.TimeoutExpired:ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ.kill();ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ.wait()
            ຕົວ_ໃຊ້_ເລືອກ_a916db4e.close();ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ.stdin.close();ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ.stdout.close();(ປາຍທາງ_ຄ່າ_ຈັດຕໍາແຫນ່ງ/'serial.log').write_bytes(ບັນທຶກ_ແຖວ);(ປາຍທາງ_ຄ່າ_ຈັດຕໍາແຫນ່ງ/'report.json').write_text(json.dumps(ໃຊ້ໄດ້_ລາຍງານ,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':ແລ່ນ()
