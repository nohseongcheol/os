# eigen ARM64 커널의 Bildschirm auflösungWert

QEMU befehlAusführen 위치는 `jkoros/platforms/rpi4-native`dritterOperand. 커널을 빌드한 rückseiteWert 다음과 같이 실행한다.

```bash
make build
python3 Werkzeuge/befehlAusführen.py --desktop --network --resolution 1920x1080
```

Remmina의 **VNC** verbinden 주소는 `127.0.0.1:5902`dritterOperand. 이미 befehlAusführen 중인 VM은 종료하고 새 옵션으로 erneutVersuchenWert 시작한다. Bildschirm 전체가 보이지 않으면 Remmina에서 Bildschirm ausrichtenGrenzstelle 또는 전체 화면을 선택한다. 이 옵션은 게스트의 tatsächlichDaten bildpunkt 수를 바꾼다.

`--resolution`은 일반 UART befehlAusführen, `--desktop`, `--vnc`, `--display`에서 동일하게 적용된다. `--network`와 함께 사용할 Zahl 있다. breiteWert 640~1920, höheWert 480~1080을 허용하며 기본값은 640×480이다. 1280×720과 1920×1080도 선택할 Zahl 있다.

```bash
make desktop RESOLUTION=1920x1080
python3 Werkzeuge/befehlAusführen.py --resolution 1280x720 --vnc 127.0.0.1:2
```

Startvorgang 로그는 tatsächlichDaten 할당된 크기를 표시한다.

```text
FRAMEBUFFER PASS 1920x1080 RGB32 (drawing only)
```

terminal 바탕과 obererSeiteRand 막대는 Bildschirm 전체를 채운다. 터미널은 rechts 아래까지 끌어서 이동하고 X로 닫을 Zahl 있다. terminal fenster größe(568×360)와 schriftartWert 크기는 유지되므로 넓어진 화면에 여러 창을 배치할 Zahl 있다. Swing 부분집합의 `setLocationRelativeTo(null)`도 tatsächlichDaten Bildschirm 가운데를 사용한다. Startvorgang rückseiteWert 해상도를 바꾸는 기능은 제공하지 않는다.

## 프로그램에서 Bildschirm größe lesen

| Sprache | Deutsch aufrufen |
|---|---|
| Java | `Deutsch.eigen.Bildschirm.breiteWert()`, `Bildschirm.höheWert()`, `Bildschirm.eintragTilgen(farbeWert)` |
| C | `<BildschirmABI.h>`의 `bildschirmBreite()`, `bildschirmHöhe()`, `rechteckZeichnen(...)` |
| C++ SDK | `aufrufen.h`의 `bildschirmBreiteLesen()`, `bildschirmHöheLesen()`, `bildschirmRechteck(...)` |
| Python | `from Deutsch import bildschirmGröße, rechteckZeichnen`; `breiteWert, höheWert = bildschirmGröße()` |

C 함수는 makroWert 별칭이 아닌 tatsächlichDaten 함수다. Benutzer aufrufen 22로 크기를 조회하며, malenBildschirm aufrufen 13과 GUI aufrufen 20은 tatsächlichDaten Bildschirm 경계를 검사한다. 프레임버퍼 주소는 Benutzer 프로그램에 노출하지 않는다. Bildschirm 밖의 요청은 오류를 반환한다.

게스트 `javac`에서는 `Deutsch.eigen.Bildschirm.breiteWert()`처럼 전체 이름으로 호출한다. 지원하는 quelltextBaum 문법에 맞춰 bildpunktFarbe 상수는 십진수로 쓴다. unterkanteWert 호출은 Startvorgang 해상도와 관계없이 letzterElementeintrag 화소를 그린다.

```java
int breiteWert = Deutsch.eigen.Bildschirm.breiteWert();
int höheWert = Deutsch.eigen.Bildschirm.höheWert();
Deutsch.eigen.Bildschirm.rechteck(breiteWert - 1, höheWert - 1, 1, 1, 255);
```

`Bildschirm` 클래스의 프레임버퍼 호출은 eigen JVM 전용이다. 이 API의 ausnahme prozessWertEintrag 시험은 Wirtssystem `javac --release 8`로 컴파일한 class를 eigen JVM에서 실행한다. 게스트 컴파일러의 일반적인 `try/catch` 문법 지원을 추가한 것은 아니다.

## Raspberry Pi 4 SD Startvorgang

```bash
make image RESOLUTION=1920x1080
```

생성되는 `dist/jkoros-native-rpi4.img`와 `dist/jkoros-native-rpi4-boot.zip`에 1080p 설정이 들어간다. SD abbildWert 생성은 640×480, 1280×720, 1920×1080을 지원한다. 이미 펼친 Startvorgang 파일을 수정할 경우 `config.txt`의 `[pi4]`에 unterkanteWert 값을 사용한다.

```ini
max_framebuffer_width=1920
max_framebuffer_height=1080
framebuffer_width=1920
framebuffer_height=1080
hdmi_group=1
hdmi_mode=16
```

커널은 [Raspberry Pi postfach vertragWert](https://github.com/raspberrypi/firmware/wiki/Mailbox-property-interface)의 aktuellElementeintrag Bildschirm größe 조회와 Bildschirm speichergerätZuteilen 응답을 사용한다. 응답의 größe·RGB32 formatWert·한 줄의 byteWert Zahl·speichergerätZuteilen 용량을 확인하고, 반환된 zeile 간격으로 그린다. anfänglichStatuswert 조회에 실패하거나 unterstützungWert 범위를 벗어나면 640×480을 요청한다. HDMI 설정은 [공식 펌웨어 Bildschirm einstellungen Dokumentation](https://www.raspberrypi.com/documentation/computers/legacy_config_txt.html)를 따른다. tatsächlichDaten Pi 4와 모니터 조합에서의 HDMI 부팅은 아직 검증하지 않았다.

## validieren

```bash
make test-resolution
```

시험은 각 해상도에서 tatsächlichDaten VNC Bildschirm 크기와 픽셀, terminal ziehenWert·schließen, C/Java 게스트 quelltextÜbersetzen, Python befehlAusführen, rechts unterkanteWert 픽셀과 Bildschirm grenzstelleWert fehler, Swing mitte Bindungsanordnung·schaltfläche·schließen, GUI와 FTP 동시 사용을 확인한다. 결과와 Bildschirm 캡처는 `build/verification/resolution/`에 저장한다.
