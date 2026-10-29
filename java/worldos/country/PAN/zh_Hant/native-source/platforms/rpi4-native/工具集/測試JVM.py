#!/usr/bin/env python3
"""OpenJDK와 內建 ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 執行命令 import 項目根


def 運行():
    輸出結果 = 項目根 / 'build/verification/jvm'
    類別路徑 = 輸出結果 / 'classes'; 類別路徑.mkdir(parents=True, exist_ok=True)
    Java捆綁 = 項目根 / 'dist/jkoros-native-korean.jar'
    原始碼列表 = sorted((項目根 / '測試/Java').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(Java捆綁), '-d', str(類別路徑)] + [str(字符串資料) for 字符串資料 in 原始碼列表])
    測試列表 = [('測試物件集', ['背景值', '分支值', '能夠計算']), ('測試異常列', []), ('集合測試', []),
             ('測試執行緒集', ['計數器值', '任務動作', '執行緒值']), ('測試韓文字母', []), ('測試聯網', []), ('測試韓語聯網', []), ('測試韓語異常列', []), ('韓文字母原始碼', []), ('測試邊界列', []), ('有效性校驗.測試捆綁', []), ('條目兼容性測試', [])]
    有效性驗證報告 = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((項目根 / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(Java捆綁.read_bytes()).hexdigest(), 'tests': []}
    try:
        for 名稱, 包含項 in 測試列表:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 臨時路徑:
                預期 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(類別路徑) + ':' + str(Java捆綁), 名稱], cwd=臨時路徑, timeout=15).decode('utf-8')
            命令參數列 = ['python3', str(項目根 / '工具集/執行檔案.py'), str(類別路徑 / (名稱.replace('.', '/') + '.class'))]
            if '.' in 名稱: 命令參數列 += ['--class-name', 名稱]
            for 包含條目 in 包含項: 命令參數列 += ['--include', str(類別路徑 / (包含條目 + '.class'))]
            if 名稱 == '韓文字母原始碼': 命令參數列[2] = str(項目根 / '測試/Java/韓文字母原始碼.java')
            已完成總量 = subprocess.run(命令參數列, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            實際結果 = 已完成總量.stdout.decode('utf-8').replace('\r\n', '\n')
            (輸出結果 / (名稱 + '.log')).write_text(實際結果, encoding='utf-8')
            是否相等 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", 實際結果, re.S)
            assert 已完成總量.returncode == 0 and 是否相等, (名稱, 實際結果)
            結果 = next(字符串資料 for 字符串資料 in 是否相等.groups() if 字符串資料 is not None) + '\n'
            assert 結果 == 預期, (名稱, 預期, 結果)
            有效性驗證報告['tests'].append({'name': 名稱, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', 名稱, flush=True)
        # 內建 JVM에 직접 연결한 中文 執行緒值/진입점은 OpenJDK용 래퍼가 아니다.
        已完成總量 = subprocess.run(['python3', str(項目根/'工具集/執行檔案.py'), str(類別路徑/'測試韓語執行緒集.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        結果 = 已完成總量.stdout.decode('utf-8').replace('\r\n', '\n')
        (輸出結果/'測試韓語執行緒集.log').write_text(結果)
        assert 已完成總量.returncode == 0 and '中文 직접 執行緒值 通過值\n' in 結果 and '\nexit 0\n' in 結果, 結果
        有效性驗證報告['direct_korean_thread_and_entry'] = True
        print('PASS: 中文 직접 執行緒值·執行任務·運行 條目分', flush=True)
        有效 = (類別路徑 / '測試物件集.class').read_bytes()
        測試情況 = [('판거부', 有效[:6] + b'\x00\x35' + 有效[8:], 'supported class versions'),
                 ('잘린클래스', 有效[:24], 'truncated class file')]
        有效性驗證報告['rejection_tests'] = []
        for 名稱, 載荷數據資料, 通知文本 in 測試情況:
            測試資料 = 輸出結果 / (名稱 + '.class'); 測試資料.write_bytes(載荷數據資料)
            已完成總量 = subprocess.run(['python3', str(項目根 / '工具集/執行檔案.py'), str(測試資料)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            文本 = 已完成總量.stdout.decode('utf-8').replace('\r\n', '\n')
            (輸出結果 / (名稱 + '.log')).write_text(文本, encoding='utf-8')
            assert 已完成總量.returncode == 1 and 通知文本 in 文本 and 'exit 1\n' in 文本, (名稱, 文本)
            有效性驗證報告['rejection_tests'].append({'name': 名稱, 'passed': True})
            print('PASS (rejected):', 名稱, flush=True)
        有效性驗證報告['passed'] = True
    finally:
        (輸出結果 / 'report.json').write_text(json.dumps(有效性驗證報告, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    運行()
