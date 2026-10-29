#!/usr/bin/env python3
"""नामकरण क्लिप·अपवाद·경로를 검사한다. --시언어는 libclang घोषणा 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

प्रोजेक्ट_मूळ = Path(__file__).resolve().parents[1]
भांडार_मूळ = प्रोजेक्ट_मूळ.parents[1]

def सुरू_करा():
    व्याकरणविश्लेषक_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    व्याकरणविश्लेषक_48ee4b1b.add_argument('--सी_भाषा', action='store_true')
    बाबी = व्याकरणविश्लेषक_48ee4b1b.parse_args()
    अपयश = []
    काम_मूल्य = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    संचिका_संख्या = 0
    परिमापन_सारणी = {}
    बहुवितर्की_फलन = set()
    अमूर्तवाक्यवृक्ष_गाठी = {}
    सामायिक_संकलक = [भांडार_मूळ/'compiler/संकलक.py', भांडार_मूळ/'compiler/आगाऊ_संबंधित_वेळ_संकलक.py']
    for मार्ग in list((प्रोजेक्ट_मूळ/'साधने').glob('*.py')) + list((प्रोजेक्ट_मूळ/'उदाहरणे').rglob('*.py')) + सामायिक_संकलक:
        if मार्ग.name.endswith(('이름반영.py', '이름분석.py')): continue
        संचिका_संख्या += 1
        अमूर्तवाक्यवृक्ष_नोड = ast.parse(मार्ग.read_text()); अमूर्तवाक्यवृक्ष_गाठी[मार्ग] = अमूर्तवाक्यवृक्ष_नोड
        for प्रविष्टी_मूल्य in ast.walk(अमूर्तवाक्यवृक्ष_नोड):
            if isinstance(प्रविष्टी_मूल्य, ast.FunctionDef):
                परिमापन_सारणी.setdefault(प्रविष्टी_मूल्य.name, set()).update(परिमापन_वितर्क.arg for परिमापन_वितर्क in प्रविष्टी_मूल्य.args.args + प्रविष्टी_मूल्य.args.kwonlyargs)
                if प्रविष्टी_मूल्य.args.kwarg: बहुवितर्की_फलन.add(प्रविष्टी_मूल्य.name)
            if isinstance(प्रविष्टी_मूल्य, ast.ClassDef):
                for फलन_मूल्य in प्रविष्टी_मूल्य.body:
                    if isinstance(फलन_मूल्य, ast.FunctionDef) and फलन_मूल्य.name == '__init__':
                        परिमापन_सारणी.setdefault(प्रविष्टी_मूल्य.name, set()).update(परिमापन_वितर्क.arg for परिमापन_वितर्क in फलन_मूल्य.args.args + फलन_मूल्य.args.kwonlyargs)
            नाव = ''
            if isinstance(प्रविष्टी_मूल्य, (ast.FunctionDef, ast.ClassDef)): नाव = प्रविष्टी_मूल्य.name
            elif isinstance(प्रविष्टी_मूल्य, ast.Name) and isinstance(प्रविष्टी_मूल्य.ctx, ast.Store): नाव = प्रविष्टी_मूल्य.id
            elif isinstance(प्रविष्टी_मूल्य, ast.arg): नाव = प्रविष्टी_मूल्य.arg
            if नाव and नाव not in काम_मूल्य and all(ord(वर्ण_मूल्य)<128 for वर्ण_मूल्य in नाव):
                अपयश.append('{}:{}: {}'.format(मार्ग.relative_to(भांडार_मूळ), प्रविष्टी_मूल्य.lineno, नाव))
    for मार्ग, अमूर्तवाक्यवृक्ष_नोड in अमूर्तवाक्यवृक्ष_गाठी.items():
        for आवाहन in ast.walk(अमूर्तवाक्यवृक्ष_नोड):
            if not isinstance(आवाहन, ast.Call): continue
            नाव = आवाहन.func.id if isinstance(आवाहन.func, ast.Name) else आवाहन.func.attr if isinstance(आवाहन.func, ast.Attribute) else ''
            if नाव not in परिमापन_सारणी or नाव in बहुवितर्की_फलन or not any(ord(वर्ण_मूल्य)>127 for वर्ण_मूल्य in नाव): continue
            for परिमापन_वितर्क in आवाहन.keywords:
                if परिमापन_वितर्क.arg and परिमापन_वितर्क.arg not in परिमापन_सारणी[नाव]:
                    अपयश.append('{}:{}: {}의 매개변수 {}'.format(मार्ग.relative_to(भांडार_मूळ), आवाहन.lineno, नाव, परिमापन_वितर्क.arg))
    for ओळ in (प्रोजेक्ट_मूळ/'नामकरण/संचिका_नाव_प्रतिचित्रण.tsv').read_text().splitlines()[1:]:
        मागील_आयटम, सध्याचे_आयटम, प्रक्रिया_मूल्य_प्रविष्टी = ओळ.split('\t')
        if not (प्रोजेक्ट_मूळ/सध्याचे_आयटम).is_file(): अपयश.append('हलवा_मूल्य फाइल अनुपस्थित_पद्धत: '+सध्याचे_आयटम)
        if प्रक्रिया_मूल्य_प्रविष्टी == '호환진입점유지' and not (प्रोजेक्ट_मूळ/मागील_आयटम).is_file(): अपयश.append('호환 प्रविष्टी_गुण अनुपस्थित_पद्धत: '+मागील_आयटम)
    उदाहरणे = (प्रोजेक्ट_मूळ.parents[1]/'example/java/जाळेउदाहरण.java').read_text()
    for निषिद्ध_कॉल्स in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if निषिद्ध_कॉल्स in उदाहरणे: अपयश.append('네트워크 예제에 남은 표준 직접 आवाहन: '+निषिद्ध_कॉल्स)
    # 사용자가 읽는 Java 예제는 राखीव_शब्द/리터럴을 제외한 식별자도 सर्व_बांधणी 한국어다.
    राखीव_शब्द = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for मार्ग in sorted((प्रोजेक्ट_मूळ.parents[1]/'example/java').glob('*.java')):
        स्रोत = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', मार्ग.read_text())
        for नाव in re.findall(r'\b[^\W\d]\w*\b', स्रोत, re.UNICODE):
            if नाव not in राखीव_शब्द and all(ord(वर्ण_मूल्य)<128 for वर्ण_मूल्य in नाव):
                अपयश.append('{}: 예제의 영어 आयडेंटिफायर_मूल्य {}'.format(मार्ग.name, नाव))
    for नाव in ('창', 'बटण', 'लेबल', 'मजकूर_फील्_ड', 'पडदा_घटक', 'इव्हेंट_रांग', 'कार्यसूत्र', 'चालवण्यायोग्य_कार्य', 'क्रिया_ग्राहक', 'क्रिया_सूचना', 'पारपाडा_कार्य'):
        स्रोत = (प्रोजेक्ट_मूळ/'स्वकीय_जावा/मराठी/स्वकीय'/(नाव+'.java')).read_text()
        स्रोत = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', स्रोत)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', स्रोत):
            अपयश.append(नाव+': मराठी 직접 구현에 표준 ऑब्जेक्ट_मूल्य 래퍼가 남았습니다.')
    सी_उदाहरण = (प्रोजेक्ट_मूळ.parents[1]/'example/c/जाळेउदाहरण.c').read_text()
    for नाव in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if नाव in सी_उदाहरण: अपयश.append('C संचार 예제에 남은 표준 नाव: '+नाव)
    पायथन_उदाहरण = (प्रोजेक्ट_मूळ.parents[1]/'example/python/जाळेउदाहरण.py').read_text()
    if 'OSError' in पायथन_उदाहरण or '.args' in पायथन_उदाहरण: अपयश.append('Python संचार 예제에 남은 표준 अपवाद 직접 वापर_मूल्य')
    शीर्ष_मूल्य = (प्रोजेक्ट_मूळ.parents[1]/'posix-kor/arm64-native/घोषणाशीर्षे/संचारजाळे_द्विमानजोडणी.h').read_text()
    for नाव in ('क्लाउड_कुटुंब', 'स्वतंत्रसंदेश_संचारद्वार', 'स्वतंत्रसंदेश_प्रोटोकॉल', 'संचारद्वार_पत्ता', 'क्लाउड_संचारद्वार_पत्ता', 'संचारटोक_तयार_करा', 'स्वतंत्रसंदेश_डेटा_पाठवा'):
        if re.search(r'^#define\s+'+नाव+r'\b', शीर्ष_मूल्य, re.M): अपयश.append('C 직접 अंमलबजावणी 대신 मॅक्रो_मूल्य वापर_मूल्य: '+नाव)
    जावा_संचिका_संख्या = 0
    for मूळ_मूल्य in ('स्रोत', 'प्रयोक्ता/जावा', 'स्वकीय_जावा'):
        for मार्ग in (प्रोजेक्ट_मूळ/मूळ_मूल्य).rglob('*.java'):
            जावा_संचिका_संख्या += 1
            स्रोत = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', मार्ग.read_text())
            for आहे_जुळलेले in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', स्रोत):
                अपयश.append('{}: 한국어화되지 않은 घोषणा {}'.format(मार्ग.relative_to(प्रोजेक्ट_मूळ), आहे_जुळलेले[1]))
            if मूळ_मूल्य == 'स्वकीय_जावा' and re.search(r'\bthrows\s+[A-Za-z]', स्रोत):
                अपयश.append('{}: 공개 अपवाद घोषणा'.format(मार्ग.relative_to(प्रोजेक्ट_मूळ)))
    आडवे_86_जावा_संचिका_संख्या = 0
    प्रमाणित_जावा_नावे = {'String', 'length', 'charAt'}
    for मार्ग in sorted((भांडार_मूळ/'os/स्रोत').glob('*.java')):
        आडवे_86_जावा_संचिका_संख्या += 1
        स्रोत = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', मार्ग.read_text())
        for नाव in re.findall(r'\b[^\W\d]\w*\b', स्रोत, re.UNICODE):
            if नाव not in राखीव_शब्द | प्रमाणित_जावा_नावे and all(ord(वर्ण_मूल्य)<128 for वर्ण_मूल्य in नाव):
                अपयश.append('{}: स्वकीय 영어 आयडेंटिफायर_मूल्य {}'.format(मार्ग.relative_to(भांडार_मूळ), नाव))
    लॉग_नोंद = {'passed': False, 'python_files': संचिका_संख्या, 'java_files': जावा_संचिका_संख्या,
          'x86_java_files': आडवे_86_जावा_संचिका_संख्या, 'host_compiler_python_files': len(सामायिक_संकलक), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if बाबी.सी_भाषा:
        subprocess.check_call(['python3', str(प्रोजेक्ट_मूळ/'साधने/विश्लेषणकरा_सी_नावे.py')])
        विश्लेषणकरा_मूल्य = json.loads((प्रोजेक्ट_मूळ/'build/한국어화/시언어분석.json').read_text())
        अपयश.extend(str(त्रुटी) for त्रुटी in विश्लेषणकरा_मूल्य['त्रुटी'])
        निर्यात_करा_द्विमानजोडणी = set(json.loads((प्रोजेक्ट_मूळ/'नामकरण/प्रमाणित_नावे.json').read_text()))
        for प्रविष्टी_मूल्य in विश्लेषणकरा_मूल्य['घोषणा'].values():
            नाव = प्रविष्टी_मूल्य['नाव']; मार्ग = Path(प्रविष्टी_मूल्य['फाइल'])
            स्रोत = मार्ग.read_bytes()
            # मराठी 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if स्रोत[प्रविष्टी_मूल्य['ऑफसेट_मूल्य']:प्रविष्टी_मूल्य['ऑफसेट_मूल्य']+len(नाव)] == नाव.encode() and नाव not in निर्यात_करा_द्विमानजोडणी:
                अपयश.append('{}:{}: {}'.format(मार्ग.relative_to(प्रोजेक्ट_मूळ), प्रविष्टी_मूल्य['ओळ'], नाव))
        लॉग_नोंद['c_semantic_checked'] = True
        लॉग_नोंद['c_source_sha256'] = {str(Path(फाइल).relative_to(प्रोजेक्ट_मूळ)):हॅश_संचिका for फाइल,हॅश_संचिका in विश्लेषणकरा_मूल्य['원문해시'].items()}
    लॉग_नोंद['passed'] = not अपयश; लॉग_नोंद['failures'] = अपयश
    गंतव्यस्थान_मूल्य = प्रोजेक्ट_मूळ/'build/verification/naming'; गंतव्यस्थान_मूल्य.mkdir(parents=True, exist_ok=True)
    (गंतव्यस्थान_मूल्य/'report.json').write_text(json.dumps(लॉग_नोंद, ensure_ascii=False, indent=2)+'\n')
    if अपयश: raise SystemExit('\n'.join(अपयश))
    print('PASS: मराठी घोषणा·फाइल मार्ग·호환 प्रविष्टी_गुण·संचार उदाहरणे')

if __name__ == '__main__': सुरू_करा()
