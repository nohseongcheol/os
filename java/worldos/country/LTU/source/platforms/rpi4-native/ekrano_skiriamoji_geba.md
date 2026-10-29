# savas ARM64 커널의 화면 skiriamoji_geba_VALUE

QEMU Vykdyti_komanda 위치는 `jkoros/platforms/rpi4-native`다. 커널을 빌드한 ATGAL_VALUE 다음과 같이 실행한다.

```bash
make build
python3 Įrankiai/Vykdyti_komanda.py --desktop --network --resolution 1920x1080
```

Remmina의 **VNC** Prisijungti 주소는 `127.0.0.1:5902`다. 이미 Vykdyti_komanda 중인 VM은 종료하고 새 옵션으로 kartoti_VALUE 시작한다. 화면 전체가 보이지 않으면 Remmina에서 화면 맞춤 또는 전체 화면을 선택한다. 이 옵션은 게스트의 faktinis_duomenys pikselis 수를 바꾼다.

`--resolution`은 일반 UART Vykdyti_komanda, `--desktop`, `--vnc`, `--display`에서 동일하게 적용된다. `--network`와 함께 사용할 numeris 있다. 너비 640~1920, 높이 480~1080을 허용하며 기본값은 640×480이다. 1280×720과 1920×1080도 선택할 numeris 있다.

```bash
make desktop RESOLUTION=1920x1080
python3 Įrankiai/Vykdyti_komanda.py --resolution 1280x720 --vnc 127.0.0.1:2
```

부팅 로그는 faktinis_duomenys 할당된 크기를 표시한다.

```text
FRAMEBUFFER PASS 1920x1080 RGB32 (drawing only)
```

Terminalas 바탕과 위쪽 막대는 화면 전체를 채운다. 터미널은 RIGHT 아래까지 끌어서 이동하고 X로 닫을 numeris 있다. Terminalas Langas Dydis(568×360)와 šriftas_VALUE 크기는 유지되므로 넓어진 화면에 여러 창을 배치할 numeris 있다. Swing 부분집합의 `setLocationRelativeTo(null)`도 faktinis_duomenys 화면 가운데를 사용한다. 부팅 ATGAL_VALUE 해상도를 바꾸는 기능은 제공하지 않는다.

## 프로그램에서 화면 Dydis Skaitymas

| Kalba | Lietuvių 호출 |
|---|---|
| Java | `Lietuvių.savas.화면.너비()`, `화면.높이()`, `화면.ištrinti_įrašas(색)` |
| C | `<화면규약.h>`의 `화면너비()`, `화면높이()`, `piešti_stačiakampis(...)` |
| C++ SDK | `호출.h`의 `화면너비읽기()`, `화면높이읽기()`, `화면사각형(...)` |
| Python | `from Lietuvių import 화면크기, piešti_stačiakampis`; `너비, 높이 = 화면크기()` |

C 함수는 makrokomanda_VALUE 별칭이 아닌 faktinis_duomenys 함수다. naudotojas 호출 22로 크기를 조회하며, 그리기 호출 13과 GUI 호출 20은 faktinis_duomenys 화면 경계를 검사한다. 프레임버퍼 주소는 naudotojas 프로그램에 노출하지 않는다. 화면 밖의 요청은 오류를 반환한다.

게스트 `javac`에서는 `Lietuvių.savas.화면.너비()`처럼 전체 이름으로 호출한다. 지원하는 šaltinis_medis 문법에 맞춰 색상 상수는 십진수로 쓴다. 아래 호출은 부팅 해상도와 관계없이 마지막 화소를 그린다.

```java
int 너비 = Lietuvių.savas.화면.너비();
int 높이 = Lietuvių.savas.화면.높이();
Lietuvių.savas.화면.stačiakampis(너비 - 1, 높이 - 1, 1, 1, 255);
```

`화면` 클래스의 프레임버퍼 호출은 savas JVM 전용이다. 이 API의 išimtis Procesas_VALUE_įrašas 시험은 organizuoti `javac --release 8`로 컴파일한 class를 savas JVM에서 실행한다. 게스트 컴파일러의 일반적인 `try/catch` 문법 지원을 추가한 것은 아니다.

## Raspberry Pi 4 SD 부팅

```bash
make image RESOLUTION=1920x1080
```

생성되는 `dist/jkoros-native-rpi4.img`와 `dist/jkoros-native-rpi4-boot.zip`에 1080p 설정이 들어간다. SD IMAGE_VALUE 생성은 640×480, 1280×720, 1920×1080을 지원한다. 이미 펼친 부팅 파일을 수정할 경우 `config.txt`의 `[pi4]`에 아래 값을 사용한다.

```ini
max_framebuffer_width=1920
max_framebuffer_height=1080
framebuffer_width=1920
framebuffer_height=1080
hdmi_group=1
hdmi_mode=16
```

커널은 [Raspberry Pi pašto_dėžutė sutarties_vertė](https://github.com/raspberrypi/firmware/wiki/Mailbox-property-interface)의 dabartinis_prekė 화면 Dydis 조회와 화면 priskirti_Saugykla 응답을 사용한다. 응답의 Dydis·RGB32 formatas_VALUE·한 줄의 baitas_VALUE numeris·priskirti_Saugykla 용량을 확인하고, 반환된 Eilutė 간격으로 그린다. pradinė_būsena 조회에 실패하거나 pagalba_VALUE 범위를 벗어나면 640×480을 요청한다. HDMI 설정은 [공식 펌웨어 화면 Nustatymai 문서](https://www.raspberrypi.com/documentation/computers/legacy_config_txt.html)를 따른다. faktinis_duomenys Pi 4와 모니터 조합에서의 HDMI 부팅은 아직 검증하지 않았다.

## tikrinti

```bash
make test-resolution
```

시험은 각 해상도에서 faktinis_duomenys VNC 화면 크기와 픽셀, Terminalas vilkti_VALUE·Užverti, C/Java 게스트 kompiliuoti_šaltinis, Python Vykdyti_komanda, RIGHT 아래 픽셀과 화면 경계 KLAIDA, Swing 가운데 sieti_schema·mygtukas·Užverti, GUI와 FTP 동시 사용을 확인한다. 결과와 화면 캡처는 `build/verification/resolution/`에 저장한다.
