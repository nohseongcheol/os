# tựThân 커널에서 vi·여러 thiếtBịCuối·vănBảnHangul 프로그래밍 사용하기

tiếngViệt TruyềnThông·ngoạiLệ 사용법은 [tiếngViệt Java API](JavaTiếngViệt/HướngDẫn.md), Hàm·giáTrịBiến·Tệp 이름의 변경과 어원 근거는 [cáchĐặtTên HướngDẫn](cáchĐặtTên/HướngDẫn.md)를 참고한다.

대상은 `platforms/rpi4-native`의 tựThân AArch64 Java 커널이다. vi와 Java/Python/C/C++ 프로그램은 EL0에서 실행한다. Linux 실행판과 별도이며 giáTrịĐáy giáTrịHỗTrợ 목록은 전체 OpenJDK·Vim·POSIX 구현을 뜻하지 않는다.

게스트 `cc`/`jaot`, JAR 직접 thựcThiLệnh, giáTrịBênNgoài TCP/UDP와 FTP는 [새 thựcThiLệnh 매뉴얼](ViệcBiênDịchVàChuyểnGiaoTệp.md)을 참고한다.

## GUI와 여러 thiếtBịCuối

```sh
cd /home/user/jkoros/platforms/rpi4-native
make desktop
```

Remmina에서 **VNC**, địaChỉ **127.0.0.1:5902**로 연결한다. MànHình giáTrịĐỉnh **+ New terminal**, **Ctrl+Shift+T**로 터미널을 추가한다. giáTrịTốiĐa 네 개다. bênThượng thiếtBịCuối 버튼 또는 창을 클릭해 선택하고 **F6**으로 순환한다. 제목줄을 끌어서 옮기고 **phải giáTrịĐỉnh X**를 클릭하면 닫힌다. phầnMụcCuối 창을 닫아도 bênThượng thựcThiLệnh 버튼으로 giáTrịThửLại giáTrịCột trịSố 있다. 기존 `terminal`, `exit`, F12도 사용할 trịSố 있다.

창마다 phầnMụcHiệnTại 디렉터리, vỏLệnh giáTrịBiến, lệnh bảnGhiNhậtKý, giáTrịVào 중인 명령과 ChươngTrình thựcThiLệnh 상태를 보관한다. Tệp 저장소는 공유한다. vi와 Swing의 이벤트 chờGiáTrị 중에 다른 터미널로 전환하면 NgườiDùng dữLiệuBộNhớ·레지스터·Tệp/giáTrịỔCắmMạng 연결을 보존했다가 돌아올 때 재개한다. **phầnMụcHiệnTại 네 프로그램이 동시에 CPU에서 실행되는 선점형 스케줄러는 아니다.** phépTính 중인 프로그램은 phầnMụcKếTiếp giáTrịVào chờGiáTrị 또는 기존 thựcThiLệnh 기한까지 전환이 지연될 trịSố 있다.

X로 터미널을 닫으면 그 터미널의 thựcThiLệnh 중인 프로그램도 종료하며 mụcBộMôTả·소켓을 회수한다. 저장하지 않은 giáTrịSửa 내용은 사라진다. 종료한 슬롯은 새 창에서 재사용한다. phầnMụcHiệnTại 모든 파일은 RAM에 있으며 VM 재시작 후에는 남지 않는다.

화면과 cửaSổ 판단은 게스트 커널이 처리한다. QEMU thựcThiLệnh 도구는 VNC 키와 마우스 좌표를 UART 패킷으로 전달한다. dữLiệuThựcTế Pi4 USB 입력기와 phầnCứngVậtLý 부팅은 아직 검증하지 않았다. 일반 UART 셸은 `make run`, GUI CôngCụ 종료는 Chủ 터미널의 Ctrl+C다.

## vi giáTrịDùng

```text
mkdir TácVụ
cd TácVụ
vi LờiChào.py
```

