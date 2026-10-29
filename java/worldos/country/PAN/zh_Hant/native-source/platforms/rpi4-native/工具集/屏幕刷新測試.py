#!/usr/bin/env python3
"""實際資料 內核值 畫圖屏幕 코드를 宿主 記憶體資料 화면에 연결해 子部分值 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

項目根 = Path(__file__).resolve().parents[1]

def 運行():
    原始碼檔案集 = ['測試/刷新屏幕.c', '計算機/屏幕繪圖.c', '計算機/終端.c', '計算機/小組件.c']
    有效性驗證原始碼列 = 原始碼檔案集 + ['原始碼/幀緩衝組合器.java', '原始碼/板.java', '../../compiler/Java工具/提前所屬時間編譯器.java']
    目的地址值 = 項目根/'build/verification/redraw'; 目的地址值.mkdir(parents=True, exist_ok=True)
    日誌記錄 = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((項目根/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {名稱: hashlib.sha256((項目根/名稱).read_bytes()).hexdigest() for 名稱 in 有效性驗證原始碼列}}
    try:
        類別路徑 = 目的地址值/'classes'; 類別路徑.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(類別路徑),
            str(項目根/'原始碼/幀緩衝組合器.java'), str(項目根/'原始碼/板.java')])
        導出表 = {'jdraw_prepare': '準備', 'jdraw_width': '獲取寬度', 'jdraw_height': '獲取高度',
            'jdraw_count_low': '獲取計數器低位', 'jdraw_count_high': '獲取計數器高位', 'jdraw_clip': '裁剪',
            'jdraw_clip_value': '裁剪值', 'jdraw_begin': '運行', 'jdraw_end': '結束操作',
            'jdraw_pixel': '像素', 'jdraw_rectangle': '矩形填充', 'jdraw_pointer': '指針'}
        編譯過程命令 = ['sh', str(項目根.parents[1]/'compiler/提前所屬時間.sh'), '--entry', '幀緩衝組合器.獲取寬度', '-o', str(目的地址值/'繪圖.c')]
        for 連接, 函數 in 導出表.items(): 編譯過程命令.extend(['--export', 連接+'=幀緩衝組合器.'+函數])
        subprocess.check_call(編譯過程命令+[str(路徑) for 路徑 in sorted(類別路徑.glob('*.class'))])
        命令 = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + 原始碼檔案集
        繪圖目的地址 = 目的地址值/'繪圖.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(目的地址值/'繪圖.c'), '-o', str(繪圖目的地址)])
        subprocess.check_call(命令+[str(繪圖目的地址), 'build/terminal-font.S', '-o', str(目的地址值/'屏幕刷新測試')], cwd=str(項目根))
        結果 = subprocess.check_output([str(目的地址值/'屏幕刷新測試')], timeout=30).decode()
        (目的地址值/'有效性校驗.log').write_text(結果)
        是否已匹配 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', 結果)
        assert 是否已匹配 and 'PASS:' in 結果, 結果
        日誌記錄.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(是否已匹配[1]), mean_framebuffer_writes_per_move=int(是否已匹配[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(結果, end='')
    finally:
        (目的地址值/'report.json').write_text(json.dumps(日誌記錄, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': 運行()
