# tựThân ARM64 커널의 MànHình giáTrịĐộPhânGiải

QEMU thựcThiLệnh 위치는 `jkoros/platforms/rpi4-native`toánHạngThứBa. 커널을 빌드한 giáTrịLùi 다음과 같이 실행한다.

```bash
make build
python3 CôngCụ/thựcThiLệnh.py --desktop --network --resolution 1920x1080
```

Remmina의 **VNC** nốiKết 주소는 `127.0.0.1:5902`toánHạngThứBa. 이미 thựcThiLệnh 중인 VM은 종료하고 새 옵션으로 giáTrịThửLại 시작한다. MànHình 전체가 보이지 않으면 Remmina에서 MànHình ranhGiớiCănChỉnh 또는 전체 화면을 선택한다. 이 옵션은 게스트의 dữLiệuThựcTế điểmẢnh 수를 바꾼다.

`--resolution`은 일반 UART thựcThiLệnh, `--desktop`, `--vnc`, `--display`에서 동일하게 적용된다. `--network`와 함께 사용할 trịSố 있다. giáTrịRộng 640~1920, giáTrịCao 480~1080을 허용하며 기본값은 640×480이다. 1280×720과 1920×1080도 선택할 trịSố 있다.

```bash
make desktop RESOLUTION=1920x1080
python3 CôngCụ/thựcThiLệnh.py --resolution 1280x720 --vnc 127.0.0.1:2
```

KhởiĐộng 로그는 dữLiệuThựcTế 할당된 크기를 표시한다.

```text
FRAMEBUFFER PASS 1920x1080 RGB32 (drawing only)
```

thiếtBịCuối 바탕과 bênThượng 막대는 MànHình 전체를 채운다. 터미널은 phải 아래까지 끌어서 이동하고 X로 닫을 trịSố 있다. thiếtBịCuối cửaSổ cỡ(568×360)와 giáTrịPhôngChữ 크기는 유지되므로 넓어진 화면에 여러 창을 배치할 trịSố 있다. Swing 부분집합의 `setLocationRelativeTo(null)`도 dữLiệuThựcTế MànHình 가운데를 사용한다. KhởiĐộng giáTrịLùi 해상도를 바꾸는 기능은 제공하지 않는다.

## 프로그램에서 MànHình cỡ đọc

| NgônNgữ | tiếngViệt gọiThựcHiện |
|---|---|
| Java | `tiếngViệt.tựThân.MànHình.giáTrịRộng()`, `MànHình.giáTrịCao()`, `MànHình.xóaMục(giáTrịMàu)` |
| C | `<ABIMànHình.h>`의 `rộngMànHình()`, `caoMànHình()`, `vẽHìnhChữNhật(...)` |
| C++ SDK | `gọiThựcHiện.h`의 `đọcRộngMànHình()`, `đọcCaoMànHình()`, `hìnhChữNhậtMànHình(...)` |
| Python | `from tiếngViệt import cỡMànHình, vẽHìnhChữNhật`; `giáTrịRộng, giáTrịCao = cỡMànHình()` |

C 함수는 giáTrịVĩLệnh 별칭이 아닌 dữLiệuThựcTế 함수다. NgườiDùng gọiThựcHiện 22로 크기를 조회하며, mànHìnhTô gọiThựcHiện 13과 GUI gọiThựcHiện 20은 dữLiệuThựcTế MànHình 경계를 검사한다. 프레임버퍼 주소는 NgườiDùng 프로그램에 노출하지 않는다. MànHình 밖의 요청은 오류를 반환한다.

게스트 `javac`에서는 `tiếngViệt.tựThân.MànHình.giáTrịRộng()`처럼 전체 이름으로 호출한다. 지원하는 câyNguồn 문법에 맞춰 màuĐiểmẢnh 상수는 십진수로 쓴다. giáTrịĐáy 호출은 KhởiĐộng 해상도와 관계없이 phầnMụcCuối 화소를 그린다.

```java
int giáTrịRộng = tiếngViệt.tựThân.MànHình.giáTrịRộng();
int giáTrịCao = tiếngViệt.tựThân.MànHình.giáTrịCao();
tiếngViệt.tựThân.MànHình.hìnhChữNhật(giáTrịRộng - 1, giáTrịCao - 1, 1, 1, 255);
```

`MànHình` 클래스의 프레임버퍼 호출은 tựThân JVM 전용이다. 이 API의 ngoạiLệ mụcGiáTrịTiếnTrình 시험은 Chủ `javac --release 8`로 컴파일한 class를 tựThân JVM에서 실행한다. 게스트 컴파일러의 일반적인 `try/catch` 문법 지원을 추가한 것은 아니다.

## Raspberry Pi 4 SD KhởiĐộng

```bash
make image RESOLUTION=1920x1080
```

생성되는 `dist/jkoros-native-rpi4.img`와 `dist/jkoros-native-rpi4-boot.zip`에 1080p 설정이 들어간다. SD giáTrịẢnh 생성은 640×480, 1280×720, 1920×1080을 지원한다. 이미 펼친 KhởiĐộng 파일을 수정할 경우 `config.txt`의 `[pi4]`에 giáTrịĐáy 값을 사용한다.

```ini
max_framebuffer_width=1920
max_framebuffer_height=1080
framebuffer_width=1920
framebuffer_height=1080
hdmi_group=1
hdmi_mode=16
```

커널은 [Raspberry Pi hộpThư giáTrịQuyƯớc](https://github.com/raspberrypi/firmware/wiki/Mailbox-property-interface)의 phầnMụcHiệnTại MànHình cỡ 조회와 MànHình cấpPhátLưuTrữ 응답을 사용한다. 응답의 cỡ·RGB32 giáTrịĐịnhDạng·한 줄의 giáTrịByte trịSố·cấpPhátLưuTrữ 용량을 확인하고, 반환된 dòng 간격으로 그린다. trạngTháiBanĐầu 조회에 실패하거나 giáTrịHỗTrợ 범위를 벗어나면 640×480을 요청한다. HDMI 설정은 [공식 펌웨어 MànHình cácThiếtLập TàiLiệu](https://www.raspberrypi.com/documentation/computers/legacy_config_txt.html)를 따른다. dữLiệuThựcTế Pi 4와 모니터 조합에서의 HDMI 부팅은 아직 검증하지 않았다.

## thẩmĐịnh

```bash
make test-resolution
```

시험은 각 해상도에서 dữLiệuThựcTế VNC MànHình 크기와 픽셀, thiếtBịCuối giáTrịKéo·đóng, C/Java 게스트 biênDịchNguồn, Python thựcThiLệnh, phải giáTrịĐáy 픽셀과 MànHình giáTrịRanhGiới lỗi, Swing giữa BốTríLiênKết·nút·đóng, GUI와 FTP 동시 사용을 확인한다. 결과와 MànHình 캡처는 `build/verification/resolution/`에 저장한다.
