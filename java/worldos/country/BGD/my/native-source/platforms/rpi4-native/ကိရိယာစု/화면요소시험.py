#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from စက်မောင်း import စီမံကိန်းအမြစ်,အမိန့်

def လုပ်ဆောင်():
    ဦးတည်ရာတန်ဖိုးနေရာ=စီမံကိန်းအမြစ်/'build/verification/swing';ဦးတည်ရာတန်ဖိုးနေရာ.mkdir(parents=True,exist_ok=True)
    အတန်းလမ်းကြောင်း=စီမံကိန်းအမြစ်/'build/verification/new-java';အတန်းလမ်းကြောင်း.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(စီမံကိန်းအမြစ်/'dist/jkoros-native-korean.jar'),'-d',str(အတန်းလမ်းကြောင်း),str(စီမံကိန်းအမြစ်/'စမ်းသပ်မှု/Java/Swingစမ်းသပ်.java'),str(စီမံကိန်းအမြစ်/'စမ်းသပ်မှု/Java/ဟန်ဂုဝင်းစမ်းသပ်.java')])
    검증기록={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((စီမံကိန်းအမြစ်/'build/kernel8.img').read_bytes()).hexdigest()};မှတ်တမ်းမှတ်တမ်းတစ်ခု=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as လုပ်ဆောင်လမ်း:
        모의제어접속=Path(လုပ်ဆောင်လမ်း)/'qmp.sock'
        ဒေတာနေရာ=subprocess.Popen(အမိန့်()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        선택기=selectors.DefaultSelector();선택기.register(ဒေတာနေရာ.stdout,selectors.EVENT_READ)
        def ကိုင်တွယ်ရာဖြစ်ရပ်(စက္ကန့်ယူနစ်=.1):
            for 누름값,_ in 선택기.select(စက္ကန့်ယူနစ်):
                ဒုတိယတန်ဖိုး=누름값.fileobj.read(65536)
                if ဒုတိယတန်ဖိုး:မှတ်တမ်းမှတ်တမ်းတစ်ခု.extend(ဒုတိယတန်ဖိုး)
            assert b'PANIC:' not in မှတ်တမ်းမှတ်တမ်းတစ်ခု and b'HALTED' not in မှတ်တမ်းမှတ်တမ်းတစ်ခု,မှတ်တမ်းမှတ်တမ်းတစ်ခု[-2048:]
        def စောင့်(확인표시,လက်ရှိနေရာ,စက္ကန့်ယူနစ်=50):
            အဆုံးအရွေ့=time.monotonic()+စက္ကန့်ယူနစ်
            while 확인표시 not in မှတ်တမ်းမှတ်တမ်းတစ်ခု[လက်ရှိနေရာ:]:
                if time.monotonic()>အဆုံးအရွေ့ or ဒေတာနေရာ.poll() is not None:raise AssertionError(မှတ်တမ်းမှတ်တမ်းတစ်ခု[လက်ရှိနေရာ:].decode('utf-8','replace'))
                ကိုင်တွယ်ရာဖြစ်ရပ်()
            return bytes(မှတ်တမ်းမှတ်တမ်းတစ်ခု[လက်ရှိနေရာ:])
        def ပို့(ဒုတိယတန်ဖိုး,확인표시=b'jkoros-native> '):
            လက်ရှိနေရာ=len(မှတ်တမ်းမှတ်တမ်းတစ်ခု);ဒေတာနေရာ.stdin.write(ဒုတိယတန်ဖိုး);ဒေတာနေရာ.stdin.flush();return စောင့်(확인표시,လက်ရှိနေရာ)
        def အမိန့်ဝင်း(အက္ခရာစဉ်ဒေတာ):return ပို့((အက္ခရာစဉ်ဒေတာ+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def 바로가기(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def 누르기(xတည်နေရာအမှတ်,yတည်နေရာအမှတ်):return bytes([30,1,1,xတည်နေရာအမှတ်&255,xတည်နေရာအမှတ်>>8,yတည်နေရာအမှတ်&255,yတည်နေရာအမှတ်>>8,30,1,0,xတည်နေရာအမှတ်&255,xတည်နေရာအမှတ်>>8,yတည်နေရာအမှတ်&255,yတည်နေရာအမှတ်>>8])
        def အမိန့်နည်းစနစ်():
            ဒေတာနေရာ.stdin.write(b'\x1b');ဒေတာနေရာ.stdin.flush();အဆုံးအရွေ့=time.monotonic()+.2
            while time.monotonic()<အဆုံးအရွေ့:ကိုင်တွယ်ရာဖြစ်ရပ်(.03)
        try:
            စောင့်(b'jkoros-native> ',0)
            အမိန့်ဝင်း('terminal');ကိုင်တွယ်ရာဖြစ်ရပ်(.3)
            ဒေတာ=(စီမံကိန်းအမြစ်/'build/verification/new-java/Swingစမ်းသပ်.class').read_bytes()
            ပို့('load Swingစမ်းသပ်.class\n'.encode(),b'hex> ')
            for အစဉ်အမှတ် in range(0,len(ဒေတာ),64):ပို့(ဒေတာ[အစဉ်အမှတ်:အစဉ်အမှတ်+64].hex().encode()+b'\n',b'hex> ')
            ပို့(b'.\n')
            ပို့('java Swingစမ်းသပ်\n'.encode(),b'SWING READY')
            အဆုံးအရွေ့=time.monotonic()+3
            while time.monotonic()<အဆုံးအရွေ့:ကိုင်တွယ်ရာဖြစ်ရပ်(.1)
            # JFrame centered at (120,100), content at y=130.
            ပို့(누르기(200,210),b'',)  # focus JTextField
            ဒေတာနေရာ.stdin.write('누리'.encode());ဒေတာနေရာ.stdin.flush()
            အဆုံးအရွေ့=time.monotonic()+.3
            while time.monotonic()<အဆုံးအရွေ့:ကိုင်တွယ်ရာဖြစ်ရပ်(.05)
            ရလဒ်=ပို့(누르기(200,255),'SWING CLICK 이름누리'.encode())
            စောင့်(b'true',len(မှတ်တမ်းမှတ်တမ်းတစ်ခု)-len(ရလဒ်))
            ပို့(바로가기(1),b'TERMINAL FOCUS 2')
            ရလဒ်=အမိန့်ဝင်း('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in ရလဒ်
            ပို့(누르기(180,12),b'TERMINAL FOCUS 1')
            အဆုံးအရွေ့=time.monotonic()+.3
            while time.monotonic()<အဆုံးအရွေ့:ကိုင်တွယ်ရာဖြစ်ရပ်(.05)
            with socket.socket(socket.AF_UNIX) as အက္ခရာကုဒ်:
                အက္ခရာကုဒ်.settimeout(10);အက္ခရာကုဒ်.connect(str(모의제어접속))
                with အက္ခရာကုဒ်.makefile('rwb') as ဖိုင်အချက်:
                    json.loads(ဖိုင်အချက်.readline())
                    for တောင်းဆိုချက်တန်ဖိုး in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(ဦးတည်ရာတန်ဖိုးနေရာ/'native-swing.png'),'format':'png'}}):
                        ဖိုင်အချက်.write((json.dumps(တောင်းဆိုချက်တန်ဖိုး)+'\n').encode());ဖိုင်အချက်.flush()
                        while True:
                            ပြန်ပေးတန်ဖိုး=json.loads(ဖိုင်အချက်.readline())
                            if 'error' in ပြန်ပေးတန်ဖိုး:raise AssertionError(ပြန်ပေးတန်ဖိုး)
                            if 'return' in ပြန်ပေးတန်ဖိုး:break
            ပို့(누르기(505,115))
            အမိန့်ဝင်း('echo SWING_CLOSED_OK')
            ဒေတာ=(အတန်းလမ်းကြောင်း/'ဟန်ဂုဝင်းစမ်းသပ်.class').read_bytes()
            ပို့('load ဟန်ဂုဝင်းစမ်းသပ်.class\n'.encode(),b'hex> ')
            for အစဉ်အမှတ် in range(0,len(ဒေတာ),64):ပို့(ဒေတာ[အစဉ်အမှတ်:အစဉ်အမှတ်+64].hex().encode()+b'\n',b'hex> ')
            ပို့(b'.\n')
            ပို့('java ဟန်ဂုဝင်းစမ်းသပ်\n'.encode(),b'KOREAN SWING READY')
            ပို့(누르기(200,255),'KOREAN SWING CLICK အမည်'.encode())
            ပို့(누르기(505,115))
            အမိန့်ဝင်း('echo KOREAN_SWING_CLOSED_OK')
            검증기록.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','မြန်မာ ဝင်း/ခလုတ်/လှုပ်ရှားမှုအသိပေးချက်/ဖြစ်ရပ်တန်းစီရာ directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if ဒေတာနေရာ.poll() is None:ဒေတာနေရာ.terminate()
            try:ဒေတာနေရာ.wait(timeout=5)
            except subprocess.TimeoutExpired:ဒေတာနေရာ.kill();ဒေတာနေရာ.wait()
            선택기.close();ဒေတာနေရာ.stdin.close();ဒေတာနေရာ.stdout.close();(ဦးတည်ရာတန်ဖိုးနေရာ/'serial.log').write_bytes(မှတ်တမ်းမှတ်တမ်းတစ်ခု);(ဦးတည်ရာတန်ဖိုးနေရာ/'report.json').write_text(json.dumps(검증기록,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':လုပ်ဆောင်()