`vi`는 새로 구현한 **vi lệnh 부분집합** 편집기다. 내장 `build/user/vi.elf`를 보호된 NgườiDùng 영역에 적재한다. Tệp 크기는 UTF-8 giáTrịByte gốcCâyDựÁn 16 KiB, 경로는 63바이트까지다. 디스크에 설치한 Vim/Neovim 바이너리를 실행하는 것이 아니다.

| giáTrịPhím/lệnh | hànhĐộng |
|---|---|
| `i`, `a`, `I`, `A` | phầnMụcHiệnTại/phầnMụcKếTiếp vịTrí 또는 dòng phầnMụcBanĐầu/끝에서 giáTrịVào |
| `o`, `O` | giáTrịĐáy/위에 새 줄을 만들고 giáTrịVào |
| Esc | 일반 giáTrịChếĐộ |
| `h j k l`, 방향키 | UTF-8 KýTự/dòng giáTrịDiChuyển |
| `0`, `$`, Home, End | dòng phầnMụcBanĐầu/phầnKết |
| `gg`, `G`, `:sốHiệu` | Tệp phầnMụcBanĐầu/phầnMụcCuối dòng/giáTrịGán dòng |
| PgUp, PgDn | MànHình giáTrịĐơnVị giáTrịDiChuyển |
| `x`, Delete | phầnMụcHiệnTại KýTự 삭제 |
| `dd`, `yy`, `p` | dòng 삭제/saoChépGiáTrị/vănBảnDán |
| `u` | phầnMụcCuối 편집을 cầuNốiTrảVề; 한 giáTrịGiaiĐoạn 토글 |
| `/ChuỗiKýTự`, `n` | 단순 ChuỗiKýTự 검색/phầnMụcKếTiếp làBằng; 정규식 phươngThứcThiếu |
| `:w`, `:w 다른이름` | RAM Tệp giáTrịCất/다른 경로로 giáTrịCất |
| `:q` | 변경이 없을 때 chươngTrìnhRa |
| `:q!` | 변경을 버리고 chươngTrìnhRa |
| `:wq`, `ZZ` | 저장하고 chươngTrìnhRa |

붙여 넣은 한글을 KýTự 경계에 맞춰 giáTrịDiChuyển·삭제한다. 일반 vi의 수량 접두사, giáTrịVĩLệnh, cácThiếtLập Tệp, 플러그인, 정규식, 여러 버퍼/분할 cửaSổ, 문법 강조 등은 아직 없다. `--desktop`에서는 F9·Shift+Space·한/toánHạngKhôngSố 키로 두벌식 조합을 전환한다. PC 입력기를 영어로 두고 cửaSổ tiêuĐềCửaSổ `[KO]`에서 입력하며, `help ko`에 단축키를 표시한다. 완성된 Unicode 문자와 VNC의 명시적 붙여넣기도 전달한다.

vi와 Swing 프로그램은 **단독 lệnh**으로 실행한다. 파이프·리다이렉션·giáTrịKịchBản·`;`/`&&`/`||`로 연결한 실행에서 tươngTác 대기를 시작하면 거부한다. giáTrịVào 대기는 약 2초 CPU 기한을 갱신하지만 giáTrịVào chờGiáTrị 없이 무한 반복하는 프로그램은 기존처럼 종료한다.

## vănBảnHangul Java

vi에서 다음을 `LờiChào.java`에 입력하고 Esc → `:wq`로 저장한다.

```java
public class LờiChào {
    static int thêmCácGiáTrị(int thứBậcĐầuTiên, int thứBậcThứHai) { return thứBậcĐầuTiên + thứBậcThứHai; }
    public static void main(String[] cácĐốiSố) {
        int giáTrịTổngCộng = thêmCácGiáTrị(20, 22);
        System.out.println("안녕하세요 · giáTrịTổngCộng=" + giáTrịTổngCộng);
    }
}
```

게스트 셸에서 실행한다.

```text
javac LờiChào.java
java LờiChào
```

