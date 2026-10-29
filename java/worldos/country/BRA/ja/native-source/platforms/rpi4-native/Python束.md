# 内蔵 커널의 Python パッケージ 値導入

内蔵 ARM64 커널의 `python`은 **MicroPython 1.24.1 整数値 システム構築**第三被演算子.
`pip`와 `python -m pip`는 이 환경을 위한 제한형 ソース木 値導入 명령이다.
PyPA pip 전체나 CPython을 이식한 것은 아니다.

호스트에서 실행한다.

```sh
cd /home/user/jkoros/platforms/rpi4-native
make build
python3 道具/命令実行.py --desktop --network --pip
```

게스트 셸에서 설치하고 사용한다.

```text
pip install micropython-bisect==3.3.3
pip list
python -c 'from bisect import insort as 순서대로넣기; 値=[1,5]; 순서대로넣기(値,3); print(値)'
python -m pip list
pip uninstall micropython-bisect
```

判定通常 命令実行 결과는 `[1, 3, 5]`第三被演算子. 예시 配布値 파일은
[PyPI의 micropython-bisect 3.3.3](https://pypi.org/project/micropython-bisect/3.3.3/)이며
SHA-256은 `b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8`이다.
`bisect`는 値導入 直前側値 내장되어 있지 않다. 내려받은 `.py`를 内蔵 커널의 EL0
MicroPython이 import하여 실행한다.

## 値導入 경로와 역할

호스트의 [束中継.py](道具/束中継.py)는 PyPI HTTPS 다운로드, 인증서 検証,
配布値 ファイル SHA-256 검증과 書庫値 해제를 맡는다. 호스트에서 `setup.py`第二被演算子 내려받은
Python 코드를 실행하지 않는다. ホスト pip 설치도 必要値 없다.
중계는 `127.0.0.1:8027`에만 열리며 게스트는 QEMU NAT의 `10.0.2.2:8027`로 연결한다.
게스트 자체에 DNS·TLS·PyPI 書庫値 記憶装置解放 기능을 추가했다는 뜻은 아니다.

게스트의 [パッケージ.py](Python橋渡し/ライブラリ/パッケージ.py)는 TCP로 받은 파일의 SHA-256과
経路·容量·문법을 검사한 後端値 `/lib`에 설치하고 `/lib/.pip.json`에 목록을 기록한다.
`/lib`와 命令実行 スクリプト値 폴더를 モジュール値 검색 경로에 추가했으므로 作業 폴더가 달라도
설치한 모듈을 import할 数 있다. 패키지 폴더와 通信相手値 import도 지원한다.

値導入 도중 番地領域 부족 등 오류가 발생하면 새 파일과 폴더를 지우고 기존 목록을
복원한다. 이미 있는 利用者 파일을 덮어쓰지 않는다. 동일 버전 재설치 요청은
ファイル 지문을 확인하고 유지한다. 다른 버전은 入口除去 後続側状況 설치한다. 入口除去 시 사용자가
수정한 파일이 발견되면 보존하고 오류를 알린다. 빈 패키지 폴더는 남을 数 있다.

**`/lib`도 RAM 파일이다. 재부팅하면 설치한 패키지가 사라진다.**
ホスト `build/pip-cache`에는 配布値 파일과 原点値·지문이 남으므로 次回項目 부팅에서 再試行処理値
설치할 数 있다. 버전을 지정하면 같은 配布値 파일을 재사용한다.

```sh
# ホスト: 인터넷이 있을 때 配布値 파일만 用意
python3 道具/束中継.py --fetch micropython-bisect==3.3.3
# 次回項目 命令実行: PyPI 接続 없이 캐시 使用値
python3 道具/命令実行.py --network --pip --pip-offline
```

다른 포트는 ホスト `--pip-port 8028`, 게스트
`pip install micropython-bisect==3.3.3 --port 8028`로 맞춘다.
ホスト 중계는 `python3 道具/束中継.py --port 8027`로 별도 실행할 수도 있다.
QEMU를 종료하거나 値中継 실행을 끝내면 이 서비스도 닫힌다.

## 支援値 切抜き

- 依存項目 없는 순수 Python wheel(`*-none-any.whl`, `Root-Is-Purelib: true`).
- 구형 `micropython-*` ソース木 배포형의 `.py`와 `PKG-INFO`.
- 꾸러미당 ソース木 16개, 合計値 64 KiB, 파일당 16 KiB, 절대 経路 UTF-8 63바이트 이하.
  전체 RAM ファイル 64개·ディレクトリ値 16개의 남은 공간과 Python ヒープ値 256 KiB 한도도 적용된다.
- `install`, `list`, `uninstall`, `--help`, `--version`.
- SHA-256, JSON, 記憶データ `io.StringIO`/`BytesIO`를 실행기에 추가했다.
  일반 ファイル オブジェクト値 `open()`은 미지원이며 `日本語.ファイル読取/ファイル書込` 또는
  `jkoros.read/write`를 사용한다.

C 拡張子値·플랫폼 전용 wheel, 일반 sdist システム構築, 자동 依存項目 해결, extras, VCS/임의 URL,
NumPy 같은 CPython 전용 패키지는 지원하지 않는다. 순수 Python 패키지도
MicroPython의 문법·표준 モジュール値·整数値 전용 환경과 맞아야 실제로 실행할 数 있다.
値導入 시 문법을 검사하지만 모든 命令実行 경로의 호환성을 증명하지는 않는다.
実際データ Raspberry Pi 4의 LAN을 통한 설치는 검증하지 않았으며 現在項目 중계는 QEMU용이다.

MicroPython 자체의 패키지 체계와 CPython pip의 차이는
[MicroPython 패키지 文書](https://docs.micropython.org/en/v1.24.0/reference/packages.html),
wheel 형식은 [PyPA 配布値 書式値 標準定義](https://packaging.python.org/en/latest/specifications/binary-distribution-format/)을 참고한다.

```sh
make test-pip
```

妥当性検査 기록은 `build/verification/pip/report.json`과 `serial.log`에 저장한다.
実際データ PyPI パッケージ 시험과 별도로 시험용 wheel로 패키지 ディレクトリ値, 구문 エラー,
番地領域 부족 되돌림을 확인한다.
