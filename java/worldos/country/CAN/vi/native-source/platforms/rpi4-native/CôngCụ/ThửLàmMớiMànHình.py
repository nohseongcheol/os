#!/usr/bin/env python3
"""dữLiệuThựcTế giáTrịNhân mànHìnhTô 코드를 Chủ dữLiệuBộNhớ 화면에 연결해 giáTrịPhầnCon 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

gốcCâyDựÁn = Path(__file__).resolve().parents[1]

def chạy():
    cácTệpNguồn = ['KiểmThử/làmMớiMànHình.c', 'máy/bảnVẽMànHình.c', 'máy/thiếtBịCuối.c', 'máy/ThànhTốGiaoDiện.c']
    cácNguồnViệcThẩmĐịnh = cácTệpNguồn + ['mãNguồn/BộGhépBộĐệmKhung.java', 'mãNguồn/BoMạch.java', '../../compiler/CôngCụJava/BiênDịchTrước.java']
    giáTrịĐích = gốcCâyDựÁn/'build/verification/redraw'; giáTrịĐích.mkdir(parents=True, exist_ok=True)
    bảnGhiNhậtKý = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((gốcCâyDựÁn/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {tên: hashlib.sha256((gốcCâyDựÁn/tên).read_bytes()).hexdigest() for tên in cácNguồnViệcThẩmĐịnh}}
    try:
        đườngDẫnLớp = giáTrịĐích/'classes'; đườngDẫnLớp.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(đườngDẫnLớp),
            str(gốcCâyDựÁn/'mãNguồn/BộGhépBộĐệmKhung.java'), str(gốcCâyDựÁn/'mãNguồn/BoMạch.java')])
        bảngTraXuất = {'jdraw_prepare': 'chuẩnBị', 'jdraw_width': 'lấyRộng', 'jdraw_height': 'lấyCao',
            'jdraw_count_low': 'lấyThấpBộĐếm', 'jdraw_count_high': 'lấyCaoTrênBộĐếm', 'jdraw_clip': 'cắtXén',
            'jdraw_clip_value': 'giáTrịCắtXén', 'jdraw_begin': 'chạy', 'jdraw_end': 'hoànThành',
            'jdraw_pixel': 'điểmẢnh', 'jdraw_rectangle': 'lấpHìnhChữNhật', 'jdraw_pointer': 'conTrỏ'}
        lệnhViệcBiênDịch = ['sh', str(gốcCâyDựÁn.parents[1]/'compiler/thờiGianCủaTrước.sh'), '--entry', 'BộGhépBộĐệmKhung.lấyRộng', '-o', str(giáTrịĐích/'HìnhVẽ.c')]
        for nốiKết, Hàm in bảngTraXuất.items(): lệnhViệcBiênDịch.extend(['--export', nốiKết+'=BộGhépBộĐệmKhung.'+Hàm])
        subprocess.check_call(lệnhViệcBiênDịch+[str(đườngDẫn) for đườngDẫn in sorted(đườngDẫnLớp.glob('*.class'))])
        lệnh = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + cácTệpNguồn
        đíchBảnVẽ = giáTrịĐích/'HìnhVẽ.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(giáTrịĐích/'HìnhVẽ.c'), '-o', str(đíchBảnVẽ)])
        subprocess.check_call(lệnh+[str(đíchBảnVẽ), 'build/terminal-font.S', '-o', str(giáTrịĐích/'ThửLàmMớiMànHình')], cwd=str(gốcCâyDựÁn))
        kếtQuả = subprocess.check_output([str(giáTrịĐích/'ThửLàmMớiMànHình')], timeout=30).decode()
        (giáTrịĐích/'thẩmĐịnh.log').write_text(kếtQuả)
        làĐãKhớp = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', kếtQuả)
        assert làĐãKhớp and 'PASS:' in kếtQuả, kếtQuả
        bảnGhiNhậtKý.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(làĐãKhớp[1]), mean_framebuffer_writes_per_move=int(làĐãKhớp[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(kếtQuả, end='')
    finally:
        (giáTrịĐích/'report.json').write_text(json.dumps(bảnGhiNhậtKý, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': chạy()
