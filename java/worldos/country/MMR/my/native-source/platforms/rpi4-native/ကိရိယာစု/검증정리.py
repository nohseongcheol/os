#!/usr/bin/env python3
"""လက်ရှိအချက်အလက်တစ်ခု 커널과 တကယ့်ဒေတာ စမ်းသပ်မှု·배포물이 일치할 때에만 통합 မှန်ကန်ကြောင်းစစ် 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

စီမံကိန်းအမြစ် = Path(__file__).resolve().parents[1]

def ဖိုင်ဟက်ရှ်တွက်(လမ်း):
    တွက်ချက်မှု = hashlib.sha256()
    with လမ်း.open('rb') as ဖိုင်:
        for ဒေတာ in iter(lambda: ဖိုင်.read(1048576), b''): တွက်ချက်မှု.update(ဒေတာ)
    return တွက်ချက်မှု.hexdigest()

def လုပ်ဆောင်():
    검증경로 = စီမံကိန်းအမြစ်/'build/verification'
    커널해시 = ဖိုင်ဟက်ရှ်တွက်(စီမံကိန်းအမြစ်/'build/kernel8.img')
    기록들 = {}
    for အမည် in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        နှိုင်းယှဉ်ဆက်နွယ်လမ်းကြောင်း = 'report.json' if အမည် == 'boot' else အမည်+'/report.json'
        ဒေတာ = json.loads((검증경로/နှိုင်းယှဉ်ဆက်နွယ်လမ်းကြောင်း).read_text())
        if not ဒေတာ.get('passed') or ဒေတာ.get('kernel_sha256') != 커널해시:
            raise SystemExit('လက်ရှိအချက်အလက်တစ်ခု 커널에 대한 အောင်မြင်မှုတန်ဖိုး 기록이 필요합니다: '+နှိုင်းယှဉ်ဆက်နွယ်လမ်းကြောင်း)
        기록들[အမည်] = {'passed': True, 'report': နှိုင်းယှဉ်ဆက်နွယ်လမ်းကြောင်း}
    အမည်စစ် = json.loads((검증경로/'naming/report.json').read_text())
    if not အမည်စစ်['passed'] or not အမည်စစ်['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 စစ်ဆေးချက် 필요')
    for လမ်း, 기대값 in အမည်စစ်['c_source_sha256'].items():
        if ဖိုင်ဟက်ရှ်တွက်(စီမံကိန်းအမြစ်/လမ်း) != 기대값: raise SystemExit('명명 စစ်ဆေးချက် နောက်တန်ဖိုး 바뀐 C မူရင်းကုဒ်: '+လမ်း)
    Javaစစ် = json.loads((검증경로/'jvm/report.json').read_text())
    တိုက်ရိုက်မျက်နှာပြင် = json.loads((검증경로/'swing/report.json').read_text())
    if not တိုက်ရိုက်မျက်နှာပြင်.get('direct_korean_gui'): raise SystemExit('မြန်မာ 직접 မျက်နှာပြင် စက်မောင်း စမ်းသပ်မှု 필요')
    ဘိုက်တန်ဖိုးစစ် = json.loads((검증경로/'naming/direct-bytecode.json').read_text())
    if not ဘိုက်တန်ဖိုးစစ်['passed'] or ဘိုက်တန်ဖိုးစစ်['jar_sha256'] != ဖိုင်ဟက်ရှ်တွက်(စီမံကိန်းအမြစ်/'dist/jkoros-native-korean.jar'):
        raise SystemExit('လက်ရှိအချက်အလက်တစ်ခု မြန်မာ 라이브러리의 직접 ခေါ်လုပ် ဘိုက်ကုဒ် အတည်ပြု 필요')
    ကြည်လင်ပြတ်သားမှုစစ် = json.loads((검증경로/'resolution/report.json').read_text())
    အရွယ်စစ် = json.loads((검증경로/'resize/report.json').read_text())
    갱신검사 = json.loads((검증경로/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != 커널해시:
        raise SystemExit('လက်ရှိအချက်အလက်တစ်ခု 커널의 အစိတ်အပိုင်းတန်ဖိုး ပြန်လည်မွမ်းမံ စမ်းသပ်မှု 필요')
    for လမ်း, 기대값 in 갱신검사['source_sha256'].items():
        if ဖိုင်ဟက်ရှ်တွက်(စီမံကိန်းအမြစ်/လမ်း) != 기대값: raise SystemExit('အစိတ်အပိုင်းတန်ဖိုး ပြန်လည်မွမ်းမံ စမ်းသပ်မှု နောက်တန်ဖိုး 바뀐 မူရင်းကုဒ်: '+လမ်း)
    if not Javaစစ်.get('direct_korean_thread_and_entry'):
        raise SystemExit('မြန်မာ 직접 가닥과 လုပ်ဆောင် အချက်အမှတ်တစ်ခု စမ်းသပ်မှု 필요')
    ဥပမာစစ် = json.loads((검증경로/'examples/report.json').read_text())
    if sorted(အရွယ်စစ်['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 အရွယ် 조절 စမ်းသပ်မှု 필요')
    if not ဥပမာစစ်.get('swing_example_korean_input_button_label_and_close') or ဥပမာစစ်['examples_executed'] != 13:
        raise SystemExit('မြန်မာ Swing 창을 포함한 ဥပမာ 13개 စမ်းသပ်မှု 필요')
    if sorted(ကြည်လင်ပြတ်သားမှုစစ်['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 တကယ့်ဒေတာ မျက်နှာပြင် စမ်းသပ်မှု 필요')
    if Javaစစ်['korean_library_sha256'] != ဖိုင်ဟက်ရှ်တွက်(စီမံကိန်းအမြစ်/'dist/jkoros-native-korean.jar'):
        raise SystemExit('Java စမ်းသပ်မှု နောက်တန်ဖိုး 라이브러리가 바뀌었습니다.')
    for အမည် in ('မြန်မာကွန်ရက်စမ်းသပ်','မြန်မာခြွင်းချက်စမ်းသပ်'):
        if not any(အချက်တန်ဖိုး['name']==အမည် and အချက်တန်ဖိုး.get('openjdk_output_equal') for အချက်တန်ဖိုး in Javaစစ်['tests']):
            raise SystemExit('OpenJDK 대조 စမ်းသပ်မှု 필요: '+အမည်)
    ခြွင်းချက်စာရင်း = sorted(လမ်း.stem for လမ်း in (စီမံကိန်းအမြစ်/'မြန်မာJava/မြန်မာ/ကိုယ်ပိုင်').glob('*ခြွင်းချက်.java'))
    ခြွင်းချက်မှတ်တမ်း = (검증경로/'jvm/မြန်မာခြွင်းချက်စမ်းသပ်.log').read_text().replace('\r\n','\n')
    for အမည် in ခြွင်းချက်စာရင်း:
        if '\n'+အမည်+'\n' not in ခြွင်းချက်မှတ်တမ်း: raise SystemExit('ခြွင်းချက် ထုတ်လုပ်·잡기·ရှင်းလင်းချက် စမ်းသပ်မှု 필요: '+အမည်)
    သတ်မှတ်စံ = json.loads((စီမံကိန်းအမြစ်/'dist/manifest.json').read_text())
    if သတ်မှတ်စံ['image_sha256'] != ဖိုင်ဟက်ရှ်တွက်(စီမံကိန်းအမြစ်/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('ဖြန့်ချိမှုတန်ဖိုး စက်ပုံရိပ်တန်ဖိုး ဖိုင်ဟက်ရှ်တွက် 불일치')
    with zipfile.ZipFile(str(စီမံကိန်းအမြစ်/'dist/jkoros-native-rpi4-boot.zip')) as အထုပ်:
        if hashlib.sha256(အထုပ်.read('kernel8.img')).hexdigest() != 커널해시:
            raise SystemExit('စက်တင် ZIP အူတိုင်တန်ဖိုး 불일치')
        စက်တင်သတ်မှတ်ချက် = အထုပ်.read('config.txt')
        for အမည်, အရွယ် in zip(('width', 'height'), သတ်မှတ်စံ['framebuffer_resolution']):
            if 'framebuffer_'+အမည်+'='+str(အရွယ်) not in စက်တင်သတ်မှတ်ချက်.decode().splitlines():
                raise SystemExit('စက်တင် ZIP မျက်နှာပြင် သတ်မှတ်ချက် 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(စီမံကိန်းအမြစ်/'build')) as ယာယီတန်ဖိုး:
        복사본 = Path(ယာယီတန်ဖိုး)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(စီမံကိန်းအမြစ်/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if ဖိုင်ဟက်ရှ်တွက်(복사본) != 커널해시: raise SystemExit('SD စက်ပုံရိပ်တန်ဖိုး အူတိုင်တန်ဖိုး 불일치')
        သတ်မှတ်ချက်ကူး = Path(ယာယီတန်ဖိုး)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(စီမံကိန်းအမြစ်/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(သတ်မှတ်ချက်ကူး)])
        if သတ်မှတ်ချက်ကူး.read_bytes() != စက်တင်သတ်မှတ်ချက်: raise SystemExit('SD 영상과 ZIP မျက်နှာပြင် သတ်မှတ်ချက် 불일치')
    မှတ်တမ်းမှတ်တမ်းတစ်ခု = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': 커널해시,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': ခြွင်းချက်စာရင်း, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': ဥပမာစစ်['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(ကြည်လင်ပြတ်သားမှုစစ်['resolutions']),
            'sd_framebuffer_resolution': သတ်မှတ်စံ['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {အမည်:ဖိုင်ဟက်ရှ်တွက်(စီမံကိန်းအမြစ်/'dist'/အမည်) for အမည် in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (검증경로/'native-runtime-summary.json').write_text(json.dumps(မှတ်တမ်းမှတ်တမ်းတစ်ခု,ensure_ascii=False,indent=2)+'\n')
    print('PASS: လက်ရှိအချက်အလက်တစ်ခု 커널의',len(기록들),'개 통합 စမ်းသပ်မှု မှတ်တမ်းမှတ်တမ်းတစ်ခု, မြန်မာ ခြွင်းချက်',len(ခြွင်းချက်စာရင်း),'အတန်းသတ်မှတ်ချက်, SD စက်ပုံရိပ်တန်ဖိုး·ZIP ဖြစ်သောညီ')

if __name__ == '__main__': လုပ်ဆောင်()
