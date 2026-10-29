#!/usr/bin/env python3
import hashlib,json,subprocess
from ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ import ໂຄງ_ການ_ເລກຮາກ

def ແລ່ນ():
    ມາດຕະການ_ຂໍ້ມູນ=ໂຄງ_ການ_ເລກຮາກ/'build/verification/stream';ມາດຕະການ_ຂໍ້ມູນ.mkdir(parents=True,exist_ok=True)
    ໃຊ້ໄດ້_ລາຍງານ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((ໂຄງ_ການ_ເລກຮາກ/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(ມາດຕະການ_ຂໍ້ມູນ),str(ໂຄງ_ການ_ເລກຮາກ/'시험/자바/흐름시험.java')])
        ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ=subprocess.run(['python3',str(ໂຄງ_ການ_ເລກຮາກ/'ເຄື່ອງມື/ປະ_ຕິ_ບັດ_ຟາຍ.py'),str(ມາດຕະການ_ຂໍ້ມູນ/'흐름시험.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (ມາດຕະການ_ຂໍ້ມູນ/'serial.log').write_bytes(ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ.stdout);assert ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ.returncode==0,ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ.stdout.decode('utf-8','replace')
        ຂໍ້ຄວາມ=ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in ຂໍ້ຄວາມ,ຂໍ້ຄວາມ
        ໃຊ້ໄດ້_ລາຍງານ.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(ມາດຕະການ_ຂໍ້ມູນ/'report.json').write_text(json.dumps(ໃຊ້ໄດ້_ລາຍງານ,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':ແລ່ນ()
