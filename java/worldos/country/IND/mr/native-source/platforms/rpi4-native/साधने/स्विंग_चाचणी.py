#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from आज्ञा_कार्यवाही_करा import प्रोजेक्ट_मूळ,आदेश

def सुरू_करा():
    गंतव्यस्थान_मूल्य_स्थान=प्रोजेक्ट_मूळ/'build/verification/swing';गंतव्यस्थान_मूल्य_स्थान.mkdir(parents=True,exist_ok=True)
    वर्ग_पथ=प्रोजेक्ट_मूळ/'build/verification/new-java';वर्ग_पथ.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(प्रोजेक्ट_मूळ/'dist/jkoros-native-korean.jar'),'-d',str(वर्ग_पथ),str(प्रोजेक्ट_मूळ/'चाचण्या/जावा/स्विंग_चाचणी_da272923.java'),str(प्रोजेक्ट_मूळ/'चाचण्या/जावा/हांगुल_विंडो_चाचणी.java')])
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
            डेटा=(प्रोजेक्ट_मूळ/'build/verification/new-java/स्विंग_चाचणी_da272923.class').read_bytes()
            पाठवा('load स्विंग_चाचणी_da272923.class\n'.encode(),b'hex> ')
            for क्रमांक_अनुक्रमणिका in range(0,len(डेटा),64):पाठवा(डेटा[क्रमांक_अनुक्रमणिका:क्रमांक_अनुक्रमणिका+64].hex().encode()+b'\n',b'hex> ')
            पाठवा(b'.\n')
            पाठवा('java स्विंग_चाचणी_da272923\n'.encode(),b'SWING READY')
            शेवट_करा_ऑफसेट=time.monotonic()+3
            while time.monotonic()<शेवट_करा_ऑफसेट:हाताळा_इव्हेंट(.1)
            # JFrame centered at (120,100), content at y=130.
            पाठवा(क्लिक_करा_बटण(200,210),b'',)  # focus JTextField
            डेटा_स्थान.stdin.write('누리'.encode());डेटा_स्थान.stdin.flush()
            शेवट_करा_ऑफसेट=time.monotonic()+.3
            while time.monotonic()<शेवट_करा_ऑफसेट:हाताळा_इव्हेंट(.05)
            मोजमाप=पाठवा(क्लिक_करा_बटण(200,255),'SWING CLICK 이름누리'.encode())
            प्रतीक्षाकरा(b'true',len(लॉग_नोंद)-len(मोजमाप))
            पाठवा(शॉर्टकट_मूल्य(1),b'TERMINAL FOCUS 2')
            मोजमाप=शेल('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in मोजमाप
            पाठवा(क्लिक_करा_बटण(180,12),b'TERMINAL FOCUS 1')
            शेवट_करा_ऑफसेट=time.monotonic()+.3
            while time.monotonic()<शेवट_करा_ऑफसेट:हाताळा_इव्हेंट(.05)
            with socket.socket(socket.AF_UNIX) as वर्ण_कोड:
                वर्ण_कोड.settimeout(10);वर्ण_कोड.connect(str(अनुकृती_नियंत्रण_कनेक्शन))
                with वर्ण_कोड.makefile('rwb') as संचिका_प्रविष्टी:
                    json.loads(संचिका_प्रविष्टी.readline())
                    for विनंती_मूल्य in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(गंतव्यस्थान_मूल्य_स्थान/'native-swing.png'),'format':'png'}}):
                        संचिका_प्रविष्टी.write((json.dumps(विनंती_मूल्य)+'\n').encode());संचिका_प्रविष्टी.flush()
                        while True:
                            परतलेले_मूल्य=json.loads(संचिका_प्रविष्टी.readline())
                            if 'error' in परतलेले_मूल्य:raise AssertionError(परतलेले_मूल्य)
                            if 'return' in परतलेले_मूल्य:break
            पाठवा(क्लिक_करा_बटण(505,115))
            शेल('echo SWING_CLOSED_OK')
            डेटा=(वर्ग_पथ/'हांगुल_विंडो_चाचणी.class').read_bytes()
            पाठवा('load हांगुल_विंडो_चाचणी.class\n'.encode(),b'hex> ')
            for क्रमांक_अनुक्रमणिका in range(0,len(डेटा),64):पाठवा(डेटा[क्रमांक_अनुक्रमणिका:क्रमांक_अनुक्रमणिका+64].hex().encode()+b'\n',b'hex> ')
            पाठवा(b'.\n')
            पाठवा('java हांगुल_विंडो_चाचणी\n'.encode(),b'KOREAN SWING READY')
            पाठवा(क्लिक_करा_बटण(200,255),'KOREAN SWING CLICK नाव'.encode())
            पाठवा(क्लिक_करा_बटण(505,115))
            शेल('echo KOREAN_SWING_CLOSED_OK')
            पडताळणी_अहवाल.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','मराठी विंडो/बटण/क्रिया_सूचना/इव्हेंट_रांग directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if डेटा_स्थान.poll() is None:डेटा_स्थान.terminate()
            try:डेटा_स्थान.wait(timeout=5)
            except subprocess.TimeoutExpired:डेटा_स्थान.kill();डेटा_स्थान.wait()
            निवडक_a916db4e.close();डेटा_स्थान.stdin.close();डेटा_स्थान.stdout.close();(गंतव्यस्थान_मूल्य_स्थान/'serial.log').write_bytes(लॉग_नोंद);(गंतव्यस्थान_मूल्य_स्थान/'report.json').write_text(json.dumps(पडताळणी_अहवाल,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':सुरू_करा()
