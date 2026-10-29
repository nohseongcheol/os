# tựThân 커널과 번역기의 tiếngViệt tên

대상은 `platforms/rpi4-native`의 tựThân Java giáTrịNhân, NgườiDùng JVM, C máy nốiKết,
TCP/UDP·FTP, C côngCụTrìnhBiênDịch 이식부, MicroPython 이식부, xâyDựngHệThống·thựcThiLệnh·KiểmThử 도구다.
`golang/worldos/giáTrịQuốcGia/KOR/mãNguồn`의 원칙처럼 기능을 먼저 구분하고 이름을 정한다.
x86 Java 커널과 공용 x86·ARM64 미리 번역기의 tựThân 선언도 cáchĐặtTên 검사에 포함한다.
Linux 실행판의 Chủ CôngCụ, OpenJDK giáTrịPhụTrợ CôngCụ 및 giáTrịBênNgoài giáTrịBảnPhânPhối câyNguồn 전체를
한국어로 giáTrịThửLại 작성했다는 뜻은 아니다.

## cáchĐặtTên 원칙과 말의 근거

- 명사는 자료의 역할을 나타낸다: `thẻXửLýTệp`, `sốCổngĐốiTác`, `lưuTrữVùngNhớĐộng`, `BànPhím`.
- 함수는 행위를 나타낸다: `đọc`, `ghi`, `mở`, `đóng`, `ràngBuộcMạngGọn`, `chạyChươngTrình`.
- TCP의 이어진 giáTrịByte 흐름과 UDP의 giáTrịRanhGiới 있는 자료를 `KếtNối`와 `KênhĐiệnDữLiệu`로 구별한다.
- 짧은 영어 변수도 쓰임에 따라 `độDài`, `vịTríDữLiệu`, `chỉSốTraCứu`, `giáTrịĐãTrảVề`으로 풀어 쓴다.
  chỉSốThứBậc·giáTrịTạm 산술값처럼 여러 역할에 재사용되는 변수는 `chỉSốThứBậc`, `giáTrịĐầuTiên`, `giáTrịThứHai`으로 구별한다.
- 이름이 같아도 giáTrịBênNgoài 구조체의 필드와 tựThân 변수는 별도로 분석한다.

`mụcKênh(通路)`는 이동이나 교류가 이루어지는 길이라는 기존 의미를 TruyềnThông 연결에
적용했다. `giáTrịCổng(窓口)`의 주고받는 접점이라는 의미를 연결을 받는 곳에 적용했다.
이는 국립국어원 한국어기초사전의 [mụcKênh](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=49310),
[giáTrịCổng](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=24898)의 뜻에 근거한다.

