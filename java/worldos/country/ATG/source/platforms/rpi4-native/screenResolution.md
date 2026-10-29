# Native ARM64 커널의 Screen resolutionValue

QEMU executeCommand 위치는 `jkoros/platforms/rpi4-native`thirdOperand. 커널을 빌드한 backValue 다음과 같이 실행한다.

```bash
make build
python3 tools/executeCommand.py --desktop --network --resolution 1920x1080
```

Remmina의 **VNC** connect 주소는 `127.0.0.1:5902`thirdOperand. 이미 executeCommand 중인 VM은 종료하고 새 옵션으로 retryValue 시작한다. Screen 전체가 보이지 않으면 Remmina에서 Screen alignBoundary 또는 전체 화면을 선택한다. 이 옵션은 게스트의 actualData pixel 수를 바꾼다.

`--resolution`은 일반 UART executeCommand, `--desktop`, `--vnc`, `--display`에서 동일하게 적용된다. `--network`와 함께 사용할 number 있다. widthValue 640~1920, heightValue 480~1080을 허용하며 기본값은 640×480이다. 1280×720과 1920×1080도 선택할 number 있다.

```bash
make desktop RESOLUTION=1920x1080
python3 tools/executeCommand.py --resolution 1280x720 --vnc 127.0.0.1:2
```

machine_boot 로그는 actualData 할당된 크기를 표시한다.

```text
FRAMEBUFFER PASS 1920x1080 RGB32 (drawing only)
```

terminal 바탕과 upperSide 막대는 Screen 전체를 채운다. 터미널은 right 아래까지 끌어서 이동하고 X로 닫을 number 있다. terminal window size(568×360)와 fontValue 크기는 유지되므로 넓어진 화면에 여러 창을 배치할 number 있다. Swing 부분집합의 `setLocationRelativeTo(null)`도 actualData Screen 가운데를 사용한다. machine_boot backValue 해상도를 바꾸는 기능은 제공하지 않는다.

## 프로그램에서 Screen size read

| language | English invoke |
|---|---|
| Java | `English.Native.Screen.widthValue()`, `Screen.heightValue()`, `Screen.eraseEntry(colourValue)` |
| C | `<ScreenABI.h>`의 `screenWidth()`, `screenHeight()`, `drawRectangle(...)` |
| C++ SDK | `invoke.h`의 `readScreenWidth()`, `readScreenHeight()`, `screenRectangle(...)` |
| Python | `from English import screenSize, drawRectangle`; `widthValue, heightValue = screenSize()` |

C 함수는 macroValue 별칭이 아닌 actualData 함수다. User invoke 22로 크기를 조회하며, paintScreen invoke 13과 GUI invoke 20은 actualData Screen 경계를 검사한다. 프레임버퍼 주소는 User 프로그램에 노출하지 않는다. Screen 밖의 요청은 오류를 반환한다.

게스트 `javac`에서는 `English.Native.Screen.widthValue()`처럼 전체 이름으로 호출한다. 지원하는 sourceTree 문법에 맞춰 pixelColour 상수는 십진수로 쓴다. bottomValue 호출은 machine_boot 해상도와 관계없이 lastItem 화소를 그린다.

```java
int widthValue = English.Native.Screen.widthValue();
int heightValue = English.Native.Screen.heightValue();
English.Native.Screen.rectangle(widthValue - 1, heightValue - 1, 1, 1, 255);
```

`Screen` 클래스의 프레임버퍼 호출은 Native JVM 전용이다. 이 API의 exception processValueEntry 시험은 Host `javac --release 8`로 컴파일한 class를 Native JVM에서 실행한다. 게스트 컴파일러의 일반적인 `try/catch` 문법 지원을 추가한 것은 아니다.

## Raspberry Pi 4 SD machine_boot

```bash
make image RESOLUTION=1920x1080
```

생성되는 `dist/jkoros-native-rpi4.img`와 `dist/jkoros-native-rpi4-boot.zip`에 1080p 설정이 들어간다. SD imageValue 생성은 640×480, 1280×720, 1920×1080을 지원한다. 이미 펼친 machine_boot 파일을 수정할 경우 `config.txt`의 `[pi4]`에 bottomValue 값을 사용한다.

```ini
max_framebuffer_width=1920
max_framebuffer_height=1080
framebuffer_width=1920
framebuffer_height=1080
hdmi_group=1
hdmi_mode=16
```

커널은 [Raspberry Pi mailbox contractValue](https://github.com/raspberrypi/firmware/wiki/Mailbox-property-interface)의 currentItem Screen size 조회와 Screen allocateStorage 응답을 사용한다. 응답의 size·RGB32 formatValue·한 줄의 byteValue number·allocateStorage 용량을 확인하고, 반환된 line 간격으로 그린다. initialState 조회에 실패하거나 supportValue 범위를 벗어나면 640×480을 요청한다. HDMI 설정은 [공식 펌웨어 Screen settings guides](https://www.raspberrypi.com/documentation/computers/legacy_config_txt.html)를 따른다. actualData Pi 4와 모니터 조합에서의 HDMI 부팅은 아직 검증하지 않았다.

## validate

```bash
make test-resolution
```

시험은 각 해상도에서 actualData VNC Screen 크기와 픽셀, terminal dragValue·close, C/Java 게스트 compileSource, Python executeCommand, right bottomValue 픽셀과 Screen boundaryValue error, Swing middle link_layout·button·close, GUI와 FTP 동시 사용을 확인한다. 결과와 Screen 캡처는 `build/verification/resolution/`에 저장한다.
