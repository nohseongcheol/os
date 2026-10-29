#!/usr/bin/env python3
"""ค่าจริง_ข้อมูล เคอร์เนล_ค่า 그리기 코드를 โฮสต์ ความจํา_ข้อมูล 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

แสดง_ราก = Path(__file__).resolve().parents[1]

def เรียกใช้งาน():
    แหล่ง_ไฟล์ = ['시험/화면갱신.c', 'เครื่อง/화면그림.c', 'เครื่อง/เทอร์มินัล.c', 'เครื่อง/วิดเจ็ต.c']
    검증원문들 = แหล่ง_ไฟล์ + ['รหัสต้นฉบับ/화면합성.java', 'รหัสต้นฉบับ/บอร์ด.java', '../../compiler/자바도구/기계어미리번역.java']
    ปลายทาง_ค่า_a0fbc067 = แสดง_ราก/'build/verification/redraw'; ปลายทาง_ค่า_a0fbc067.mkdir(parents=True, exist_ok=True)
    บันทึก_สถิติ = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((แสดง_ราก/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {ชื่อ: hashlib.sha256((แสดง_ราก/ชื่อ).read_bytes()).hexdigest() for ชื่อ in 검증원문들}}
    try:
        คลาส_พาธ = ปลายทาง_ค่า_a0fbc067/'classes'; คลาส_พาธ.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(คลาส_พาธ),
            str(แสดง_ราก/'รหัสต้นฉบับ/화면합성.java'), str(แสดง_ราก/'รหัสต้นฉบับ/บอร์ด.java')])
        ส่งออก_ตาราง = {'jdraw_prepare': 'จัดเตรียม', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'คลิป',
            'jdraw_clip_value': 'คลิป_ค่า', 'jdraw_begin': 'เรียกใช้งาน', 'jdraw_end': 'เสร็จสิ้น',
            'jdraw_pixel': 'พิกเซล', 'jdraw_rectangle': 'สี่เหลี่ยมผืนผ้า_เติม', 'jdraw_pointer': 'ตัวชี้'}
        번역명령 = ['sh', str(แสดง_ราก.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(ปลายทาง_ค่า_a0fbc067/'รูปวาด_ค่า.c')]
        for เชื่อมต่อ, ฟังก์ชัน_ค่า in ส่งออก_ตาราง.items(): 번역명령.extend(['--export', เชื่อมต่อ+'=화면합성.'+ฟังก์ชัน_ค่า])
        subprocess.check_call(번역명령+[str(เส้นทาง) for เส้นทาง in sorted(คลาส_พาธ.glob('*.class'))])
        คําสั่ง = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + แหล่ง_ไฟล์
        รูปวาด_ปลายทาง = ปลายทาง_ค่า_a0fbc067/'รูปวาด_ค่า.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(ปลายทาง_ค่า_a0fbc067/'รูปวาด_ค่า.c'), '-o', str(รูปวาด_ปลายทาง)])
        subprocess.check_call(คําสั่ง+[str(รูปวาด_ปลายทาง), 'build/terminal-font.S', '-o', str(ปลายทาง_ค่า_a0fbc067/'화면갱신시험')], cwd=str(แสดง_ราก))
        ผลลัพธ์ = subprocess.check_output([str(ปลายทาง_ค่า_a0fbc067/'화면갱신시험')], timeout=30).decode()
        (ปลายทาง_ค่า_a0fbc067/'ตรวจสอบความถูกต้อง.log').write_text(ผลลัพธ์)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', ผลลัพธ์)
        assert 맞음 and 'PASS:' in ผลลัพธ์, ผลลัพธ์
        บันทึก_สถิติ.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(ผลลัพธ์, end='')
    finally:
        (ปลายทาง_ค่า_a0fbc067/'report.json').write_text(json.dumps(บันทึก_สถิติ, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': เรียกใช้งาน()
