#!/usr/bin/env python3
"""ค่าจริง_ข้อมูล เอง 커널의 IP/ICMP, สถานะ_ค่า คิวรี_ค่า, 현지어 คําสั่ง, 게스트 ออก_แอป ตรวจสอบความถูกต้อง."""
import argparse
import ftplib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import re
import selectors
import signal
import socket
import subprocess
import sys
import tempfile
import time


def เรียกใช้งาน():
    ตัวแยกวิเคราะห์_48ee4b1b=argparse.ArgumentParser();ตัวแยกวิเคราะห์_48ee4b1b.add_argument('--edition',type=Path);ตัวแยกวิเคราะห์_48ee4b1b.add_argument('--output',type=Path);ตัวแยกวิเคราะห์_48ee4b1b.add_argument('--poweroff-only',action='store_true');อาร์กิวเมนต์=ตัวแยกวิเคราะห์_48ee4b1b.parse_args()
    แสดง_ราก=Path(__file__).resolve().parents[1];ตั้งค่า={};ชื่อ_ตาราง={}
    if อาร์กิวเมนต์.edition:
        คันทรี_ค่า=อาร์กิวเมนต์.edition.resolve();ตั้งค่า=json.loads((คันทรี_ค่า/'native.json').read_text());ชื่อ_ตาราง=ตั้งค่า['identifiers'];แสดง_ราก=คันทรี_ค่า/ตั้งค่า['source']/ตั้งค่า['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(คันทรี_ค่า/'native-edition.py'),'check'])
        โฮสต์=คันทรี_ค่า/'host/qemu'
        if โฮสต์.is_file():os.environ['QEMU_AARCH64']=str(โฮสต์)
    เครื่องมือ=แสดง_ราก/Path(ตั้งค่า.get('runner','เครื่องมือ/ดําเนินการ_คําสั่ง.py')).parent
    sys.path.insert(0,str(เครื่องมือ))
    def อ่าน(ชื่อ):
        เส้นทาง=เครื่องมือ/(ชื่อ_ตาราง.get(ชื่อ,ชื่อ)+'.py');มูลค่าตามสัญญา=importlib.util.spec_from_file_location('test_'+ชื่อ,str(เส้นทาง));มอดูล_ค่า=importlib.util.module_from_spec(มูลค่าตามสัญญา);มูลค่าตามสัญญา.loader.exec_module(มอดูล_ค่า);return มอดูล_ค่า
    실행모듈=อ่าน('ดําเนินการ_คําสั่ง');เครือข่าย_มอดูล=อ่าน('บริดจ์_3de4fe3a');คําสั่ง=getattr(실행모듈,ชื่อ_ตาราง.get('คําสั่ง','คําสั่ง'));บริดจ์_ชนิด=getattr(เครือข่าย_มอดูล,ชื่อ_ตาราง.get('บริดจ์_3de4fe3a','บริดจ์_3de4fe3a'))
    ทางลัด_ค่า_0a38607b=ตั้งค่า.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'ที่อยู่_IP','ping':'การทดสอบ_การตอบ','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'แสดง_ความช่วยเหลือ'})
    sys.path.insert(0,str(แสดง_ราก/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(แสดง_ราก);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    ข้อความออก=อาร์กิวเมนต์.output or แสดง_ราก/'build/verification/system-tools';ข้อความออก.mkdir(parents=True,exist_ok=True)
    รายงาน_ค่า={'passed':False,'country':ตั้งค่า.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((แสดง_ราก/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    บันทึก_สถิติ=bytearray();ลําดับ_ค่า_e9fa7815=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        ควบคุม_พาธ=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as ค้นหา_ค่า:ค้นหา_ค่า.bind(('127.0.0.1',0));หมายเลขพอร์ต=ค้นหา_ค่า.getsockname()[1]
            if not 50000<=หมายเลขพอร์ต<=50007:break
        with บริดจ์_ชนิด(หมายเลขพอร์ต,จับ=True,ผู้เยี่ยมชม_อีเมล=ipTestText('10.0.2.20'),โฮสต์_อีเมล='127.0.0.2') as บริดจ์_ค่า:
            กระบวนการ_ค่า=subprocess.Popen(คําสั่ง()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(ควบคุม_พาธ)]+บริดจ์_ค่า.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            เลือก_รายการ=selectors.DefaultSelector();เลือก_รายการ.register(กระบวนการ_ค่า.stdout,selectors.EVENT_READ)
            def รับ(แสดง_ค่า,เรียกใช้งาน=0,제한=45):
                끝=time.monotonic()+제한
                while แสดง_ค่า not in บันทึก_สถิติ[เรียกใช้งาน:]:
                    if time.monotonic()>끝 or กระบวนการ_ค่า.poll() is not None:raise AssertionError('Missing '+repr(แสดง_ค่า)+'\n'+บันทึก_สถิติ[เรียกใช้งาน:].decode('utf-8','replace'))
                    for คีย์_ค่า,_ in เลือก_รายการ.select(.1):
                        ข้อมูล=คีย์_ค่า.fileobj.read(65536)
                        if ข้อมูล:บันทึก_สถิติ.extend(ข้อมูล)
                return บันทึก_สถิติ[เรียกใช้งาน:].decode('utf-8','replace').replace('\r\n','\n')
            def ส่ง(ข้อมูล):กระบวนการ_ค่า.stdin.write(ข้อมูล);กระบวนการ_ค่า.stdin.flush()
            def เชลล์(ข้อความ):
                ข้อความ=ipTestText(ข้อความ)
                print(รายงาน_ค่า['country'],ข้อความ,flush=True);ลําดับ_ค่า_e9fa7815[0]+=1;แสดง_ค่า='__SYSTEM_DONE_'+str(ลําดับ_ค่า_e9fa7815[0])+'__';เรียกใช้งาน=len(บันทึก_สถิติ)
                ส่ง((ข้อความ+'; echo; echo '+แสดง_ค่า+'\n').encode())
                สิ้นสุดการโทร_มาร์กเกอร์=('\r\n'+แสดง_ค่า+'\r\n').encode();รับ(สิ้นสุดการโทร_มาร์กเกอร์,เรียกใช้งาน)
                สิ้นสุดการโทร_ตําแหน่ง=บันทึก_สถิติ.index(สิ้นสุดการโทร_มาร์กเกอร์,เรียกใช้งาน)+len(สิ้นสุดการโทร_มาร์กเกอร์)
                รับ(b'jkoros-native> ',สิ้นสุดการโทร_ตําแหน่ง)
                return บันทึก_สถิติ[เรียกใช้งาน:].decode('utf-8','replace').replace('\r\n','\n')
            def ยืนยัน(ข้อความ,*값들):
                ตอบกลับ=เชลล์(ข้อความ)
                for ค่า in 값들:assert ipTestText(ค่า) in ตอบกลับ,(ข้อความ,ค่า,ตอบกลับ)
                return ตอบกลับ
            try:
                รับ(b'jkoros-native> ')
                if not อาร์กิวเมนต์.poweroff_only:
                    ความช่วยเหลือ_ค่า=ยืนยัน('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in ทางลัด_ค่า_0a38607b.values():assert 별칭 in ความช่วยเหลือ_ค่า,(별칭,ความช่วยเหลือ_ค่า)
                    ยืนยัน(ทางลัด_ค่า_0a38607b['help']+' system','Network / system')
                    ยืนยัน('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    ยืนยัน(ทางลัด_ค่า_0a38607b['ipconfig'],'inet 10.0.2.15');ยืนยัน('ip addr show','sl0: UP');ยืนยัน('ifconfig','sl0: UP')
                    for ไม่ถูกต้อง_การตั้งค่า in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        ข้อผิดพลาด=ยืนยัน('ipconfig set '+ไม่ถูกต้อง_การตั้งค่า+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in ข้อผิดพลาด,ข้อผิดพลาด
                        ยืนยัน('ipconfig','inet 10.0.2.15')
                    ยืนยัน('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    ยืนยัน(ทางลัด_ค่า_0a38607b['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    ยืนยัน('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    ยืนยัน('ip link set dev sl0 down','sl0: DOWN');ยืนยัน('ping -c 1 10.0.2.2; echo STATUS=$?','ข้อผิดพลาด -100','STATUS=1')
                    ยืนยัน('ipconfig up','sl0: UP')
                    ยืนยัน(ทางลัด_ค่า_0a38607b['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    ยืนยัน('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    ยืนยัน('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');ยืนยัน(ทางลัด_ค่า_0a38607b['route'],'10.0.2.2 sl0')
                    ยืนยัน('ftpd start','FTP listening')
                    ยืนยัน(ทางลัด_ค่า_0a38607b['netstat'],'10.0.2.20:21','LISTEN');ยืนยัน('ss','LISTEN')
                    ยืนยัน('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','ข้อผิดพลาด -16')
                    with ftplib.FTP() as ไคลเอ็นต์_ค่า:
                        ไคลเอ็นต์_ค่า.connect('127.0.0.2',หมายเลขพอร์ต,timeout=20);ไคลเอ็นต์_ค่า.login();ข้อมูล=b'Network address was changed in the guest.\n'
                        ไคลเอ็นต์_ค่า.storbinary('STOR net-state.txt',io.BytesIO(ข้อมูล));받은자료=bytearray();ไคลเอ็นต์_ค่า.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==ข้อมูล;ไคลเอ็นต์_ค่า.delete('net-state.txt')
                    ยืนยัน('ftpd stop','FTP stopped');ยืนยัน('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    รายงาน_ค่า['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(ข้อความ):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',ข้อความ);assert 찾음,ข้อความ;return tuple(map(int,찾음.groups()))
                    전=저장값(ยืนยัน('df','RAM only'));ยืนยัน('echo disk-proof > sys-state.txt');후=저장값(ยืนยัน(ทางลัด_ค่า_0a38607b['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    ยืนยัน('rm sys-state.txt');assert 저장값(เชลล์('df'))==전
                    ความจํา_ค่า=ยืนยัน(ทางลัด_ค่า_0a38607b['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');ปริมาณ_ค่า=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',ความจํา_ค่า).groups()));assert 0<ปริมาณ_ค่า[1]<=ปริมาณ_ค่า[0] and ปริมาณ_ค่า[1]+ปริมาณ_ค่า[2]==ปริมาณ_ค่า[0]
                    ยืนยัน(ทางลัด_ค่า_0a38607b['ps'],'kernel/shell');ยืนยัน(ทางลัด_ค่า_0a38607b['uptime'],'seconds')
                    สถานะ_ข้อมูล=ยืนยัน(ทางลัด_ค่า_0a38607b['top']+' -n 2','kernel/shell');assert สถานะ_ข้อมูล.count('PID SLOT STATE')==2,สถานะ_ข้อมูล
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    ยืนยัน('terminal','TERMINAL READY');เรียกใช้งาน=len(บันทึก_สถิติ);ส่ง(b'vi process.txt\n');รับ(b'NORMAL',เรียกใช้งาน)
                    เรียกใช้งาน=len(บันทึก_สถิติ);ส่ง(bytes([30,2,1,0,0,0,0]));รับ(b'jkoros-native> ',เรียกใช้งาน)
                    รายการ_รายการ=ยืนยัน('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',รายการ_รายการ);assert 찾음 and int(찾음.group(2))>0,รายการ_รายการ
                    ยืนยัน('free','EL0 mapped KiB: '+찾음.group(2))
                    เรียกใช้งาน=len(บันทึก_สถิติ);ส่ง(b'top\n');รับ(b'PID SLOT STATE',เรียกใช้งาน);ส่ง(b'q');รับ(b'jkoros-native> ',เรียกใช้งาน)
                    # Test a multibyte prefix through the real shell completion path.
                    if ทางลัด_ค่า_0a38607b['df']!='df':
                        เรียกใช้งาน=len(บันทึก_สถิติ);ส่ง((ทางลัด_ค่า_0a38607b['df'][:-1]+'\t\n').encode());รับ(b'RAM only',เรียกใช้งาน);รับ(b'jkoros-native> ',เรียกใช้งาน)
                    รายงาน_ค่า['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as ควบคุม_ค่า:
                    ควบคุม_ค่า.settimeout(15);ควบคุม_ค่า.connect(str(ควบคุม_พาธ));สตรีม_ค่า=ควบคุม_ค่า.makefile('rwb');json.loads(สตรีม_ค่า.readline());สตรีม_ค่า.write(b'{"execute":"qmp_capabilities"}\n');สตรีม_ค่า.flush()
                    while 'return' not in json.loads(สตรีม_ค่า.readline()):pass
                    ส่ง((('poweroff' if อาร์กิวเมนต์.poweroff_only else ทางลัด_ค่า_0a38607b['poweroff'])+'\n').encode())
                    while True:
                        เหตุการณ์=json.loads(สตรีม_ค่า.readline())
                        if เหตุการณ์.get('event')=='SHUTDOWN':break
                    assert เหตุการณ์['data']['guest'] and เหตุการณ์['data']['reason']=='guest-shutdown',เหตุการณ์
                    assert กระบวนการ_ค่า.wait(timeout=15)==0
                    รายงาน_ค่า['shutdown']=เหตุการณ์;รายงาน_ค่า['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                รายงาน_ค่า['network_trace']=บริดจ์_ค่า.แฟ้มบันทึกการติดตาม
                assert อาร์กิวเมนต์.poweroff_only or any(รายการ_ค่า['protocol']==1 and รายการ_ค่า['direction']=='from_guest' for รายการ_ค่า in บริดจ์_ค่า.แฟ้มบันทึกการติดตาม)
                รายงาน_ค่า['passed']=True
            finally:
                if กระบวนการ_ค่า.poll() is None:os.killpg(กระบวนการ_ค่า.pid,signal.SIGTERM)
                try:กระบวนการ_ค่า.wait(timeout=10)
                except subprocess.TimeoutExpired:กระบวนการ_ค่า.kill();กระบวนการ_ค่า.wait()
                เลือก_รายการ.close();(ข้อความออก/'serial.log').write_bytes(บันทึก_สถิติ);(ข้อความออก/'report.json').write_text(json.dumps(รายงาน_ค่า,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({คีย์_ค่า:ค่า for คีย์_ค่า,ค่า in รายงาน_ค่า.items() if คีย์_ค่า!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':เรียกใช้งาน()
