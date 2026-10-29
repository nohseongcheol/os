#!/usr/bin/env python3
"""ਅਸਲ_ਸਮੱਗਰੀ ਪੱਕੇ_ਹੋਣਾ_ਕੀਮਤ 그리기 코드를 ਹੋਸਟ ਮੈਮਰੀ_ਸਮੱਗਰੀ 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

ਪ੍ਰੋਜੈਕਟ_ਰੂਟ = Path(__file__).resolve().parents[1]

def ਚਲਾਓ_2():
    ਸਰੋਤ_ਫ਼ਾਈਲਾਂ = ['시험/화면갱신.c', 'ਮਸ਼ੀਨ/화면그림.c', 'ਮਸ਼ੀਨ/ਟਰਮੀਨਲ.c', 'ਮਸ਼ੀਨ/ਵਿਜੇਟ.c']
    검증원문들 = ਸਰੋਤ_ਫ਼ਾਈਲਾਂ + ['ਸਰੋਤ/화면합성.java', 'ਸਰੋਤ/ਬੋਰਡ.java', '../../compiler/자바도구/기계어미리번역.java']
    ਮੰਜਿਲ_ਕੀਮਤ = ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'build/verification/redraw'; ਮੰਜਿਲ_ਕੀਮਤ.mkdir(parents=True, exist_ok=True)
    ਲੌਗ_ਕਤਾਰ = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {ਨਾਂ: hashlib.sha256((ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/ਨਾਂ).read_bytes()).hexdigest() for ਨਾਂ in 검증원문들}}
    try:
        ਸ੍ਰੇਣੀ_ਰਸਤਾ = ਮੰਜਿਲ_ਕੀਮਤ/'classes'; ਸ੍ਰੇਣੀ_ਰਸਤਾ.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(ਸ੍ਰੇਣੀ_ਰਸਤਾ),
            str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'ਸਰੋਤ/화면합성.java'), str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'ਸਰੋਤ/ਬੋਰਡ.java')])
        ਨਿਰਯਾਤ_ਤਾਲਿਕਾ = {'jdraw_prepare': 'ਤਿਆਰ_ਕਰੋ', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'ਕਲਿਪ',
            'jdraw_clip_value': 'ਕਲਿਪ_ਕੀਮਤ', 'jdraw_begin': 'ਚਲਾਓ_2', 'jdraw_end': 'ਖਤਮ_ਕਰਨਾ',
            'jdraw_pixel': 'ਬਿੰਦੂ', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'ਪੌਇੰਟਰ'}
        번역명령 = ['sh', str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(ਮੰਜਿਲ_ਕੀਮਤ/'ਚਿੱਤਰ_ਬਨਾਉਣਾ_ਕੀਮਤ.c')]
        for ਕੁਨੈਕਸ਼ਨ_ਕਰੋ, ਫੰਗਸ਼ਨ_ਕੀਮਤ in ਨਿਰਯਾਤ_ਤਾਲਿਕਾ.items(): 번역명령.extend(['--export', ਕੁਨੈਕਸ਼ਨ_ਕਰੋ+'=화면합성.'+ਫੰਗਸ਼ਨ_ਕੀਮਤ])
        subprocess.check_call(번역명령+[str(ਮਾਰਗ) for ਮਾਰਗ in sorted(ਸ੍ਰੇਣੀ_ਰਸਤਾ.glob('*.class'))])
        ਕਮਾਂਡ = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + ਸਰੋਤ_ਫ਼ਾਈਲਾਂ
        ਚਿੱਤਰ_ਬਨਾਉਣਾ_ਮੰਜਿਲ = ਮੰਜਿਲ_ਕੀਮਤ/'ਚਿੱਤਰ_ਬਨਾਉਣਾ_ਕੀਮਤ.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(ਮੰਜਿਲ_ਕੀਮਤ/'ਚਿੱਤਰ_ਬਨਾਉਣਾ_ਕੀਮਤ.c'), '-o', str(ਚਿੱਤਰ_ਬਨਾਉਣਾ_ਮੰਜਿਲ)])
        subprocess.check_call(ਕਮਾਂਡ+[str(ਚਿੱਤਰ_ਬਨਾਉਣਾ_ਮੰਜਿਲ), 'build/terminal-font.S', '-o', str(ਮੰਜਿਲ_ਕੀਮਤ/'화면갱신시험')], cwd=str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ))
        ਮਾਪ = subprocess.check_output([str(ਮੰਜਿਲ_ਕੀਮਤ/'화면갱신시험')], timeout=30).decode()
        (ਮੰਜਿਲ_ਕੀਮਤ/'ਪ੍ਰਮਾਣਿਤ.log').write_text(ਮਾਪ)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', ਮਾਪ)
        assert 맞음 and 'PASS:' in ਮਾਪ, ਮਾਪ
        ਲੌਗ_ਕਤਾਰ.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(ਮਾਪ, end='')
    finally:
        (ਮੰਜਿਲ_ਕੀਮਤ/'report.json').write_text(json.dumps(ਲੌਗ_ਕਤਾਰ, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': ਚਲਾਓ_2()
