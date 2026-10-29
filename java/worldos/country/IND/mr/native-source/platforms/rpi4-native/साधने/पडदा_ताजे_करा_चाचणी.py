#!/usr/bin/env python3
"""वास्तविक_डेटा गाभा_मूल्य पेंट_पडदा 코드를 होस्ट स्मृती_डेटा 화면에 연결해 उपभाग_मूल्य 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

प्रोजेक्ट_मूळ = Path(__file__).resolve().parents[1]

def सुरू_करा():
    स्रोत_संचिका = ['चाचण्या/ताजे_करा_पडदा.c', 'मशीन/पडदा_रेखांकन.c', 'मशीन/टर्मिनल.c', 'मशीन/विजेट.c']
    पडताळणी_स्रोत = स्रोत_संचिका + ['स्रोत/प्रतिमास्मृती_संयोजक.java', 'स्रोत/बोर्ड.java', '../../compiler/जावा_साधने/आगाऊ_संबंधित_वेळ_संकलक.java']
    गंतव्यस्थान_मूल्य = प्रोजेक्ट_मूळ/'build/verification/redraw'; गंतव्यस्थान_मूल्य.mkdir(parents=True, exist_ok=True)
    लॉग_नोंद = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((प्रोजेक्ट_मूळ/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {नाव: hashlib.sha256((प्रोजेक्ट_मूळ/नाव).read_bytes()).hexdigest() for नाव in पडताळणी_स्रोत}}
    try:
        वर्ग_पथ = गंतव्यस्थान_मूल्य/'classes'; वर्ग_पथ.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(वर्ग_पथ),
            str(प्रोजेक्ट_मूळ/'स्रोत/प्रतिमास्मृती_संयोजक.java'), str(प्रोजेक्ट_मूळ/'स्रोत/बोर्ड.java')])
        निर्यात_करा_सारणी = {'jdraw_prepare': 'तयार_करणे', 'jdraw_width': 'रुंदी_मिळवा', 'jdraw_height': 'उंची_मिळवा',
            'jdraw_count_low': 'काउंटर_कमी_मिळवा', 'jdraw_count_high': 'काउंटर_उच्च_मिळवा', 'jdraw_clip': 'क्लिप',
            'jdraw_clip_value': 'क्लिप_मूल्य', 'jdraw_begin': 'सुरू_करा', 'jdraw_end': 'समाप्त',
            'jdraw_pixel': 'पिक्सेल', 'jdraw_rectangle': 'आयत_भरणे', 'jdraw_pointer': 'निर्देशक'}
        संकलन_आज्ञा = ['sh', str(प्रोजेक्ट_मूळ.parents[1]/'compiler/आगाऊ_संबंधित_वेळ.sh'), '--entry', 'प्रतिमास्मृती_संयोजक.रुंदी_मिळवा', '-o', str(गंतव्यस्थान_मूल्य/'रेखांकन_मूल्य.c')]
        for जोडा, फलन_मूल्य in निर्यात_करा_सारणी.items(): संकलन_आज्ञा.extend(['--export', जोडा+'=प्रतिमास्मृती_संयोजक.'+फलन_मूल्य])
        subprocess.check_call(संकलन_आज्ञा+[str(मार्ग) for मार्ग in sorted(वर्ग_पथ.glob('*.class'))])
        आदेश = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + स्रोत_संचिका
        रेखांकन_गंतव्यस्थान = गंतव्यस्थान_मूल्य/'रेखांकन_मूल्य.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(गंतव्यस्थान_मूल्य/'रेखांकन_मूल्य.c'), '-o', str(रेखांकन_गंतव्यस्थान)])
        subprocess.check_call(आदेश+[str(रेखांकन_गंतव्यस्थान), 'build/terminal-font.S', '-o', str(गंतव्यस्थान_मूल्य/'पडदा_ताजे_करा_चाचणी')], cwd=str(प्रोजेक्ट_मूळ))
        मोजमाप = subprocess.check_output([str(गंतव्यस्थान_मूल्य/'पडदा_ताजे_करा_चाचणी')], timeout=30).decode()
        (गंतव्यस्थान_मूल्य/'प्रमाणित.log').write_text(मोजमाप)
        आहे_जुळलेले = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', मोजमाप)
        assert आहे_जुळलेले and 'PASS:' in मोजमाप, मोजमाप
        लॉग_नोंद.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(आहे_जुळलेले[1]), mean_framebuffer_writes_per_move=int(आहे_जुळलेले[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(मोजमाप, end='')
    finally:
        (गंतव्यस्थान_मूल्य/'report.json').write_text(json.dumps(लॉग_नोंद, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': सुरू_करा()
