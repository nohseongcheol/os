#!/usr/bin/env python3
"""OpenJDK와 tựThân ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from thựcThiLệnh import gốcCâyDựÁn


def chạy():
    đầuRa = gốcCâyDựÁn / 'build/verification/jvm'
    đườngDẫnLớp = đầuRa / 'classes'; đườngDẫnLớp.mkdir(parents=True, exist_ok=True)
    góiGộpJava = gốcCâyDựÁn / 'dist/jkoros-native-korean.jar'
    DanhSáchMãNguồn = sorted((gốcCâyDựÁn / 'KiểmThử/Java').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(góiGộpJava), '-d', str(đườngDẫnLớp)] + [str(dữLiệuChuỗi) for dữLiệuChuỗi in DanhSáchMãNguồn])
    thửDanhSách = [('thửCácĐốiTượng', ['giáTrịNền', 'giáTrịNhánh', 'cóThểTính']), ('thửCácNgoạiLệ', []), ('ThửTậpHợp', []),
             ('thửCácLuồngChạy', ['giáTrịBộĐếm', 'HànhĐộngTácVụ', 'giáTrịLuồngChạy']), ('thửHangul', []), ('thửKếtNốiMạng', []), ('thửKếtNốiMạngTiếngHàn', []), ('thửCácNgoạiLệTiếngHàn', []), ('nguồnHangul', []), ('thửCácRanhGiới', []), ('thẩmĐịnh.thửGóiGộp', []), ('ThửTươngThíchMục', [])]
    báoCáoViệcThẩmĐịnh = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((gốcCâyDựÁn / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(góiGộpJava.read_bytes()).hexdigest(), 'tests': []}
    try:
        for tên, cóBaoGồm in thửDanhSách:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as đườngDẫnTạm:
                dựKiến = subprocess.check_output(['java', '-Xverify:all', '-cp', str(đườngDẫnLớp) + ':' + str(góiGộpJava), tên], cwd=đườngDẫnTạm, timeout=15).decode('utf-8')
            cácĐốiSốLệnh = ['python3', str(gốcCâyDựÁn / 'CôngCụ/thựcThiTệp.py'), str(đườngDẫnLớp / (tên.replace('.', '/') + '.class'))]
            if '.' in tên: cácĐốiSốLệnh += ['--class-name', tên]
            for baoGồm in cóBaoGồm: cácĐốiSốLệnh += ['--include', str(đườngDẫnLớp / (baoGồm + '.class'))]
            if tên == 'nguồnHangul': cácĐốiSốLệnh[2] = str(gốcCâyDựÁn / 'KiểmThử/Java/nguồnHangul.java')
            lượngĐãHoànTất = subprocess.run(cácĐốiSốLệnh, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            kếtQuảThựcTế = lượngĐãHoànTất.stdout.decode('utf-8').replace('\r\n', '\n')
            (đầuRa / (tên + '.log')).write_text(kếtQuảThựcTế, encoding='utf-8')
            làBằng = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", kếtQuảThựcTế, re.S)
            assert lượngĐãHoànTất.returncode == 0 and làBằng, (tên, kếtQuảThựcTế)
            kếtQuả = next(dữLiệuChuỗi for dữLiệuChuỗi in làBằng.groups() if dữLiệuChuỗi is not None) + '\n'
            assert kếtQuả == dựKiến, (tên, dựKiến, kếtQuả)
            báoCáoViệcThẩmĐịnh['tests'].append({'name': tên, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', tên, flush=True)
        # tựThân JVM에 직접 연결한 tiếngViệt giáTrịLuồngChạy/진입점은 OpenJDK용 래퍼가 아니다.
        lượngĐãHoànTất = subprocess.run(['python3', str(gốcCâyDựÁn/'CôngCụ/thựcThiTệp.py'), str(đườngDẫnLớp/'thửCácLuồngChạyTiếngHàn.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        kếtQuả = lượngĐãHoànTất.stdout.decode('utf-8').replace('\r\n', '\n')
        (đầuRa/'thửCácLuồngChạyTiếngHàn.log').write_text(kếtQuả)
        assert lượngĐãHoànTất.returncode == 0 and 'tiếngViệt 직접 giáTrịLuồngChạy giáTrịQua\n' in kếtQuả and '\nexit 0\n' in kếtQuả, kếtQuả
        báoCáoViệcThẩmĐịnh['direct_korean_thread_and_entry'] = True
        print('PASS: tiếngViệt 직접 giáTrịLuồngChạy·thựcThiTácVụ·chạy điểmMục', flush=True)
        hợpLệ = (đườngDẫnLớp / 'thửCácĐốiTượng.class').read_bytes()
        thửTrườngHợp = [('판거부', hợpLệ[:6] + b'\x00\x35' + hợpLệ[8:], 'supported class versions'),
                 ('잘린클래스', hợpLệ[:24], 'truncated class file')]
        báoCáoViệcThẩmĐịnh['rejection_tests'] = []
        for tên, dữLiệuNộiTải, vănBảnThôngBáo in thửTrườngHợp:
            thửDữLiệu = đầuRa / (tên + '.class'); thửDữLiệu.write_bytes(dữLiệuNộiTải)
            lượngĐãHoànTất = subprocess.run(['python3', str(gốcCâyDựÁn / 'CôngCụ/thựcThiTệp.py'), str(thửDữLiệu)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            vănBản = lượngĐãHoànTất.stdout.decode('utf-8').replace('\r\n', '\n')
            (đầuRa / (tên + '.log')).write_text(vănBản, encoding='utf-8')
            assert lượngĐãHoànTất.returncode == 1 and vănBảnThôngBáo in vănBản and 'exit 1\n' in vănBản, (tên, vănBản)
            báoCáoViệcThẩmĐịnh['rejection_tests'].append({'name': tên, 'passed': True})
            print('PASS (rejected):', tên, flush=True)
        báoCáoViệcThẩmĐịnh['passed'] = True
    finally:
        (đầuRa / 'report.json').write_text(json.dumps(báoCáoViệcThẩmĐịnh, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    chạy()