vănBảnHangul vănBảnTênTệp·tênLớp·vănBảnTênPhươngThức·변수명·문자열을 사용할 trịSố 있다. **게스트 javac는 giáTrịTĩnh Java 부분집합**이다. giáTrịĐốiTượng·리스너·Swing·소켓을 사용하는 소스는 phầnMụcHiệnTại Chủ JDK에서 `javac --release 8 -encoding UTF-8`로 컴파일하고 tựThân JVM에 class를 올린다. tựThân JVM에서 지원하는 mãByte/API 범위는 [MôiTrườngMôiTrườngChạyJava.md](MôiTrườngMôiTrườngChạyJava.md)를 따른다.

```sh
# Chủ
mkdir -p build/my-java
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/my-java KiểmThử/Java/ThửSwing.java
python3 CôngCụ/cácTệpTảiLên.py build/my-java/ThửSwing.class
```

`upload.py`는 게스트 `load`에 붙여 넣을 16진수 명령을 생성한다. ĐầuRa 전체를 GUI 터미널에 보내면 업로드한다. 업로드 trạngTháiSau **별도로** `java ThửSwing`을 실행한다. 종속 class가 있으면 각각 업로드한다. 패키지 class의 파일명은 `패키지.giáTrịLớp.class` 형식이다. 내장 tiếngViệt 라이브러리는 별도 업로드가 giáTrịCầnĐến 없다. tiếngViệt cửaSổ API의 예제는 [thửCửaSổHangul.java](KiểmThử/Java/thửCửaSổHangul.java)이며 같은 방법으로 biênDịchNguồn·업로드해 `java thửCửaSổHangul`으로 실행한다.

GUI가 giáTrịCầnĐến 없는 단일 câyNguồn/클래스는 호스트의 `python3 CôngCụ/thựcThiTệp.py đườngDẫn/LờiChào.java`로 별도 QEMU에 업로드·thựcThiLệnh·종료할 trịSố 있다. tươngTác Swing에는 thựcThiLệnh trạngTháiSau NgườiDùng 입력을 유지하는 `make desktop`을 사용한다.

## tựThân JVM의 Swing cắtXén

실제로 제공하는 것은 **표준 패키지 이름으로 호출하는 tựThân Swing API 부분집합**이다. OpenJDK `java.desktop` 모듈이나 AWT 전체를 이식한 것은 아니다.

| API | hànhĐộng |
|---|---|
| `JFrame` | tiêuĐềCửaSổ, cỡ·vịTrí, hiệnCửaSổ, đóng 정책, dispose |
| `JPanel` | giáTrịCon 요소를 담는 패널 |
| `JLabel` | 한글을 포함한 ChuỗiKýTự hiệnGiáTrị·đổiGiáTrị |
| `JButton` | 버튼과 ActionListener giáTrịNhấnChuột mụcGiáTrịTiếnTrình |
| `JTextField` | 한 dòng UTF-8 giáTrịVào, 삭제, getText/setText, Enter 이벤트 |
| giáTrịChung | setBounds, setSize, add, getContentPane, repaint, validate |
| `SwingUtilities` | invokeLater, isEventDispatchThread |
| `ActionEvent` | getSource, getActionCommand, getID |

`setLayout(null)`과 `setBounds`로 배치한다. FlowLayout/BorderLayout/GridLayout, pack, 폰트·스타일 전체, 메뉴·테이블·트리·스크롤 패널, Java2D, 네이티브 AWT peer/JNI, 복잡한 KýTự 조판은 아직 없다. 이벤트 콜백은 tựThân JVM의 단일 이벤트 thựcThiLệnh 흐름에서 처리하며 OpenJDK EDT 구현과 동일하지 않다. cửaSổ·요소는 thựcThiLệnh 하나당 giáTrịTổngCộng 32개, giáTrịPhầnTử 글자는 giáTrịTốiĐa 127 코드포인트다. giáTrịMặcĐịnh 서체와 색은 커널이 제공한다.

