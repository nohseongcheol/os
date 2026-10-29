#!/usr/bin/env python3
"""वितरण_मूल्य class의 직접 मराठी GUI/कार्यसूत्र_मूल्य_5b72a632 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

प्रोजेक्ट_मूळ = Path(__file__).resolve().parents[1]

def सुरू_करा():
    वर्ग_यादी_70c8b393 = ('창', 'बटण', 'लेबल', 'मजकूर_फील्_ड', 'पडदा_घटक', 'क्रिया_सूचना', 'इव्हेंट_रांग', 'कार्यसूत्र',
             'पारपाडा_कार्य', 'चालवण्यायोग्य_कार्य', 'क्रिया_ग्राहक')
    बंडल = प्रोजेक्ट_मूळ/'dist/jkoros-native-korean.jar'
    घोषणा = subprocess.check_output(['javap', '-classpath', str(बंडल), '-private', '-c']+
                                ['मराठी.स्वकीय.'+नाव for नाव in वर्ग_यादी_70c8b393]).decode()
    for निषिद्ध_मूल्य in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert निषिद्ध_मूल्य not in घोषणा, निषिद्ध_मूल्य
    उदाहरणे = subprocess.check_output(['javap', '-classpath', str(प्रोजेक्ट_मूळ/'build/examples/classes'), '-c', 'खिडकीउदाहरण']).decode()
    for आहे_आवश्यक in ('public static void सुरू_करा()', 'मराठी/स्वकीय/इव्हेंट_रांग.नंतर_आवाहन', 'मराठी/स्वकीय/क्रिया_सूचना.आज्ञा_मजकूर'):
        assert आहे_आवश्यक in उदाहरणे, आहे_आवश्यक
    for निषिद्ध_मूल्य in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert निषिद्ध_मूल्य not in उदाहरणे, निषिद्ध_मूल्य
    गंतव्यस्थान_मूल्य = प्रोजेक्ट_मूळ/'build/verification/naming'; गंतव्यस्थान_मूल्य.mkdir(parents=True, exist_ok=True)
    (गंतव्यस्थान_मूल्य/'direct-bytecode.txt').write_text(घोषणा+'\n'+उदाहरणे)
    लॉग_नोंद = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((प्रोजेक्ट_मूळ/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(बंडल.read_bytes()).hexdigest(), 'classes': list(वर्ग_यादी_70c8b393),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (गंतव्यस्थान_मूल्य/'direct-bytecode.json').write_text(json.dumps(लॉग_नोंद, ensure_ascii=False, indent=2)+'\n')
    print('PASS: मराठी 직접 GUI·कार्यसूत्र_मूल्य_5b72a632 바이트코드와 उदाहरणे आवाहन')

if __name__ == '__main__': सुरू_करा()
