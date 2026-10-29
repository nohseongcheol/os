#!/usr/bin/env python3
"""OpenJDK와 内蔵 ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 命令実行 import 計画根


def 起動処理():
    出力結果 = 計画根 / 'build/verification/jvm'
    クラス経路 = 出力結果 / 'classes'; クラス経路.mkdir(parents=True, exist_ok=True)
    Java束 = 計画根 / 'dist/jkoros-native-korean.jar'
    ソース一覧 = sorted((計画根 / '試験/Java').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(Java束), '-d', str(クラス経路)] + [str(文字列データ) for 文字列データ in ソース一覧])
    一覧試験 = [('オブジェクト群試験', ['背景値', '分岐値', '可能判定計算']), ('例外一覧試験', []), ('集成試験', []),
             ('スレッド群試験', ['計数器値', '作業動作', 'スレッド値']), ('ハングル試験', []), ('通信機構試験', []), ('韓国語通信機構試験', []), ('韓国語例外一覧試験', []), ('ハングルソース', []), ('境界一覧試験', []), ('妥当性検査.束試験', []), ('入口互換性試験', [])]
    妥当性報告 = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((計画根 / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(Java束.read_bytes()).hexdigest(), 'tests': []}
    try:
        for 名前, 包含引数 in 一覧試験:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 一時経路:
                期待 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(クラス経路) + ':' + str(Java束), 名前], cwd=一時経路, timeout=15).decode('utf-8')
            命令引数列 = ['python3', str(計画根 / '道具/ファイル実行.py'), str(クラス経路 / (名前.replace('.', '/') + '.class'))]
            if '.' in 名前: 命令引数列 += ['--class-name', 名前]
            for 包含項目 in 包含引数: 命令引数列 += ['--include', str(クラス経路 / (包含項目 + '.class'))]
            if 名前 == 'ハングルソース': 命令引数列[2] = str(計画根 / '試験/Java/ハングルソース.java')
            完了済み総量 = subprocess.run(命令引数列, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            実際結果 = 完了済み総量.stdout.decode('utf-8').replace('\r\n', '\n')
            (出力結果 / (名前 + '.log')).write_text(実際結果, encoding='utf-8')
            判定等価 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", 実際結果, re.S)
            assert 完了済み総量.returncode == 0 and 判定等価, (名前, 実際結果)
            結果 = next(文字列データ for 文字列データ in 判定等価.groups() if 文字列データ is not None) + '\n'
            assert 結果 == 期待, (名前, 期待, 結果)
            妥当性報告['tests'].append({'name': 名前, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', 名前, flush=True)
        # 内蔵 JVM에 직접 연결한 日本語 スレッド値/진입점은 OpenJDK용 래퍼가 아니다.
        完了済み総量 = subprocess.run(['python3', str(計画根/'道具/ファイル実行.py'), str(クラス経路/'韓国語スレッド群試験.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        結果 = 完了済み総量.stdout.decode('utf-8').replace('\r\n', '\n')
        (出力結果/'韓国語スレッド群試験.log').write_text(結果)
        assert 完了済み総量.returncode == 0 and '日本語 직접 スレッド値 通過値\n' in 結果 and '\nexit 0\n' in 結果, 結果
        妥当性報告['direct_korean_thread_and_entry'] = True
        print('PASS: 日本語 직접 スレッド値·作業実行·起動処理 入口点', flush=True)
        妥当 = (クラス経路 / 'オブジェクト群試験.class').read_bytes()
        場合試験 = [('판거부', 妥当[:6] + b'\x00\x35' + 妥当[8:], 'supported class versions'),
                 ('잘린클래스', 妥当[:24], 'truncated class file')]
        妥当性報告['rejection_tests'] = []
        for 名前, 本文データデータ, 通知本文 in 場合試験:
            データ試験 = 出力結果 / (名前 + '.class'); データ試験.write_bytes(本文データデータ)
            完了済み総量 = subprocess.run(['python3', str(計画根 / '道具/ファイル実行.py'), str(データ試験)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            文 = 完了済み総量.stdout.decode('utf-8').replace('\r\n', '\n')
            (出力結果 / (名前 + '.log')).write_text(文, encoding='utf-8')
            assert 完了済み総量.returncode == 1 and 通知本文 in 文 and 'exit 1\n' in 文, (名前, 文)
            妥当性報告['rejection_tests'].append({'name': 名前, 'passed': True})
            print('PASS (rejected):', 名前, flush=True)
        妥当性報告['passed'] = True
    finally:
        (出力結果 / 'report.json').write_text(json.dumps(妥当性報告, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    起動処理()