[ThửSwing.java](KiểmThử/Java/ThửSwing.java)는 cửaSổ·vănBảnHangul giáTrịThẻ·TrườngVănBản·버튼·이벤트 처리의 thựcThiLệnh 가능한 예제다. [tựThân Swing MànHình](build/verification/swing/native-swing.png)을 참고한다.

tiếngViệt 라이브러리에는 다음을 추가했다. Chủ biênDịchNguồn 시 `dist/jkoros-native-korean.jar`를 classpath에 넣는다.

- `tiếngViệt.tựThân.cửaSổ`: `thêmPhầnTử`, `hiệnCửaSổ`, `đóng`.
- `tiếngViệt.tựThân.ThànhTốGiaoDiện`: `giáTrịThẻ`, `nút`, `TrườngVănBản` sinh.
- `tiếngViệt.tựThân.vậnChuyểnKếtNối`: `nốiKết`, `lắngNgheĐiểmCuối`, `nhận`.
- 기존 `ĐầuRa`, `KýTự`, `Tệp`, `TácVụ`, `danhSáchMục`, `TừĐiển`, `TruyềnThông`, `MànHình`, `giáTrịNhân`도 유지한다.

## Java 네트워크

기존 `DatagramSocket`/`DatagramPacket`의 UDP 루프백에 `Socket`/`ServerSocket`의 **giáTrịNhân 내부 연결형 giáTrịByte giáTrịLuồng**을 추가했다. Tệp/소켓과 마찬가지로 SVC를 통해 Java 커널이 전송한다. 물리 NIC의 TCP/IP 패킷 스택은 아니다.

```java
java.net.ServerSocket giáTrịMáyChủ = new java.net.ServerSocket(9250);
java.net.Socket giáTrịKhách = new java.net.Socket("localhost", 9250);
java.net.Socket nốiKết = giáTrịMáyChủ.accept();
giáTrịKhách.getOutputStream().write("안녕하세요".getBytes("UTF-8"));
byte[] phầnMụcĐãNhận = new byte[64];
int độDài = nốiKết.getInputStream().read(phầnMụcĐãNhận);
nốiKết.close(); giáTrịKhách.close(); giáTrịMáyChủ.close();
```

sinh·nốiKết·accept·양방향 giáTrịByte/giáTrịMảng đầuRaĐầuVào·close·EOF·setSoTimeout을 지원한다. `String.getBytes()`와 UTF-8 이름을 지정한 getBytes도 제공한다. 루프백 주소는 `localhost`/`127.0.0.1`이다. 연결형 điểmKếtThúc 16개, nhậnGiáTrị 버퍼당 1024바이트, chờGiáTrị nốiKết giáTrịTốiĐa 4개이며 Java의 대기는 내부 가닥에 실행을 양보한다. giáTrịMặcĐịnh giáTrịThờiGian giáTrịGiớiHạn 0은 별도 giáTrịỔCắmMạng 기한을 설정하지 않지만 JVM lệnh trịSố/giáTrịNhân thựcThiLệnh 기한은 여전히 적용된다.

giáTrịBênNgoài giáTrịChữSố IPv4 TCP/UDP는 lwIP/SLIP로 지원한다. dữLiệuThựcTế Ethernet/Wi-Fi 드라이버, DNS·TLS·HTTP thưViện 전체는 미지원이다. `java.net`의 모든 메서드와 옵션, `SocketChannel`/select, SSL, shutdownInput/Output는 아직 없다. [thửLuồng.java](KiểmThử/Java/thửLuồng.java)는 dữLiệuThựcTế 송수신·EOF·기한·nốiKết 회수의 KiểmThử 예제다.

## vănBảnHangul Python

게스트 vi에서 vănBảnHangul 이름을 사용해 작성한다.

```python
giáTrị = 21

def 두배(giáTrịChữSố):
    return giáTrịChữSố * 2

print("kếtQuả:", 두배(giáTrị))
```

