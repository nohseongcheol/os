#!/usr/bin/env python3
"""현재 커널과 бодит_өгөгдөл 시험·배포물이 일치할 때에만 통합 баталгаажуулах 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

기준 = Path(__file__).resolve().parents[1]

def Оруулсан_мэдээллийг_өөрчлөх_хэрэгсэл_файл(ЗАМ):
    계산 = hashlib.sha256()
    with ЗАМ.open('rb') as Файл:
        for өгөгдөл in iter(lambda: Файл.read(1048576), b''): 계산.update(өгөгдөл)
    return 계산.hexdigest()

def Ажиллуулах():
    баталгаажуулалт_зам = 기준/'build/verification'
    кернел_Оруулсан_мэдээллийг_өөрчлөх_хэрэгсэл = Оруулсан_мэдээллийг_өөрчлөх_хэрэгсэл_файл(기준/'build/kernel8.img')
    기록들 = {}
    for Нэр in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if Нэр == 'boot' else Нэр+'/report.json'
        өгөгдөл = json.loads((баталгаажуулалт_зам/상대경로).read_text())
        if not өгөгдөл.get('passed') or өгөгдөл.get('kernel_sha256') != кернел_Оруулсан_мэдээллийг_өөрчлөх_хэрэгсэл:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[Нэр] = {'passed': True, 'report': 상대경로}
    чек_нэр = json.loads((баталгаажуулалт_зам/'naming/report.json').read_text())
    if not чек_нэр['passed'] or not чек_нэр['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for ЗАМ, 기대값 in чек_нэр['c_source_sha256'].items():
        if Оруулсан_мэдээллийг_өөрчлөх_хэрэгсэл_файл(기준/ЗАМ) != 기대값: raise SystemExit('명명 검사 Буцах_утга 바뀐 C ЭХ: '+ЗАМ)
    자바검사 = json.loads((баталгаажуулалт_зам/'jvm/report.json').read_text())
    직접화면 = json.loads((баталгаажуулалт_зам/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('Монгол 직접 화면 Гүйцэтгэх_команд 시험 필요')
    чек_байт_утга = json.loads((баталгаажуулалт_зам/'naming/direct-bytecode.json').read_text())
    if not чек_байт_утга['passed'] or чек_байт_утга['jar_sha256'] != Оруулсан_мэдээллийг_өөрчлөх_хэрэгсэл_файл(기준/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 Монгол 라이브러리의 직접 호출 바이트코드 шалгах 필요')
    чек_нягтрал = json.loads((баталгаажуулалт_зам/'resolution/report.json').read_text())
    чек_хэмжээ = json.loads((баталгаажуулалт_зам/'resize/report.json').read_text())
    갱신검사 = json.loads((баталгаажуулалт_зам/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != кернел_Оруулсан_мэдээллийг_өөрчлөх_хэрэгсэл:
        raise SystemExit('현재 커널의 부분 сэргээх 시험 필요')
    for ЗАМ, 기대값 in 갱신검사['source_sha256'].items():
        if Оруулсан_мэдээллийг_өөрчлөх_хэрэгсэл_файл(기준/ЗАМ) != 기대값: raise SystemExit('부분 сэргээх 시험 Буцах_утга 바뀐 ЭХ: '+ЗАМ)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('Монгол 직접 가닥과 Ажиллуулах оролт_цэг 시험 필요')
    예제검사 = json.loads((баталгаажуулалт_зам/'examples/report.json').read_text())
    if sorted(чек_хэмжээ['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 Хэмжээ 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('Монгол Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(чек_нягтрал['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 бодит_өгөгдөл 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != Оруулсан_мэдээллийг_өөрчлөх_хэрэгсэл_файл(기준/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 Буцах_утга 라이브러리가 바뀌었습니다.')
    for Нэр in ('한국어통신시험','한국어예외시험'):
        if not any(оролт_утга['name']==Нэр and оролт_утга.get('openjdk_output_equal') for оролт_утга in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+Нэр)
    예외들 = sorted(ЗАМ.stem for ЗАМ in (기준/'한국어자바/Монгол/자체').glob('*예외.java'))
    예외기록 = (баталгаажуулалт_зам/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Нэр in 예외들:
        if '\n'+Нэр+'\n' not in 예외기록: raise SystemExit('예외 생성·잡기·설명 시험 필요: '+Нэр)
    명세 = json.loads((기준/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != Оруулсан_мэдээллийг_өөрчлөх_хэрэгсэл_файл(기준/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 зураг_утга Оруулсан_мэдээллийг_өөрчлөх_хэрэгсэл_файл 불일치')
    with zipfile.ZipFile(str(기준/'dist/jkoros-native-rpi4-boot.zip')) as багц:
        if hashlib.sha256(багц.read('kernel8.img')).hexdigest() != кернел_Оруулсан_мэдээллийг_өөрчлөх_хэрэгсэл:
            raise SystemExit('부팅 ZIP кернел_утга 불일치')
        부팅설정 = багц.read('config.txt')
        for Нэр, Хэмжээ in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+Нэр+'='+str(Хэмжээ) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 Тохиргоо 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(기준/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(기준/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if Оруулсан_мэдээллийг_өөрчлөх_хэрэгсэл_файл(복사본) != кернел_Оруулсан_мэдээллийг_өөрчлөх_хэрэгсэл: raise SystemExit('SD зураг_утга кернел_утга 불일치')
        хуулах_Тохиргоо = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(기준/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(хуулах_Тохиргоо)])
        if хуулах_Тохиргоо.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Тохиргоо 불일치')
    бичих_мөр_6e8b375a = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': кернел_Оруулсан_мэдээллийг_өөрчлөх_хэрэгсэл,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': 예외들, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(чек_нягтрал['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Нэр:Оруулсан_мэдээллийг_өөрчлөх_хэрэгсэл_файл(기준/'dist'/Нэр) for Нэр in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (баталгаажуулалт_зам/'native-runtime-summary.json').write_text(json.dumps(бичих_мөр_6e8b375a,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 бичих_мөр_6e8b375a, Монгол 예외',len(예외들),'класс_Тайлбар, SD зураг_утга·ZIP 일치')

if __name__ == '__main__': Ажиллуулах()
