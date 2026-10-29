#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from អនុវត្ត_ពាក្យបញ្ជា import បញ្ចាំង_ឬស,ពាក្យ_បញ្ជា

def រត់():
    ទិសដៅ_តំលៃ_កំណត់ទីតាំង=បញ្ចាំង_ឬស/'build/verification/swing';ទិសដៅ_តំលៃ_កំណត់ទីតាំង.mkdir(parents=True,exist_ok=True)
    ថ្នាក់_ផ្លូវ=បញ្ចាំង_ឬស/'build/verification/new-java';ថ្នាក់_ផ្លូវ.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(បញ្ចាំង_ឬស/'dist/jkoros-native-korean.jar'),'-d',str(ថ្នាក់_ផ្លូវ),str(បញ្ចាំង_ឬស/'시험/자바/스윙시험.java'),str(បញ្ចាំង_ឬស/'시험/자바/한글창시험.java')])
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
            ទិន្នន័យ=(បញ្ចាំង_ឬស/'build/verification/new-java/스윙시험.class').read_bytes()
            ផ្ញើ('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(ទិន្នន័យ),64):ផ្ញើ(ទិន្នន័យ[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            ផ្ញើ(b'.\n')
            ផ្ញើ('java 스윙시험\n'.encode(),b'SWING READY')
            បញ្ចប់_ការបែង_ភាគ=time.monotonic()+3
            while time.monotonic()<បញ្ចប់_ការបែង_ភាគ:ការកាន់កាប់_ព្រឹត្តិការណ៍(.1)
            # JFrame centered at (120,100), content at y=130.
            ផ្ញើ(ចុច_ប៊ូតុង(200,210),b'',)  # focus JTextField
            ទិន្នន័យ_កំណត់ទីតាំង.stdin.write('누리'.encode());ទិន្នន័យ_កំណត់ទីតាំង.stdin.flush()
            បញ្ចប់_ការបែង_ភាគ=time.monotonic()+.3
            while time.monotonic()<បញ្ចប់_ការបែង_ភាគ:ការកាន់កាប់_ព្រឹត្តិការណ៍(.05)
            ការវាស់វែង=ផ្ញើ(ចុច_ប៊ូតុង(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(កំណត់_ហេតុ_ថត)-len(ការវាស់វែង))
            ផ្ញើ(ផ្លូវកាត់_តំលៃ(1),b'TERMINAL FOCUS 2')
            ការវាស់វែង=셸('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in ការវាស់វែង
            ផ្ញើ(ចុច_ប៊ូតុង(180,12),b'TERMINAL FOCUS 1')
            បញ្ចប់_ការបែង_ភាគ=time.monotonic()+.3
            while time.monotonic()<បញ្ចប់_ការបែង_ភាគ:ការកាន់កាប់_ព្រឹត្តិការណ៍(.05)
            with socket.socket(socket.AF_UNIX) as កូដនៃតួអក្សរ:
                កូដនៃតួអក្សរ.settimeout(10);កូដនៃតួអក្សរ.connect(str(모의제어접속))
                with កូដនៃតួអក្សរ.makefile('rwb') as ឯកសារ_ការបញ្ចូល:
                    json.loads(ឯកសារ_ការបញ្ចូល.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(ទិសដៅ_តំលៃ_កំណត់ទីតាំង/'native-swing.png'),'format':'png'}}):
                        ឯកសារ_ការបញ្ចូល.write((json.dumps(요청값)+'\n').encode());ឯកសារ_ការបញ្ចូល.flush()
                        while True:
                            반환값=json.loads(ឯកសារ_ការបញ្ចូល.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            ផ្ញើ(ចុច_ប៊ូតុង(505,115))
            셸('echo SWING_CLOSED_OK')
            ទិន្នន័យ=(ថ្នាក់_ផ្លូវ/'한글창시험.class').read_bytes()
            ផ្ញើ('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(ទិន្នន័យ),64):ផ្ញើ(ទិន្នន័យ[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            ផ្ញើ(b'.\n')
            ផ្ញើ('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            ផ្ញើ(ចុច_ប៊ូតុង(200,255),'KOREAN SWING CLICK ឈ្មោះ'.encode())
            ផ្ញើ(ចុច_ប៊ូតុង(505,115))
            셸('echo KOREAN_SWING_CLOSED_OK')
            សុពលភាព_រាយការណ៍.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','한국어 វីនដូ/ប៊ូតុង/동작알림/ព្រឹត្តិការណ៍_ជួរ directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if ទិន្នន័យ_កំណត់ទីតាំង.poll() is None:ទិន្នន័យ_កំណត់ទីតាំង.terminate()
            try:ទិន្នន័យ_កំណត់ទីតាំង.wait(timeout=5)
            except subprocess.TimeoutExpired:ទិន្នន័យ_កំណត់ទីតាំង.kill();ទិន្នន័យ_កំណត់ទីតាំង.wait()
            អ្នកជ្រើសរើស_a916db4e.close();ទិន្នន័យ_កំណត់ទីតាំង.stdin.close();ទិន្នន័យ_កំណត់ទីតាំង.stdout.close();(ទិសដៅ_តំលៃ_កំណត់ទីតាំង/'serial.log').write_bytes(កំណត់_ហេតុ_ថត);(ទិសដៅ_តំលៃ_កំណត់ទីតាំង/'report.json').write_text(json.dumps(សុពលភាព_រាយការណ៍,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':រត់()
