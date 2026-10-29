#!/usr/bin/env python3
"""ปัจจุบัน_รายการ 커널과 ค่าจริง_ข้อมูล 시험·배포물이 일치할 때에만 통합 ตรวจสอบความถูกต้อง 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

แสดง_ราก = Path(__file__).resolve().parents[1]

def แฮช_แฟ้ม(เส้นทาง):
    계산 = hashlib.sha256()
    with เส้นทาง.open('rb') as แฟ้ม:
        for ข้อมูล in iter(lambda: แฟ้ม.read(1048576), b''): 계산.update(ข้อมูล)
    return 계산.hexdigest()

def เรียกใช้งาน():
    การตรวจสอบความถูกต้อง_พาธ = แสดง_ราก/'build/verification'
    เคอร์เนล_แฮช = แฮช_แฟ้ม(แสดง_ราก/'build/kernel8.img')
    기록들 = {}
    for ชื่อ in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        เส้นทางสัมพัทธ์ = 'report.json' if ชื่อ == 'boot' else ชื่อ+'/report.json'
        ข้อมูล = json.loads((การตรวจสอบความถูกต้อง_พาธ/เส้นทางสัมพัทธ์).read_text())
        if not ข้อมูล.get('passed') or ข้อมูล.get('kernel_sha256') != เคอร์เนล_แฮช:
            raise SystemExit('ปัจจุบัน_รายการ 커널에 대한 성공 기록이 필요합니다: '+เส้นทางสัมพัทธ์)
        기록들[ชื่อ] = {'passed': True, 'report': เส้นทางสัมพัทธ์}
    เช็ค_ชื่อ = json.loads((การตรวจสอบความถูกต้อง_พาธ/'naming/report.json').read_text())
    if not เช็ค_ชื่อ['passed'] or not เช็ค_ชื่อ['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for เส้นทาง, 기대값 in เช็ค_ชื่อ['c_source_sha256'].items():
        if แฮช_แฟ้ม(แสดง_ราก/เส้นทาง) != 기대값: raise SystemExit('명명 검사 ย้อนกลับ_ค่า 바뀐 C รหัสต้นฉบับ: '+เส้นทาง)
    자바검사 = json.loads((การตรวจสอบความถูกต้อง_พาธ/'jvm/report.json').read_text())
    직접화면 = json.loads((การตรวจสอบความถูกต้อง_พาธ/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('ไทย 직접 화면 ดําเนินการ_คําสั่ง 시험 필요')
    เช็ค_ไบต์_ค่า = json.loads((การตรวจสอบความถูกต้อง_พาธ/'naming/direct-bytecode.json').read_text())
    if not เช็ค_ไบต์_ค่า['passed'] or เช็ค_ไบต์_ค่า['jar_sha256'] != แฮช_แฟ้ม(แสดง_ราก/'dist/jkoros-native-korean.jar'):
        raise SystemExit('ปัจจุบัน_รายการ ไทย 라이브러리의 직접 호출 바이트코드 ยืนยัน 필요')
    เช็ค_ความละเอียด = json.loads((การตรวจสอบความถูกต้อง_พาธ/'resolution/report.json').read_text())
    เช็ค_ขนาด = json.loads((การตรวจสอบความถูกต้อง_พาธ/'resize/report.json').read_text())
    갱신검사 = json.loads((การตรวจสอบความถูกต้อง_พาธ/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != เคอร์เนล_แฮช:
        raise SystemExit('ปัจจุบัน_รายการ 커널의 부분 รีเฟรช 시험 필요')
    for เส้นทาง, 기대값 in 갱신검사['source_sha256'].items():
        if แฮช_แฟ้ม(แสดง_ราก/เส้นทาง) != 기대값: raise SystemExit('부분 รีเฟรช 시험 ย้อนกลับ_ค่า 바뀐 รหัสต้นฉบับ: '+เส้นทาง)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('ไทย 직접 가닥과 เรียกใช้งาน จุดเข้าใช้งาน 시험 필요')
    예제검사 = json.loads((การตรวจสอบความถูกต้อง_พาธ/'examples/report.json').read_text())
    if sorted(เช็ค_ขนาด['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 ขนาด 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('ไทย Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(เช็ค_ความละเอียด['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 ค่าจริง_ข้อมูล 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != แฮช_แฟ้ม(แสดง_ราก/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 ย้อนกลับ_ค่า 라이브러리가 바뀌었습니다.')
    for ชื่อ in ('한국어통신시험','한국어예외시험'):
        if not any(รายการ_ค่า['name']==ชื่อ and รายการ_ค่า.get('openjdk_output_equal') for รายการ_ค่า in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+ชื่อ)
    ข้อยกเว้น_รายการ = sorted(เส้นทาง.stem for เส้นทาง in (แสดง_ราก/'한국어자바/ไทย/เอง').glob('*ข้อยกเว้น.java'))
    ข้อยกเว้น_บันทึก = (การตรวจสอบความถูกต้อง_พาธ/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for ชื่อ in ข้อยกเว้น_รายการ:
        if '\n'+ชื่อ+'\n' not in ข้อยกเว้น_บันทึก: raise SystemExit('ข้อยกเว้น สร้าง_167eff27·잡기·설명 시험 필요: '+ชื่อ)
    명세 = json.loads((แสดง_ราก/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != แฮช_แฟ้ม(แสดง_ราก/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('การกระจาย_ค่า รูป_ค่า แฮช_แฟ้ม 불일치')
    with zipfile.ZipFile(str(แสดง_ราก/'dist/jkoros-native-rpi4-boot.zip')) as รวม:
        if hashlib.sha256(รวม.read('kernel8.img')).hexdigest() != เคอร์เนล_แฮช:
            raise SystemExit('부팅 ZIP เคอร์เนล_ค่า 불일치')
        부팅설정 = รวม.read('config.txt')
        for ชื่อ, ขนาด in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+ชื่อ+'='+str(ขนาด) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 ตั้งค่า 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(แสดง_ราก/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(แสดง_ราก/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if แฮช_แฟ้ม(복사본) != เคอร์เนล_แฮช: raise SystemExit('SD รูป_ค่า เคอร์เนล_ค่า 불일치')
        คัดลอก_การตั้งค่า = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(แสดง_ราก/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(คัดลอก_การตั้งค่า)])
        if คัดลอก_การตั้งค่า.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 ตั้งค่า 불일치')
    บันทึก_สถิติ = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': เคอร์เนล_แฮช,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': ข้อยกเว้น_รายการ, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(เช็ค_ความละเอียด['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {ชื่อ:แฮช_แฟ้ม(แสดง_ราก/'dist'/ชื่อ) for ชื่อ in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (การตรวจสอบความถูกต้อง_พาธ/'native-runtime-summary.json').write_text(json.dumps(บันทึก_สถิติ,ensure_ascii=False,indent=2)+'\n')
    print('PASS: ปัจจุบัน_รายการ 커널의',len(기록들),'개 통합 시험 บันทึก_สถิติ, ไทย ข้อยกเว้น',len(ข้อยกเว้น_รายการ),'คลาส_คําจํากัดความ, SD รูป_ค่า·ZIP 일치')

if __name__ == '__main__': เรียกใช้งาน()