giáTrịCất trạngTháiSau `python LờiChào.py`로 실행한다. 실행기는 MicroPython 1.24.1이다. Python 문법 키워드는 그대로 사용하며 Hàm·giáTrịBiến·Tệp 이름과 문자열을 한글로 쓴다.

[tiếngViệt.py](VíDụ/LậpTrìnhHangul/tiếngViệt.py)를 같은 디렉터리에 두면 phầnMụcKếTiếp 별칭을 사용할 trịSố 있다.

```python
import tiếngViệt
tiếngViệt.ghiTệp("LờiChào.txt", "안녕하세요")
tiếngViệt.ĐầuRa(tiếngViệt.đọcTệp("LờiChào.txt").decode())
```

ĐầuRa·Tệp đọc/ghi/삭제·표준 giáTrịVào·hìnhChữNhật·giáTrịThờiGian·UDP를 연결한다. 기존 `udp_send`는 루프백, 새 `udp_sendto(fd, "10.0.2.2", port, data)`는 giáTrịChữSố IPv4 địaChỉ 전송이다. `wait_key()`는 화면을 확인할 때 tươngTác 입력을 기다린다. Python 함수는 `jkoros` 내장 모듈을 통해 SVC를 사용한다. C ABI인 posix-kor giáTrịTĩnh 라이브러리를 Python이 직접 링크하는 구성은 아니다. CPython과 일반 giáTrịPhầnMởRộng 모듈은 아직 없다. 제한형 `pip`의 câyNguồn 설치는 [Python GóiGộp HướngDẫn](GóiGộpPython.md)를 따른다. [giáTrịBa 언어의 dữLiệuThựcTế VíDụ](../../example/README.md).

## C·C++에서 posix-kor gọiThựcHiện

두 NgônNgữ xâyDựngTấtCả tiếngViệt 헤더와 Hàm 이름을 직접 사용한다. [LờiChào.c](VíDụ/LậpTrìnhHangul/LờiChào.c), [LờiChào.cpp](VíDụ/LậpTrìnhHangul/LờiChào.cpp)toánHạngĐầuTiên dữLiệuThựcTế EL0 thựcThiLệnh KiểmThử 대상이다.

```c
#include "ABITệp.h"
#ifdef __cplusplus
extern "C"
#endif
int bắtChạyChươngTrìnhNgườiDùng(int cácĐốiSố) {
    (void)cácĐốiSố;
    const char lờiChào[] = "안녕하세요\n";
    int TàiLiệu = mởTệp("LờiChào.txt", GhiĐọc | ThiếuNếuTạo | CácNộiDungCắtNgắn, 0600);
    if (TàiLiệu < 0) return 1;
    kiểuKếtQuảVàoRa sốLượngĐãGhi = ghiDữLiệuTệp(TàiLiệu, lờiChào, sizeof(lờiChào) - 1);
    đóngTệp(TàiLiệu);
    ghiDữLiệuTệp(1, lờiChào, sizeof(lờiChào) - 1); /* phầnMụcHiệnTại thiếtBịCuối stdout */
    return sốLượngĐãGhi == sizeof(lờiChào) - 1 ? 0 : 2;
}
```

파일은 게스트 vi로 작성할 trịSố 있다. C는 게스트 `cc` 또는 Chủ SDK, C++는 Chủ SDK의 Clang++로 컴파일한다. giáTrịĐáy 예제는 기존 Chủ SDK 경로다. 게스트 내부 GCC/Clang·libc/libstdc++ 전체를 탑재한 것은 아니다. SDK가 `.c`에는 C11, `.cpp`에는 C++11을 선택한다.

