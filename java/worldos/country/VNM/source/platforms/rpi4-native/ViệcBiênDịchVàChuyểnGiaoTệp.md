# tựThân ARM64 giáTrịNhân: FTP, C, JAR와 AOT thựcThiLệnh

대상은 **Linux를 적재하지 않는 Raspberry Pi 4용 Java AOT giáTrịNhân**이다. CPU·ThiếtBị 경계는 C/어셈블리, Tệp 체계와 셸은 Java이며, 이번 TCP/IP 스택은 C로 작성된 lwIP 2.2.0을 이식했다. 게스트 TinyCC와 `jaot`도 EL0에서 실행한다. 호스트에 컴파일을 요청하거나 Chủ JVM으로 대신 실행하지 않는다.

## 먼저 알아둘 giáTrịHỗTrợ giáTrịRanhGiới

| yêuCầu | 이번 phầnCàiĐặt | 남은 cắtXén |
|---|---|---|
| JAR를 thựcThiLệnh 파일처럼 thựcThiLệnh | `java -jar Tệp.jar`, `./Tệp.jar cácĐốiSố`; Main-Class와 giáTrịCất/DEFLATE ZIP, CRC CácPhépKiểmTra | 전체 Java SE, 임의의 모든 JAR 호환성 |
| 게스트 AOT | `jaot Tệp.class -o Tệp.elf`, `jaot Tệp.jar -o Tệp.elf`; dữLiệuThựcTế ARM64 기계어 sinh | giáTrịĐốiTượng·ngoạiLệ·Thread·Swing·Socket의 AOT chuyểnĐổiGiáTrị, 여러 애플리케이션 giáTrịLớp nốiKết |
| C biênDịchNguồn | 게스트 `cc`/`tcc`, TinyCC C 전처리기·ARM64 생성기·링커; tiếngViệt 식별자와 posix-kor | 전체 libc, 일반 Linux thựcThiLệnh Tệp, 게스트 C++ TrìnhBiênDịch |
| 업로드한 ELF thựcThiLệnh | ELF64/AArch64 헤더 CácPhépKiểmTra, 확장자 없는 `./Tệp`; tựThân ABI 및 명시적인 제한형 Linux ABI | 일반 Linux 바이너리 호환, 동적 링커, 공유 thưViện |
| giáTrịBênNgoài TCP/UDP | 게스트 lwIP IPv4 ngănXếpToánHạng, POSIX 소켓과 JVM의 giáTrịChữSố IPv4 địaChỉ | GENET/Wi-Fi 드라이버, DHCP·DNS·TLS, phầnCứngVậtLý BoMạch 네트워크 KiểmThử |
| FTP | 게스트 서비스, 패시브 giáTrịChuyểnGiao, UTF-8 tên, STOR/RETR/SIZE/LIST/NLST/MLSD/DELE | TLS·사용자별 giáTrịQuyền·하위 디렉터리·영속 giáTrịCất |
| vănBảnHangul Java | 기존 `tiếngViệt.tựThân` 클래스와 giáTrịBênNgoài địaChỉ UDP 오버로드 | 전체 JDK의 일대일 tiếngViệt giáTrịPhépÁnhXạ API |

JVM은 giáTrịLớp 버전 45…52의 문서화한 부분집합이다. `java`는 mãByte 실행기이고, `jaot`toánHạngĐầuTiên 별도의 네이티브 thựcThiLệnh 파일을 만든다. **JAR giáTrịKhoLưuTrữ 해제나 JVM을 함께 묶는 것을 AOT라고 표시하지 않는다.** 지원하지 않는 mãByte/API는 `jaot`toánHạngĐầuTiên 진단하고 출력을 만들지 않는다. 기존 ĐầuRa ELF도 biênDịchNguồn giáTrịSựThấtBại 때 보존한다.

