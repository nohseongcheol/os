# 內建 커널의 Python 軟件包 安裝值

內建 ARM64 커널의 `python`은 **MicroPython 1.24.1 整數 構建系統**第三操作數.
`pip`와 `python -m pip`는 이 환경을 위한 제한형 原始碼樹 安裝值 명령이다.
PyPA pip 전체나 CPython을 이식한 것은 아니다.

호스트에서 실행한다.

```sh
cd /home/user/jkoros/platforms/rpi4-native
make build
python3 工具集/執行命令.py --desktop --network --pip
```

게스트 셸에서 설치하고 사용한다.

```text
pip install micropython-bisect==3.3.3
pip list
python -c 'from bisect import insort as 순서대로넣기; 值=[1,5]; 순서대로넣기(值,3); print(值)'
python -m pip list
pip uninstall micropython-bisect
```

是否常規 執行命令 결과는 `[1, 3, 5]`第三操作數. 예시 分發值 파일은
[PyPI의 micropython-bisect 3.3.3](https://pypi.org/project/micropython-bisect/3.3.3/)이며
SHA-256은 `b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8`이다.
`bisect`는 安裝值 之前值 내장되어 있지 않다. 내려받은 `.py`를 內建 커널의 EL0
MicroPython이 import하여 실행한다.

## 安裝值 경로와 역할

호스트의 [捆綁中繼.py](工具集/捆綁中繼.py)는 PyPI HTTPS 다운로드, 인증서 驗證,
分發值 檔案 SHA-256 검증과 存檔值 해제를 맡는다. 호스트에서 `setup.py`第二操作數 내려받은
Python 코드를 실행하지 않는다. 宿主 pip 설치도 所需條件值 없다.
중계는 `127.0.0.1:8027`에만 열리며 게스트는 QEMU NAT의 `10.0.2.2:8027`로 연결한다.
게스트 자체에 DNS·TLS·PyPI 存檔值 釋放存儲裝置 기능을 추가했다는 뜻은 아니다.

게스트의 [軟件包.py](Python橋接/庫/軟件包.py)는 TCP로 받은 파일의 SHA-256과
路徑·大小·문법을 검사한 後端值 `/lib`에 설치하고 `/lib/.pip.json`에 목록을 기록한다.
`/lib`와 執行命令 腳本值 폴더를 模塊值 검색 경로에 추가했으므로 任務 폴더가 달라도
설치한 모듈을 import할 數 있다. 패키지 폴더와 對端值 import도 지원한다.

安裝值 도중 地址區域 부족 등 오류가 발생하면 새 파일과 폴더를 지우고 기존 목록을
복원한다. 이미 있는 使用者 파일을 덮어쓰지 않는다. 동일 버전 재설치 요청은
檔案 지문을 확인하고 유지한다. 다른 버전은 移除條目 之後狀態 설치한다. 移除條目 시 사용자가
수정한 파일이 발견되면 보존하고 오류를 알린다. 빈 패키지 폴더는 남을 數 있다.

**`/lib`도 RAM 파일이다. 재부팅하면 설치한 패키지가 사라진다.**
宿主 `build/pip-cache`에는 分發值 파일과 原點值·지문이 남으므로 下一項目 부팅에서 重試值
설치할 數 있다. 버전을 지정하면 같은 分發值 파일을 재사용한다.

```sh
# 宿主: 인터넷이 있을 때 分發值 파일만 準備
python3 工具集/捆綁中繼.py --fetch micropython-bisect==3.3.3
# 下一項目 執行命令: PyPI 連接 없이 캐시 使用值
python3 工具集/執行命令.py --network --pip --pip-offline
```

다른 포트는 宿主 `--pip-port 8028`, 게스트
`pip install micropython-bisect==3.3.3 --port 8028`로 맞춘다.
宿主 중계는 `python3 工具集/捆綁中繼.py --port 8027`로 별도 실행할 수도 있다.
QEMU를 종료하거나 中繼值 실행을 끝내면 이 서비스도 닫힌다.

## 支持值 裁剪

- 依賴項列 없는 순수 Python wheel(`*-none-any.whl`, `Root-Is-Purelib: true`).
- 구형 `micropython-*` 原始碼樹 배포형의 `.py`와 `PKG-INFO`.
- 꾸러미당 原始碼樹 16개, 總計值 64 KiB, 파일당 16 KiB, 절대 路徑 UTF-8 63바이트 이하.
  전체 RAM 檔案 64개·目錄值 16개의 남은 공간과 Python 堆值 256 KiB 한도도 적용된다.
- `install`, `list`, `uninstall`, `--help`, `--version`.
- SHA-256, JSON, 記憶體資料 `io.StringIO`/`BytesIO`를 실행기에 추가했다.
  일반 檔案 物件值 `open()`은 미지원이며 `中文.讀取檔案/寫入檔案` 또는
  `jkoros.read/write`를 사용한다.

C 擴展名值·플랫폼 전용 wheel, 일반 sdist 構建系統, 자동 依賴項列 해결, extras, VCS/임의 URL,
NumPy 같은 CPython 전용 패키지는 지원하지 않는다. 순수 Python 패키지도
MicroPython의 문법·표준 模塊值·整數 전용 환경과 맞아야 실제로 실행할 數 있다.
安裝值 시 문법을 검사하지만 모든 執行命令 경로의 호환성을 증명하지는 않는다.
實際資料 Raspberry Pi 4의 LAN을 통한 설치는 검증하지 않았으며 當前項目 중계는 QEMU용이다.

MicroPython 자체의 패키지 체계와 CPython pip의 차이는
[MicroPython 패키지 文檔集](https://docs.micropython.org/en/v1.24.0/reference/packages.html),
wheel 형식은 [PyPA 分發值 格式值 標準定義](https://packaging.python.org/en/latest/specifications/binary-distribution-format/)을 참고한다.

```sh
make test-pip
```

有效性校驗 기록은 `build/verification/pip/report.json`과 `serial.log`에 저장한다.
實際資料 PyPI 軟件包 시험과 별도로 시험용 wheel로 패키지 目錄值, 구문 錯誤,
地址區域 부족 되돌림을 확인한다.
