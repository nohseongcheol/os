#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from आज्ञा_कार्यवाही_करा import प्रोजेक्ट_मूळ,आदेश

def सुरू_करा():
    गंतव्यस्थान_मूल्य_स्थान=प्रोजेक्ट_मूळ/'build/verification/windows';गंतव्यस्थान_मूल्य_स्थान.mkdir(parents=True,exist_ok=True)
    पडताळणी_अहवाल={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((प्रोजेक्ट_मूळ/'build/kernel8.img').read_bytes()).hexdigest()};लॉग_नोंद=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as कार्यरत_पथ:
        अनुकृती_नियंत्रण_कनेक्शन=Path(कार्यरत_पथ)/'qmp.sock'
        डेटा_स्थान=subprocess.Popen(आदेश()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(अनुकृती_नियंत्रण_कनेक्शन)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        निवडक_a916db4e=selectors.DefaultSelector();निवडक_a916db4e.register(डेटा_स्थान.stdout,selectors.EVENT_READ)
        def हाताळा_इव्हेंट(सेकंद_एकक=.1):
            for दाबलेले_मूल्य,_ in निवडक_a916db4e.select(सेकंद_एकक):
                दुसरे_मूल्य=दाबलेले_मूल्य.fileobj.read(65536)
                if दुसरे_मूल्य:लॉग_नोंद.extend(दुसरे_मूल्य)
            assert b'PANIC:' not in लॉग_नोंद and b'HALTED' not in लॉग_नोंद,लॉग_नोंद[-2048:]
        def प्रतीक्षाकरा(खूण,सध्याचे_स्थान,सेकंद_एकक=50):
            शेवट_करा_ऑफसेट=time.monotonic()+सेकंद_एकक
            while खूण not in लॉग_नोंद[सध्याचे_स्थान:]:
                if time.monotonic()>शेवट_करा_ऑफसेट or डेटा_स्थान.poll() is not None:raise AssertionError(लॉग_नोंद[सध्याचे_स्थान:].decode('utf-8','replace'))
                हाताळा_इव्हेंट()
            return bytes(लॉग_नोंद[सध्याचे_स्थान:])
        def पाठवा(दुसरे_मूल्य,खूण=b'jkoros-native> '):
            सध्याचे_स्थान=len(लॉग_नोंद);डेटा_स्थान.stdin.write(दुसरे_मूल्य);डेटा_स्थान.stdin.flush();return प्रतीक्षाकरा(खूण,सध्याचे_स्थान)
        def शेल(स्ट्रींग_डेटा):return पाठवा((स्ट्रींग_डेटा+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def शॉर्टकट_मूल्य(तिसरे_अनुक्रमणिका):return bytes([30,2,तिसरे_अनुक्रमणिका,0,0,0,0])
        def क्लिक_करा_बटण(आडवे_समन्वयीत,उभे_समन्वयीत):return bytes([30,1,1,आडवे_समन्वयीत&255,आडवे_समन्वयीत>>8,उभे_समन्वयीत&255,उभे_समन्वयीत>>8,30,1,0,आडवे_समन्वयीत&255,आडवे_समन्वयीत>>8,उभे_समन्वयीत&255,उभे_समन्वयीत>>8])
        def आज्ञा_मोड():
            डेटा_स्थान.stdin.write(b'\x1b');डेटा_स्थान.stdin.flush();शेवट_करा_ऑफसेट=time.monotonic()+.2
            while time.monotonic()<शेवट_करा_ऑफसेट:हाताळा_इव्हेंट(.03)
        try:
            प्रतीक्षाकरा(b'jkoros-native> ',0)
            शेल('terminal');हाताळा_इव्हेंट(.3)
            शेल('mkdir first; cd first; export NAME=one')
            पाठवा('vi पहिले_क्रमांक.py\n'.encode(),b'NORMAL')
            पाठवा('i값 = 21\nprint(मूल्य * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            शेवट_करा_ऑफसेट=time.monotonic()+3
            while time.monotonic()<शेवट_करा_ऑफसेट:हाताळा_इव्हेंट(.1)
            पाठवा(शॉर्टकट_मूल्य(1),b'TERMINAL FOCUS 2');हाताळा_इव्हेंट(.2)
            assert b'/\r\n' in शेल('pwd')
            शेल('export NAME=two')
            पाठवा('vi दुसरे_क्रमांक.txt\n'.encode(),b'NORMAL')
            पाठवा('i두 번째 विंडो\n'.encode(),b'INSERT')
            पाठवा(क्लिक_करा_बटण(180,12),b'TERMINAL FOCUS 1');हाताळा_इव्हेंट(.2)
            आज्ञा_मोड();पाठवा(b':wq\r')
            assert b'one:/first' in शेल('echo "$NAME:$PWD"')
            assert 'मूल्य = 21\r\nprint(मूल्य * 2)'.encode() in शेल('cat पहिले_क्रमांक.py')
            मोजमाप=शेल('python पहिले_क्रमांक.py');assert b'42\r\n' in मोजमाप,मोजमाप
            # Close the first shell with its actual title-bar X; second editor resumes.
            पाठवा(क्लिक_करा_बटण(560,63),b'TERMINAL FOCUS 2');हाताळा_इव्हेंट(.2)
            आज्ञा_मोड();पाठवा(b':wq\r')
            assert b'two:/' in शेल('echo "$NAME:$PWD"')
            assert '두 번째 विंडो'.encode() in शेल('cat दुसरे_क्रमांक.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            पाठवा('vi दुसरे_क्रमांक.txt\n'.encode(),b'NORMAL');पाठवा(b'xu',b'NORMAL')
            पाठवा(b'iX',b'INSERT');आज्ञा_मोड();पाठवा(b':q\r',b'Unsaved')
            पाठवा(b':q!\r');assert '두 번째 विंडो'.encode() in शेल('cat दुसरे_क्रमांक.txt')
            पाठवा(शॉर्टकट_मूल्य(1),b'TERMINAL FOCUS 1');हाताळा_इव्हेंट(.2)
            पाठवा(शॉर्टकट_मूल्य(1),b'TERMINAL FOCUS 3');हाताळा_इव्हेंट(.2)
            पाठवा(शॉर्टकट_मूल्य(1),b'TERMINAL FOCUS 4');हाताळा_इव्हेंट(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            डेटा_स्थान.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));डेटा_स्थान.stdin.flush()
            शेल('echo DRAGGED_OK')
            पाठवा('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            पाठवा('i저장하지 않은 डेटा'.encode(),b'INSERT')
            पाठवा(क्लिक_करा_बटण(578,97),b'TERMINAL FOCUS 3');हाताळा_इव्हेंट(.2)
            assert '버릴문서.txt'.encode() not in शेल('ls')
            पाठवा(शॉर्टकट_मूल्य(1),b'TERMINAL FOCUS 4');हाताळा_इव्हेंट(.2)
            शेल('echo REUSED_WINDOW_OK')
            पूर्णझालेले_रक्कम=लॉग_नोंद.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            प्रतीक्षाकरा(b'jkoros-native> ',पूर्णझालेले_रक्कम)
            # UART completion precedes the next QEMU display refresh.
            शेवट_करा_ऑफसेट=time.monotonic()+.3
            while time.monotonic()<शेवट_करा_ऑफसेट:हाताळा_इव्हेंट(.05)
            with socket.socket(socket.AF_UNIX) as वर्ण_कोड:
                वर्ण_कोड.settimeout(10);वर्ण_कोड.connect(str(अनुकृती_नियंत्रण_कनेक्शन))
                with वर्ण_कोड.makefile('rwb') as संचिका_प्रविष्टी:
                    json.loads(संचिका_प्रविष्टी.readline())
                    for विनंती_मूल्य in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(गंतव्यस्थान_मूल्य_स्थान/'four-terminals.png'),'format':'png'}}):
                        संचिका_प्रविष्टी.write((json.dumps(विनंती_मूल्य)+'\n').encode());संचिका_प्रविष्टी.flush()
                        while True:
                            परतलेले_मूल्य=json.loads(संचिका_प्रविष्टी.readline())
                            if 'error' in परतलेले_मूल्य:raise AssertionError(परतलेले_मूल्य)
                            if 'return' in परतलेले_मूल्य:break
            from PIL import Image
            चित्रबिंदू_यादी=Image.open(str(गंतव्यस्थान_मूल्य_स्थान/'four-terminals.png')).convert('RGB')
            for कोऑर्डीनेट_पेअर,पिक्सेल_रंग in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert चित्रबिंदू_यादी.getpixel(कोऑर्डीनेट_पेअर)==पिक्सेल_रंग,(कोऑर्डीनेट_पेअर,चित्रबिंदू_यादी.getpixel(कोऑर्डीनेट_पेअर))
            शेल('echo FOUR_WINDOWS_OK')
            पडताळणी_अहवाल.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if डेटा_स्थान.poll() is None:डेटा_स्थान.terminate()
            try:डेटा_स्थान.wait(timeout=5)
            except subprocess.TimeoutExpired:डेटा_स्थान.kill();डेटा_स्थान.wait()
            निवडक_a916db4e.close();डेटा_स्थान.stdin.close();डेटा_स्थान.stdout.close();(गंतव्यस्थान_मूल्य_स्थान/'serial.log').write_bytes(लॉग_नोंद);(गंतव्यस्थान_मूल्य_स्थान/'report.json').write_text(json.dumps(पडताळणी_अहवाल,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':सुरू_करा()
