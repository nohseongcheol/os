#!/usr/bin/env python3
import hashlib,json,subprocess
from നടപ്പാക്കുക_കമാന്_ഡ് import പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം

def നടപ്പിലാക്കുക():
    അളവ്_ഡാറ്റാ=പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'build/verification/stream';അളവ്_ഡാറ്റാ.mkdir(parents=True,exist_ok=True)
    నిర్ధారణ_నివేదిక={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(അളവ്_ഡാറ്റാ),str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'시험/자바/흐름시험.java')])
        ഡാറ്റാ_പദവി=subprocess.run(['python3',str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'ഉപകരണങ്ങൾ/നടപ്പാക്കുക_ഫയല്.py'),str(അളവ്_ഡാറ്റാ/'흐름시험.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (അളവ്_ഡാറ്റാ/'serial.log').write_bytes(ഡാറ്റാ_പദവി.stdout);assert ഡാറ്റാ_പദവി.returncode==0,ഡാറ്റാ_പദവി.stdout.decode('utf-8','replace')
        പദാവലി=ഡാറ്റാ_പദവി.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in പദാവലി,പദാവലി
        నిర్ధారణ_నివేదిక.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(അളവ്_ഡാറ്റാ/'report.json').write_text(json.dumps(నిర్ధారణ_నివేదిక,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':നടപ്പിലാക്കുക()
