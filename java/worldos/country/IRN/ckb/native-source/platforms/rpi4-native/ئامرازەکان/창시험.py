#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from جێبەجێکردن_فەرمان import 기준,فەرمان

def ڕادان():
    목적위치=기준/'build/verification/windows';목적위치.mkdir(parents=True,exist_ok=True)
    ڕەواکردن_ڕاپۆرت={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest()};تۆمار_ڕزن=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        자료위치=subprocess.Popen(فەرمان()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        هەڵبژێرەر_a916db4e=selectors.DefaultSelector();هەڵبژێرەر_a916db4e.register(자료위치.stdout,selectors.EVENT_READ)
        def دەسک_پێشهات(초단위=.1):
            for 누름값,_ in هەڵبژێرەر_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:تۆمار_ڕزن.extend(둘째값)
            assert b'PANIC:' not in تۆمار_ڕزن and b'HALTED' not in تۆمار_ڕزن,تۆمار_ڕزن[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            دوایی_کردن_ئۆفسێت=time.monotonic()+초단위
            while 확인표시 not in تۆمار_ڕزن[현재위치:]:
                if time.monotonic()>دوایی_کردن_ئۆفسێت or 자료위치.poll() is not None:raise AssertionError(تۆمار_ڕزن[현재위치:].decode('utf-8','replace'))
                دەسک_پێشهات()
            return bytes(تۆمار_ڕزن[현재위치:])
        def ناردن(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(تۆمار_ڕزن);자료위치.stdin.write(둘째값);자료위치.stdin.flush();return 기다리기(확인표시,현재위치)
        def توێکڵ(رست_دەیتا):return ناردن((رست_دەیتا+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def کورتەڕێ_نرخ(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def کرته_کردن_دوگمه(پۆوتانی_x,세로좌표):return bytes([30,1,1,پۆوتانی_x&255,پۆوتانی_x>>8,세로좌표&255,세로좌표>>8,30,1,0,پۆوتانی_x&255,پۆوتانی_x>>8,세로좌표&255,세로좌표>>8])
        def فەرمان_دۆخ():
            자료위치.stdin.write(b'\x1b');자료위치.stdin.flush();دوایی_کردن_ئۆفسێت=time.monotonic()+.2
            while time.monotonic()<دوایی_کردن_ئۆفسێت:دەسک_پێشهات(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            توێکڵ('terminal');دەسک_پێشهات(.3)
            توێکڵ('mkdir first; cd first; export NAME=one')
            ناردن('vi 첫째.py\n'.encode(),b'NORMAL')
            ناردن('i값 = 21\nprint(نرخ * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            دوایی_کردن_ئۆفسێت=time.monotonic()+3
            while time.monotonic()<دوایی_کردن_ئۆفسێت:دەسک_پێشهات(.1)
            ناردن(کورتەڕێ_نرخ(1),b'TERMINAL FOCUS 2');دەسک_پێشهات(.2)
            assert b'/\r\n' in توێکڵ('pwd')
            توێکڵ('export NAME=two')
            ناردن('vi 둘째.txt\n'.encode(),b'NORMAL')
            ناردن('i두 번째 پەنجەرە\n'.encode(),b'INSERT')
            ناردن(کرته_کردن_دوگمه(180,12),b'TERMINAL FOCUS 1');دەسک_پێشهات(.2)
            فەرمان_دۆخ();ناردن(b':wq\r')
            assert b'one:/first' in توێکڵ('echo "$NAME:$PWD"')
            assert 'نرخ = 21\r\nprint(نرخ * 2)'.encode() in توێکڵ('cat 첫째.py')
            결과=توێکڵ('python 첫째.py');assert b'42\r\n' in 결과,결과
            # Close the first shell with its actual title-bar X; second editor resumes.
            ناردن(کرته_کردن_دوگمه(560,63),b'TERMINAL FOCUS 2');دەسک_پێشهات(.2)
            فەرمان_دۆخ();ناردن(b':wq\r')
            assert b'two:/' in توێکڵ('echo "$NAME:$PWD"')
            assert '두 번째 پەنجەرە'.encode() in توێکڵ('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            ناردن('vi 둘째.txt\n'.encode(),b'NORMAL');ناردن(b'xu',b'NORMAL')
            ناردن(b'iX',b'INSERT');فەرمان_دۆخ();ناردن(b':q\r',b'Unsaved')
            ناردن(b':q!\r');assert '두 번째 پەنجەرە'.encode() in توێکڵ('cat 둘째.txt')
            ناردن(کورتەڕێ_نرخ(1),b'TERMINAL FOCUS 1');دەسک_پێشهات(.2)
            ناردن(کورتەڕێ_نرخ(1),b'TERMINAL FOCUS 3');دەسک_پێشهات(.2)
            ناردن(کورتەڕێ_نرخ(1),b'TERMINAL FOCUS 4');دەسک_پێشهات(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            자료위치.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));자료위치.stdin.flush()
            توێکڵ('echo DRAGGED_OK')
            ناردن('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            ناردن('i저장하지 않은 دەیتا'.encode(),b'INSERT')
            ناردن(کرته_کردن_دوگمه(578,97),b'TERMINAL FOCUS 3');دەسک_پێشهات(.2)
            assert '버릴문서.txt'.encode() not in توێکڵ('ls')
            ناردن(کورتەڕێ_نرخ(1),b'TERMINAL FOCUS 4');دەسک_پێشهات(.2)
            توێکڵ('echo REUSED_WINDOW_OK')
            완료량=تۆمار_ڕزن.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            دوایی_کردن_ئۆفسێت=time.monotonic()+.3
            while time.monotonic()<دوایی_کردن_ئۆفسێت:دەسک_پێشهات(.05)
            with socket.socket(socket.AF_UNIX) as کۆدی_نووسە:
                کۆدی_نووسە.settimeout(10);کۆدی_نووسە.connect(str(모의제어접속))
                with کۆدی_نووسە.makefile('rwb') as فایل_تێنووسین:
                    json.loads(فایل_تێنووسین.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(목적위치/'four-terminals.png'),'format':'png'}}):
                        فایل_تێنووسین.write((json.dumps(요청값)+'\n').encode());فایل_تێنووسین.flush()
                        while True:
                            반환값=json.loads(فایل_تێنووسین.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(목적위치/'four-terminals.png')).convert('RGB')
            for جووتی_ڕێکخستن,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(جووتی_ڕێکخستن)==색상,(جووتی_ڕێکخستن,화소들.getpixel(جووتی_ڕێکخستن))
            توێکڵ('echo FOUR_WINDOWS_OK')
            ڕەواکردن_ڕاپۆرت.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if 자료위치.poll() is None:자료위치.terminate()
            try:자료위치.wait(timeout=5)
            except subprocess.TimeoutExpired:자료위치.kill();자료위치.wait()
            هەڵبژێرەر_a916db4e.close();자료위치.stdin.close();자료위치.stdout.close();(목적위치/'serial.log').write_bytes(تۆمار_ڕزن);(목적위치/'report.json').write_text(json.dumps(ڕەواکردن_ڕاپۆرت,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':ڕادان()
