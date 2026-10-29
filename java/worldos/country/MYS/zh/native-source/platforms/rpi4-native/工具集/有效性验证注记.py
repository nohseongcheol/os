#!/usr/bin/env python3
"""当前项目 커널과 实际数据 测试·배포물이 일치할 때에만 통합 有效性校验 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

项目根 = Path(__file__).resolve().parents[1]

def 哈希文件(路径):
    计算结果 = hashlib.sha256()
    with 路径.open('rb') as 文件:
        for 数据 in iter(lambda: 文件.read(1048576), b''): 计算结果.update(数据)
    return 计算结果.hexdigest()

def 运行():
    有效性验证路径 = 项目根/'build/verification'
    内核哈希 = 哈希文件(项目根/'build/kernel8.img')
    日志记录列 = {}
    for 名称 in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        相对路径 = 'report.json' if 名称 == 'boot' else 名称+'/report.json'
        数据 = json.loads((有效性验证路径/相对路径).read_text())
        if not 数据.get('passed') or 数据.get('kernel_sha256') != 内核哈希:
            raise SystemExit('当前项目 커널에 대한 成功值 기록이 필요합니다: '+相对路径)
        日志记录列[名称] = {'passed': True, 'report': 相对路径}
    检查名称 = json.loads((有效性验证路径/'naming/report.json').read_text())
    if not 检查名称['passed'] or not 检查名称['c_semantic_checked']: raise SystemExit('C 선언을 포함한 命名 检查项 所需条件值')
    for 路径, 预期值 in 检查名称['c_source_sha256'].items():
        if 哈希文件(项目根/路径) != 预期值: raise SystemExit('命名 检查项 后端值 바뀐 C 源代码: '+路径)
    检查Java = json.loads((有效性验证路径/'jvm/report.json').read_text())
    直接屏幕 = json.loads((有效性验证路径/'swing/report.json').read_text())
    if not 直接屏幕.get('direct_korean_gui'): raise SystemExit('中文 직접 屏幕 执行命令 测试 所需条件值')
    检查字节值 = json.loads((有效性验证路径/'naming/direct-bytecode.json').read_text())
    if not 检查字节值['passed'] or 检查字节值['jar_sha256'] != 哈希文件(项目根/'dist/jkoros-native-korean.jar'):
        raise SystemExit('当前项目 中文 라이브러리의 직접 调用 字节码 验证 所需条件值')
    检查分辨率 = json.loads((有效性验证路径/'resolution/report.json').read_text())
    检查大小 = json.loads((有效性验证路径/'resize/report.json').read_text())
    检查用于汇报 = json.loads((有效性验证路径/'redraw/report.json').read_text())
    if not 检查用于汇报['passed'] or 检查用于汇报['kernel_sha256'] != 内核哈希:
        raise SystemExit('当前项目 커널의 子部分值 刷新 测试 所需条件值')
    for 路径, 预期值 in 检查用于汇报['source_sha256'].items():
        if 哈希文件(项目根/路径) != 预期值: raise SystemExit('子部分值 刷新 测试 后端值 바뀐 源代码: '+路径)
    if not 检查Java.get('direct_korean_thread_and_entry'):
        raise SystemExit('中文 직접 가닥과 运行 条目分 测试 所需条件值')
    检查示例 = json.loads((有效性验证路径/'examples/report.json').read_text())
    if sorted(检查大小['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 角值 大小 조절 测试 所需条件值')
    if not 检查示例.get('swing_example_korean_input_button_label_and_close') or 检查示例['examples_executed'] != 13:
        raise SystemExit('中文 Swing 창을 포함한 用例 13개 测试 所需条件值')
    if sorted(检查分辨率['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 实际数据 屏幕 测试 所需条件值')
    if 检查Java['korean_library_sha256'] != 哈希文件(项目根/'dist/jkoros-native-korean.jar'):
        raise SystemExit('Java 测试 后端值 라이브러리가 바뀌었습니다.')
    for 名称 in ('测试韩语联网','测试韩语异常列'):
        if not any(条目值['name']==名称 and 条目值.get('openjdk_output_equal') for 条目值 in 检查Java['tests']):
            raise SystemExit('OpenJDK 대조 测试 所需条件值: '+名称)
    异常列表 = sorted(路径.stem for 路径 in (项目根/'中文Java/中文/内置').glob('*异常.java'))
    异常日志 = (有效性验证路径/'jvm/测试韩语异常列.log').read_text().replace('\r\n','\n')
    for 名称 in 异常列表:
        if '\n'+名称+'\n' not in 异常日志: raise SystemExit('异常 生成·잡기·说明 测试 所需条件值: '+名称)
    规格 = json.loads((项目根/'dist/manifest.json').read_text())
    if 规格['image_sha256'] != 哈希文件(项目根/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('分发值 映像值 哈希文件 불일치')
    with zipfile.ZipFile(str(项目根/'dist/jkoros-native-rpi4-boot.zip')) as 软件包:
        if hashlib.sha256(软件包.read('kernel8.img')).hexdigest() != 内核哈希:
            raise SystemExit('启动 ZIP 内核值 불일치')
        启动设置 = 软件包.read('config.txt')
        for 名称, 大小 in zip(('width', 'height'), 规格['framebuffer_resolution']):
            if 'framebuffer_'+名称+'='+str(大小) not in 启动设置.decode().splitlines():
                raise SystemExit('启动 ZIP 屏幕 设置 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(项目根/'build')) as 临时值:
        已复制值 = Path(临时值)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(项目根/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(已复制值)])
        if 哈希文件(已复制值) != 内核哈希: raise SystemExit('SD 映像值 内核值 불일치')
        复制设置 = Path(临时值)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(项目根/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(复制设置)])
        if 复制设置.read_bytes() != 启动设置: raise SystemExit('SD 영상과 ZIP 屏幕 设置 불일치')
    日志记录 = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': 内核哈希,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 日志记录列, 'naming_report': 'naming/report.json',
            'korean_exception_classes': 异常列表, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 检查示例['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(检查分辨率['resolutions']),
            'sd_framebuffer_resolution': 规格['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {名称:哈希文件(项目根/'dist'/名称) for 名称 in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (有效性验证路径/'native-runtime-summary.json').write_text(json.dumps(日志记录,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 当前项目 커널의',len(日志记录列),'개 통합 测试 日志记录, 中文 异常',len(异常列表),'类定义, SD 映像值·ZIP 是否相等')

if __name__ == '__main__': 运行()
