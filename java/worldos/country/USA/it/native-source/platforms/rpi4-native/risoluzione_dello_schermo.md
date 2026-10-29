# nativo ARM64 커널의 schermata risoluzione_VALORE

QEMU Esegui_comando 위치는 `jkoros/platforms/rpi4-native`다. 커널을 빌드한 BACK_VALORE 다음과 같이 실행한다.

```bash
make build
python3 strumenti/Esegui_comando.py --desktop --network --resolution 1920x1080
```

Remmina의 **VNC** Connetti 주소는 `127.0.0.1:5902`다. 이미 Esegui_comando 중인 VM은 종료하고 새 옵션으로 retry_VALORE 시작한다. schermata 전체가 보이지 않으면 Remmina에서 schermata allineare_limite 또는 전체 화면을 선택한다. 이 옵션은 게스트의 effettivo_dati pixel 수를 바꾼다.

`--resolution`은 일반 UART Esegui_comando, `--desktop`, `--vnc`, `--display`에서 동일하게 적용된다. `--network`와 함께 사용할 numero 있다. 너비 640~1920, altezza_VALORE 480~1080을 허용하며 기본값은 640×480이다. 1280×720과 1920×1080도 선택할 numero 있다.

```bash
make desktop RESOLUTION=1920x1080
python3 strumenti/Esegui_comando.py --resolution 1280x720 --vnc 127.0.0.1:2
```

avvio_macchina 로그는 effettivo_dati 할당된 크기를 표시한다.

```text
FRAMEBUFFER PASS 1920x1080 RGB32 (drawing only)
```

terminale 바탕과 위쪽 막대는 schermata 전체를 채운다. 터미널은 DESTRA 아래까지 끌어서 이동하고 X로 닫을 numero 있다. terminale Finestra Dimensione(568×360)와 tipo_di_carattere_VALORE 크기는 유지되므로 넓어진 화면에 여러 창을 배치할 numero 있다. Swing 부분집합의 `setLocationRelativeTo(null)`도 effettivo_dati schermata 가운데를 사용한다. avvio_macchina BACK_VALORE 해상도를 바꾸는 기능은 제공하지 않는다.

## 프로그램에서 schermata Dimensione Lettura

| Lingua | Italiano 호출 |
|---|---|
| Java | `Italiano.nativo.schermata.너비()`, `schermata.altezza_VALORE()`, `schermata.cancellare_voce(색)` |
| C | `<schermata_ABI.h>`의 `화면너비()`, `schermata_altezza()`, `Disegno_rettangolo(...)` |
| C++ SDK | `호출.h`의 `화면너비읽기()`, `화면높이읽기()`, `schermata_rettangolo(...)` |
| Python | `from Italiano import schermata_ridimensionare, Disegno_rettangolo`; `너비, altezza_VALORE = schermata_ridimensionare()` |

C 함수는 macro_VALORE 별칭이 아닌 effettivo_dati 함수다. spazio_utente 호출 22로 크기를 조회하며, Paint_schermata 호출 13과 GUI 호출 20은 effettivo_dati schermata 경계를 검사한다. 프레임버퍼 주소는 spazio_utente 프로그램에 노출하지 않는다. schermata 밖의 요청은 오류를 반환한다.

게스트 `javac`에서는 `Italiano.nativo.schermata.너비()`처럼 전체 이름으로 호출한다. 지원하는 fonte_albero 문법에 맞춰 색상 상수는 십진수로 쓴다. 아래 호출은 avvio_macchina 해상도와 관계없이 마지막 화소를 그린다.

```java
int 너비 = Italiano.nativo.schermata.너비();
int altezza_VALORE = Italiano.nativo.schermata.altezza_VALORE();
Italiano.nativo.schermata.rettangolo(너비 - 1, altezza_VALORE - 1, 1, 1, 255);
```

`schermata` 클래스의 프레임버퍼 호출은 nativo JVM 전용이다. 이 API의 eccezione Processi_VALORE_voce 시험은 host `javac --release 8`로 컴파일한 class를 nativo JVM에서 실행한다. 게스트 컴파일러의 일반적인 `try/catch` 문법 지원을 추가한 것은 아니다.

## Raspberry Pi 4 SD avvio_macchina

```bash
make image RESOLUTION=1920x1080
```

생성되는 `dist/jkoros-native-rpi4.img`와 `dist/jkoros-native-rpi4-boot.zip`에 1080p 설정이 들어간다. SD foto_VALORE 생성은 640×480, 1280×720, 1920×1080을 지원한다. 이미 펼친 avvio_macchina 파일을 수정할 경우 `config.txt`의 `[pi4]`에 아래 값을 사용한다.

```ini
max_framebuffer_width=1920
max_framebuffer_height=1080
framebuffer_width=1920
framebuffer_height=1080
hdmi_group=1
hdmi_mode=16
```

커널은 [Raspberry Pi cassetta_postale valore_di_contratto](https://github.com/raspberrypi/firmware/wiki/Mailbox-property-interface)의 Regolari_articolo schermata Dimensione 조회와 schermata allocare_Memoria 응답을 사용한다. 응답의 Dimensione·RGB32 formato_VALORE·한 줄의 byte_VALORE numero·allocare_Memoria 용량을 확인하고, 반환된 riga_di_ingresso 간격으로 그린다. stato_iniziale 조회에 실패하거나 Supporto_VALORE 범위를 벗어나면 640×480을 요청한다. HDMI 설정은 [공식 펌웨어 schermata Impostazioni Guides](https://www.raspberrypi.com/documentation/computers/legacy_config_txt.html)를 따른다. effettivo_dati Pi 4와 모니터 조합에서의 HDMI 부팅은 아직 검증하지 않았다.

## convalidare

```bash
make test-resolution
```

시험은 각 해상도에서 effettivo_dati VNC schermata 크기와 픽셀, terminale trascinare_VALORE·Chiudi, C/Java 게스트 compilare_fonte, Python Esegui_comando, DESTRA 아래 픽셀과 schermata limite_VALORE errore, Swing 가운데 disposizione_di_collegamento·pulsante·Chiudi, GUI와 FTP 동시 사용을 확인한다. 결과와 schermata 캡처는 `build/verification/resolution/`에 저장한다.
