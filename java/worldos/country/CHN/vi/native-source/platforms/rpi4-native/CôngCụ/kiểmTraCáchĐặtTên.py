#!/usr/bin/env python3
"""cáchĐặtTên cắtXén·ngoạiLệ·경로를 검사한다. --시언어는 libclang KhaiBáo 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

gốcCâyDựÁn = Path(__file__).resolve().parents[1]
gốcCâyKhoNguồn = gốcCâyDựÁn.parents[1]

def chạy():
    BộPhânTích = argparse.ArgumentParser(description=__doc__)
    BộPhânTích.add_argument('--ngônNgữC', action='store_true')
    cácĐốiSố = BộPhânTích.parse_args()
    cácThấtBại = []
    giáTrịQuyƯớc = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    sốLượngTệp = 0
    bảngTraThamSố = {}
    hàmBiếnĐốiSố = set()
    cácNútCâyCâyCúPháp = {}
    cácTrìnhBiênDịchDùngChung = [gốcCâyKhoNguồn/'compiler/TrìnhBiênDịch.py', gốcCâyKhoNguồn/'compiler/BiênDịchTrước.py']
    for đườngDẫn in list((gốcCâyDựÁn/'CôngCụ').glob('*.py')) + list((gốcCâyDựÁn/'VíDụ').rglob('*.py')) + cácTrìnhBiênDịchDùngChung:
        if đườngDẫn.name.endswith(('이름반영.py', '이름분석.py')): continue
        sốLượngTệp += 1
        nútCâyCâyCúPháp = ast.parse(đườngDẫn.read_text()); cácNútCâyCâyCúPháp[đườngDẫn] = nútCâyCâyCúPháp
        for giáTrịMục in ast.walk(nútCâyCâyCúPháp):
            if isinstance(giáTrịMục, ast.FunctionDef):
                bảngTraThamSố.setdefault(giáTrịMục.name, set()).update(đốiSốThamSố.arg for đốiSốThamSố in giáTrịMục.args.args + giáTrịMục.args.kwonlyargs)
                if giáTrịMục.args.kwarg: hàmBiếnĐốiSố.add(giáTrịMục.name)
            if isinstance(giáTrịMục, ast.ClassDef):
                for Hàm in giáTrịMục.body:
                    if isinstance(Hàm, ast.FunctionDef) and Hàm.name == '__init__':
                        bảngTraThamSố.setdefault(giáTrịMục.name, set()).update(đốiSốThamSố.arg for đốiSốThamSố in Hàm.args.args + Hàm.args.kwonlyargs)
            tên = ''
            if isinstance(giáTrịMục, (ast.FunctionDef, ast.ClassDef)): tên = giáTrịMục.name
            elif isinstance(giáTrịMục, ast.Name) and isinstance(giáTrịMục.ctx, ast.Store): tên = giáTrịMục.id
            elif isinstance(giáTrịMục, ast.arg): tên = giáTrịMục.arg
            if tên and tên not in giáTrịQuyƯớc and all(ord(giáTrịKýTự)<128 for giáTrịKýTự in tên):
                cácThấtBại.append('{}:{}: {}'.format(đườngDẫn.relative_to(gốcCâyKhoNguồn), giáTrịMục.lineno, tên))
    for đườngDẫn, nútCâyCâyCúPháp in cácNútCâyCâyCúPháp.items():
        for gọiThựcHiện in ast.walk(nútCâyCâyCúPháp):
            if not isinstance(gọiThựcHiện, ast.Call): continue
            tên = gọiThựcHiện.func.id if isinstance(gọiThựcHiện.func, ast.Name) else gọiThựcHiện.func.attr if isinstance(gọiThựcHiện.func, ast.Attribute) else ''
            if tên not in bảngTraThamSố or tên in hàmBiếnĐốiSố or not any(ord(giáTrịKýTự)>127 for giáTrịKýTự in tên): continue
            for đốiSốThamSố in gọiThựcHiện.keywords:
                if đốiSốThamSố.arg and đốiSốThamSố.arg not in bảngTraThamSố[tên]:
                    cácThấtBại.append('{}:{}: {}의 매개변수 {}'.format(đườngDẫn.relative_to(gốcCâyKhoNguồn), gọiThựcHiện.lineno, tên, đốiSốThamSố.arg))
    for dòng in (gốcCâyDựÁn/'cáchĐặtTên/phépÁnhXạTênTệp.tsv').read_text().splitlines()[1:]:
        phầnMụcTrướcĐó, phầnMụcHiệnTại, mụcGiáTrịTiếnTrình = dòng.split('\t')
        if not (gốcCâyDựÁn/phầnMụcHiệnTại).is_file(): cácThấtBại.append('giáTrịDiChuyển Tệp phươngThứcThiếu: '+phầnMụcHiệnTại)
        if mụcGiáTrịTiếnTrình == '호환진입점유지' and not (gốcCâyDựÁn/phầnMụcTrướcĐó).is_file(): cácThấtBại.append('호환 điểmMục phươngThứcThiếu: '+phầnMụcTrướcĐó)
    VíDụ = (gốcCâyDựÁn.parents[1]/'example/java/VíDụMạng.java').read_text()
    for cácLờiGọiBịCấm in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if cácLờiGọiBịCấm in VíDụ: cácThấtBại.append('네트워크 예제에 남은 표준 직접 gọiThựcHiện: '+cácLờiGọiBịCấm)
    # 사용자가 읽는 Java 예제는 cácTừĐượcDànhTrước/리터럴을 제외한 식별자도 xâyDựngTấtCả 한국어다.
    cácTừĐượcDànhTrước = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for đườngDẫn in sorted((gốcCâyDựÁn.parents[1]/'example/java').glob('*.java')):
        mãNguồn = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', đườngDẫn.read_text())
        for tên in re.findall(r'\b[^\W\d]\w*\b', mãNguồn, re.UNICODE):
            if tên not in cácTừĐượcDànhTrước and all(ord(giáTrịKýTự)<128 for giáTrịKýTự in tên):
                cácThấtBại.append('{}: 예제의 영어 giáTrịĐịnhDanh {}'.format(đườngDẫn.name, tên))
    for tên in ('창', 'nút', 'nhãn', 'TrườngVănBản', 'PhầnTửMànHình', 'HàngĐợiSựKiện', 'bộLàmViệc', 'TácVụChạyĐược', 'BộNhậnHànhĐộng', 'ThôngBáoHànhĐộng', 'TácVụ'):
        mãNguồn = (gốcCâyDựÁn/'JavaTiếngViệt/tiếngViệt/tựThân'/(tên+'.java')).read_text()
        mãNguồn = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', mãNguồn)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', mãNguồn):
            cácThấtBại.append(tên+': tiếngViệt 직접 구현에 표준 giáTrịĐốiTượng 래퍼가 남았습니다.')
    víDụC = (gốcCâyDựÁn.parents[1]/'example/c/VíDụMạng.c').read_text()
    for tên in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if tên in víDụC: cácThấtBại.append('C TruyềnThông 예제에 남은 표준 tên: '+tên)
    víDụPython = (gốcCâyDựÁn.parents[1]/'example/python/VíDụMạng.py').read_text()
    if 'OSError' in víDụPython or '.args' in víDụPython: cácThấtBại.append('Python TruyềnThông 예제에 남은 표준 ngoạiLệ 직접 giáTrịDùng')
    giáTrịĐầu = (gốcCâyDựÁn.parents[1]/'posix-kor/arm64-native/TệpĐầuMục/ABIMạng.h').read_text()
    for tên in ('HọLiênMạng', 'ỔCắmMạngĐiệnDữLiệu', 'GiaoThứcĐiệnDữLiệu', 'ĐịaChỉỔCắmMạng', 'ĐịaChỉỔCắmMạngLiênMạng', 'tạoĐiểmCuối', 'gửiDữLiệuĐiệnDữLiệu'):
        if re.search(r'^#define\s+'+tên+r'\b', giáTrịĐầu, re.M): cácThấtBại.append('C 직접 phầnCàiĐặt 대신 giáTrịVĩLệnh giáTrịDùng: '+tên)
    sốLượngTệpJava = 0
    for giáTrịGốcCây in ('mãNguồn', 'NgườiDùng/Java', 'JavaTiếngViệt'):
        for đườngDẫn in (gốcCâyDựÁn/giáTrịGốcCây).rglob('*.java'):
            sốLượngTệpJava += 1
            mãNguồn = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', đườngDẫn.read_text())
            for làĐãKhớp in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', mãNguồn):
                cácThấtBại.append('{}: 한국어화되지 않은 KhaiBáo {}'.format(đườngDẫn.relative_to(gốcCâyDựÁn), làĐãKhớp[1]))
            if giáTrịGốcCây == 'JavaTiếngViệt' and re.search(r'\bthrows\s+[A-Za-z]', mãNguồn):
                cácThấtBại.append('{}: 공개 ngoạiLệ KhaiBáo'.format(đườngDẫn.relative_to(gốcCâyDựÁn)))
    sốTệpJavaX86 = 0
    cácTênJavaChuẩn = {'String', 'length', 'charAt'}
    for đườngDẫn in sorted((gốcCâyKhoNguồn/'os/mãNguồn').glob('*.java')):
        sốTệpJavaX86 += 1
        mãNguồn = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', đườngDẫn.read_text())
        for tên in re.findall(r'\b[^\W\d]\w*\b', mãNguồn, re.UNICODE):
            if tên not in cácTừĐượcDànhTrước | cácTênJavaChuẩn and all(ord(giáTrịKýTự)<128 for giáTrịKýTự in tên):
                cácThấtBại.append('{}: tựThân 영어 giáTrịĐịnhDanh {}'.format(đườngDẫn.relative_to(gốcCâyKhoNguồn), tên))
    bảnGhiNhậtKý = {'passed': False, 'python_files': sốLượngTệp, 'java_files': sốLượngTệpJava,
          'x86_java_files': sốTệpJavaX86, 'host_compiler_python_files': len(cácTrìnhBiênDịchDùngChung), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if cácĐốiSố.ngônNgữC:
        subprocess.check_call(['python3', str(gốcCâyDựÁn/'CôngCụ/phânTíchCácTênC.py')])
        phânTíchGiáTrị = json.loads((gốcCâyDựÁn/'build/한국어화/시언어분석.json').read_text())
        cácThấtBại.extend(str(lỗi) for lỗi in phânTíchGiáTrị['lỗi'])
        aBIXuất = set(json.loads((gốcCâyDựÁn/'cáchĐặtTên/cácTênChuẩn.json').read_text()))
        for giáTrịMục in phânTíchGiáTrị['KhaiBáo'].values():
            tên = giáTrịMục['tên']; đườngDẫn = Path(giáTrịMục['Tệp'])
            mãNguồn = đườngDẫn.read_bytes()
            # tiếngViệt 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if mãNguồn[giáTrịMục['giáTrịĐộLệch']:giáTrịMục['giáTrịĐộLệch']+len(tên)] == tên.encode() and tên not in aBIXuất:
                cácThấtBại.append('{}:{}: {}'.format(đườngDẫn.relative_to(gốcCâyDựÁn), giáTrịMục['dòng'], tên))
        bảnGhiNhậtKý['c_semantic_checked'] = True
        bảnGhiNhậtKý['c_source_sha256'] = {str(Path(Tệp).relative_to(gốcCâyDựÁn)):tệpMãBăm for Tệp,tệpMãBăm in phânTíchGiáTrị['원문해시'].items()}
    bảnGhiNhậtKý['passed'] = not cácThấtBại; bảnGhiNhậtKý['failures'] = cácThấtBại
    giáTrịĐích = gốcCâyDựÁn/'build/verification/naming'; giáTrịĐích.mkdir(parents=True, exist_ok=True)
    (giáTrịĐích/'report.json').write_text(json.dumps(bảnGhiNhậtKý, ensure_ascii=False, indent=2)+'\n')
    if cácThấtBại: raise SystemExit('\n'.join(cácThấtBại))
    print('PASS: tiếngViệt KhaiBáo·Tệp đườngDẫn·호환 điểmMục·TruyềnThông VíDụ')

if __name__ == '__main__': chạy()
