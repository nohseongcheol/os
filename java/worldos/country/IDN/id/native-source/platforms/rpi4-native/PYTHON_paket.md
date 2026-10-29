# Asli 커널의 Python paket instal_VALUE

Asli ARM64 커널의 `python`은 **MicroPython 1.24.1 bilangan_bulat bangun**다.
`pip`와 `python -m pip`는 이 환경을 위한 제한형 sumber_pohon instal_VALUE 명령이다.
PyPA pip 전체나 CPython을 이식한 것은 아니다.

호스트에서 실행한다.

```sh
cd /home/user/jkoros/platforms/rpi4-native
make build
python3 alat/Jalankan_perintah.py --desktop --network --pip
```

게스트 셸에서 설치하고 사용한다.

```text
pip install micropython-bisect==3.3.3
pip list
python -c 'from bisect import insort as 순서대로넣기; VALUE=[1,5]; 순서대로넣기(VALUE,3); print(VALUE)'
python -m pip list
pip uninstall micropython-bisect
```

정상 Jalankan_perintah 결과는 `[1, 3, 5]`다. 예시 배포 파일은
[PyPI의 micropython-bisect 3.3.3](https://pypi.org/project/micropython-bisect/3.3.3/)이며
SHA-256은 `b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8`이다.
`bisect`는 instal_VALUE 전 내장되어 있지 않다. 내려받은 `.py`를 Asli 커널의 EL0
MicroPython이 import하여 실행한다.

## instal_VALUE 경로와 역할

호스트의 [꾸러미중계.py](alat/꾸러미중계.py)는 PyPI HTTPS 다운로드, 인증서 periksa,
배포 berkas SHA-256 검증과 Arsip_VALUE 해제를 맡는다. 호스트에서 `setup.py`SECOND_operand 내려받은
Python 코드를 실행하지 않는다. host pip 설치도 필요 없다.
중계는 `127.0.0.1:8027`에만 열리며 게스트는 QEMU NAT의 `10.0.2.2:8027`로 연결한다.
게스트 자체에 DNS·TLS·PyPI Arsip_VALUE lepas_Storage 기능을 추가했다는 뜻은 아니다.

게스트의 [paket.py](PYTHON_bridge/pustaka/paket.py)는 TCP로 받은 파일의 SHA-256과
jalur·Ukuran·문법을 검사한 BACK_VALUE `/lib`에 설치하고 `/lib/.pip.json`에 목록을 기록한다.
`/lib`와 Jalankan_perintah skrip_VALUE 폴더를 modul_VALUE 검색 경로에 추가했으므로 작업 폴더가 달라도
설치한 모듈을 import할 수 있다. 패키지 폴더와 serekan_VALUE import도 지원한다.

instal_VALUE 도중 surel_wilayah 부족 등 오류가 발생하면 새 파일과 폴더를 지우고 기존 목록을
복원한다. 이미 있는 ruang_pengguna 파일을 덮어쓰지 않는다. 동일 버전 재설치 요청은
berkas 지문을 확인하고 유지한다. 다른 버전은 hapus_entri 후 설치한다. hapus_entri 시 사용자가
수정한 파일이 발견되면 보존하고 오류를 알린다. 빈 패키지 폴더는 남을 수 있다.

**`/lib`도 RAM 파일이다. 재부팅하면 설치한 패키지가 사라진다.**
host `build/pip-cache`에는 배포 파일과 출처·지문이 남으므로 Berikutnya_item 부팅에서 coba_lagi_VALUE
설치할 수 있다. 버전을 지정하면 같은 배포 파일을 재사용한다.

```sh
# host: 인터넷이 있을 때 배포 파일만 Siapkan
python3 alat/꾸러미중계.py --fetch micropython-bisect==3.3.3
# Berikutnya_item Jalankan_perintah: PyPI Sambung 없이 캐시 gunakan_VALUE
python3 alat/Jalankan_perintah.py --network --pip --pip-offline
```

다른 포트는 host `--pip-port 8028`, 게스트
`pip install micropython-bisect==3.3.3 --port 8028`로 맞춘다.
host 중계는 `python3 alat/꾸러미중계.py --port 8027`로 별도 실행할 수도 있다.
QEMU를 종료하거나 중계 실행을 끝내면 이 서비스도 닫힌다.

## dukung_VALUE klip

- 의존성 없는 순수 Python wheel(`*-none-any.whl`, `Root-Is-Purelib: true`).
- 구형 `micropython-*` sumber_pohon 배포형의 `.py`와 `PKG-INFO`.
- 꾸러미당 sumber_pohon 16개, total_VALUE 64 KiB, 파일당 16 KiB, 절대 jalur UTF-8 63바이트 이하.
  전체 RAM berkas 64개·Direktori_VALUE 16개의 남은 공간과 Python 힙 256 KiB 한도도 적용된다.
- `install`, `list`, `uninstall`, `--help`, `--version`.
- SHA-256, JSON, Memori_data `io.StringIO`/`BytesIO`를 실행기에 추가했다.
  일반 berkas objek_VALUE `open()`은 미지원이며 `Indonesia.파일읽기/tulis_file` 또는
  `jkoros.read/write`를 사용한다.

C ekstensi_VALUE·플랫폼 전용 wheel, 일반 sdist bangun, 자동 의존성 해결, extras, VCS/임의 URL,
NumPy 같은 CPython 전용 패키지는 지원하지 않는다. 순수 Python 패키지도
MicroPython의 문법·표준 modul_VALUE·bilangan_bulat 전용 환경과 맞아야 실제로 실행할 수 있다.
instal_VALUE 시 문법을 검사하지만 모든 Jalankan_perintah 경로의 호환성을 증명하지는 않는다.
aktual_data Raspberry Pi 4의 LAN을 통한 설치는 검증하지 않았으며 saat_ini_item 중계는 QEMU용이다.

MicroPython 자체의 패키지 체계와 CPython pip의 차이는
[MicroPython 패키지 문서](https://docs.micropython.org/en/v1.24.0/reference/packages.html),
wheel 형식은 [PyPA 배포 format_VALUE SD](https://packaging.python.org/en/latest/specifications/binary-distribution-format/)을 참고한다.

```sh
make test-pip
```

validasi 기록은 `build/verification/pip/report.json`과 `serial.log`에 저장한다.
aktual_data PyPI paket 시험과 별도로 시험용 wheel로 패키지 Direktori_VALUE, 구문 galat,
surel_wilayah 부족 되돌림을 확인한다.
