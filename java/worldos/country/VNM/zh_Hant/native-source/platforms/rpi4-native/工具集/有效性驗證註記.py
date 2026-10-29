#!/usr/bin/env python3
"""當前項目 커널과 實際資料 測試·배포물이 일치할 때에만 통합 有效性校驗 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

項目根 = Path(__file__).resolve().parents[1]

def 哈希檔案(路徑):
    計算結果 = hashlib.sha256()
    with 路徑.open('rb') as 檔案:
        for 資料 in iter(lambda: 檔案.read(1048576), b''): 計算結果.update(資料)
    return 計算結果.hexdigest()

def 運行():
    有效性驗證路徑 = 項目根/'build/verification'
    內核哈希 = 哈希檔案(項目根/'build/kernel8.img')
    日誌記錄列 = {}
    for 名稱 in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        相對路徑 = 'report.json' if 名稱 == 'boot' else 名稱+'/report.json'
        資料 = json.loads((有效性驗證路徑/相對路徑).read_text())
        if not 資料.get('passed') or 資料.get('kernel_sha256') != 內核哈希:
            raise SystemExit('當前項目 커널에 대한 成功值 기록이 필요합니다: '+相對路徑)
        日誌記錄列[名稱] = {'passed': True, 'report': 相對路徑}
    檢查名稱 = json.loads((有效性驗證路徑/'naming/report.json').read_text())
    if not 檢查名稱['passed'] or not 檢查名稱['c_semantic_checked']: raise SystemExit('C 선언을 포함한 命名 檢查項 所需條件值')
    for 路徑, 預期值 in 檢查名稱['c_source_sha256'].items():
        if 哈希檔案(項目根/路徑) != 預期值: raise SystemExit('命名 檢查項 後端值 바뀐 C 原始碼: '+路徑)
    檢查Java = json.loads((有效性驗證路徑/'jvm/report.json').read_text())
    直接屏幕 = json.loads((有效性驗證路徑/'swing/report.json').read_text())
    if not 直接屏幕.get('direct_korean_gui'): raise SystemExit('中文 직접 屏幕 執行命令 測試 所需條件值')
    檢查位元組值 = json.loads((有效性驗證路徑/'naming/direct-bytecode.json').read_text())
    if not 檢查位元組值['passed'] or 檢查位元組值['jar_sha256'] != 哈希檔案(項目根/'dist/jkoros-native-korean.jar'):
        raise SystemExit('當前項目 中文 라이브러리의 직접 調用 字節碼 驗證 所需條件值')
    檢查分辨率 = json.loads((有效性驗證路徑/'resolution/report.json').read_text())
    檢查大小 = json.loads((有效性驗證路徑/'resize/report.json').read_text())
    檢查用於彙報 = json.loads((有效性驗證路徑/'redraw/report.json').read_text())
    if not 檢查用於彙報['passed'] or 檢查用於彙報['kernel_sha256'] != 內核哈希:
        raise SystemExit('當前項目 커널의 子部分值 刷新 測試 所需條件值')
    for 路徑, 預期值 in 檢查用於彙報['source_sha256'].items():
        if 哈希檔案(項目根/路徑) != 預期值: raise SystemExit('子部分值 刷新 測試 後端值 바뀐 原始碼: '+路徑)
    if not 檢查Java.get('direct_korean_thread_and_entry'):
        raise SystemExit('中文 직접 가닥과 運行 條目分 測試 所需條件值')
    檢查範例 = json.loads((有效性驗證路徑/'examples/report.json').read_text())
    if sorted(檢查大小['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 角值 大小 조절 測試 所需條件值')
    if not 檢查範例.get('swing_example_korean_input_button_label_and_close') or 檢查範例['examples_executed'] != 13:
        raise SystemExit('中文 Swing 창을 포함한 範例 13개 測試 所需條件值')
    if sorted(檢查分辨率['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 實際資料 屏幕 測試 所需條件值')
    if 檢查Java['korean_library_sha256'] != 哈希檔案(項目根/'dist/jkoros-native-korean.jar'):
        raise SystemExit('Java 測試 後端值 라이브러리가 바뀌었습니다.')
    for 名稱 in ('測試韓語聯網','測試韓語異常列'):
        if not any(條目值['name']==名稱 and 條目值.get('openjdk_output_equal') for 條目值 in 檢查Java['tests']):
            raise SystemExit('OpenJDK 대조 測試 所需條件值: '+名稱)
    異常列表 = sorted(路徑.stem for 路徑 in (項目根/'中文Java/中文/內建').glob('*異常.java'))
    異常日誌 = (有效性驗證路徑/'jvm/測試韓語異常列.log').read_text().replace('\r\n','\n')
    for 名稱 in 異常列表:
        if '\n'+名稱+'\n' not in 異常日誌: raise SystemExit('異常 生成·잡기·說明 測試 所需條件值: '+名稱)
    規格 = json.loads((項目根/'dist/manifest.json').read_text())
    if 規格['image_sha256'] != 哈希檔案(項目根/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('分發值 映像值 哈希檔案 불일치')
    with zipfile.ZipFile(str(項目根/'dist/jkoros-native-rpi4-boot.zip')) as 軟件包:
        if hashlib.sha256(軟件包.read('kernel8.img')).hexdigest() != 內核哈希:
            raise SystemExit('啓動 ZIP 內核值 불일치')
        啓動設置 = 軟件包.read('config.txt')
        for 名稱, 大小 in zip(('width', 'height'), 規格['framebuffer_resolution']):
            if 'framebuffer_'+名稱+'='+str(大小) not in 啓動設置.decode().splitlines():
                raise SystemExit('啓動 ZIP 屏幕 設置 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(項目根/'build')) as 臨時值:
        已複製值 = Path(臨時值)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(項目根/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(已複製值)])
        if 哈希檔案(已複製值) != 內核哈希: raise SystemExit('SD 映像值 內核值 불일치')
        複製設置 = Path(臨時值)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(項目根/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(複製設置)])
        if 複製設置.read_bytes() != 啓動設置: raise SystemExit('SD 영상과 ZIP 屏幕 設置 불일치')
    日誌記錄 = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': 內核哈希,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 日誌記錄列, 'naming_report': 'naming/report.json',
            'korean_exception_classes': 異常列表, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 檢查範例['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(檢查分辨率['resolutions']),
            'sd_framebuffer_resolution': 規格['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {名稱:哈希檔案(項目根/'dist'/名稱) for 名稱 in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (有效性驗證路徑/'native-runtime-summary.json').write_text(json.dumps(日誌記錄,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 當前項目 커널의',len(日誌記錄列),'개 통합 測試 日誌記錄, 中文 異常',len(異常列表),'類別定義, SD 映像值·ZIP 是否相等')

if __name__ == '__main__': 運行()
