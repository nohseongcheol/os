#!/usr/bin/env python3
"""実際データ 中核値 塗装画面 코드를 ホスト 記憶データ 화면에 연결해 部分要素値 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

計画根 = Path(__file__).resolve().parents[1]

def 起動処理():
    ソースファイル群 = ['試験/画面再読込.c', '機械/画面描画中.c', '機械/端末.c', '機械/操作部品.c']
    妥当性ソース一覧 = ソースファイル群 + ['ソース/描画領域組立器.java', 'ソース/基板.java', '../../compiler/Java道具/事前用時間コンパイラ.java']
    宛先値 = 計画根/'build/verification/redraw'; 宛先値.mkdir(parents=True, exist_ok=True)
    履歴記録記録 = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((計画根/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {名前: hashlib.sha256((計画根/名前).read_bytes()).hexdigest() for 名前 in 妥当性ソース一覧}}
    try:
        クラス経路 = 宛先値/'classes'; クラス経路.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(クラス経路),
            str(計画根/'ソース/描画領域組立器.java'), str(計画根/'ソース/基板.java')])
        公開表 = {'jdraw_prepare': '用意', 'jdraw_width': '幅取得', 'jdraw_height': '高さ取得',
            'jdraw_count_low': '計数器下位取得', 'jdraw_count_high': '計数器上位取得', 'jdraw_clip': '切抜き',
            'jdraw_clip_value': '切抜き値', 'jdraw_begin': '起動処理', 'jdraw_end': '終了処理',
            'jdraw_pixel': '画素', 'jdraw_rectangle': '矩形塗潰し', 'jdraw_pointer': 'ポインタ'}
        翻訳工程命令 = ['sh', str(計画根.parents[1]/'compiler/事前用時間.sh'), '--entry', '描画領域組立器.幅取得', '-o', str(宛先値/'描画.c')]
        for 接続, 関数 in 公開表.items(): 翻訳工程命令.extend(['--export', 接続+'=描画領域組立器.'+関数])
        subprocess.check_call(翻訳工程命令+[str(経路) for 経路 in sorted(クラス経路.glob('*.class'))])
        命令 = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + ソースファイル群
        描画中宛先 = 宛先値/'描画.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(宛先値/'描画.c'), '-o', str(描画中宛先)])
        subprocess.check_call(命令+[str(描画中宛先), 'build/terminal-font.S', '-o', str(宛先値/'画面再読込試験')], cwd=str(計画根))
        結果 = subprocess.check_output([str(宛先値/'画面再読込試験')], timeout=30).decode()
        (宛先値/'妥当性検査.log').write_text(結果)
        判定照合済み = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', 結果)
        assert 判定照合済み and 'PASS:' in 結果, 結果
        履歴記録記録.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(判定照合済み[1]), mean_framebuffer_writes_per_move=int(判定照合済み[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(結果, end='')
    finally:
        (宛先値/'report.json').write_text(json.dumps(履歴記録記録, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': 起動処理()