`điệnDữLiệu(電文)`은 전보에 담는 글이라는 기존 TruyềnThông 어휘에서 가져와, UDP 자료의
경계가 보존된다는 특징을 드러내는 데 쓴다. 근거는
[한국어기초사전 điệnDữLiệu](https://krdict.korean.go.kr/eng/dicSearch/SearchView?ParaWordNo=74335)이다.
`giáTrịLuồng`, `giáTrịLuồngChạy`, `쌓임`은 우리말의 움직임·làSựTiếpDiễn·쌓이는 모양을 빌린 표현이다.
`LuồngĐầuVào`, `bộLàmViệc`, `lưuTrữNgănXếp` 같은 복합 이름은 이 프로젝트의 기능별 조어다.
이 TừĐiển 근거를 특정 중세 문헌의 최초 출현이나 공인 전산 번역으로 확대하지 않는다.
공인 표준 dịchThuậtNguồn·국어사 điệnDữLiệu 감수를 마쳤다는 뜻도 아니다.

| 기능 | 채택한 tên | giáTrịLýDo |
|---|---|---|
| TCP Socket | KếtNối | 상대와 연결되어 giáTrịThứTự 있는 바이트를 주고받음 |
| ServerSocket | nhậnCổng | 새 연결이 들어오는 접점 |
| DatagramSocket | KênhĐiệnDữLiệu | 각 자료의 경계를 보존하는 TruyềnThông |
| InputStream / OutputStream | LuồngĐầuVào / LuồngĐầuRa | 들어오고 나가는 바이트의 giáTrịThứTự |
| heap / stack | lưuTrữVùngNhớĐộng / lưuTrữNgănXếp | cấpPhátLưuTrữ 방식과 쌓고 꺼내는 KiếnTrúc |
| thread / keyboard | bộLàmViệc / BànPhím | 이어지는 실행과 글쇠의 giáTrịMảng |
| exception / timeout | ngoạiLệ / NgoạiLệHếtGiờChờ | làBìnhThường 처리에서 벗어남과 그 구체적 giáTrịLýDo |

## 경로와 대응표

| phầnCàiĐặt | tiếngViệt đườngDẫn |
|---|---|
| giáTrịNhân·vỏLệnh·Tệp giáTrịTầng | `mãNguồn/*.java` |
| NgườiDùng JVM | `NgườiDùng/Java/MáyẢoJava.java` |
| ARM64 máy nốiKết | `máy/*.c`, `KhởiĐộng/` |
| TCP·UDP·FTP | `NgănXếpMạng/NgănXếpMạng.c`, `NgănXếpMạng/chuyểnGiaoTệp.c` |
| C côngCụTrìnhBiênDịch ChuyểnNền | `TrìnhBiênDịchC/` |
| MicroPython ChuyểnNền | `cầuNốiPython/` |
| xâyDựngHệThống·thựcThiLệnh·KiểmThử | `CôngCụ/`, `tạoMục.mk` |
| Java NgườiDùng API | `JavaTiếngViệt/tiếngViệt/tựThân/` |

[phépÁnhXạTênTệp.tsv](phépÁnhXạTênTệp.tsv), [phépÁnhXạTênJava.tsv](phépÁnhXạTênJava.tsv),
[phépÁnhXạTênC.tsv](phépÁnhXạTênC.tsv), [phépÁnhXạTênPython.tsv](phépÁnhXạTênPython.tsv)에
phầnMụcTrướcĐó 이름과 바뀐 이름이 있다. C/Java 대응표의 Tệp·위치는 이행 당시 기준이다.
đườngDẫn 이동은 Tệp 대응표를 함께 본다. 기존 `tools/*.py`는 tiếngViệt 구현을 호출하는
호환 진입점이며 구현을 두 벌 유지하지 않는다.

## 보존하는 địnhNghĩaChuẩn tên

`public`, `class`, `int`는 예약어다. `String`, `main`, 배열의 `length`는 예약어가 아니다.
phầnMụcHiệnTại 다섯 Java 예제는 `chạy()`·`CácĐốiSố`·tiếngViệt MànHình/giáTrịLuồngChạy API를 사용해
cácTừĐượcDànhTrước·리터럴 외의 식별자를 한국어로 작성한다. MànHình/가닥은 표준 객체를
감싸지 않고 tựThân JVM에 직접 구현했다. 자세한 계약은 [tiếngViệt Java API](../JavaTiếngViệt/HướngDẫn.md)를 본다.

표준 javac는 ChuỗiKýTự 리터럴에 `java.lang.String`, ChuỗiKýTự 결합에 `StringBuilder`
같은 이름을 생성한다. 이들은 tiếngViệt 소스에서도 바이트코드에 남을 trịSố 있다.
기존 표준 class를 실행하는 JVM의 giáTrịPhépÁnhXạ ChuỗiKýTự, 아직 표준 라이브러리를 쓰는
TruyềnThông·Tệp 연결부까지 xâyDựngTấtCả 한국어로 재구현한 것은 아니다. 이름만 일괄 치환하면
mụcBộMôTả·재정의·native 연결이 달라져 호환성이 깨진다.

C 표준 Hàm·kiểuSốNguyên·POSIX ABI, CPU thanhGhi tên, 어셈블리 lệnh, 링커 절 tên,
TinyCC·lwIP·MicroPython이 요구하는 cácThiếtLập 매크로와 헤더 이름도 보존한다.
예: `main`, `memcpy`, `pk_bind`, `mpconfigport.h`, `lwipopts.h`, `stdint.h`.
tựThân C 함수의 câyNguồn 이름은 한국어이며, [cácTênLiênKếtMáy.h](cácTênLiênKếtMáy.h)toánHạngĐầuTiên
기존 AOT·어셈블리·SDK에 공개한 máy 심볼과 연결한다.
Python의 `__init__`, `setUp`, `handle`, 표준 giáTrịMôĐun giáTrịThuộcTính, 명령행 옵션과 JSON 키도
giáTrịBênNgoài 계약이다. `build/`, giáTrịBảnPhânPhối 바이너리 이름과 `/sdk`는 기존 thựcThiLệnh 경로를 유지한다.
giáTrịBênNgoài 원본은 `vendor/`에서 이용허락·해시와 함께 관리한다.

## 검사와 재실행

```sh
cd /home/user/jkoros/platforms/rpi4-native
python3 CôngCụ/kiểmTraCáchĐặtTên.py
make xâyDựngHệThống
make KiểmThử
make test-examples test-ftp test-elf
python3 CôngCụ/thựcThiLệnh.py --desktop --network
```

`CôngCụ/phânTíchCácTênC.py`는 libclang 6으로 C 선언과 참조를 검사한다.
`CôngCụ/*이름반영.py`는 đổiGiáTrị giáTrịTrướcKhi câyNguồn·분석표를 필요로 하는 일회성 이행 도구다.
이미 변경된 소스에 giáTrịThửLại 적용하여 대응표를 덮어쓰지 않는다.

## C TruyềnThông 구조체와 Python lỗi

C 통신에서 `갈래`는 địaChỉ 체계를 구분하고 `sốCổng`는 port, `giáTrịĐịaChỉ`은
IPv4 주소의 32비트 값을 나타낸다. `GiaoThứcĐiệnDữLiệu`은 앞서 설명한 điệnDữLiệu(電文)과
giáTrịQuyƯớc(規約)을 결합해 UDP의 기능을 드러낸 프로젝트 이름이다.

| 표준 표현 | tiếngViệt 직접 phầnCàiĐặt |
|---|---|
| AF_INET / SOCK_DGRAM / IPPROTO_UDP | enum의 HọLiênMạng / ỔCắmMạngĐiệnDữLiệu / GiaoThứcĐiệnDữLiệu |
| struct pk_sockaddr_in | struct ĐịaChỉỔCắmMạngLiênMạng |
| sin_family / sin_port | họĐịaChỉ / sốCổng |
| sin_addr.s_addr | ĐịaChỉLiênMạng.giáTrịĐịaChỉ |
| OSError / lỗi.args[0] | LỗiHệThống / lỗi.sốHiệu |

tiếngViệt 구조체는 `#define` 치환이나 giáTrịTrường 별칭이 아닌 별개 자료형이다.
표준 구조체와 같은 16바이트 배치를 선언하며 giáTrịNhân SVC에서 giáTrịByte 복사로
검사한다. `tạoĐiểmCuối`·`gửiDữLiệuĐiệnDữLiệu`와 Tệp 함수는 giáTrịTĩnh 라이브러리에
dữLiệuThựcTế tiếngViệt 이름의 Hàm 심볼을 갖는다. 기존 pk_* 심볼도 유지한다.
phầnMụcTrướcĐó 코드에서 tiếngViệt TruyềnThông 함수에 pk_sockaddr*를 전달했다면 tiếngViệt 구조체로
옮기거나, 표준 구조체와 pk_* 함수의 짝을 유지한다.

Python의 `LỗiHệThống`는 OSError의 tiếngViệt 하위 클래스이며 연결부에서
lỗi 번호를 보존하여 변환한다. 일반 Python 문법과 giáTrịBênNgoài 패키지의 API는 유지한다.

## 직접 GUI 이름의 뜻과 검토 cắtXén

`TácVụChạyĐược`은 수행할 내용을, `thựcThiTácVụ`는 그 수행을 나타낸다.
`BộNhậnHànhĐộng`는 동작이 발생했다는 알림을 받는 역할, `ThôngBáoHànhĐộng`은 전달되는 사건이다.
`nút`는 눌러 동작시키는 조작부, `nhãn`는 HướngDẫn 글의 chỉSốVịTrí,
`TrườngVănBản`은 글을 적는 chỉSốVịTrí, `bộLàmViệc`은 이어지는 thựcThiLệnh 흐름을 뜻한다.
`thựcThiLệnh(實行)`·`hànhĐộng(動作)`의 기존 뜻과 `받다`·`알리다`·`giáTrịLuồngChạy`의 기능을
결합한 프로젝트 이름이다. 새 복합어가 역사 문헌에 그대로 있었다거나
특정 시대에 phầnMụcBanĐầu 쓰였다고 주장하지 않는다.

전체 저장소는 `python3 CôngCụ/XemDuyệtNguồn.py`로 검토한다.
결과는 `build/verification/naming/source-review.json`이며 파일별 tệpMãBăm,
ASCII 파일명과 Python의 영어 KhaiBáo 위치를 기록한다.
공용 ARM64·x86 번역기의 구현은 `compiler/CôngCụJava/BiênDịchTrước.java`로 전환했다. `compiler/BiênDịchTrước.py`는 호환 진입점이다.
`compiler/arm64.py`는 phầnMụcTrướcĐó 경로와 `ARM64(...).generate(...)` 호출을 giáTrịSựTiếpDiễn 주는
호환 진입점이다. `compiler/classfile.py`, OpenJDK giáTrịPhụTrợ CôngCụ, Linux giáTrịPhiênBản 도구와
기존 호환 진입점에는 영어 이름이 남아 있다. 따라서 전체 저장소가
cácTừĐượcDànhTrước 외 100% 한국어라고 판정하지 않는다.
`CôngCụ/kiểmTraCáchĐặtTên.py --ngônNgữC`는 hoạtĐộng ARM64 소스의 KhaiBáo, C 의미 phânTíchGiáTrị,
x86 Java 커널과 공용 번역기의 tựThân KhaiBáo, Java VíDụ 전체 giáTrịĐịnhDanh,
ARM64 Python 예제와 직접 GUI/가닥에 표준 래퍼가 없는지를 별도로 검사한다.

## phầnMụcHiệnTại 기능을 기준으로 보완한 tên

번역은 글자를 음역하는 대신 자료의 역할과 함수의 행동을 구분한다.
동일한 영어 이름도 문맥이 다르면 tiếngViệt 이름을 달리 정한다.
Tệp 이름은 주된 기능을 나타내고, Hàm 이름은 행동을, giáTrịBiến 이름은 담는 자료를 나타낸다.
cácTừĐượcDànhTrước, 표준 API 및 giáTrịBênNgoài nốiKết 규약은 따로 기록한다.

| phầnMụcTrướcĐó tên | 적용한 tên | phầnMụcHiệnTại 기능 |
|---|---|---|
| `arm64.py`의 phầnCàiĐặt | `compiler/CôngCụJava/BiênDịchTrước.java` | Java 바이트코드를 독립 실행용 C 원문으로 미리 dịchThuậtNguồn |
| `ARM64`, `generate` | `TrìnhBiênDịchMãMáy`, `sinh` | dịchThuậtNguồn 상태를 담는 객체와 C mãNguồn sinh giáTrịHànhVi |
| `prototype`, `method` | `nguyênMẫuPhươngThức`, `thânPhươngThức` | 함수의 giáTrịĐịnhDạng 선언과 dữLiệuThựcTế lệnh mãNguồn |
| `profile`, `heap_words` | `đốiĐíchViệcThựcThi`, `sốLượngTừVùngNhớĐộng` | giáTrịNhân·NgườiDùng 구분과 cấpPhátLưuTrữ BộNhớ 공간의 máy từTừVựng trịSố |
| `pc`, `op` | `vịTríLệnh`, `명령번호` | 바이트코드에서의 위치와 수행할 명령의 sốHiệu |
| `x`, `y`, `w`, `h` | `tọaĐộX`, `tọaĐộY`, `rộngMiền`, `caoMiền` | giáTrịTừXa 화면의 위치와 직사각형 cỡ |
| `p`, `n`, `i`, `j` | `vịTríDữLiệu`, `giáTrị`, `chỉSốThứBậc`, `thứBậcPhíaTrong` | giáTrịTừXa MànHình DữLiệu·giáTrịChữSố·giáTrịLầnLặp chỉSốVịTrí; 파일별 기능을 확인해 적용 |
| `aot_heap_info`, `__stack_top` | `traCứuBộNhớBiênDịchTrước`, `ĐỉnhNgănXếp` | máy nốiKết 규약을 유지하면서 tựThân 소스에서 사용하는 tên |
| `앞캐리지` | `dòngTrướcĐóĐếnTrảVề` | 앞서 받은 문자가 줄복귀였는지 기억하여 중복 줄바꿈을 막음 |

[cácTênTrìnhBiênDịchDùngChung.tsv](cácTênTrìnhBiênDịchDùngChung.tsv)에 côngCụTrìnhBiênDịch 참조의 dữLiệuThựcTế đổiGiáTrị 기록을 남겼다.
추가로 보존한 C·POSIX/lwIP/libassh 이름의 이유는
[bằngChứngTênChuẩn.json](bằngChứngTênChuẩn.json)에 기록한다.
`TrìnhBiênDịchC/côngCụTrìnhBiênDịch.c`는 TinyCC giáTrịBênNgoài 원문을 포함하는 nốiKết 파일로 tựThân 선언이 없어서
C tựThân KhaiBáo 분석에서는 제외한다. dữLiệuThựcTế giáTrịNhân 빌드에서는 việcXửLýTiếpTục 컴파일한다.

### 말의 뿌리와 새로운 복합 tên

`BộNhớ(記憶)`과 `chỉSốTraCứu(索引)`은 기존 한자어를 쓴다.
기억은 자료를 간직하는 기능에, 색인은 giáTrịThứTự 있는 항목을 찾아 지정하는 기능에 적용한다.
TừĐiển 근거는 국립국어원 한국어기초사전의
[BộNhớ](https://krdict.korean.go.kr/eng/dicSearch/SearchView?ParaWordNo=38812&nation=eng),
[chỉSốTraCứu](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=63787)이다.

`lưuTrữNgănXếp`, `đẩyGiáTrị`, `lấyĐỉnhGiáTrị`는 자료를 포개고 phầnMụcCuối 자료부터 꺼내는 thựcThiLệnh 구조를 드러낸다.
`쌓다`의 기존 뜻에 근거한 기능별 조어이며, 사전의
[쌓다](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=62095)를 참고한다.
`thờiGianCủaTrước`은 thựcThiLệnh 전에 번역한다는 기능을 직접 나타낸다.
`từMáy`은 처리기의 DữLiệu 단위를 가리키며, 언어의 일반 낱말과 구별하도록 `máy`를 붙였다.
`BiênDịchTrước`, `sốLượngTừVùngNhớĐộng` 같은 복합 이름은 phầnMụcHiệnTại 기능에 맞게 만든 프로젝트 용어다.
이 복합어가 옛 문헌에 그대로 있었다거나 특정 시대에 phầnMụcBanĐầu 나타났다는 뜻은 아니다.
확인되지 않은 중세 형태나 최초 giáTrịDùng 연대는 어원 근거로 적지 않는다.

생성되는 C의 내부 kiểuDữLiệu·giáTrịMảng·Hàm·phạmViCụcBộ giáTrịBiến·nhánh 이름도 한국어로 바꾼다.
직접 vănBảnHangul 식별자를 읽지 못하는 예전 GCC를 위해 호환 API는 같은 tiếngViệt 이름을
표준 C 범용 KýTự 표기로 출력한다. dữLiệuThựcTế ARM64 빌드는 Clang으로 읽을 trịSố 있는 vănBảnHangul 원문을 사용한다.
ChuỗiKýTự, C 표준 Hàm, `java_entry` 같은 공개 nốiKết 이름은 바꾸지 않는다.

셸의 사용법·문법 lỗi·Tệp 및 BộNhớ miềnĐịaChỉ 안내도 한국어로 보완했다.
`READY`, `PASS`, `HEX BEGIN`처럼 KiểmThử·Tệp giáTrịChuyểnGiao 도구가 읽는 giáTrịDấuMốc,
명령행 옵션과 기존 giáTrịChỉLệnh, JVM giáTrịLớp tên·Tệp giáTrịĐịnhDạng·ThiếtBị 이름은 호환 표기로 남는다.
x86 VGA KýTự 화면은 한글을 표시하지 못하므로 tiếngViệt 문구는 UTF-8 giáTrịNốiTiếp 단말에서 확인한다.
