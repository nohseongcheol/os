#!/usr/bin/env python3
"""Exercise the installed Remmina in an isolated X display and D-Bus session.

Needs Remmina's VNC plugin, xdotool, Xvfb (or the existing ARM64 Xvfb rootfs
and qemu-aarch64), dbus-run-session, and ImageMagick import. Never uses :0.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import selectors
import shutil
import subprocess
import tempfile
import time
from ดําเนินการ_คําสั่ง import แสดง_ราก


def เรียกใช้งาน():
    เมตริก_ข้อมูล=แสดง_ราก/'build/verification/remmina';เมตริก_ข้อมูล.mkdir(parents=True,exist_ok=True)
    การตรวจสอบความถูกต้อง_รายงาน={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((แสดง_ราก/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];ตัวเลือก_582fe3b9=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            가상표시장치=shutil.which('Xvfb')
            if 가상표시장치: เซิร์ฟเวอร์_ค่า=[가상표시장치]
            else:
                뿌리파일계층=แสดง_ราก.parent/'rpi4/build/rootfs'
                เซิร์ฟเวอร์_ค่า=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def เรียกใช้งาน(อาร์กิวเมนต์_อาร์เรย์,สภาพแวดล้อม=None,**อาร์กิวเมนต์ที่ระบุชื่อ):
                บันทึก_สถิติ=(เมตริก_ข้อมูล/('process-%d.log'%len(기록들))).open('wb');기록들.append(บันทึก_สถิติ)
                ข้อมูล_ตําแหน่ง=subprocess.Popen(อาร์กิวเมนต์_อาร์เรย์,env=สภาพแวดล้อม,stdout=บันทึก_สถิติ,stderr=subprocess.STDOUT,**อาร์กิวเมนต์ที่ระบุชื่อ)
                실행과정들.append(ข้อมูล_ตําแหน่ง);return ข้อมูล_ตําแหน่ง
            สภาพแวดล้อม=dict(os.environ)
            for ชื่อ in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):สภาพแวดล้อม.pop(ชื่อ,None)
            สภาพแวดล้อม.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(개수 for 개수 in range(80,200) if not Path('/tmp/.X11-unix/X'+str(개수)).exists() and not Path('/tmp/.X%d-lock'%개수).exists())
            สภาพแวดล้อม['DISPLAY']=':'+str(수치)
            จอแสดงผล=เรียกใช้งาน(เซิร์ฟเวอร์_ค่า+[สภาพแวดล้อม['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],สภาพแวดล้อม=สภาพแวดล้อม)
            วันครบกําหนด_เวลา=time.monotonic()+30
            while True:
                assert จอแสดงผล.poll() is None and time.monotonic()<วันครบกําหนด_เวลา,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=สภาพแวดล้อม,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            ผู้เยี่ยมชม=subprocess.Popen(['python3',str(แสดง_ราก/'เครื่องมือ/ดําเนินการ_คําสั่ง.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(ผู้เยี่ยมชม);ตัวเลือก_582fe3b9.register(ผู้เยี่ยมชม.stdout,selectors.EVENT_READ)
            def 기다리기(มาร์กเกอร์,ออฟเซต_ค่า=0):
                วันครบกําหนด_เวลา=time.monotonic()+45
                while มาร์กเกอร์ not in 직렬입출력[ออฟเซต_ค่า:]:
                    assert ผู้เยี่ยมชม.poll() is None and time.monotonic()<วันครบกําหนด_เวลา,직렬입출력[ออฟเซต_ค่า:].decode('utf-8','replace')
                    for 누름값,_ in ตัวเลือก_582fe3b9.select(.1):
                        ข้อมูล=누름값.fileobj.read(65536)
                        if ข้อมูล:직렬입출력.extend(ข้อมูล)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            หมายเลขพอร์ต=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            โปรไฟล์=작업경로/'test.remmina'
            โปรไฟล์.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%หมายเลขพอร์ต)
            เรียกใช้งาน(['dbus-run-session','--','remmina','-c',str(โปรไฟล์)],สภาพแวดล้อม=สภาพแวดล้อม,start_new_session=True)
            def 가상입력도구(*อาร์กิวเมนต์_อาร์เรย์):return subprocess.check_output(['xdotool']+list(อาร์กิวเมนต์_อาร์เรย์),env=สภาพแวดล้อม,stderr=subprocess.STDOUT)
            วันครบกําหนด_เวลา=time.monotonic()+60;หน้าต่าง=None
            while time.monotonic()<วันครบกําหนด_เวลา:
                ค้นหา_เมตริก=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=สภาพแวดล้อม,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if ค้นหา_เมตริก.returncode==0:
                    후보=ค้นหา_เมตริก.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    โฟกัส_f7e69dab=subprocess.run(['xdotool','windowfocus','--sync',후보],env=สภาพแวดล้อม,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if โฟกัส_f7e69dab.returncode==0:หน้าต่าง=후보;break
                time.sleep(.1)
            assert หน้าต่าง,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            가상입력도구('mousemove','--window',หน้าต่าง,'280','240','click','1')
            time.sleep(1)
            def 글자입력(ข้อความ):가상입력도구('type','--clearmodifiers','--delay','50',ข้อความ)
            def 누름값(*누름열):가상입력도구('key','--clearmodifiers',*누름열)
            ออฟเซต_ค่า=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),ออฟเซต_ค่า)
            ออฟเซต_ค่า=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),ออฟเซต_ค่า)
            ออฟเซต_ค่า=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/ศูนย์_ตัวถูกดําเนินการ คีย์_ค่า, Shift+Space 또는 F9'.encode(),ออฟเซต_ค่า);기다리기(b'jkoros-native> ',ออฟเซต_ค่า)
            ออฟเซต_ค่า=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),ออฟเซต_ค่า)
            subprocess.check_call(['import','-display',สภาพแวดล้อม['DISPLAY'],'-window',หน้าต่าง,str(เมตริก_ข้อมูล/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',ออฟเซต_ค่า)
            # ค่าจริง_ข้อมูล Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            รูปวาด_ค่า=Image.open(str(เมตริก_ข้อมูล/'remmina-korean.png')).convert('RGB')
            แถบชื่อเรื่อง=None
            for แนวตั้ง_ตําแหน่ง in range(รูปวาด_ค่า.height):
                가로들=[가로 for 가로 in range(รูปวาด_ค่า.width) if รูปวาด_ค่า.getpixel((가로,แนวตั้ง_ตําแหน่ง))==(32,80,144)]
                if len(가로들)>=500:แถบชื่อเรื่อง=(min(가로들),แนวตั้ง_ตําแหน่ง);break
            assert แถบชื่อเรื่อง,'native terminal title bar not found'
            가로,แนวตั้ง_ตําแหน่ง=แถบชื่อเรื่อง[0]+564,แถบชื่อเรื่อง[1]+356
            가상입력도구('mousemove','--window',หน้าต่าง,str(가로),str(แนวตั้ง_ตําแหน่ง))
            def 화상기다리기(ชื่อ,점들):
                วันครบกําหนด_ค่า=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',สภาพแวดล้อม['DISPLAY'],'-window',หน้าต่าง,str(เมตริก_ข้อมูล/ชื่อ)])
                    บิตแมป_รูป=Image.open(str(เมตริก_ข้อมูล/ชื่อ)).convert('RGB')
                    if all(บิตแมป_รูป.getpixel(ตําแหน่ง)==빛 for ตําแหน่ง,빛 in 점들):return
                    assert time.monotonic()<วันครบกําหนด_ค่า,'Remmina framebuffer did not settle: '+ชื่อ
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,แนวตั้ง_ตําแหน่ง-7),(255,255,255)),((가로+7,แนวตั้ง_ตําแหน่ง+7),(255,255,255))])
            가상입력도구('mousedown','1','mousemove','--window',หน้าต่าง,str(가로-120),str(แนวตั้ง_ตําแหน่ง-80),'mouseup','1')
            time.sleep(.4)
            ออฟเซต_ค่า=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',ออฟเซต_ค่า)
            가상입력도구('mousemove','--window',หน้าต่าง,'500','45')
            화상기다리기('remmina-resized.png',[
                ((แถบชื่อเรื่อง[0]+447,แถบชื่อเรื่อง[1]+279),(39,49,64)),((가로,แนวตั้ง_ตําแหน่ง),(24,32,48))])
            if shutil.which('dpkg-query'):
                หมายเลขรุ่น=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                หมายเลขรุ่น=subprocess.check_output(['remmina','--version'],env=สภาพแวดล้อม,stderr=subprocess.STDOUT).decode('utf-8','replace')
            การตรวจสอบความถูกต้อง_รายงาน.update(passed=True,display=สภาพแวดล้อม['DISPLAY'],remmina_version=หมายเลขรุ่น,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not การตรวจสอบความถูกต้อง_รายงาน['passed'] and 'สภาพแวดล้อม' in locals() and สภาพแวดล้อม.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',สภาพแวดล้อม['DISPLAY'],'-window','root',str(เมตริก_ข้อมูล/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for ข้อมูล_ตําแหน่ง in reversed(실행과정들):
                if ข้อมูล_ตําแหน่ง.poll() is None:
                    if ข้อมูล_ตําแหน่ง.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(ข้อมูล_ตําแหน่ง.pid,signal.SIGTERM)
                    else:ข้อมูล_ตําแหน่ง.terminate()
                    try:ข้อมูล_ตําแหน่ง.wait(timeout=5)
                    except subprocess.TimeoutExpired:ข้อมูล_ตําแหน่ง.kill();ข้อมูล_ตําแหน่ง.wait()
            ตัวเลือก_582fe3b9.close()
            for แฟ้ม_รายการ_3d0c1245 in 기록들:แฟ้ม_รายการ_3d0c1245.close()
            (เมตริก_ข้อมูล/'serial.log').write_bytes(직렬입출력)
            (เมตริก_ข้อมูล/'report.json').write_text(json.dumps(การตรวจสอบความถูกต้อง_รายงาน,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':เรียกใช้งาน()
