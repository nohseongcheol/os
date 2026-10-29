#!/usr/bin/env python3
"""현재 커널과 ຕົວ_ຈິງ_ຂໍ້ມູນ 시험·배포물이 일치할 때에만 통합 ຮັບ_ຮອງ 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

ໂຄງ_ການ_ເລກຮາກ = Path(__file__).resolve().parents[1]

def ແຮຊ_ຟາຍ(ທາງໂຄຈອນ):
    계산 = hashlib.sha256()
    with ທາງໂຄຈອນ.open('rb') as ຟາຍ:
        for ຂໍ້ມູນ in iter(lambda: ຟາຍ.read(1048576), b''): 계산.update(ຂໍ້ມູນ)
    return 계산.hexdigest()

def ແລ່ນ():
    ໃຊ້ໄດ້_ທາງໂຄຈອນ = ໂຄງ_ການ_ເລກຮາກ/'build/verification'
    ແກນກາງ_ແຮຊ = ແຮຊ_ຟາຍ(ໂຄງ_ການ_ເລກຮາກ/'build/kernel8.img')
    기록들 = {}
    for ຊື່ in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if ຊື່ == 'boot' else ຊື່+'/report.json'
        ຂໍ້ມູນ = json.loads((ໃຊ້ໄດ້_ທາງໂຄຈອນ/상대경로).read_text())
        if not ຂໍ້ມູນ.get('passed') or ຂໍ້ມູນ.get('kernel_sha256') != ແກນກາງ_ແຮຊ:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[ຊື່] = {'passed': True, 'report': 상대경로}
    ເຊັກເງິນ_ຊື່ = json.loads((ໃຊ້ໄດ້_ທາງໂຄຈອນ/'naming/report.json').read_text())
    if not ເຊັກເງິນ_ຊື່['passed'] or not ເຊັກເງິນ_ຊື່['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for ທາງໂຄຈອນ, 기대값 in ເຊັກເງິນ_ຊື່['c_source_sha256'].items():
        if ແຮຊ_ຟາຍ(ໂຄງ_ການ_ເລກຮາກ/ທາງໂຄຈອນ) != 기대값: raise SystemExit('명명 검사 ກັບ_ຄືນ_ຄ່າ 바뀐 C ແຫຼ່ງທີ່ມາ: '+ທາງໂຄຈອນ)
    자바검사 = json.loads((ໃຊ້ໄດ້_ທາງໂຄຈອນ/'jvm/report.json').read_text())
    직접화면 = json.loads((ໃຊ້ໄດ້_ທາງໂຄຈອນ/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('한국어 직접 화면 ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ 시험 필요')
    ເຊັກເງິນ_ໄບ_ຄ່າ = json.loads((ໃຊ້ໄດ້_ທາງໂຄຈອນ/'naming/direct-bytecode.json').read_text())
    if not ເຊັກເງິນ_ໄບ_ຄ່າ['passed'] or ເຊັກເງິນ_ໄບ_ຄ່າ['jar_sha256'] != ແຮຊ_ຟາຍ(ໂຄງ_ການ_ເລກຮາກ/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 한국어 라이브러리의 직접 호출 바이트코드 확인 필요')
    ເຊັກເງິນ_ຄວາມລະອຽດ = json.loads((ໃຊ້ໄດ້_ທາງໂຄຈອນ/'resolution/report.json').read_text())
    ເຊັກເງິນ_ຂະ_ຫນາດ = json.loads((ໃຊ້ໄດ້_ທາງໂຄຈອນ/'resize/report.json').read_text())
    갱신검사 = json.loads((ໃຊ້ໄດ້_ທາງໂຄຈອນ/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != ແກນກາງ_ແຮຊ:
        raise SystemExit('현재 커널의 부분 ລຶ້ມຄືນໃຫມ່ 시험 필요')
    for ທາງໂຄຈອນ, 기대값 in 갱신검사['source_sha256'].items():
        if ແຮຊ_ຟາຍ(ໂຄງ_ການ_ເລກຮາກ/ທາງໂຄຈອນ) != 기대값: raise SystemExit('부분 ລຶ້ມຄືນໃຫມ່ 시험 ກັບ_ຄືນ_ຄ່າ 바뀐 ແຫຼ່ງທີ່ມາ: '+ທາງໂຄຈອນ)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('한국어 직접 가닥과 ແລ່ນ ເຂົ້າໃນ_ຈຸດ 시험 필요')
    예제검사 = json.loads((ໃຊ້ໄດ້_ທາງໂຄຈອນ/'examples/report.json').read_text())
    if sorted(ເຊັກເງິນ_ຂະ_ຫນາດ['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 ຂະ_ຫນາດ 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('한국어 Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(ເຊັກເງິນ_ຄວາມລະອຽດ['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 ຕົວ_ຈິງ_ຂໍ້ມູນ 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != ແຮຊ_ຟາຍ(ໂຄງ_ການ_ເລກຮາກ/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 ກັບ_ຄືນ_ຄ່າ 라이브러리가 바뀌었습니다.')
    for ຊື່ in ('한국어통신시험','한국어예외시험'):
        if not any(ເຂົ້າໃນ_ຄ່າ['name']==ຊື່ and ເຂົ້າໃນ_ຄ່າ.get('openjdk_output_equal') for ເຂົ້າໃນ_ຄ່າ in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+ຊື່)
    ຂໍ້ຍົກເວັ້ນ_ລາຍຊື່ = sorted(ທາງໂຄຈອນ.stem for ທາງໂຄຈອນ in (ໂຄງ_ການ_ເລກຮາກ/'한국어자바/한국어/자체').glob('*ຂໍ້ຍົກເວັ້ນ.java'))
    ຂໍ້ຍົກເວັ້ນ_ບັນທຶກ = (ໃຊ້ໄດ້_ທາງໂຄຈອນ/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for ຊື່ in ຂໍ້ຍົກເວັ້ນ_ລາຍຊື່:
        if '\n'+ຊື່+'\n' not in ຂໍ້ຍົກເວັ້ນ_ບັນທຶກ: raise SystemExit('ຂໍ້ຍົກເວັ້ນ ສ້າງ_167eff27·잡기·설명 시험 필요: '+ຊື່)
    명세 = json.loads((ໂຄງ_ການ_ເລກຮາກ/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != ແຮຊ_ຟາຍ(ໂຄງ_ການ_ເລກຮາກ/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 ຮູບ_ຄ່າ ແຮຊ_ຟາຍ 불일치')
    with zipfile.ZipFile(str(ໂຄງ_ການ_ເລກຮາກ/'dist/jkoros-native-rpi4-boot.zip')) as ຊຸດ:
        if hashlib.sha256(ຊຸດ.read('kernel8.img')).hexdigest() != ແກນກາງ_ແຮຊ:
            raise SystemExit('부팅 ZIP ແກນກາງ_ຄ່າ 불일치')
        부팅설정 = ຊຸດ.read('config.txt')
        for ຊື່, ຂະ_ຫນາດ in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+ຊື່+'='+str(ຂະ_ຫນາດ) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 ການຕັ້ງຄ່າ 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(ໂຄງ_ການ_ເລກຮາກ/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(ໂຄງ_ການ_ເລກຮາກ/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if ແຮຊ_ຟາຍ(복사본) != ແກນກາງ_ແຮຊ: raise SystemExit('SD ຮູບ_ຄ່າ ແກນກາງ_ຄ່າ 불일치')
        ກ່າຍ_ການຕັ້ງຄ່າ = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(ໂຄງ_ການ_ເລກຮາກ/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(ກ່າຍ_ການຕັ້ງຄ່າ)])
        if ກ່າຍ_ການຕັ້ງຄ່າ.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 ການຕັ້ງຄ່າ 불일치')
    ບັນທຶກ_ແຖວ = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': ແກນກາງ_ແຮຊ,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': ຂໍ້ຍົກເວັ້ນ_ລາຍຊື່, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(ເຊັກເງິນ_ຄວາມລະອຽດ['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {ຊື່:ແຮຊ_ຟາຍ(ໂຄງ_ການ_ເລກຮາກ/'dist'/ຊື່) for ຊື່ in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (ໃຊ້ໄດ້_ທາງໂຄຈອນ/'native-runtime-summary.json').write_text(json.dumps(ບັນທຶກ_ແຖວ,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 ບັນທຶກ_ແຖວ, 한국어 ຂໍ້ຍົກເວັ້ນ',len(ຂໍ້ຍົກເວັ້ນ_ລາຍຊື່),'ປະເພດສິ່ງຂອງ_ຄໍານິຍາມ, SD ຮູບ_ຄ່າ·ZIP 일치')

if __name__ == '__main__': ແລ່ນ()
