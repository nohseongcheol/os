# vlastní 커널의 Python sada instalovat_HODNOTA

vlastní ARM64 커널의 `python`은 **MicroPython 1.24.1 integer BLD_Systém**다.
`pip`와 `python -m pip`는 이 환경을 위한 제한형 zdroj_strom instalovat_HODNOTA 명령이다.
PyPA pip 전체나 CPython을 이식한 것은 아니다.

호스트에서 실행한다.

```sh
cd /home/user/jkoros/platforms/rpi4-native
make build
python3 nástroje/Provést_příkaz.py --desktop --network --pip
```

게스트 셸에서 설치하고 사용한다.

```text
pip install micropython-bisect==3.3.3
pip list
python -c 'from bisect import insort as 순서대로넣기; HODNOTA=[1,5]; 순서대로넣기(HODNOTA,3); print(HODNOTA)'
python -m pip list
pip uninstall micropython-bisect
```

informační_systémy_normální Provést_příkaz 결과는 `[1, 3, 5]`다. 예시 distribuce_HODNOTA 파일은
[PyPI의 micropython-bisect 3.3.3](https://pypi.org/project/micropython-bisect/3.3.3/)이며
SHA-256은 `b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8`이다.
`bisect`는 instalovat_HODNOTA 전 내장되어 있지 않다. 내려받은 `.py`를 vlastní 커널의 EL0
MicroPython이 import하여 실행한다.

## instalovat_HODNOTA 경로와 역할

호스트의 [sada_Přenos.py](nástroje/sada_Přenos.py)는 PyPI HTTPS 다운로드, 인증서 ověřit,
distribuce_HODNOTA název_souboru SHA-256 검증과 Archiv_HODNOTA 해제를 맡는다. 호스트에서 `setup.py`SEKUNDA_operand 내려받은
Python 코드를 실행하지 않는다. hostit pip 설치도 필요 없다.
중계는 `127.0.0.1:8027`에만 열리며 게스트는 QEMU NAT의 `10.0.2.2:8027`로 연결한다.
게스트 자체에 DNS·TLS·PyPI Archiv_HODNOTA verze_Storage 기능을 추가했다는 뜻은 아니다.

게스트의 [sada.py](PYTHON_most/knihovna/sada.py)는 TCP로 받은 파일의 SHA-256과
cesta_2·Velikost·문법을 검사한 BACK_HODNOTA `/lib`에 설치하고 `/lib/.pip.json`에 목록을 기록한다.
`/lib`와 Provést_příkaz skript_HODNOTA 폴더를 modul_HODNOTA 검색 경로에 추가했으므로 작업 폴더가 달라도
설치한 모듈을 import할 číslo 있다. 패키지 폴더와 partner_HODNOTA import도 지원한다.

instalovat_HODNOTA 도중 ODKAZ_oblast 부족 등 오류가 발생하면 새 파일과 폴더를 지우고 기존 목록을
복원한다. 이미 있는 uživatelský_prostor 파일을 덮어쓰지 않는다. 동일 버전 재설치 요청은
název_souboru 지문을 확인하고 유지한다. 다른 버전은 odebrat_položka 후 설치한다. odebrat_položka 시 사용자가
수정한 파일이 발견되면 보존하고 오류를 알린다. 빈 패키지 폴더는 남을 číslo 있다.

**`/lib`도 RAM 파일이다. 재부팅하면 설치한 패키지가 사라진다.**
hostit `build/pip-cache`에는 distribuce_HODNOTA 파일과 origin_HODNOTA·지문이 남으므로 Další_zboží 부팅에서 zkusit_znovu_HODNOTA
설치할 číslo 있다. 버전을 지정하면 같은 distribuce_HODNOTA 파일을 재사용한다.

```sh
# hostit: 인터넷이 있을 때 distribuce_HODNOTA 파일만 Připravit
python3 nástroje/sada_Přenos.py --fetch micropython-bisect==3.3.3
# Další_zboží Provést_příkaz: PyPI Připojit 없이 캐시 použít_HODNOTA
python3 nástroje/Provést_příkaz.py --network --pip --pip-offline
```

다른 포트는 hostit `--pip-port 8028`, 게스트
`pip install micropython-bisect==3.3.3 --port 8028`로 맞춘다.
hostit 중계는 `python3 nástroje/sada_Přenos.py --port 8027`로 별도 실행할 수도 있다.
QEMU를 종료하거나 Přenos_HODNOTA 실행을 끝내면 이 서비스도 닫힌다.

## vzpěra_HODNOTA oříznout

- 의존성 없는 순수 Python wheel(`*-none-any.whl`, `Root-Is-Purelib: true`).
- 구형 `micropython-*` zdroj_strom 배포형의 `.py`와 `PKG-INFO`.
- 꾸러미당 zdroj_strom 16개, celkem_HODNOTA 64 KiB, 파일당 16 KiB, 절대 cesta_2 UTF-8 63바이트 이하.
  전체 RAM název_souboru 64개·Adresář_HODNOTA 16개의 남은 공간과 Python halda_HODNOTA 256 KiB 한도도 적용된다.
- `install`, `list`, `uninstall`, `--help`, `--version`.
- SHA-256, JSON, Paměť_data `io.StringIO`/`BytesIO`를 실행기에 추가했다.
  일반 název_souboru objekt_HODNOTA `open()`은 미지원이며 `čeština.파일읽기/zápis_Soubor` 또는
  `jkoros.read/write`를 사용한다.

C přípona_HODNOTA·플랫폼 전용 wheel, 일반 sdist BLD_Systém, 자동 의존성 해결, extras, VCS/임의 URL,
NumPy 같은 CPython 전용 패키지는 지원하지 않는다. 순수 Python 패키지도
MicroPython의 문법·표준 modul_HODNOTA·integer 전용 환경과 맞아야 실제로 실행할 číslo 있다.
instalovat_HODNOTA 시 문법을 검사하지만 모든 Provést_příkaz 경로의 호환성을 증명하지는 않는다.
skutečný_data Raspberry Pi 4의 LAN을 통한 설치는 검증하지 않았으며 dobrá_zboží 중계는 QEMU용이다.

MicroPython 자체의 패키지 체계와 CPython pip의 차이는
[MicroPython 패키지 문서](https://docs.micropython.org/en/v1.24.0/reference/packages.html),
wheel 형식은 [PyPA distribuce_HODNOTA formát_HODNOTA SD](https://packaging.python.org/en/latest/specifications/binary-distribution-format/)을 참고한다.

```sh
make test-pip
```

ověřit_5fb2b747 기록은 `build/verification/pip/report.json`과 `serial.log`에 저장한다.
skutečný_data PyPI sada 시험과 별도로 시험용 wheel로 패키지 Adresář_HODNOTA, 구문 chyba,
ODKAZ_oblast 부족 되돌림을 확인한다.
