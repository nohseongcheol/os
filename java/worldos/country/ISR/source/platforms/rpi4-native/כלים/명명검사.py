#!/usr/bin/env python3
"""명명 לגזור·חריגה·경로를 검사한다. --시언어는 libclang הצהרה 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

לשקף_בסיס = Path(__file__).resolve().parents[1]
מאגר_בסיס = לשקף_בסיס.parents[1]

def הפעלה():
    מנתח_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    מנתח_48ee4b1b.add_argument('--מ_שפה', action='store_true')
    ארגומנטים = מנתח_48ee4b1b.parse_args()
    실패들 = []
    ערך_חוזה = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    파일수 = 0
    פרמטר_טבלה = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [מאגר_בסיס/'compiler/מהדר.py', מאגר_בסיס/'compiler/기계어미리번역.py']
    for נתיב in list((לשקף_בסיס/'כלים').glob('*.py')) + list((לשקף_בסיס/'예제').rglob('*.py')) + 공용번역기들:
        if נתיב.name.endswith(('이름반영.py', '이름분석.py')): continue
        파일수 += 1
        나무 = ast.parse(נתיב.read_text()); 나무들[נתיב] = 나무
        for ערך_ערך in ast.walk(나무):
            if isinstance(ערך_ערך, ast.FunctionDef):
                פרמטר_טבלה.setdefault(ערך_ערך.name, set()).update(פרמטר_ארגומנט.arg for פרמטר_ארגומנט in ערך_ערך.args.args + ערך_ערך.args.kwonlyargs)
                if ערך_ערך.args.kwarg: 가변매개함수.add(ערך_ערך.name)
            if isinstance(ערך_ערך, ast.ClassDef):
                for פונקציה_ערך in ערך_ערך.body:
                    if isinstance(פונקציה_ערך, ast.FunctionDef) and פונקציה_ערך.name == '__init__':
                        פרמטר_טבלה.setdefault(ערך_ערך.name, set()).update(פרמטר_ארגומנט.arg for פרמטר_ארגומנט in פונקציה_ערך.args.args + פונקציה_ערך.args.kwonlyargs)
            שם = ''
            if isinstance(ערך_ערך, (ast.FunctionDef, ast.ClassDef)): שם = ערך_ערך.name
            elif isinstance(ערך_ערך, ast.Name) and isinstance(ערך_ערך.ctx, ast.Store): שם = ערך_ערך.id
            elif isinstance(ערך_ערך, ast.arg): שם = ערך_ערך.arg
            if שם and שם not in ערך_חוזה and all(ord(תו_ערך)<128 for תו_ערך in שם):
                실패들.append('{}:{}: {}'.format(נתיב.relative_to(מאגר_בסיס), ערך_ערך.lineno, שם))
    for נתיב, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            שם = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if שם not in פרמטר_טבלה or שם in 가변매개함수 or not any(ord(תו_ערך)>127 for תו_ערך in שם): continue
            for פרמטר_ארגומנט in 호출.keywords:
                if פרמטר_ארגומנט.arg and פרמטר_ארגומנט.arg not in פרמטר_טבלה[שם]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(נתיב.relative_to(מאגר_בסיס), 호출.lineno, שם, פרמטר_ארגומנט.arg))
    for שורה in (לשקף_בסיס/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, נוכחי_פריט, תהליך_ערך_ערך = שורה.split('\t')
        if not (לשקף_בסיס/נוכחי_פריט).is_file(): 실패들.append('להעביר_ערך קובץ 없음: '+נוכחי_פריט)
        if תהליך_ערך_ערך == '호환진입점유지' and not (לשקף_בסיס/이전).is_file(): 실패들.append('호환 נקודת_כניסה 없음: '+이전)
    예제 = (לשקף_בסיס.parents[1]/'example/java/דוגמתרשת.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for נתיב in sorted((לשקף_בסיס.parents[1]/'example/java').glob('*.java')):
        קודמקור = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', נתיב.read_text())
        for שם in re.findall(r'\b[^\W\d]\w*\b', קודמקור, re.UNICODE):
            if שם not in 예약어 and all(ord(תו_ערך)<128 for תו_ערך in שם):
                실패들.append('{}: 예제의 영어 מזהה_ערך {}'.format(נתיב.name, שם))
    for שם in ('חלון', 'לחצן', 'תווית', 'שדה_טקסט', '화면구성요소', 'אירוע_תור', 'משימתרקע', '실행할일', '동작받이', 'המלצה_הודעה', '작업'):
        קודמקור = (לשקף_בסיס/'한국어자바/עברית/עצמי'/(שם+'.java')).read_text()
        קודמקור = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', קודמקור)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', קודמקור):
            실패들.append(שם+': עברית 직접 구현에 표준 אובייקט_ערך 래퍼가 남았습니다.')
    시언어예제 = (לשקף_בסיס.parents[1]/'example/c/דוגמתרשת.c').read_text()
    for שם in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if שם in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 שם: '+שם)
    파이썬예제 = (לשקף_בסיס.parents[1]/'example/python/דוגמתרשת.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 חריגה 직접 שימוש_ערך')
    ראש_ערך = (לשקף_בסיס.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for שם in ('ענן_משפחה', 'Socket_של_יחידת_נתונים', 'יחידת_נתונים_פרוטוקול', '통신주소', '인터넷통신주소', 'ליצור_משתתף', 'שלח_יחידת_נתונים_נתונים'):
        if re.search(r'^#define\s+'+שם+r'\b', ראש_ערך, re.M): 실패들.append('C 직접 구현 대신 מאקרו_ערך שימוש_ערך: '+שם)
    자바파일수 = 0
    for בסיס_ערך in ('קודמקור', 'משתמש/자바', '한국어자바'):
        for נתיב in (לשקף_בסיס/בסיס_ערך).rglob('*.java'):
            자바파일수 += 1
            קודמקור = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', נתיב.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', קודמקור):
                실패들.append('{}: 한국어화되지 않은 הצהרה {}'.format(נתיב.relative_to(לשקף_בסיס), 맞음[1]))
            if בסיס_ערך == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', קודמקור):
                실패들.append('{}: 공개 חריגה הצהרה'.format(נתיב.relative_to(לשקף_בסיס)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for נתיב in sorted((מאגר_בסיס/'os/קודמקור').glob('*.java')):
        x86자바파일수 += 1
        קודמקור = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', נתיב.read_text())
        for שם in re.findall(r'\b[^\W\d]\w*\b', קודמקור, re.UNICODE):
            if שם not in 예약어 | 표준자바이름 and all(ord(תו_ערך)<128 for תו_ערך in שם):
                실패들.append('{}: עצמי 영어 מזהה_ערך {}'.format(נתיב.relative_to(מאגר_בסיס), שם))
    לרשום_שיא = {'passed': False, 'python_files': 파일수, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if ארגומנטים.מ_שפה:
        subprocess.check_call(['python3', str(לשקף_בסיס/'כלים/시언어이름분석.py')])
        לנתח_ערך = json.loads((לשקף_בסיס/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(שגיאה) for שגיאה in לנתח_ערך['שגיאה'])
        공개규약 = set(json.loads((לשקף_בסיס/'명명/규격이름.json').read_text()))
        for ערך_ערך in לנתח_ערך['הצהרה'].values():
            שם = ערך_ערך['שם']; נתיב = Path(ערך_ערך['קובץ'])
            קודמקור = נתיב.read_bytes()
            # עברית 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if קודמקור[ערך_ערך['היסט_ערך']:ערך_ערך['היסט_ערך']+len(שם)] == שם.encode() and שם not in 공개규약:
                실패들.append('{}:{}: {}'.format(נתיב.relative_to(לשקף_בסיס), ערך_ערך['שורה'], שם))
        לרשום_שיא['c_semantic_checked'] = True
        לרשום_שיא['c_source_sha256'] = {str(Path(קובץ).relative_to(לשקף_בסיס)):קוד_Hash_קובץ for קובץ,קוד_Hash_קובץ in לנתח_ערך['원문해시'].items()}
    לרשום_שיא['passed'] = not 실패들; לרשום_שיא['failures'] = 실패들
    יעד_ערך = לשקף_בסיס/'build/verification/naming'; יעד_ערך.mkdir(parents=True, exist_ok=True)
    (יעד_ערך/'report.json').write_text(json.dumps(לרשום_שיא, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: עברית הצהרה·קובץ נתיב·호환 נקודת_כניסה·통신 예제')

if __name__ == '__main__': הפעלה()