Android의 Dalvik/ART는 일반 JVM giáTrịLớp/JAR가 아닌 **DEX**를 실행한다. ART의 AOT에는 GC, giáTrịLớp 로딩, JNI 등 thựcThiLệnh 기반도 필요하다. 따라서 ART처럼 기계어로 바꾸는 기능만으로 임의의 OpenJDK JAR 및 Swing이 자동 호환되지는 않는다. [Android 공식 런타임 môTả](https://source.android.com/docs/core/runtime)

## phầnMụcHiệnTại 컴퓨터에서 FTP kếtNối

Chủ thiếtBịCuối 1:

```sh
cd /home/user/jkoros/platforms/rpi4-native
make build
python3 CôngCụ/thựcThiLệnh.py --network
```

Remmina GUI에서도 같은 네트워크를 사용하려면 thựcThiLệnh 명령을
`python3 CôngCụ/thựcThiLệnh.py --desktop --network`로 바꾸고 VNC `127.0.0.1:5902`에
접속한다. FTP와 네트워크는 같은 게스트 안에서 동작한다.

부팅한 **jkoros vỏLệnh**:

```text
ftpd start
```

Chủ thiếtBịCuối 2:

제공한 예제로 작은 thựcThiLệnh JAR를 먼저 만든다. tiếngViệt 라이브러리는 게스트에 내장되어 있어 이 VíDụ JAR에 중복해서 넣지 않는다.

```sh
cd /home/user/jkoros/platforms/rpi4-native
mkdir -p build/upload
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/upload VíDụ/giáTrịBảnPhânPhối/Màu.java
jar cfe build/upload/LờiChào.jar Màu -C build/upload Màu.class
```

```sh
python3 - <<'PY'
from ftplib import FTP
ftp = FTP()
ftp.encoding = 'utf-8'
ftp.connect('127.0.0.1', 2121)
ftp.login()                         # anonymous; jkoros도 같은 TácVụ miềnĐịaChỉ
with open('build/upload/LờiChào.jar', 'rb') as f:
    ftp.storbinary('STOR LờiChào.jar', f)
print(ftp.nlst())
ftp.quit()
PY
```

giáTrịThửLại **jkoros vỏLệnh**:

```text
java -jar /LờiChào.jar
/LờiChào.jar
ftpd status
ftpd stop
```

FTP는 루트 RAM 파일만 공개한다. 익명 로그인이며 비밀번호로 권한을 구분하지 않는다. giáTrịMặcĐịnh Chủ 바인딩은 `127.0.0.1`이고, giáTrịĐiềuKhiển 포트는 2121, 데이터 포트는 50000…50007이다. `--ftp-port 2122`로 giáTrịĐiềuKhiển 포트를 바꿀 trịSố 있다. 동시에 한 FTP 세션을 제공하며 명령이 없는 세션은 60초 trạngTháiSau 닫는다. TYPE A도 바이트를 변경하지 않으므로 프로그램은 바이너리 전송한다.

파일은 **64개, 각각 16 KiB**, 경로는 UTF-8 63바이트이다. KhởiĐộng 시 준비되는 `/example`도 이 한도를 공유한다. 초과/끊어진 STOR는 기존 파일에 반영하지 않는다. FTP 업로드는 RAM에만 저장되며 재부팅하면 사라진다. 이 giáTrịGiớiHạn 때문에 일반적인 대형 JAR 배포판을 그대로 올릴 trịSố 없다.

QEMU의 raspi4b에는 GENET Ethernet 장치가 없다. 따라서 `network_bridge.py`toánHạngĐầuTiên QEMU NAT의 Ethernet과 giáTrịPhụTrợ UART의 SLIP를 변환한다. **TCP nốiKết mụcGiáTrịTiếnTrình·체크섬·재전송·FTP 명령과 Tệp 저장은 게스트 안에서 수행한다.** Chủ 브리지는 FTP 서버가 아니다. [QEMU 공식 ThiếtBị giáTrịHỗTrợ danhSáchMục](https://www.qemu.org/docs/master/system/arm/raspi.html)

이 경로는 QEMU에서 검증했다. giáTrịPhụTrợ UART의 dữLiệuThựcTế Pi 4 핀/클럭 설정과 내장 RJ45 GENET 드라이버는 phầnCàiĐặt·검증하지 않았으므로, SD 이미지에 커널이 포함되어 있다는 사실을 dữLiệuThựcTế 보드의 LAN/FTP hànhĐộng 보장으로 해석하면 안 된다.

## tiếngViệt Java를 게스트에서 컴파일하고 AOT thựcThiLệnh

게스트 `vi Màu.java`로 phầnMụcKếTiếp 소스를 작성한다.

```java
public class Màu {
    public static void main(String[] cácĐốiSố) throws Exception {
        int giáTrịTổng = 0;
        int trịSố = 1;
        while (trịSố <= 10) {
            giáTrịTổng = giáTrịTổng + trịSố;
            trịSố = trịSố + 1;
        }
        tiếngViệt.tựThân.ĐầuRa.ghiSố(giáTrịTổng);
        tiếngViệt.tựThân.Tệp.ghi("aot.txt", "vănBảnHangul AOT Tệp 😀");
        tiếngViệt.tựThân.ĐầuRa.ghiDòng(tiếngViệt.tựThân.Tệp.đọc("aot.txt"));
    }
}
```

```text
javac Màu.java
java Màu
jaot Màu.class -o Màu.elf
run Màu.elf
```

`jaot`은 클래스의 바이트코드를 C로 변환하고, **게스트 TinyCC**toánHạngĐầuTiên ARM64 명령어를 sinh·연결한다. thựcThiLệnh 때 JVM 인터프리터를 호출하지 않는다. JAR의 Main-Class가 같은 giáTrịHỗTrợ 범위이면 다음도 가능하다.

```text
jaot Màu.jar -o Màu.elf
run Màu.elf
```

AOT 지원은 한 애플리케이션 클래스의 giáTrịTĩnh giáTrịPhươngThức/giáTrịTrường, int 계열, SốNguyên 배열과 thamChiếu, cácĐốiSố giáTrịMảng, điềuKiện·nhánh·giáTrịLầnLặp, ChuỗiKýTự 리터럴, `System.out.print/println`의 int/String, tiếngViệt ĐầuRa·Tệp đọc/쓰기로 제한된다. giáTrịLớp/giáTrịPhươngThức 수와 ngănXếpToánHạng 등에도 고정 상한이 있다. Java ngoạiLệ mụcGiáTrịTiếnTrình, giáTrịĐốiTượng sinh, 가상 giáTrịPhươngThức 일반, switch/wide, long/float/double, invokedynamic, ChuỗiKýTự 결합용 StringBuilder, 일반 JDK·Socket·Thread·Swing은 이 AOT 백엔드에서 미지원이다. 내장 NUL/고립된 서로게이트 문자열도 거부한다. 잘못된 giáTrịMảng mụcTruyCập/0으로 cácGiáTrịChia 등은 네이티브 런타임 오류로 종료하며 Java ngoạiLệ 객체로 전달하지 않는다.

giáTrịVào 클래스뿐 아니라 **생성된 ELF도 16 KiB 이하**여야 한다. 기계어 확장과 ELF 페이지 giáTrịCănChỉnh 때문에 짧은 클래스도 이 한도를 넘을 trịSố 있으며, 이 경우 오류를 내고 기존 출력을 보존한다.

게스트 `javac`도 부분집합이다. 일반적인 giáTrịĐốiTượng·Thread·Swing 소스는 호스트에서 `javac --release 8`로 컴파일하고, **기존 JVM의 giáTrịHỗTrợ cắtXén 안에서** `java`/`java -jar`로 실행한다. 정확한 API는 [JVM 매뉴얼](MôiTrườngMôiTrườngChạyJava.md)과 [vănBảnHangul phátTriển 매뉴얼](HướngDẫnPhátTriển.md)을 참고한다.

JAR는 하나의 애플리케이션 giáTrịLớp 경로다. 내부 tên `GóiGộp/ChươngTrình.class`와 점으로 구분한 Main-Class를 지원한다. 내부 클래스는 파일로 풀어 VFS 슬롯을 소비하지 않는다. 내장 tiếngViệt 클래스를 추가로 찾지만 phầnMụcHiệnTại TácVụ 폴더의 다른 클래스는 자동 혼합하지 않는다. ZIP64·mậtMãHóaDữLiệu ZIP·manifest Class-Path·서명 검증은 지원하지 않는다. JAR 하나가 16 KiB 이하이어도 클래스당/적재 trịSố/VM giáTrịVùngNhớĐộng 제한은 그대로 적용된다.

## C에서 tiếngViệt POSIX gọiThựcHiện

게스트에서 `vi LờiChào.c`로 작성하거나 FTP로 소스를 업로드한다.

```c
#include <ABITệp.h>

int main(void) {
    const char lờiChào[] = "tựThân ARM64 C에서 vănBảnHangul POSIX gọiThựcHiện\n";
    int TàiLiệu = mởTệp("LờiChào.txt", GhiĐọc | ThiếuNếuTạo | CácNộiDungCắtNgắn, 0600);
    if (TàiLiệu < 0) return 1;
    kiểuKếtQuảVàoRa sốLượngĐãGhi = ghiDữLiệuTệp(TàiLiệu, lờiChào, sizeof(lờiChào) - 1);
    đóngTệp(TàiLiệu);
    ghiDữLiệuTệp(1, lờiChào, sizeof(lờiChào) - 1);
    return sốLượngĐãGhi == sizeof(lờiChào) - 1 ? 0 : 2;
}
```

```text
cc LờiChào.c -o LờiChào.elf
run LờiChào.elf
cat LờiChào.txt
```

TinyCC의 표준 C điểmMục `main`을 사용한다. 기존 Chủ C/C++ SDK의 `bắtChạyChươngTrìnhNgườiDùng(int)` 진입점과 구분한다. TệpĐầuMục Tệp·chạy giáTrịĐốiTượng·`libposix-kor-user.a`는 TrìnhBiênDịch 내부의 đọc 전용 SDK에 들어 있다. C 전처리기/구조체/Hàm/재귀/conTrỏ/부동소수점 sinh 등을 사용하되 **일반 libc/libstdc++를 제공한다는 뜻은 아니다**. 제공하지 않는 함수는 nốiKết 오류가 난다. TrìnhBiênDịch 자체의 KýTự/giáTrịChữSố chuyểnĐổiGiáTrị 지원도 완전한 libc 대체품이 아니다.

`mởTệp` 등은 별도의 모의 호출이 아닌 기존 `pk_open` 등의 tiếngViệt 매크로이며, ELF의 SVC를 통해 dữLiệuThựcTế Java Tệp 체계에 도달한다. Tệp/giáTrịỔCắmMạng gọiThựcHiện 목록은 [NgườiDùng ABI](ABIGọiNgườiDùng.md)에 있다. C/C++ Chủ SDK thựcThiLệnh 파일도 FTP로 업로드 trạngTháiSau `run` 또는 `./Tệp`로 실행하며 확장자는 giáTrịCầnĐến 없다. Linux ARM64 giáTrịTĩnh ELF에는 별도의 제한된 호환 đườngDẫn `run --linux Tệp`을 추가했다. [ELF·Linux ABI 매뉴얼](aBITệpThựcThi.md)에 정확한 giáTrịĐịnhDạng·시스템 gọiThựcHiện·địaChỉ 제한을 정리했다.

## tiếngViệt 네트워크·TácVụ·MànHình API

| giáTrịLớp | gọiThựcHiện 예 | thựcThiLệnh đườngDẫn |
|---|---|---|
| `ĐầuRa` | `ghiDòng("안녕")`, `ghiSố(42)` | JVM 및 제한형 AOT |
| `Tệp` | `ghi("TàiLiệu.txt", "giáTrịNộiDung")`, `đọc("TàiLiệu.txt")` | JVM 및 제한형 AOT |
| `TruyềnThông` | `mở(0)`, `gửi(điểmCuối, "10.0.2.2", 9000, "vănBảnHangul")`, `nhận(điểmCuối)` | JVM의 UDP |
| `vậnChuyểnKếtNối` | `nốiKết("10.0.2.2", 9000)`, `lắngNgheĐiểmCuối(9000)`, `nhận(giáTrịMáyChủ)` | JVM의 Socket/ServerSocket |
| `TácVụ` | `chạy(Runnable)`, `đợi(Thread)`, `nhườngTácVụ()` | JVM의 협력식 giáTrịLuồngChạy |
| `cửaSổ`, `ThànhTốGiaoDiện` | cửaSổ·버튼·giáTrịKýTự·TrườngVănBản·sựKiện nốiKết | JVM의 Swing 부분집합 |

명명에서는 표준 영어 API를 보존하고 tiếngViệt gọiThựcHiện 계층을 추가한다. `TruyềnThông(通信)`, `nốiKết(連結)`, `ĐầuRa(出力)`은 기존 단어의 뜻을 사용한다. `TácVụ giáTrịLuồngChạy`은 한 thựcThiLệnh 흐름을 가닥에 빗댄 giáTrịBộMôTả 표현, `giáTrịCổng`는 포트의 접점을 설명하는 표현이다. 새 giáTrịBộMôTả 결합어를 고대에 이미 존재한 용어처럼 설명하지 않는다. 전체 JDK의 번역을 완료했다고 표시하지 않는다.

giáTrịBênNgoài 주소는 giáTrịChữSố IPv4이며 QEMU 호스트는 `10.0.2.2`, 게스트는 `10.0.2.15`toánHạngThứBa. UDP 전문은 512바이트까지다. 소켓은 비차단 tựThân ABI이며 JVM이 제한된 chờGiáTrị/재시도를 제공한다. TCP connect 대기는 giáTrịTốiĐa 1초, NgườiDùng ChươngTrình 전체에는 기존 약 2초 CPU 기한이 적용된다. 일반적인 장기 thựcThiLệnh NgườiDùng 서버와 pthread는 아직 없다. FTP는 NgườiDùng ChươngTrình 기한과 별개인 giáTrịNhân 서비스다.

게스트의 NgườiDùng TCP/UDP 서버로 들어오는 연결은 NAT 포트를 추가한다. 예를 들어 `python3 CôngCụ/thựcThiLệnh.py --network --forward tcp:9300:9300 --forward udp:9301:9301`로 실행하면 호스트의 localhost 9300/TCP·9301/UDP를 게스트의 같은 포트로 전달한다. FTP의 giáTrịMặcĐịnh giáTrịĐiềuKhiển/데이터 포트와 겹치면 thựcThiLệnh 전에 거부한다.

## 시험과 xâyDựngHệThống 재현

```sh
cd /home/user/jkoros/platforms/rpi4-native
make test-ftp
make test
make image
```

`build/verification/ftp/report.json`은 dữLiệuThựcTế FTP giáTrịChuyểnGiao, vănBảnHangul Tệp, cỡ 초과 보존, giáTrịKhoLưuTrữ JAR thựcThiLệnh, 게스트 C biênDịchNguồn/ELF 재업로드, giáTrịBênNgoài Java TCP/UDP, 게스트 javac/AOT 실행을 기록한다. `serial.log`에서 게스트 명령과 결과를 확인할 trịSố 있다. 보고서의 giáTrịNhân SHA-256과 giáTrịBảnPhânPhối 이미지의 커널을 비교한다.

빌드는 기존 JDK/Clang/AArch64 binutils와 함께 `../rpi4/build/rootfs`의 ARM64 SDK KhaiBáo 헤더와 libgcc giáTrịSốHọc giáTrịPhụTrợ 함수를 사용한다(`make rpi-prepare`). **musl libc, Linux giáTrịNhân, 동적 로더를 게스트에 링크하지 않는다.** TinyCC/lwIP/uzlib 원본과 라이선스·버전 정보는 `vendor/`, ChuyểnNền 코드는 `ccompiler/`, `network/`, `NgườiDùng/GóiGộp.c`에 있다.

전체 JDK/AOT JVM으로 확장하려면 타입 thẩmĐịnh·giáTrịĐốiTượng/ngoạiLệ/GC·동적 로딩·JNI, 영속 Tệp giáTrịHệThốngĐiềuHành·mmap/TLS/시그널·스레드 ABI, OpenJDK native thưViện, GUI peer/폰트/입력기, GENET 및 phầnCứngVậtLý ThiếtBị 검증이 더 필요하다. 이 문서의 thựcThiLệnh 시험은 그 전체 이식을 대신하지 않는다.
