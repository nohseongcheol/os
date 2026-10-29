#!/usr/bin/env python3
"""Run all examples in the real combined VNC + SLIP/FTP native VM."""
import ftplib
import hashlib
import io
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from khungNhìnMànLàmViệc import giáTrịChínhXác
from MáyChủVọngMẫu import CácMáyChủVọngLại
from thựcThiLệnh import gốcCâyDựÁn


def thửNgônNgữ(NgônNgữ,mụcMáyChủVọngLại,dữLiệuKếtQuả):
    with socket.socket() as tạm:
        tạm.bind(('127.0.0.1',0));sốCổngChuyểnGiaoTệp=tạm.getsockname()[1]
    tiếnTrình=subprocess.Popen(['python3',str(gốcCâyDựÁn/'CôngCụ/thựcThiLệnh.py'),'--desktop','--network','--port','0','--ftp-port',str(sốCổngChuyểnGiaoTệp)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    bộChọn=selectors.DefaultSelector();bộChọn.register(tiếnTrình.stdout,selectors.EVENT_READ)
    bảnGhiDiễnTiến=bytearray();máyKhách=None;kếtNốiChuyểnGiaoTệp=None
    def nhậnThôngĐiệp(dấuMốc,chạy=0):
        độLệchKếtThúc=time.monotonic()+60
        while dấuMốc not in bảnGhiDiễnTiến[chạy:]:
            if time.monotonic()>độLệchKếtThúc or tiếnTrình.poll() is not None:raise AssertionError(bảnGhiDiễnTiến[chạy:].decode('utf-8','replace'))
            for giáTrịĐãNhấn,_ in bộChọn.select(.1):
                DữLiệu=giáTrịĐãNhấn.fileobj.read(65536)
                if DữLiệu:bảnGhiDiễnTiến.extend(DữLiệu)
        return bảnGhiDiễnTiến[chạy:].decode('utf-8','replace').replace('\r\n','\n')
    def giáTrịĐãNhấn(giáTrịKýHiệu,làĐangNhấn=True):máyKhách.sendall(struct.pack('>BBHI',4,int(làĐangNhấn),0,giáTrịKýHiệu))
    def bắtChạyĐộLệch(dòng):
        chạy=len(bảnGhiDiễnTiến)
        for mãKýTự in dòng+'\n':
            giáTrịKýHiệu=0xff0d if mãKýTự=='\n' else ord(mãKýTự) if ord(mãKýTự)<256 else 0x1000000|ord(mãKýTự)
            giáTrịĐãNhấn(giáTrịKýHiệu);giáTrịĐãNhấn(giáTrịKýHiệu,False)
        return chạy
    def vỏLệnh(dòng):return nhậnThôngĐiệp(b'jkoros-native> ',bắtChạyĐộLệch(dòng))
    def thựcThiLệnh(dòng,dựKiến):
        vănBản=vỏLệnh(dòng);assert dựKiến in vănBản and 'exit 0' in vănBản,(dòng,vănBản)
        return vănBản
    def danhSáchCácĐiểmẢnh():
        máyKhách.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        màuRGB=bytearray(640*480*3)
        while True:
            giáTrịLoạiMục=giáTrịChínhXác(máyKhách,1)[0]
            if giáTrịLoạiMục==2:continue
            if giáTrịLoạiMục==3:
                sốLượngPhầnMục=struct.unpack('>I',giáTrịChínhXác(máyKhách,7)[3:])[0];giáTrịChínhXác(máyKhách,sốLượngPhầnMục);continue
            assert giáTrịLoạiMục==0,giáTrịLoạiMục
            sốLượngMục=struct.unpack('>H',giáTrịChínhXác(máyKhách,3)[1:])[0]
            for _ in range(sốLượngMục):
                tọaĐộX,tọaĐộY,giáTrịRộngĐãYêuCầu,giáTrịCaoĐãYêuCầu,bảngMãKýTự=struct.unpack('>HHHHi',giáTrịChínhXác(máyKhách,12));assert bảngMãKýTự==0,bảngMãKýTự
                DữLiệu=giáTrịChínhXác(máyKhách,giáTrịRộngĐãYêuCầu*giáTrịCaoĐãYêuCầu*4)
                for vịTríHàng in range(giáTrịCaoĐãYêuCầu):
                    for vịTríCột in range(giáTrịRộngĐãYêuCầu):
                        dữLiệuNguyênBản=(vịTríHàng*giáTrịRộngĐãYêuCầu+vịTríCột)*4;giáTrịĐốiĐích=((tọaĐộY+vịTríHàng)*640+tọaĐộX+vịTríCột)*3
                        màuRGB[giáTrịĐốiĐích:giáTrịĐốiĐích+3]=bytes((DữLiệu[dữLiệuNguyênBản+2],DữLiệu[dữLiệuNguyênBản+1],DữLiệu[dữLiệuNguyênBản]))
            if sốLượngMục:return màuRGB
    try:
        nhậnThôngĐiệp(b'TERMINAL READY');nhậnThôngĐiệp(b'jkoros-native> ',bảnGhiDiễnTiến.rfind(b'TERMINAL READY'))
        sốCổng=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',bảnGhiDiễnTiến).group(1))
        máyKhách=socket.create_connection(('127.0.0.1',sốCổng),timeout=10)
        assert giáTrịChínhXác(máyKhách,12)==b'RFB 003.008\n';máyKhách.sendall(b'RFB 003.008\n')
        assert 1 in giáTrịChínhXác(máyKhách,giáTrịChínhXác(máyKhách,1)[0]);máyKhách.sendall(b'\x01');assert giáTrịChínhXác(máyKhách,4)==b'\0'*4
        máyKhách.sendall(b'\x01');giáTrịBanĐầu=giáTrịChínhXác(máyKhách,24);giáTrịChínhXác(máyKhách,struct.unpack('>I',giáTrịBanĐầu[20:])[0])
        máyKhách.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        máyKhách.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in vỏLệnh('ftpd start')
        kếtNốiChuyểnGiaoTệp=ftplib.FTP();kếtNốiChuyểnGiaoTệp.encoding='utf-8';kếtNốiChuyểnGiaoTệp.connect('127.0.0.1',sốCổngChuyểnGiaoTệp,timeout=20);kếtNốiChuyểnGiaoTệp.login()
        dữLiệuNộiTải=('GUI와 FTP 동시 giáTrịDùng '+NgônNgữ+' 😀\n').encode()
        kếtNốiChuyểnGiaoTệp.storbinary('STOR 함께.txt',io.BytesIO(dữLiệuNộiTải))
        assert dữLiệuNộiTải.decode().strip() in vỏLệnh('cat /함께.txt')
        sốLượngĐãNhận=bytearray();kếtNốiChuyểnGiaoTệp.retrbinary('RETR 함께.txt',sốLượngĐãNhận.extend);assert sốLượngĐãNhận==dữLiệuNộiTải;kếtNốiChuyểnGiaoTệp.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        gửiDanhSách=vỏLệnh('ls /example')
        assert all(tên in gửiDanhSách for tên in ('java/','c/','python/','README.md')),gửiDanhSách
        if NgônNgữ=='java':
            bảnKêGóiGộp=json.loads((gốcCâyDựÁn/'build/examples/manifest.json').read_text())
            for đườngDẫn,điểmMục in bảnKêGóiGộp.items():
                vỏLệnh('cp '+đườngDẫn+' /example-check.bin')
                giáTrịNộiDung=bytearray();kếtNốiChuyểnGiaoTệp.retrbinary('RETR example-check.bin',giáTrịNộiDung.extend)
                assert len(giáTrịNộiDung)==điểmMục['bytes'] and hashlib.sha256(giáTrịNộiDung).hexdigest()==điểmMục['sha256'],đườngDẫn
            kếtNốiChuyểnGiaoTệp.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            nhịPhân=bytes(range(256))*64
            kếtNốiChuyểnGiaoTệp.storbinary('STOR boundary.bin',io.BytesIO(nhịPhân))
            giáTrịNộiDung=bytearray();kếtNốiChuyểnGiaoTệp.retrbinary('RETR boundary.bin',giáTrịNộiDung.extend)
            assert giáTrịNộiDung==nhịPhân and 'boundary.bin' in kếtNốiChuyểnGiaoTệp.nlst()
            vỏLệnh('cp /boundary.bin /boundary-copy.bin')
            giáTrịNộiDung=bytearray();kếtNốiChuyểnGiaoTệp.retrbinary('RETR boundary-copy.bin',giáTrịNộiDung.extend)
            assert giáTrịNộiDung==nhịPhân
            kếtNốiChuyểnGiaoTệp.delete('boundary.bin');kếtNốiChuyểnGiaoTệp.delete('boundary-copy.bin')
        assert 'VíDụIn' in vỏLệnh('ls /example/'+NgônNgữ)
        vỏLệnh('cd /example/'+NgônNgữ)
        bảngTraTên={'java':'JAVA','c':'C','python':'PYTHON'}[NgônNgữ]
        tệpDựKiến=bảngTraTên+' Tệp: 한글 DữLiệu 😀\n'
        if NgônNgữ=='java':
            thựcThiLệnh('javac VíDụIn.java','Compiled:');thựcThiLệnh('java VíDụIn','JAVA ĐầuRa: 안녕하세요 😀')
            thựcThiLệnh('javac VíDụTệp.java','Compiled:');thựcThiLệnh('java VíDụTệp',tệpDựKiến)
            thựcThiLệnh('java VíDụMạng {} {}'.format(mụcMáyChủVọngLại.cổngTCP,mụcMáyChủVọngLại.cổngUDP),'JAVA 네트워크 xácMinh: TCP UDP 한글')
            lệnhĐồHọa='java VíDụVẽ'
        elif NgônNgữ=='c':
            for tên,giáTrịĐãChuyểnTiếp,dựKiến in [('ĐầuRa','', 'C ĐầuRa: 안녕하세요 😀'),('Tệp','',tệpDựKiến),
                    ('네트워크',' '+str(mụcMáyChủVọngLại.cổngUDP),'C 네트워크 xácMinh: UDP 한글')]:
                thựcThiLệnh('cc '+tên+'VíDụ.c -o thựcThiLệnh','Compiled native ARM64 ELF:')
                thựcThiLệnh('./thựcThiLệnh'+giáTrịĐãChuyểnTiếp,dựKiến)
            thựcThiLệnh('cc VíDụVẽ.c -o thựcThiLệnh','Compiled native ARM64 ELF:');lệnhĐồHọa='./thựcThiLệnh'
        else:
            for tên,giáTrịĐãChuyểnTiếp,dựKiến in [('ĐầuRa','','PYTHON ĐầuRa: 안녕하세요 😀'),('Tệp','',tệpDựKiến),
                    ('네트워크',' '+str(mụcMáyChủVọngLại.cổngUDP),'PYTHON 네트워크 xácMinh: UDP 한글')]:
                thựcThiLệnh('python '+tên+'VíDụ.py'+giáTrịĐãChuyểnTiếp,dựKiến)
            lệnhĐồHọa='python VíDụVẽ.py'
        bắtChạyBảnVẽ=bắtChạyĐộLệch(lệnhĐồHọa)
        vănBản=nhậnThôngĐiệp('그림을 확인한 giáTrịLùi Enter를 누르세요.\r\n'.encode(),bắtChạyBảnVẽ)
        assert bảngTraTên+' 그래픽: 빨강 초록 파랑' in vănBản and 'exit 0' not in vănBản,vănBản
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        kếtNốiChuyểnGiaoTệp.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        sốLượngĐãNhận=bytearray();kếtNốiChuyểnGiaoTệp.retrbinary('RETR 도중.txt',sốLượngĐãNhận.extend);assert sốLượngĐãNhận==b'FTP DURING GRAPHICS';kếtNốiChuyểnGiaoTệp.delete('도중.txt')
        màuRGB=danhSáchCácĐiểmẢnh()
        for tọaĐộY,màuĐiểmẢnh in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            giáTrịĐộLệch=(tọaĐộY*640+610)*3;assert tuple(màuRGB[giáTrịĐộLệch:giáTrịĐộLệch+3])==màuĐiểmẢnh,(NgônNgữ,tọaĐộY,tuple(màuRGB[giáTrịĐộLệch:giáTrịĐộLệch+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(màuRGB)).save(str(dữLiệuKếtQuả/(NgônNgữ+'-graphics.png')))
        giáTrịĐãNhấn(0xff0d);giáTrịĐãNhấn(0xff0d,False)
        assert 'exit 0' in nhậnThôngĐiệp(b'jkoros-native> ',bắtChạyBảnVẽ)
        if NgônNgữ=='java':
            bắtChạyCửaSổ=bắtChạyĐộLệch('java VíDụCửaSổ')
            nhậnThôngĐiệp('GUI VíDụ chuẩnBị: VíDụCửaSổ'.encode(),bắtChạyCửaSổ)
            def giáTrịNhấnChuột(vịTríNgang,vịTríDọc):
                for nút in (1,0):máyKhách.sendall(struct.pack('>BBHH',5,nút,vịTríNgang,vịTríDọc))
            time.sleep(.3)
            ảnhTrướcĐó=Image.frombytes('RGB',(640,480),bytes(danhSáchCácĐiểmẢnh()))
            giáTrịNhấnChuột(160,196)
            for _ in range(2):giáTrịĐãNhấn(0xff08);giáTrịĐãNhấn(0xff08,False)
            for giáTrịKýTự in '한글':giáTrịĐãNhấn(0x1000000|ord(giáTrịKýTự));giáTrịĐãNhấn(0x1000000|ord(giáTrịKýTự),False)
            for sốLượngSựLặp in (1,2):
                chạy=len(bảnGhiDiễnTiến);giáTrịNhấnChuột(180,242)
                nhậnThôngĐiệp(('GUI LờiChào: 안녕하세요, 한글님! ('+str(sốLượngSựLặp)+')').encode(),chạy)
            time.sleep(.3)
            bảnVẽCửaSổ=Image.frombytes('RGB',(640,480),bytes(danhSáchCácĐiểmẢnh()))
            assert ảnhTrướcĐó.crop((110,272,530,300)).tobytes()!=bảnVẽCửaSổ.crop((110,272,530,300)).tobytes()
            bảnVẽCửaSổ.save(str(dữLiệuKếtQuả/'java-swing.png'))
            chạy=len(bảnGhiDiễnTiến);giáTrịNhấnChuột(535,105)
            assert 'exit 0' in nhậnThôngĐiệp(b'jkoros-native> ',chạy)
        # Download the guest-created bytes through FTP in the same GUI VM.
        tênMụcTệp={'java':'java.txt','c':'c.txt','python':'python.txt'}[NgônNgữ]
        vỏLệnh('cp '+tênMụcTệp+' /thẩmĐịnh.txt')
        sốLượngĐãNhận=bytearray();kếtNốiChuyểnGiaoTệp.retrbinary('RETR thẩmĐịnh.txt',sốLượngĐãNhận.extend);assert sốLượngĐãNhận==tệpDựKiến.encode()
        vỏLệnh('echo preserved > VíDụIn.'+('py' if NgônNgữ=='python' else NgônNgữ))
        assert 'EXAMPLES READY' in vỏLệnh('example '+NgônNgữ)
        assert '\npreserved\n' in vỏLệnh('cat VíDụIn.'+('py' if NgônNgữ=='python' else NgônNgữ))
        assert '한/toánHạngKhôngSố giáTrịPhím, Shift+Space 또는 F9' in vỏLệnh('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in vỏLệnh('echo GUI NETWORK TOGETHER')
        kếtNốiChuyểnGiaoTệp.quit();kếtNốiChuyểnGiaoTệp=None;assert 'FTP stopped' in vỏLệnh('ftpd stop')
        print('PASS '+NgônNgữ+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if kếtNốiChuyểnGiaoTệp:
            try:kếtNốiChuyểnGiaoTệp.close()
            except OSError:pass
        if máyKhách:máyKhách.close()
        tiếnTrình.terminate()
        try:tiếnTrình.wait(timeout=8)
        except subprocess.TimeoutExpired:tiếnTrình.kill();tiếnTrình.wait()
        bộChọn.close();tiếnTrình.stdout.close();(dữLiệuKếtQuả/(NgônNgữ+'-serial.log')).write_bytes(bảnGhiDiễnTiến)


def chạy():
    dữLiệuKếtQuả=gốcCâyDựÁn/'build/verification/examples';dữLiệuKếtQuả.mkdir(parents=True,exist_ok=True)
    báoCáoViệcThẩmĐịnh={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((gốcCâyDựÁn/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with CácMáyChủVọngLại() as mụcMáyChủVọngLại:
            for NgônNgữ in ('java','c','python'):
                thửNgônNgữ(NgônNgữ,mụcMáyChủVọngLại,dữLiệuKếtQuả);báoCáoViệcThẩmĐịnh['languages'].append(NgônNgữ)
            dựKiến=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert mụcMáyChủVọngLại.cóĐãNhận==[(giáTrịLoạiMục,DữLiệu.encode()) for giáTrịLoạiMục,DữLiệu in dựKiến],mụcMáyChủVọngLại.cóĐãNhận
            báoCáoViệcThẩmĐịnh['host_network_payloads']=[{'protocol':giáTrịLoạiMục,'text':DữLiệu.decode()} for giáTrịLoạiMục,DữLiệu in mụcMáyChủVọngLại.cóĐãNhận]
        báoCáoViệcThẩmĐịnh.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(dữLiệuKếtQuả/'report.json').write_text(json.dumps(báoCáoViệcThẩmĐịnh,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':chạy()
