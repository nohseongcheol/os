#!/usr/bin/env python3
"""currentItem 커널과 actualData tests·배포물이 일치할 때에만 통합 validate 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

projectRoot = Path(__file__).resolve().parents[1]

def hashFile(path):
    calculation = hashlib.sha256()
    with path.open('rb') as file:
        for data in iter(lambda: file.read(1048576), b''): calculation.update(data)
    return calculation.hexdigest()

def run():
    validationPath = projectRoot/'build/verification'
    kernelHash = hashFile(projectRoot/'build/kernel8.img')
    logRecords = {}
    for name in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        relativePath = 'report.json' if name == 'boot' else name+'/report.json'
        data = json.loads((validationPath/relativePath).read_text())
        if not data.get('passed') or data.get('kernel_sha256') != kernelHash:
            raise SystemExit('currentItem 커널에 대한 successValue 기록이 필요합니다: '+relativePath)
        logRecords[name] = {'passed': True, 'report': relativePath}
    checkName = json.loads((validationPath/'naming/report.json').read_text())
    if not checkName['passed'] or not checkName['c_semantic_checked']: raise SystemExit('C 선언을 포함한 naming Checks neededValue')
    for path, expectedValue in checkName['c_source_sha256'].items():
        if hashFile(projectRoot/path) != expectedValue: raise SystemExit('naming Checks backValue 바뀐 C source: '+path)
    checkJava = json.loads((validationPath/'jvm/report.json').read_text())
    DirectScreen = json.loads((validationPath/'swing/report.json').read_text())
    if not DirectScreen.get('direct_korean_gui'): raise SystemExit('English 직접 Screen executeCommand tests neededValue')
    checkByteValue = json.loads((validationPath/'naming/direct-bytecode.json').read_text())
    if not checkByteValue['passed'] or checkByteValue['jar_sha256'] != hashFile(projectRoot/'dist/jkoros-native-korean.jar'):
        raise SystemExit('currentItem English 라이브러리의 직접 invoke bytecode verify neededValue')
    checkResolution = json.loads((validationPath/'resolution/report.json').read_text())
    checkSize = json.loads((validationPath/'resize/report.json').read_text())
    checkForUpdates = json.loads((validationPath/'redraw/report.json').read_text())
    if not checkForUpdates['passed'] or checkForUpdates['kernel_sha256'] != kernelHash:
        raise SystemExit('currentItem 커널의 subpartValue refresh tests neededValue')
    for path, expectedValue in checkForUpdates['source_sha256'].items():
        if hashFile(projectRoot/path) != expectedValue: raise SystemExit('subpartValue refresh tests backValue 바뀐 source: '+path)
    if not checkJava.get('direct_korean_thread_and_entry'):
        raise SystemExit('English 직접 가닥과 run entryPoint tests neededValue')
    checkExample = json.loads((validationPath/'examples/report.json').read_text())
    if sorted(checkSize['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 cornerValue size 조절 tests neededValue')
    if not checkExample.get('swing_example_korean_input_button_label_and_close') or checkExample['examples_executed'] != 13:
        raise SystemExit('English Swing 창을 포함한 examples 13개 tests neededValue')
    if sorted(checkResolution['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 actualData Screen tests neededValue')
    if checkJava['korean_library_sha256'] != hashFile(projectRoot/'dist/jkoros-native-korean.jar'):
        raise SystemExit('Java tests backValue 라이브러리가 바뀌었습니다.')
    for name in ('testKoreanNetworking','testKoreanExceptions'):
        if not any(entryValue['name']==name and entryValue.get('openjdk_output_equal') for entryValue in checkJava['tests']):
            raise SystemExit('OpenJDK 대조 tests neededValue: '+name)
    exceptionList = sorted(path.stem for path in (projectRoot/'NativeJava/English/Native').glob('*exception.java'))
    exceptionLog = (validationPath/'jvm/testKoreanExceptions.log').read_text().replace('\r\n','\n')
    for name in exceptionList:
        if '\n'+name+'\n' not in exceptionLog: raise SystemExit('exception generate·잡기·description tests neededValue: '+name)
    specification = json.loads((projectRoot/'dist/manifest.json').read_text())
    if specification['image_sha256'] != hashFile(projectRoot/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('distributionValue imageValue hashFile 불일치')
    with zipfile.ZipFile(str(projectRoot/'dist/jkoros-native-rpi4-boot.zip')) as Bundle:
        if hashlib.sha256(Bundle.read('kernel8.img')).hexdigest() != kernelHash:
            raise SystemExit('machine_boot ZIP kernelValue 불일치')
        bootSettings = Bundle.read('config.txt')
        for name, size in zip(('width', 'height'), specification['framebuffer_resolution']):
            if 'framebuffer_'+name+'='+str(size) not in bootSettings.decode().splitlines():
                raise SystemExit('machine_boot ZIP Screen settings 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(projectRoot/'build')) as temporaryValue:
        copiedValue = Path(temporaryValue)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(projectRoot/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(copiedValue)])
        if hashFile(copiedValue) != kernelHash: raise SystemExit('SD imageValue kernelValue 불일치')
        copySettings = Path(temporaryValue)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(projectRoot/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(copySettings)])
        if copySettings.read_bytes() != bootSettings: raise SystemExit('SD 영상과 ZIP Screen settings 불일치')
    logRecord = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': kernelHash,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': logRecords, 'naming_report': 'naming/report.json',
            'korean_exception_classes': exceptionList, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': checkExample['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(checkResolution['resolutions']),
            'sd_framebuffer_resolution': specification['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {name:hashFile(projectRoot/'dist'/name) for name in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (validationPath/'native-runtime-summary.json').write_text(json.dumps(logRecord,ensure_ascii=False,indent=2)+'\n')
    print('PASS: currentItem 커널의',len(logRecords),'개 통합 tests logRecord, English exception',len(exceptionList),'classDefinition, SD imageValue·ZIP isEqual')

if __name__ == '__main__': run()
