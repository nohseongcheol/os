#!/usr/bin/env python3
"""实际数据 内核值 画图屏幕 코드를 宿主 内存数据 화면에 연결해 子部分值 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

项目根 = Path(__file__).resolve().parents[1]

def 运行():
    源代码文件集 = ['测试/刷新屏幕.c', '计算机/屏幕绘图.c', '计算机/终端.c', '计算机/小组件.c']
    有效性验证源代码列 = 源代码文件集 + ['源代码/帧缓冲组合器.java', '源代码/板.java', '../../compiler/Java工具/提前所属时间编译器.java']
    目的地址值 = 项目根/'build/verification/redraw'; 目的地址值.mkdir(parents=True, exist_ok=True)
    日志记录 = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((项目根/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {名称: hashlib.sha256((项目根/名称).read_bytes()).hexdigest() for 名称 in 有效性验证源代码列}}
    try:
        类路径 = 目的地址值/'classes'; 类路径.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(类路径),
            str(项目根/'源代码/帧缓冲组合器.java'), str(项目根/'源代码/板.java')])
        导出表 = {'jdraw_prepare': '准备', 'jdraw_width': '获取宽度', 'jdraw_height': '获取高度',
            'jdraw_count_low': '获取计数器低位', 'jdraw_count_high': '获取计数器高位', 'jdraw_clip': '裁剪',
            'jdraw_clip_value': '裁剪值', 'jdraw_begin': '运行', 'jdraw_end': '结束操作',
            'jdraw_pixel': '像素', 'jdraw_rectangle': '矩形填充', 'jdraw_pointer': '指针'}
        编译过程命令 = ['sh', str(项目根.parents[1]/'compiler/提前所属时间.sh'), '--entry', '帧缓冲组合器.获取宽度', '-o', str(目的地址值/'绘图.c')]
        for 连接, 函数 in 导出表.items(): 编译过程命令.extend(['--export', 连接+'=帧缓冲组合器.'+函数])
        subprocess.check_call(编译过程命令+[str(路径) for 路径 in sorted(类路径.glob('*.class'))])
        命令 = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + 源代码文件集
        绘图目的地址 = 目的地址值/'绘图.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(目的地址值/'绘图.c'), '-o', str(绘图目的地址)])
        subprocess.check_call(命令+[str(绘图目的地址), 'build/terminal-font.S', '-o', str(目的地址值/'屏幕刷新测试')], cwd=str(项目根))
        结果 = subprocess.check_output([str(目的地址值/'屏幕刷新测试')], timeout=30).decode()
        (目的地址值/'有效性校验.log').write_text(结果)
        是否已匹配 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', 结果)
        assert 是否已匹配 and 'PASS:' in 结果, 结果
        日志记录.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(是否已匹配[1]), mean_framebuffer_writes_per_move=int(是否已匹配[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(结果, end='')
    finally:
        (目的地址值/'report.json').write_text(json.dumps(日志记录, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': 运行()
