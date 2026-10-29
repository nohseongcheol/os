#!/usr/bin/env python3
"""現在項目 커널과 実際データ 試験·배포물이 일치할 때에만 통합 妥当性検査 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

計画根 = Path(__file__).resolve().parents[1]

def ハッシュファイル(経路):
    計算結果 = hashlib.sha256()
    with 経路.open('rb') as ファイル:
        for データ in iter(lambda: ファイル.read(1048576), b''): 計算結果.update(データ)
    return 計算結果.hexdigest()

def 起動処理():
    妥当性経路 = 計画根/'build/verification'
    中核ハッシュ = ハッシュファイル(計画根/'build/kernel8.img')
    履歴記録記録一覧 = {}
    for 名前 in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        相対経路 = 'report.json' if 名前 == 'boot' else 名前+'/report.json'
        データ = json.loads((妥当性経路/相対経路).read_text())
        if not データ.get('passed') or データ.get('kernel_sha256') != 中核ハッシュ:
            raise SystemExit('現在項目 커널에 대한 成功値 기록이 필요합니다: '+相対経路)
        履歴記録記録一覧[名前] = {'passed': True, 'report': 相対経路}
    名前検査 = json.loads((妥当性経路/'naming/report.json').read_text())
    if not 名前検査['passed'] or not 名前検査['c_semantic_checked']: raise SystemExit('C 선언을 포함한 命名 検査項目 必要値')
    for 経路, 期待値 in 名前検査['c_source_sha256'].items():
        if ハッシュファイル(計画根/経路) != 期待値: raise SystemExit('命名 検査項目 後端値 바뀐 C ソース: '+経路)
    Java検査 = json.loads((妥当性経路/'jvm/report.json').read_text())
    直接画面 = json.loads((妥当性経路/'swing/report.json').read_text())
    if not 直接画面.get('direct_korean_gui'): raise SystemExit('日本語 직접 画面 命令実行 試験 必要値')
    バイト値検査 = json.loads((妥当性経路/'naming/direct-bytecode.json').read_text())
    if not バイト値検査['passed'] or バイト値検査['jar_sha256'] != ハッシュファイル(計画根/'dist/jkoros-native-korean.jar'):
        raise SystemExit('現在項目 日本語 라이브러리의 직접 呼出 バイトコード 検証 必要値')
    解像度検査 = json.loads((妥当性経路/'resolution/report.json').read_text())
    容量検査 = json.loads((妥当性経路/'resize/report.json').read_text())
    対象更新一覧検査 = json.loads((妥当性経路/'redraw/report.json').read_text())
    if not 対象更新一覧検査['passed'] or 対象更新一覧検査['kernel_sha256'] != 中核ハッシュ:
        raise SystemExit('現在項目 커널의 部分要素値 再読込 試験 必要値')
    for 経路, 期待値 in 対象更新一覧検査['source_sha256'].items():
        if ハッシュファイル(計画根/経路) != 期待値: raise SystemExit('部分要素値 再読込 試験 後端値 바뀐 ソース: '+経路)
    if not Java検査.get('direct_korean_thread_and_entry'):
        raise SystemExit('日本語 직접 가닥과 起動処理 入口点 試験 必要値')
    例検査 = json.loads((妥当性経路/'examples/report.json').read_text())
    if sorted(容量検査['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 隅値 容量 조절 試験 必要値')
    if not 例検査.get('swing_example_korean_input_button_label_and_close') or 例検査['examples_executed'] != 13:
        raise SystemExit('日本語 Swing 창을 포함한 用例 13개 試験 必要値')
    if sorted(解像度検査['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 実際データ 画面 試験 必要値')
    if Java検査['korean_library_sha256'] != ハッシュファイル(計画根/'dist/jkoros-native-korean.jar'):
        raise SystemExit('Java 試験 後端値 라이브러리가 바뀌었습니다.')
    for 名前 in ('韓国語通信機構試験','韓国語例外一覧試験'):
        if not any(入口値['name']==名前 and 入口値.get('openjdk_output_equal') for 入口値 in Java検査['tests']):
            raise SystemExit('OpenJDK 대조 試験 必要値: '+名前)
    例外一覧 = sorted(経路.stem for 経路 in (計画根/'日本語Java/日本語/内蔵').glob('*例外.java'))
    例外履歴記録 = (妥当性経路/'jvm/韓国語例外一覧試験.log').read_text().replace('\r\n','\n')
    for 名前 in 例外一覧:
        if '\n'+名前+'\n' not in 例外履歴記録: raise SystemExit('例外 生成·잡기·説明 試験 必要値: '+名前)
    仕様 = json.loads((計画根/'dist/manifest.json').read_text())
    if 仕様['image_sha256'] != ハッシュファイル(計画根/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('配布値 イメージ値 ハッシュファイル 불일치')
    with zipfile.ZipFile(str(計画根/'dist/jkoros-native-rpi4-boot.zip')) as パッケージ:
        if hashlib.sha256(パッケージ.read('kernel8.img')).hexdigest() != 中核ハッシュ:
            raise SystemExit('起動 ZIP 中核値 불일치')
        起動設定値 = パッケージ.read('config.txt')
        for 名前, 容量 in zip(('width', 'height'), 仕様['framebuffer_resolution']):
            if 'framebuffer_'+名前+'='+str(容量) not in 起動設定値.decode().splitlines():
                raise SystemExit('起動 ZIP 画面 設定値 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(計画根/'build')) as 一時値:
        複写済み値 = Path(一時値)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(計画根/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(複写済み値)])
        if ハッシュファイル(複写済み値) != 中核ハッシュ: raise SystemExit('SD イメージ値 中核値 불일치')
        設定値複写 = Path(一時値)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(計画根/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(設定値複写)])
        if 設定値複写.read_bytes() != 起動設定値: raise SystemExit('SD 영상과 ZIP 画面 設定値 불일치')
    履歴記録記録 = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': 中核ハッシュ,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 履歴記録記録一覧, 'naming_report': 'naming/report.json',
            'korean_exception_classes': 例外一覧, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 例検査['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(解像度検査['resolutions']),
            'sd_framebuffer_resolution': 仕様['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {名前:ハッシュファイル(計画根/'dist'/名前) for 名前 in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (妥当性経路/'native-runtime-summary.json').write_text(json.dumps(履歴記録記録,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 現在項目 커널의',len(履歴記録記録一覧),'개 통합 試験 履歴記録記録, 日本語 例外',len(例外一覧),'クラス定義, SD イメージ値·ZIP 判定等価')

if __name__ == '__main__': 起動処理()