```sh
# 호스트에서 SDK sinh·tríchXuất
make sdk
mkdir -p build/sdk-work
tar -xzf dist/jkoros-native-aarch64-sdk.tar.gz -C build/sdk-work
cd build/sdk-work/jkoros-native-sdk
python3 compile.py examples/LờiChào.c -o LờiChào-c.elf
python3 compile.py examples/LờiChào.cpp -o LờiChào-cpp.elf

# 프로젝트로 돌아와 별도 QEMU에서 dữLiệuThựcTế thựcThiLệnh
cd /home/user/jkoros/platforms/rpi4-native
python3 CôngCụ/thựcThiTệp.py build/sdk-work/jkoros-native-sdk/LờiChào-c.elf
python3 CôngCụ/thựcThiTệp.py build/sdk-work/jkoros-native-sdk/LờiChào-cpp.elf
```

phầnMụcHiệnTại GUI VM에서 실행하려면 `python3 CôngCụ/cácTệpTảiLên.py đườngDẫn/LờiChào-c.elf`의 출력을 게스트에 보내고 `run LờiChào-c.elf`를 입력한다. 게스트에서 작성한 소스의 전송은 `hex vănBảnTênTệp`으로 내용을 얻어 호스트에서 `bytes.fromhex(...)`로 복원할 trịSố 있다. 호스트와 게스트의 Tệp 시스템은 별개다.

| tiếngViệt tên | C kýHiệu | cắtXén |
|---|---|---|
| mởTệp/đóngTệp | pk_open/pk_close | RAM Tệp, giáTrịĐốiTác/절대 đườngDẫn |
| đọcDữLiệuTệp/ghiDữLiệuTệp | pk_read/pk_write | Tệp, fd 0/1/2 표준 đầuRaĐầuVào, 연결형 giáTrịỔCắmMạng |
| dịchVịTệp | pk_lseek | PhầnĐầuTừ/gốcCâyHiệnTại/gốcKếtThúc |
| cỡTệp/đặtGiáTrịĐộDàiTệp | pk_size/pk_ftruncate | độDài giáTrịTruyVấn/đổiGiáTrị |
| gỡTênMụcTệp | pk_unlink | Tệp tên 삭제 |
| lưuTrữTệpChốt | pk_fsync | RAM이므로 -1, sốLỗi=ENOSYS |
| tạoĐiểmCuối/ràngBuộcĐịaChỉ | pk_socket/pk_bind | AF_INET, SOCK_DGRAM 또는 SOCK_STREAM |
| gửiDữLiệuĐiệnDữLiệu/nhậnDữLiệuĐiệnDữLiệu | pk_sendto/pk_recvfrom | UDP 루프백 |
| kếtNốiMạng | pk_connect | 연결형 루프백 |
| chờKếtNốiMạngCho | pk_listen | chờGiáTrị nốiKết giáTrịTốiĐa 4개 |
| chấpNhậnKếtNốiMạng | pk_accept | phầnMụcHiệnTại địaChỉ 인수는 NULL/NULL만 giáTrịHỗTrợ |
| đọcĐịaChỉỔCắmMạng | pk_getsockname | 로컬 địaChỉ/giáTrịCổng |

`ABIMạng.h`의 tựThân `pk_sockaddr_in`을 사용하며 giáTrịCổng·주소는 `ngắnKiểuMạng`/`sốNguyênMạng`로 변환한다. C giáTrịỔCắmMạng 호출은 비차단이며 DữLiệu/연결이 없으면 -1과 `sốLỗi=11`(EAGAIN)을 반환한다. 양수 đầuRaĐầuVào 결과가 요청보다 작을 trịSố 있으므로 giáTrịLầnLặp 처리한다. giáTrịSựThấtBại 후에만 오류번호를 확인한다.

[giáTrịLuồng.c](VíDụ/LậpTrìnhHangul/giáTrịLuồng.c)는 C에서 tiếngViệt 이름으로 nốiKết·accept·giáTrịPhầnCon đọc/ghi·큐 포화·EOF를 처리하는 thựcThiLệnh 예제다. SDK의 `examples/giáTrịLuồng.c`를 같은 `compile.py`로 컴파일한다.

