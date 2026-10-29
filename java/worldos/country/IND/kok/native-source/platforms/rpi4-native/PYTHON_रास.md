# 자체 커널의 Python रास स्थापणूक_मोल

자체 ARM64 커널의 `python`은 **MicroPython 1.24.1 पुर्णांक दाळचे_प्रणाली**다.
`pip`와 `python -m pip`는 이 환경을 위한 제한형 स्त्रोत_ट्री स्थापणूक_मोल 명령이다.
PyPA pip 전체나 CPython을 이식한 것은 아니다.

호스트에서 실행한다.

```sh
cd /home/user/jkoros/platforms/rpi4-native
make build
python3 साधनां/पाळो_दिवचो_आदेश.py --desktop --network --pip
```

게스트 셸에서 설치하고 사용한다.

```text
pip install micropython-bisect==3.3.3
pip list
python -c 'from bisect import insort as 순서대로넣기; मोल=[1,5]; 순서대로넣기(मोल,3); print(मोल)'
python -m pip list
pip uninstall micropython-bisect
```

정상 पाळो_दिवचो_आदेश 결과는 `[1, 3, 5]`다. 예시 배포 파일은
[PyPI의 micropython-bisect 3.3.3](https://pypi.org/project/micropython-bisect/3.3.3/)이며
SHA-256은 `b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8`이다.
`bisect`는 स्थापणूक_मोल 전 내장되어 있지 않다. 내려받은 `.py`를 자체 커널의 EL0
MicroPython이 import하여 실행한다.

## स्थापणूक_मोल 경로와 역할

호스트의 [꾸러미중계.py](साधनां/꾸러미중계.py)는 PyPI HTTPS 다운로드, 인증서 पुनर्तपासणी_करची,
배포 फायल SHA-256 검증과 संग्रह_मोल 해제를 맡는다. 호스트에서 `setup.py`나 내려받은
Python 코드를 실행하지 않는다. येजमान pip 설치도 필요 없다.
중계는 `127.0.0.1:8027`에만 열리며 게스트는 QEMU NAT의 `10.0.2.2:8027`로 연결한다.
게스트 자체에 DNS·TLS·PyPI संग्रह_मोल रिलीज_सांठवण 기능을 추가했다는 뜻은 아니다.

게스트의 [रास.py](PYTHON_ब्रिज/लायब्ररी/रास.py)는 TCP로 받은 파일의 SHA-256과
पाथ·आवाठ·문법을 검사한 फाटीं_मोल `/lib`에 설치하고 `/lib/.pip.json`에 목록을 기록한다.
`/lib`와 पाळो_दिवचो_आदेश स्क्रिप्ट_मोल 폴더를 मॉड्यूल_मोल 검색 경로에 추가했으므로 작업 폴더가 달라도
설치한 모듈을 import할 수 있다. 패키지 폴더와 पीयर_मोल import도 지원한다.

स्थापणूक_मोल 도중 공간 부족 등 오류가 발생하면 새 파일과 폴더를 지우고 기존 목록을
복원한다. 이미 있는 उपेगकर्तो 파일을 덮어쓰지 않는다. 동일 버전 재설치 요청은
फायल 지문을 확인하고 유지한다. 다른 버전은 काडचें_प्रवेश 후 설치한다. काडचें_प्रवेश 시 사용자가
수정한 파일이 발견되면 보존하고 오류를 알린다. 빈 패키지 폴더는 남을 수 있다.

**`/lib`도 RAM 파일이다. 재부팅하면 설치한 패키지가 사라진다.**
येजमान `build/pip-cache`에는 배포 파일과 출처·지문이 남으므로 फुडलें_आयटम 부팅에서 다시
설치할 수 있다. 버전을 지정하면 같은 배포 파일을 재사용한다.

```sh
# येजमान: 인터넷이 있을 때 배포 파일만 तयार_करचें_9ce364fc
python3 साधनां/꾸러미중계.py --fetch micropython-bisect==3.3.3
# फुडलें_आयटम पाळो_दिवचो_आदेश: PyPI कनॅक्ट 없이 캐시 사용
python3 साधनां/पाळो_दिवचो_आदेश.py --network --pip --pip-offline
```

다른 포트는 येजमान `--pip-port 8028`, 게스트
`pip install micropython-bisect==3.3.3 --port 8028`로 맞춘다.
येजमान 중계는 `python3 साधनां/꾸러미중계.py --port 8027`로 별도 실행할 수도 있다.
QEMU를 종료하거나 중계 실행을 끝내면 이 서비스도 닫힌다.

## तेंको_मोल क्लिप

- 의존성 없는 순수 Python wheel(`*-none-any.whl`, `Root-Is-Purelib: true`).
- 구형 `micropython-*` स्त्रोत_ट्री 배포형의 `.py`와 `PKG-INFO`.
- 꾸러미당 स्त्रोत_ट्री 16개, 합계 64 KiB, 파일당 16 KiB, 절대 पाथ UTF-8 63바이트 이하.
  전체 RAM फायल 64개·नामावळ_मोल 16개의 남은 공간과 Python 힙 256 KiB 한도도 적용된다.
- `install`, `list`, `uninstall`, `--help`, `--version`.
- SHA-256, JSON, मेमरी_डेटा `io.StringIO`/`BytesIO`를 실행기에 추가했다.
  일반 फायल ऑब्जॅक्ट_मोल `open()`은 미지원이며 `한국어.파일읽기/बरोवचें_फायल` 또는
  `jkoros.read/write`를 사용한다.

C विस्तार_मोल·플랫폼 전용 wheel, 일반 sdist दाळचे_प्रणाली, 자동 의존성 해결, extras, VCS/임의 URL,
NumPy 같은 CPython 전용 패키지는 지원하지 않는다. 순수 Python 패키지도
MicroPython의 문법·표준 मॉड्यूल_मोल·पुर्णांक 전용 환경과 맞아야 실제로 실행할 수 있다.
स्थापणूक_मोल 시 문법을 검사하지만 모든 पाळो_दिवचो_आदेश 경로의 호환성을 증명하지는 않는다.
प्रत्यक्ष_डेटा Raspberry Pi 4의 LAN을 통한 설치는 검증하지 않았으며 현재 중계는 QEMU용이다.

MicroPython 자체의 패키지 체계와 CPython pip의 차이는
[MicroPython 패키지 문서](https://docs.micropython.org/en/v1.24.0/reference/packages.html),
wheel 형식은 [PyPA 배포 स्वरूप_मोल SD](https://packaging.python.org/en/latest/specifications/binary-distribution-format/)을 참고한다.

```sh
make test-pip
```

पुनर्तपासणी_करची_5fb2b747 기록은 `build/verification/pip/report.json`과 `serial.log`에 저장한다.
प्रत्यक्ष_डेटा PyPI रास 시험과 별도로 시험용 wheel로 패키지 नामावळ_मोल, 구문 चूक,
공간 부족 되돌림을 확인한다.
