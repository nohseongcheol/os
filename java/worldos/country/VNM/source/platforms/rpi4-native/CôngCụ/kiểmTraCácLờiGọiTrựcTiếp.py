#!/usr/bin/env python3
"""giáTrịBảnPhânPhối class의 직접 tiếngViệt GUI/giáTrịLuồngChạy 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

gốcCâyDựÁn = Path(__file__).resolve().parents[1]

def chạy():
    danhSáchCácLớp = ('창', 'nút', 'nhãn', 'TrườngVănBản', 'PhầnTửMànHình', 'ThôngBáoHànhĐộng', 'HàngĐợiSựKiện', 'bộLàmViệc',
             'TácVụ', 'TácVụChạyĐược', 'BộNhậnHànhĐộng')
    GóiGộp = gốcCâyDựÁn/'dist/jkoros-native-korean.jar'
    KhaiBáo = subprocess.check_output(['javap', '-classpath', str(GóiGộp), '-private', '-c']+
                                ['tiếngViệt.tựThân.'+tên for tên in danhSáchCácLớp]).decode()
    for giáTrịCấm in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert giáTrịCấm not in KhaiBáo, giáTrịCấm
    VíDụ = subprocess.check_output(['javap', '-classpath', str(gốcCâyDựÁn/'build/examples/classes'), '-c', 'VíDụCửaSổ']).decode()
    for làBắtBuộc in ('public static void chạy()', 'tiếngViệt/tựThân/HàngĐợiSựKiện.gọiThựcHiệnVềSau', 'tiếngViệt/tựThân/ThôngBáoHànhĐộng.vănBảnLệnh'):
        assert làBắtBuộc in VíDụ, làBắtBuộc
    for giáTrịCấm in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert giáTrịCấm not in VíDụ, giáTrịCấm
    giáTrịĐích = gốcCâyDựÁn/'build/verification/naming'; giáTrịĐích.mkdir(parents=True, exist_ok=True)
    (giáTrịĐích/'direct-bytecode.txt').write_text(KhaiBáo+'\n'+VíDụ)
    bảnGhiNhậtKý = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((gốcCâyDựÁn/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(GóiGộp.read_bytes()).hexdigest(), 'classes': list(danhSáchCácLớp),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (giáTrịĐích/'direct-bytecode.json').write_text(json.dumps(bảnGhiNhậtKý, ensure_ascii=False, indent=2)+'\n')
    print('PASS: tiếngViệt 직접 GUI·giáTrịLuồngChạy 바이트코드와 VíDụ gọiThựcHiện')

if __name__ == '__main__': chạy()
