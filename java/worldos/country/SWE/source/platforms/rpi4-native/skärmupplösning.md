# eget ARM64 커널의 skärmbild upplösning_värde

QEMU köra_kommando 위치는 `jkoros/platforms/rpi4-native`다. 커널을 빌드한 BACK_värde 다음과 같이 실행한다.

```bash
make build
python3 verktyg/köra_kommando.py --desktop --network --resolution 1920x1080
```

Remmina의 **VNC** Anslut 주소는 `127.0.0.1:5902`다. 이미 köra_kommando 중인 VM은 종료하고 새 옵션으로 försöka_igen_värde 시작한다. skärmbild 전체가 보이지 않으면 Remmina에서 skärmbild justera_gräns 또는 전체 화면을 선택한다. 이 옵션은 게스트의 verklig_data bildpunkt 수를 바꾼다.

`--resolution`은 일반 UART köra_kommando, `--desktop`, `--vnc`, `--display`에서 동일하게 적용된다. `--network`와 함께 사용할 nummer 있다. 너비 640~1920, 높이 480~1080을 허용하며 기본값은 640×480이다. 1280×720과 1920×1080도 선택할 nummer 있다.

```bash
make desktop RESOLUTION=1920x1080
python3 verktyg/köra_kommando.py --resolution 1280x720 --vnc 127.0.0.1:2
```

maskinstart 로그는 verklig_data 할당된 크기를 표시한다.

```text
FRAMEBUFFER PASS 1920x1080 RGB32 (drawing only)
```

kommandotolk 바탕과 위쪽 막대는 skärmbild 전체를 채운다. 터미널은 HÖGER 아래까지 끌어서 이동하고 X로 닫을 nummer 있다. kommandotolk Fönster Storlek(568×360)와 teckensnitt_värde 크기는 유지되므로 넓어진 화면에 여러 창을 배치할 nummer 있다. Swing 부분집합의 `setLocationRelativeTo(null)`도 verklig_data skärmbild 가운데를 사용한다. maskinstart BACK_värde 해상도를 바꾸는 기능은 제공하지 않는다.

## 프로그램에서 skärmbild Storlek Läs

| Språk | Svenska 호출 |
|---|---|
| Java | `Svenska.eget.skärmbild.너비()`, `skärmbild.높이()`, `skärmbild.radera_post(색)` |
| C | `<화면규약.h>`의 `화면너비()`, `화면높이()`, `Rita_rektangel(...)` |
| C++ SDK | `호출.h`의 `화면너비읽기()`, `화면높이읽기()`, `skärmbild_rektangel(...)` |
| Python | `from Svenska import skärmbild_storlek, Rita_rektangel`; `너비, 높이 = skärmbild_storlek()` |

C 함수는 makro_värde 별칭이 아닌 verklig_data 함수다. användarutrymme 호출 22로 크기를 조회하며, Paint_skärmbild 호출 13과 GUI 호출 20은 verklig_data skärmbild 경계를 검사한다. 프레임버퍼 주소는 användarutrymme 프로그램에 노출하지 않는다. skärmbild 밖의 요청은 오류를 반환한다.

게스트 `javac`에서는 `Svenska.eget.skärmbild.너비()`처럼 전체 이름으로 호출한다. 지원하는 källa_träd 문법에 맞춰 색상 상수는 십진수로 쓴다. 아래 호출은 maskinstart 해상도와 관계없이 마지막 화소를 그린다.

```java
int 너비 = Svenska.eget.skärmbild.너비();
int 높이 = Svenska.eget.skärmbild.높이();
Svenska.eget.skärmbild.rektangel(너비 - 1, 높이 - 1, 1, 1, 255);
```

`skärmbild` 클래스의 프레임버퍼 호출은 eget JVM 전용이다. 이 API의 fel_31f743d2 Process_värde_post 시험은 värd `javac --release 8`로 컴파일한 class를 eget JVM에서 실행한다. 게스트 컴파일러의 일반적인 `try/catch` 문법 지원을 추가한 것은 아니다.

## Raspberry Pi 4 SD maskinstart

```bash
make image RESOLUTION=1920x1080
```

생성되는 `dist/jkoros-native-rpi4.img`와 `dist/jkoros-native-rpi4-boot.zip`에 1080p 설정이 들어간다. SD BILD_värde 생성은 640×480, 1280×720, 1920×1080을 지원한다. 이미 펼친 maskinstart 파일을 수정할 경우 `config.txt`의 `[pi4]`에 아래 값을 사용한다.

```ini
max_framebuffer_width=1920
max_framebuffer_height=1080
framebuffer_width=1920
framebuffer_height=1080
hdmi_group=1
hdmi_mode=16
```

커널은 [Raspberry Pi postlåda kontraktsvärde](https://github.com/raspberrypi/firmware/wiki/Mailbox-property-interface)의 aktuellt_objekt skärmbild Storlek 조회와 skärmbild allokera_minne 응답을 사용한다. 응답의 Storlek·RGB32 format_värde·한 줄의 byte_värde nummer·allokera_minne 용량을 확인하고, 반환된 inmatningsrad 간격으로 그린다. starttillstånd 조회에 실패하거나 stöd_värde 범위를 벗어나면 640×480을 요청한다. HDMI 설정은 [공식 펌웨어 skärmbild Inställningar 문서](https://www.raspberrypi.com/documentation/computers/legacy_config_txt.html)를 따른다. verklig_data Pi 4와 모니터 조합에서의 HDMI 부팅은 아직 검증하지 않았다.

## validera

```bash
make test-resolution
```

시험은 각 해상도에서 verklig_data VNC skärmbild 크기와 픽셀, kommandotolk dra_värde·Stäng, C/Java 게스트 kompilera_källa, Python köra_kommando, HÖGER 아래 픽셀과 skärmbild gräns_värde fel, Swing 가운데 länkningslayout·knapp·Stäng, GUI와 FTP 동시 사용을 확인한다. 결과와 skärmbild 캡처는 `build/verification/resolution/`에 저장한다.
