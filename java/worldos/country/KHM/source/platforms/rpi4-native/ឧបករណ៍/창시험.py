#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from អនុវត្ត_ពាក្យបញ្ជា import បញ្ចាំង_ឬស,ពាក្យ_បញ្ជា

def រត់():
    ទិសដៅ_តំលៃ_កំណត់ទីតាំង=បញ្ចាំង_ឬស/'build/verification/windows';ទិសដៅ_តំលៃ_កំណត់ទីតាំង.mkdir(parents=True,exist_ok=True)
    សុពលភាព_រាយការណ៍={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((បញ្ចាំង_ឬស/'build/kernel8.img').read_bytes()).hexdigest()};កំណត់_ហេតុ_ថត=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        ទិន្នន័យ_កំណត់ទីតាំង=subprocess.Popen(ពាក្យ_បញ្ជា()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        អ្នកជ្រើសរើស_a916db4e=selectors.DefaultSelector();អ្នកជ្រើសរើស_a916db4e.register(ទិន្នន័យ_កំណត់ទីតាំង.stdout,selectors.EVENT_READ)
        def ការកាន់កាប់_ព្រឹត្តិការណ៍(초단위=.1):
            for 누름값,_ in អ្នកជ្រើសរើស_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:កំណត់_ហេតុ_ថត.extend(둘째값)
            assert b'PANIC:' not in កំណត់_ហេតុ_ថត and b'HALTED' not in កំណត់_ហេតុ_ថត,កំណត់_ហេតុ_ថត[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            បញ្ចប់_ការបែង_ភាគ=time.monotonic()+초단위
            while 확인표시 not in កំណត់_ហេតុ_ថត[현재위치:]:
                if time.monotonic()>បញ្ចប់_ការបែង_ភាគ or ទិន្នន័យ_កំណត់ទីតាំង.poll() is not None:raise AssertionError(កំណត់_ហេតុ_ថត[현재위치:].decode('utf-8','replace'))
                ការកាន់កាប់_ព្រឹត្តិការណ៍()
            return bytes(កំណត់_ហេតុ_ថត[현재위치:])
        def ផ្ញើ(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(កំណត់_ហេតុ_ថត);ទិន្នន័យ_កំណត់ទីតាំង.stdin.write(둘째값);ទិន្នន័យ_កំណត់ទីតាំង.stdin.flush();return 기다리기(확인표시,현재위치)
        def 셸(សំនុំអក្សរ_ទិន្នន័យ):return ផ្ញើ((សំនុំអក្សរ_ទិន្នន័យ+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def ផ្លូវកាត់_តំលៃ(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def ចុច_ប៊ូតុង(កូអរដោណេ_x,ប៊ូតុង_Y_កូអរដោនេ):return bytes([30,1,1,កូអរដោណេ_x&255,កូអរដោណេ_x>>8,ប៊ូតុង_Y_កូអរដោនេ&255,ប៊ូតុង_Y_កូអរដោនេ>>8,30,1,0,កូអរដោណេ_x&255,កូអរដោណេ_x>>8,ប៊ូតុង_Y_កូអរដោនេ&255,ប៊ូតុង_Y_កូអរដោនេ>>8])
        def ពាក្យបញ្ជា_ម៉ូដ():
            ទិន្នន័យ_កំណត់ទីតាំង.stdin.write(b'\x1b');ទិន្នន័យ_កំណត់ទីតាំង.stdin.flush();បញ្ចប់_ការបែង_ភាគ=time.monotonic()+.2
            while time.monotonic()<បញ្ចប់_ការបែង_ភាគ:ការកាន់កាប់_ព្រឹត្តិការណ៍(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            셸('terminal');ការកាន់កាប់_ព្រឹត្តិការណ៍(.3)
            셸('mkdir first; cd first; export NAME=one')
            ផ្ញើ('vi 첫째.py\n'.encode(),b'NORMAL')
            ផ្ញើ('i값 = 21\nprint(តំលៃ * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            បញ្ចប់_ការបែង_ភាគ=time.monotonic()+3
            while time.monotonic()<បញ្ចប់_ការបែង_ភាគ:ការកាន់កាប់_ព្រឹត្តិការណ៍(.1)
            ផ្ញើ(ផ្លូវកាត់_តំលៃ(1),b'TERMINAL FOCUS 2');ការកាន់កាប់_ព្រឹត្តិការណ៍(.2)
            assert b'/\r\n' in 셸('pwd')
            셸('export NAME=two')
            ផ្ញើ('vi 둘째.txt\n'.encode(),b'NORMAL')
            ផ្ញើ('i두 번째 វីនដូ\n'.encode(),b'INSERT')
            ផ្ញើ(ចុច_ប៊ូតុង(180,12),b'TERMINAL FOCUS 1');ការកាន់កាប់_ព្រឹត្តិការណ៍(.2)
            ពាក្យបញ្ជា_ម៉ូដ();ផ្ញើ(b':wq\r')
            assert b'one:/first' in 셸('echo "$NAME:$PWD"')
            assert 'តំលៃ = 21\r\nprint(តំលៃ * 2)'.encode() in 셸('cat 첫째.py')
            ការវាស់វែង=셸('python 첫째.py');assert b'42\r\n' in ការវាស់វែង,ការវាស់វែង
            # Close the first shell with its actual title-bar X; second editor resumes.
            ផ្ញើ(ចុច_ប៊ូតុង(560,63),b'TERMINAL FOCUS 2');ការកាន់កាប់_ព្រឹត្តិការណ៍(.2)
            ពាក្យបញ្ជា_ម៉ូដ();ផ្ញើ(b':wq\r')
            assert b'two:/' in 셸('echo "$NAME:$PWD"')
            assert '두 번째 វីនដូ'.encode() in 셸('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            ផ្ញើ('vi 둘째.txt\n'.encode(),b'NORMAL');ផ្ញើ(b'xu',b'NORMAL')
            ផ្ញើ(b'iX',b'INSERT');ពាក្យបញ្ជា_ម៉ូដ();ផ្ញើ(b':q\r',b'Unsaved')
            ផ្ញើ(b':q!\r');assert '두 번째 វីនដូ'.encode() in 셸('cat 둘째.txt')
            ផ្ញើ(ផ្លូវកាត់_តំលៃ(1),b'TERMINAL FOCUS 1');ការកាន់កាប់_ព្រឹត្តិការណ៍(.2)
            ផ្ញើ(ផ្លូវកាត់_តំលៃ(1),b'TERMINAL FOCUS 3');ការកាន់កាប់_ព្រឹត្តិការណ៍(.2)
            ផ្ញើ(ផ្លូវកាត់_តំលៃ(1),b'TERMINAL FOCUS 4');ការកាន់កាប់_ព្រឹត្តិការណ៍(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            ទិន្នន័យ_កំណត់ទីតាំង.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));ទិន្នន័យ_កំណត់ទីតាំង.stdin.flush()
            셸('echo DRAGGED_OK')
            ផ្ញើ('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            ផ្ញើ('i저장하지 않은 ទិន្នន័យ'.encode(),b'INSERT')
            ផ្ញើ(ចុច_ប៊ូតុង(578,97),b'TERMINAL FOCUS 3');ការកាន់កាប់_ព្រឹត្តិការណ៍(.2)
            assert '버릴문서.txt'.encode() not in 셸('ls')
            ផ្ញើ(ផ្លូវកាត់_តំលៃ(1),b'TERMINAL FOCUS 4');ការកាន់កាប់_ព្រឹត្តិការណ៍(.2)
            셸('echo REUSED_WINDOW_OK')
            완료량=កំណត់_ហេតុ_ថត.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            បញ្ចប់_ការបែង_ភាគ=time.monotonic()+.3
            while time.monotonic()<បញ្ចប់_ការបែង_ភាគ:ការកាន់កាប់_ព្រឹត្តិការណ៍(.05)
            with socket.socket(socket.AF_UNIX) as កូដនៃតួអក្សរ:
                កូដនៃតួអក្សរ.settimeout(10);កូដនៃតួអក្សរ.connect(str(모의제어접속))
                with កូដនៃតួអក្សរ.makefile('rwb') as ឯកសារ_ការបញ្ចូល:
                    json.loads(ឯកសារ_ការបញ្ចូល.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(ទិសដៅ_តំលៃ_កំណត់ទីតាំង/'four-terminals.png'),'format':'png'}}):
                        ឯកសារ_ការបញ្ចូល.write((json.dumps(요청값)+'\n').encode());ឯកសារ_ការបញ្ចូល.flush()
                        while True:
                            반환값=json.loads(ឯកសារ_ការបញ្ចូល.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(ទិសដៅ_តំលៃ_កំណត់ទីតាំង/'four-terminals.png')).convert('RGB')
            for គូកូអរដោនេ,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(គូកូអរដោនេ)==색상,(គូកូអរដោនេ,화소들.getpixel(គូកូអរដោនេ))
            셸('echo FOUR_WINDOWS_OK')
            សុពលភាព_រាយការណ៍.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if ទិន្នន័យ_កំណត់ទីតាំង.poll() is None:ទិន្នន័យ_កំណត់ទីតាំង.terminate()
            try:ទិន្នន័យ_កំណត់ទីតាំង.wait(timeout=5)
            except subprocess.TimeoutExpired:ទិន្នន័យ_កំណត់ទីតាំង.kill();ទិន្នន័យ_កំណត់ទីតាំង.wait()
            អ្នកជ្រើសរើស_a916db4e.close();ទិន្នន័យ_កំណត់ទីតាំង.stdin.close();ទិន្នន័យ_កំណត់ទីតាំង.stdout.close();(ទិសដៅ_តំលៃ_កំណត់ទីតាំង/'serial.log').write_bytes(កំណត់_ហេតុ_ថត);(ទិសដៅ_តំលៃ_កំណត់ទីតាំង/'report.json').write_text(json.dumps(សុពលភាព_រាយការណ៍,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':រត់()
