#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from आज्ञा_कार्यवाही_करा import प्रोजेक्ट_मूळ

def सुरू_करा():
    मोजमाप_डेटा=प्रोजेक्ट_मूळ/'build/verification/coding';मोजमाप_डेटा.mkdir(parents=True,exist_ok=True)
    पडताळणी_अहवाल={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((प्रोजेक्ट_मूळ/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(प्रोजेक्ट_मूळ/'साधने/निर्यात_करा_विकाससाधनसंच.py')])
        with tarfile.open(str(प्रोजेक्ट_मूळ/'dist/jkoros-native-aarch64-sdk.tar.gz')) as संपीडित_बंडल:संपीडित_बंडल.extractall(str(मोजमाप_डेटा))
        विकास_संच=मोजमाप_डेटा/'jkoros-native-sdk'
        चिन्हे_यादी=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(विकास_संच/'lib/libposix-kor-user.a')]).decode()
        for नाव in ('संचारटोक_तयार_करा','बाइंड_करा_पत्ता','स्वतंत्रसंदेश_डेटा_पाठवा','स्वतंत्रसंदेश_डेटा_स्वीकारा','संचिका_उघडा','संचिका_डेटा_वाचा','संचिका_डेटा_लिहा'):
            assert ' T '+नाव+'\n' in चिन्हे_यादी, नाव
        (मोजमाप_डेटा/'korean-function-symbols.txt').write_text(चिन्हे_यादी)
        पडताळणी_अहवाल['checks'].append('real-korean-c-function-symbols')
        def आज्ञा_कार्यवाही_करा(नाव,मार्ग,वितर्क_ऍरे,अपेक्षित):
            डेटा_स्थान=subprocess.run(['python3',str(प्रोजेक्ट_मूळ/'साधने/संचिका_कार्यवाही_करा.py'),str(मार्ग)]+वितर्क_ऍरे,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (मोजमाप_डेटा/(नाव+'.log')).write_bytes(डेटा_स्थान.stdout);assert डेटा_स्थान.returncode==0,डेटा_स्थान.stdout.decode('utf-8','replace')
            assert अपेक्षित.encode() in डेटा_स्थान.stdout,डेटा_स्थान.stdout;पडताळणी_अहवाल['checks'].append(नाव)
        for प्रत्यय_मूल्य in ('c','cpp'):
            निष्पादनीय_संचिका=मोजमाप_डेटा/('अभिवादन_ae353e94-'+प्रत्यय_मूल्य+'.elf')
            subprocess.check_call(['python3',str(विकास_संच/'compile.py'),str(विकास_संच/'examples'/('अभिवादन_ae353e94.'+प्रत्यय_मूल्य)),'-o',str(निष्पादनीय_संचिका)])
            आज्ञा_कार्यवाही_करा('korean-'+प्रत्यय_मूल्य,निष्पादनीय_संचिका,[],'posix-kor आवाहन')
        निष्पादनीय_संचिका=मोजमाप_डेटा/'प्रवाह_मूल्य.elf'
        subprocess.check_call(['python3',str(विकास_संच/'compile.py'),str(विकास_संच/'examples/प्रवाह_मूल्य.c'),'-o',str(निष्पादनीय_संचिका)])
        आज्ञा_कार्यवाही_करा('c-stream-queues',निष्पादनीय_संचिका,[],'C posix-kor 연결형 संचार PASS')
        आज्ञा_कार्यवाही_करा('korean-python',प्रोजेक्ट_मूळ/'उदाहरणे/हांगुल_संकेतन/अभिवादन_ae353e94.py',['--include',str(प्रोजेक्ट_मूळ/'उदाहरणे/हांगुल_संकेतन/मराठी.py')],'안녕하세요 누리')
        आज्ञा_कार्यवाही_करा('guest-korean-javac',प्रोजेक्ट_मूळ/'उदाहरणे/हांगुल_संकेतन/अभिवादन_ae353e94.java',[],'안녕하세요 · एकूण_मूल्य=42')
        पडताळणी_अहवाल['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(मोजमाप_डेटा/'report.json').write_text(json.dumps(पडताळणी_अहवाल,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':सुरू_करा()
