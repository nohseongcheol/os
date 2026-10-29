# tựThân 커널의 Python GóiGộp càiĐặtGiáTrị

tựThân ARM64 커널의 `python`은 **MicroPython 1.24.1 SốNguyên xâyDựngHệThống**toánHạngThứBa.
`pip`와 `python -m pip`는 이 환경을 위한 제한형 câyNguồn càiĐặtGiáTrị 명령이다.
PyPA pip 전체나 CPython을 이식한 것은 아니다.

호스트에서 실행한다.

```sh
cd /home/user/jkoros/platforms/rpi4-native
make build
python3 CôngCụ/thựcThiLệnh.py --desktop --network --pip
```

게스트 셸에서 설치하고 사용한다.

```text
pip install micropython-bisect==3.3.3
pip list
python -c 'from bisect import insort as 순서대로넣기; giáTrị=[1,5]; 순서대로넣기(giáTrị,3); print(giáTrị)'
python -m pip list
pip uninstall micropython-bisect
```

làBìnhThường thựcThiLệnh 결과는 `[1, 3, 5]`toánHạngThứBa. 예시 giáTrịBảnPhânPhối 파일은
[PyPI의 micropython-bisect 3.3.3](https://pypi.org/project/micropython-bisect/3.3.3/)이며
SHA-256은 `b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8`이다.
`bisect`는 càiĐặtGiáTrị giáTrịTrướcKhi 내장되어 있지 않다. 내려받은 `.py`를 tựThân 커널의 EL0
MicroPython이 import하여 실행한다.

## càiĐặtGiáTrị 경로와 역할

호스트의 [chuyểnTiếpGóiGộp.py](CôngCụ/chuyểnTiếpGóiGộp.py)는 PyPI HTTPS 다운로드, 인증서 xácMinh,
giáTrịBảnPhânPhối Tệp SHA-256 검증과 giáTrịKhoLưuTrữ 해제를 맡는다. 호스트에서 `setup.py`toánHạngThứHai 내려받은
Python 코드를 실행하지 않는다. Chủ pip 설치도 giáTrịCầnĐến 없다.
중계는 `127.0.0.1:8027`에만 열리며 게스트는 QEMU NAT의 `10.0.2.2:8027`로 연결한다.
게스트 자체에 DNS·TLS·PyPI giáTrịKhoLưuTrữ giảiPhóngLưuTrữ 기능을 추가했다는 뜻은 아니다.

게스트의 [GóiGộp.py](cầuNốiPython/thưViện/GóiGộp.py)는 TCP로 받은 파일의 SHA-256과
đườngDẫn·cỡ·문법을 검사한 giáTrịLùi `/lib`에 설치하고 `/lib/.pip.json`에 목록을 기록한다.
`/lib`와 thựcThiLệnh giáTrịKịchBản 폴더를 giáTrịMôĐun 검색 경로에 추가했으므로 TácVụ 폴더가 달라도
설치한 모듈을 import할 trịSố 있다. 패키지 폴더와 giáTrịĐốiTác import도 지원한다.

càiĐặtGiáTrị 도중 miềnĐịaChỉ 부족 등 오류가 발생하면 새 파일과 폴더를 지우고 기존 목록을
복원한다. 이미 있는 NgườiDùng 파일을 덮어쓰지 않는다. 동일 버전 재설치 요청은
Tệp 지문을 확인하고 유지한다. 다른 버전은 gỡMục trạngTháiSau 설치한다. gỡMục 시 사용자가
수정한 파일이 발견되면 보존하고 오류를 알린다. 빈 패키지 폴더는 남을 trịSố 있다.

**`/lib`도 RAM 파일이다. 재부팅하면 설치한 패키지가 사라진다.**
Chủ `build/pip-cache`에는 giáTrịBảnPhânPhối 파일과 giáTrịGốc·지문이 남으므로 phầnMụcKếTiếp 부팅에서 giáTrịThửLại
설치할 trịSố 있다. 버전을 지정하면 같은 giáTrịBảnPhânPhối 파일을 재사용한다.

```sh
# Chủ: 인터넷이 있을 때 giáTrịBảnPhânPhối 파일만 chuẩnBị
python3 CôngCụ/chuyểnTiếpGóiGộp.py --fetch micropython-bisect==3.3.3
# phầnMụcKếTiếp thựcThiLệnh: PyPI nốiKết 없이 캐시 giáTrịDùng
python3 CôngCụ/thựcThiLệnh.py --network --pip --pip-offline
```

다른 포트는 Chủ `--pip-port 8028`, 게스트
`pip install micropython-bisect==3.3.3 --port 8028`로 맞춘다.
Chủ 중계는 `python3 CôngCụ/chuyểnTiếpGóiGộp.py --port 8027`로 별도 실행할 수도 있다.
QEMU를 종료하거나 chuyểnTiếpGiáTrị 실행을 끝내면 이 서비스도 닫힌다.

## giáTrịHỗTrợ cắtXén

- cácPhụThuộc 없는 순수 Python wheel(`*-none-any.whl`, `Root-Is-Purelib: true`).
- 구형 `micropython-*` câyNguồn 배포형의 `.py`와 `PKG-INFO`.
- 꾸러미당 câyNguồn 16개, giáTrịTổngCộng 64 KiB, 파일당 16 KiB, 절대 đườngDẫn UTF-8 63바이트 이하.
  전체 RAM Tệp 64개·giáTrịThưMục 16개의 남은 공간과 Python giáTrịVùngNhớĐộng 256 KiB 한도도 적용된다.
- `install`, `list`, `uninstall`, `--help`, `--version`.
- SHA-256, JSON, dữLiệuBộNhớ `io.StringIO`/`BytesIO`를 실행기에 추가했다.
  일반 Tệp giáTrịĐốiTượng `open()`은 미지원이며 `tiếngViệt.đọcTệp/ghiTệp` 또는
  `jkoros.read/write`를 사용한다.

C giáTrịPhầnMởRộng·플랫폼 전용 wheel, 일반 sdist xâyDựngHệThống, 자동 cácPhụThuộc 해결, extras, VCS/임의 URL,
NumPy 같은 CPython 전용 패키지는 지원하지 않는다. 순수 Python 패키지도
MicroPython의 문법·표준 giáTrịMôĐun·SốNguyên 전용 환경과 맞아야 실제로 실행할 trịSố 있다.
càiĐặtGiáTrị 시 문법을 검사하지만 모든 thựcThiLệnh 경로의 호환성을 증명하지는 않는다.
dữLiệuThựcTế Raspberry Pi 4의 LAN을 통한 설치는 검증하지 않았으며 phầnMụcHiệnTại 중계는 QEMU용이다.

MicroPython 자체의 패키지 체계와 CPython pip의 차이는
[MicroPython 패키지 TàiLiệu](https://docs.micropython.org/en/v1.24.0/reference/packages.html),
wheel 형식은 [PyPA giáTrịBảnPhânPhối giáTrịĐịnhDạng địnhNghĩaChuẩn](https://packaging.python.org/en/latest/specifications/binary-distribution-format/)을 참고한다.

```sh
make test-pip
```

thẩmĐịnh 기록은 `build/verification/pip/report.json`과 `serial.log`에 저장한다.
dữLiệuThựcTế PyPI GóiGộp 시험과 별도로 시험용 wheel로 패키지 giáTrịThưMục, 구문 lỗi,
miềnĐịaChỉ 부족 되돌림을 확인한다.