SDK는 **libposix-kor-user.a**를 링크한다. gọiThựcHiện 흐름은 C/C++ → dữLiệuThựcTế tiếngViệt C Hàm 또는 호환용 `pk_*` → `svc #0` → 커널의 소유권·conTrỏ CácPhépKiểmTra → Java RAM Tệp/루프백 또는 giáTrịBênNgoài lwIP TCP/UDP 구현이다. `libposix-kor-arm64.a`는 giáTrịNhân 내부용이므로 EL0 프로그램에 링크하지 않는다. Linux 헤더나 Linux ELF와 혼합하지 않는다. 동적 nốiKết, 표준 C printf, libstdc++/STL, ngoạiLệ·RTTI는 제공하지 않으며 C++의 giáTrịTĩnh 생성자·phạmViCụcBộ giáTrịĐốiTượng 소멸자는 지원한다. 상세 sốHiệu·dữLiệuBộNhớ 범위는 [ABIGọiNgườiDùng.md](ABIGọiNgườiDùng.md)를 참고한다.

## thẩmĐịnh

`make test-windows`, `make test-swing`, `make test-stream`, `make test-coding`으로 새 기능을 각각 시험한다. `make test`는 기존 vỏLệnh·VNC·JVM·AOT·giáTrịNhân bảoVệGiáTrị 시험까지 포함한다. dữLiệuThựcTế BoMạch 대신 QEMU raspi4b에서 수행한다. 결과는 [phầnMụcTrướcĐó GUI giáTrịPhầnMởRộng thẩmĐịnh bảnGhiNhậtKý](build/verification/release.json)과 [phầnMụcHiệnTại MôiTrườngChạy thẩmĐịnh bảnGhiNhậtKý](build/verification/native-runtime-summary.json), [여러 thiếtBịCuối MànHình](build/verification/windows/four-terminals.png), [Swing MànHình](build/verification/swing/native-swing.png)을 참고한다.

phầnCàiĐặt 시 참고한 표준 API: [Socket](https://docs.oracle.com/javase/8/docs/api/java/net/Socket.html), [JFrame](https://docs.oracle.com/javase/8/docs/api/javax/swing/JFrame.html), [JButton](https://docs.oracle.com/javase/8/docs/api/javax/swing/JButton.html). 이 문서의 phầnCàiĐặt 범위가 giáTrịĐỉnh 표준 전체를 지원한다는 뜻은 아니다.

## tiếngViệt 이름으로 직접 작성하는 창과 giáTrịLuồngChạy

`example/java/VíDụCửaSổ.java`는 `TácVụChạyĐược.thựcThiTácVụ`,
`BộNhậnHànhĐộng.nhậnHànhĐộng(ThôngBáoHànhĐộng)`, `nút`, `HàngĐợiSựKiện.gọiThựcHiệnVềSau`, `chạy()`을 쓴다.
tựThân JVM에 이 이름들의 giáTrịĐốiTượng·giáTrịPhươngThức·콜백을 직접 구현했으며 영어 Swing 객체를
보관하는 래퍼가 아니다. `bộLàmViệc`도 tựThân 스케줄러와 직접 연결된다.
세부 메서드와 기존 tiếngViệt API에서의 변경은 [tiếngViệt API TàiLiệu](JavaTiếngViệt/HướngDẫn.md)를 본다.

Chủ javac는 giáTrịBảnPhânPhối JAR를 giáTrịLớp 경로로 사용한다.

```sh
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/한국어사용 ../../example/java/VíDụCửaSổ.java
python3 CôngCụ/thựcThiLệnh.py --desktop --network --resolution 1920x1080
```

게스트에는 빌드한 예제가 `/example/java`에 설치된다.

```text
cd /example/java
java VíDụCửaSổ
```

직접 MànHình/giáTrịLuồngChạy API와 `chạy()` 진입점은 tựThân JVM 전용이다.
전체 OpenJDK·Swing 재구현이나 일반 OpenJDK에서 같은 API의 실행을 보장하지 않는다.
기존 표준 `main(String[])` 프로그램은 việcXửLýTiếpTục 실행할 trịSố 있다.
