# tựThân ARM64 JVM 0.4와 tiếngViệt thưViện

tiếngViệt TruyềnThông·ngoạiLệ 사용법은 [tiếngViệt Java API](JavaTiếngViệt/HướngDẫn.md), Hàm·giáTrịBiến·Tệp 이름의 변경과 어원 근거는 [cáchĐặtTên HướngDẫn](cáchĐặtTên/HướngDẫn.md)를 참고한다.

JAR thựcThiLệnh, giáTrịBênNgoài IPv4 TCP/UDP, 별도 giáTrịTĩnh 부분집합 `jaot`와 게스트 C 컴파일은 [FTP·C·JAR·AOT 매뉴얼](ViệcBiênDịchVàChuyểnGiaoTệp.md)에 설명한다. giáTrịĐáy giáTrịĐốiTượng·Thread·Swing은 JVM 경로의 기능이며 AOT giáTrịHỗTrợ 범위와 같지 않다.

이 구현은 **Linux 없이 부팅한 Java AOT 커널의 EL0에서 thựcThiLệnh**한다. JDK/JRE의 거의 모든 기능을 제공하는 단계는 아직 아니다. HotSpot·OpenJDK giáTrịLớp thưViện 전체를 이식하거나 Java SE 인증/TCK를 통과한 구현도 아니다. 이번 확장은 단일 giáTrịLớp·giáTrịTĩnh giáTrịPhươngThức 중심이던 실행기를 giáTrịĐốiTượng·thưViện thựcThiLệnh 기반으로 넓힌 것이다.

## 실행과 biênDịchNguồn

```sh
cd /home/user/jkoros/platforms/rpi4-native
make build
# tựThân giáTrịNhân 안에서 câyNguồn biênDịchNguồn → class thựcThiLệnh, tiếngViệt API gọiThựcHiện
python3 CôngCụ/thựcThiTệp.py KiểmThử/Java/nguồnHangul.java

# giáTrịĐốiTượng·ngoạiLệ 등은 Chủ JDK로 Java 8 class를 만든 trạngTháiSau tựThân 커널에서 thựcThiLệnh
mkdir -p build/my-java
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/my-java KiểmThử/Java/thửHangul.java
python3 CôngCụ/thựcThiTệp.py build/my-java/thửHangul.class

# 의존 class 파일은 --include로 함께 giáTrịChuyểnGiao
javac --release 8 -encoding UTF-8 -d build/my-java KiểmThử/Java/thửCácĐốiTượng.java
python3 CôngCụ/thựcThiTệp.py build/my-java/thửCácĐốiTượng.class \
  --include build/my-java/giáTrịNền.class --include build/my-java/giáTrịNhánh.class \
  --include build/my-java/cóThểTính.class

make test-jvm
```

`--include DIR`는 그 디렉터리의 class 파일을 재귀적으로 읽어 `패키지.giáTrịLớp.class`라는 RAM Tệp 이름으로 전송한다. 주 클래스도 패키지가 있다면 `--class-name 패키지.giáTrịLớp`를 지정한다. 셸에서는 해당 이름으로 업로드하고 `java 패키지.giáTrịLớp`로 실행한다. JVM 0.4는 Main-Class가 있는 16 KiB 이하 JAR도 `java -jar Tệp.jar`로 실행한다. JAR 모드에서는 JAR 내부 클래스와 내장 tiếngViệt 클래스만 찾는다. giáTrịBảnPhânPhối tiếngViệt thưViện JAR는 Chủ javac의 classpath로 사용하며, 같은 클래스가 NgườiDùng JVM ELF에도 đọc 전용 자료로 포함된다. 일반 class 모드에서는 사용자가 같은 이름으로 올린 RAM class를 먼저 읽는다.

게스트 `javac`는 여전히 giáTrịTĩnh giáTrịPhươngThức, int/boolean/char/String, điềuKiện·giáTrịLầnLặp, ChuỗiKýTự cácGiáTrịKếtHợp, 일부 Tệp 스트림 등의 **tựThân 부분집합 TrìnhBiênDịch**toánHạngThứBa. giáTrịĐốiTượng KhaiBáo·상속·try/catch·Thread giáTrịDùng 소스를 게스트 javac가 xâyDựngTấtCả 컴파일하는 것은 아니다. giáTrịĐỉnh 기능은 `javac --release 8`로 만든 class를 tựThân JVM에서 실행한다. tiếngViệt API 중 ĐầuRa·KýTự 스칼라 Hàm·Tệp đọc/쓰기는 게스트 컴파일러에도 연결했다. 다음처럼 전체 이름으로 호출한다.

```java
public class LờiChào {
    public static void main(String[] cácĐốiSố) throws Exception {
        tiếngViệt.tựThân.ĐầuRa.ghiDòng("안녕하세요😀");
        tiếngViệt.tựThân.ĐầuRa.ghiSố(tiếngViệt.tựThân.KýTự.sốLượngĐiểmMã("vănBảnHangul😀"));
        tiếngViệt.tựThân.Tệp.ghi("LờiChào.txt", "vănBảnHangul Tệp😀");
        tiếngViệt.tựThân.ĐầuRa.ghiDòng(tiếngViệt.tựThân.Tệp.đọc("LờiChào.txt"));
    }
}
```

## tựThân JVM에서 구현한 cắtXén

| giáTrịMiền | 제공 cắtXén |
|---|---|
| giáTrịLớp | class 버전 45…52, 여러 giáTrịLớp 로딩, 인스턴스/giáTrịTĩnh giáTrịTrường, 생성자, 상속, 가상 gọiThựcHiện, 인터페이스 gọiThựcHiện, giáTrịTĩnh khởiTạo |
| giáTrị·lệnh | 32비트 int 계열, boolean/byte/char/short, thamChiếu, 1차원 giáTrịMảng, nhánh·switch·wide, instanceof/checkcast, category-1 ngănXếpToánHạng lệnh |
| ngoạiLệ | 지원하는 표준 ngoạiLệ sinh·throw·catch·finally, giáTrịPhươngThức 경계를 넘는 giáTrịTiến, getMessage; giáTrịĐáy giáTrịGiớiHạn thamChiếu |
| dữLiệuBộNhớ | 비이동 mark/sweep GC, 빈 giáTrịMiền 병합, ngănXếpToánHạng·giáTrịTĩnh giáTrịTrường·컬렉션·giáTrịLuồngChạy·모니터·ChuỗiKýTự 상수의 thamChiếu giữLạiGiáTrị |
| ChuỗiKýTự | UTF-16, length/charAt/equals/isEmpty/substring/concat/hashCode/toString, String.valueOf(int), StringBuilder의 giáTrịMặcĐịnh sinh·append(int/boolean/char/String)·toString |
| trịSố | Integer.parseInt/valueOf/intValue/toString, 작은 Integer 캐시, Math.abs/min/max(int) |
| 표준 ĐầuRa | System.out/err, PrintStream.print/println의 int/boolean/char/String 및 빈 println |
| giáTrịMảng | int/byte/boolean/char/short/thamChiếu giáTrịMảng, độDài·cắtXén CácPhépKiểmTra, thamChiếu giáTrịMảng phầnTửPhầnMục giáTrịKiểu CácPhépKiểmTra, System.arraycopy의 cácChồngLấn/cắtXén/phầnTửPhầnMục giáTrịKiểu CácPhépKiểmTra |
| Tệp | FileInputStream(String), FileOutputStream(String[,boolean]); read()/read(byte[][,offset,len]), write(int)/write(byte[][,offset,len]), close, ĐầuRa flush. EOF는 -1 |
| 컬렉션 | ArrayList/List: add(E), get, set, remove(int), size, isEmpty, clear. HashMap/Map: put/get/remove/containsKey/size/isEmpty/clear |
| giáTrịLuồngChạy | Thread(), Thread(Runnable), Thread 상속, start/join/isAlive/currentThread/yield; synchronized giáTrịPhươngThức·블록의 재진입·경합·ngoạiLệ 시 giảiPhóngLưuTrữ |
| UDP | DatagramSocket의 giáTrịMặcĐịnh/cổngPhầnCứng 생성자, send/receive/close/getLocalPort/setSoTimeout; DatagramPacket의 byte[]/độDài sinh 및 địaChỉ·cổngPhầnCứng TệpĐầuMục sinh, getData/getLength/getAddress/getPort/setLength |
| địaChỉ | InetAddress.getByName은 localhost/giáTrịChữSố IPv4 (DNS làKhôngHỗTrợ), getLoopbackAddress/getHostAddress |
| HìnhVẽ | tiếngViệt MànHình API가 EL0 SVC를 통해 프레임버퍼에 사각형을 HìnhVẽ; cắtXén CácPhépKiểmTra |

컬렉션은 지정한 메서드만 제공하며 iterator/stream/giáTrịCănChỉnh·NgườiDùng giáTrịĐịnhNghĩa equals/hashCode 콜백은 없다. 사전의 열쇠는 String/Integer/null 사용을 시험했다. UTF-16 giáTrịMã 단위와 Unicode giáTrịMã 포인트 수는 구분한다. vănBảnHangul giáTrịVào PhốiHợp·chuẩnHóaGiáTrị·아랍어 조판·GUI 다국어 글꼴은 이 ChuỗiKýTự 지원과 별개다.

예외는 Throwable/Exception/RuntimeException, ArithmeticException, NullPointerException, IndexOutOfBoundsException/ArrayIndexOutOfBoundsException/StringIndexOutOfBoundsException, IllegalArgumentException/NumberFormatException/IllegalThreadStateException, IOException/FileNotFoundException, IllegalStateException, ClassCastException, NegativeArraySizeException, ArrayStoreException, UnknownHostException, SocketTimeoutException의 제한된 sinh·giáTrịLoạiMục·처리를 제공한다. NgườiDùng giáTrịĐịnhNghĩa Throwable 상속, stack trace/cause/suppressed ngoạiLệ, try-with-resources의 addSuppressed, 완전한 khởiTạo lỗi 포장은 아직 없다. 잡히지 않은 예외는 phầnMụcHiệnTại 전체 Java 실행을 실패로 끝낸다.

## tiếngViệt API

독립 패키지 **`tiếngViệt.tựThân`**를 사용한다. Linux판 `tiếngViệt.Java`toánHạngĐầuTiên 요구하는 NIO/Swing/HTTP API를 tựThân 커널에서 실행할 trịSố 있다고 혼동하지 않도록 패키지를 나눴다. 이 라이브러리는 giáTrịLớp tên·giáTrịPhươngThức·cácĐốiSố·giáTrịTrường·Tệp 이름에 한국어를 사용한다. 표준 Java giáTrịLớp 이름은 호환성을 위해 보존한다.

| giáTrịLớp | 공개 기능 | 이름의 의미 |
|---|---|---|
| ĐầuRa | ghi, ghiDòng, ghiSố | ĐầuRa(出力): 내용을 바깥으로 giáTrịĐãXuất |
| KýTự | độDài, vănBảnBằng, vănBảnDán, giáTrịCắt, phânTíchCúPhápSốNguyên/ghiGiáTrịSốNguyên, sốLượngĐiểmMã, mãHóa/giảiMậtMãDữLiệu | KýTự(文字), giáTrịBảngMã(符號): 글의 단위와 그 값을 바이트로 나타내는 giáTrịQuyTắc |
| Tệp | đọc/ghi(String tên), đọcGiáTrịByte/ghiGiáTrịByte | 널리 쓰는 NgườiDùng 용어를 보존; RAM 자료의 tên |
| danhSáchMục | thêmCácGiáTrị, đọc, thayGiáTrị, xóaMục, cỡ, làGiáTrịRỗng, xóaSạchCácNộiDung | danhSáchMục(目錄): 순서가 있는 giáTrịMục 모음 |
| TừĐiển | đặtGiáTrị, tìmMục, thựcHiệnĐượcTồnTại, xóaMục, cỡ, xóaSạchCácNộiDung | TừĐiển(辭典): 찾는 말인 열쇠에 값을 giáTrịPhépÁnhXạ |
| TácVụ | chạy(TácVụChạyĐược), đợi(bộLàmViệc), nhườngTácVụ, làCònSống | TácVụ giáTrịLuồngChạy: 한 ChươngTrình 안의 thựcThiLệnh giáTrịLuồng |
| TruyềnThông | mở, gửi, nhận, hếtGiờ, đóng | TruyềnThông(通信), điệnDữLiệu(電文), giáTrịCổng: DữLiệu 교환·메시지·포트의 역할 |
| MànHình | hìnhChữNhật, xóaMục | MànHình(畫面): dữLiệuThựcTế 그림을 표시하는 면 |
| giáTrịNhân | miliGiây, hìnhChữNhật | tựThân JVM의 고정 native nốiKết; 일반 JNI는 아님 |

이 명명은 phầnMụcHiệnTại 기능을 설명하는 용어 선택이다. 기존 한국어에 없던 역사적 어원을 만들어 주장하지 않는다. vănBảnTênTệp·식별자는 UTF-8 소스로 보관한다. `KýTự.giảiMậtMãDữLiệu`는 잘못된 UTF-8에 IllegalArgumentException을 던지며, `mãHóa`는 짝이 없는 서로게이트를 `?`로 바꾼다. `Tệp.đọc`는 엄격한 UTF-8 복호화를 적용한다. MànHình 색은 `빨강 | (초록 << 8) | (파랑 << 16)` 형식이다.

## thựcThiLệnh 제한과 남은 TácVụ

- 동시에 적재하는 class giáTrịTốiĐa 16개(tiếngViệt giáTrịLớp TệpĐầuMục), class당 16 KiB·giáTrịHằng 풀 511항목, 전체 giáTrịPhươngThức/giáTrịTrường 각각 512개. giáTrịPhươngThức giáTrịMã 8 KiB, phạmViCụcBộ giáTrịBiến·피연산자 ngănXếpToánHạng 각각 128슬롯, cácĐốiSố giáTrịTốiĐa 16개(this TệpĐầuMục).
- VM 가닥은 main TệpĐầuMục **실행당 giáTrịTốiĐa 4개**, 가닥당 gọiThựcHiện giáTrịĐộSâu 32. 100개 명령마다 thựcThiLệnh 대상을 바꾼다. 네이티브 gọiThựcHiện 도중에는 전환하지 않는다. pthread/SMP/OS 스레드가 아니며 Thread.sleep/interrupt/daemon/우선순위, Object.wait/notify, java.util.concurrent는 없다.
- giáTrịĐốiTượng 힙은 32768개의 32비트 슬롯이다. 런타임의 AOT 배열은 dữLiệuThựcTế 메모리에서 64비트 슬롯을 사용한다. GC가 있어도 대형 Tệp·대형 ChuỗiKýTự·객체가 이 제한을 넘을 trịSố 있다.
- 실행은 50만 mãByte lệnh 및 커널의 약 2초 EL0 기한으로 제한된다. Swing의 giáTrịVào 대기는 기한을 갱신하고 cửaSổ chếĐộChuyển 시 중단·재개한다. 일반 giáTrịMáyChủ·계산의 무제한 실행은 아직 없다. làKhôngHỗTrợ lệnh·giáTrịTàiNguyên 부족은 명시적인 오류로 종료한다.
- RAM Tệp giáTrịTốiĐa 64개, 파일당 16384바이트, đườngDẫn UTF-8 63바이트. RAM 디렉터리와 giáTrịĐốiTác/절대 경로를 제공하며 영속 저장은 아직 없다. 내장 tiếngViệt class는 RAM Tệp 슬롯을 소비하지 않는다. 셸의 `cd`로 정한 phầnMụcHiệnTại 경로에서 câyNguồn·giáTrịLớp·DữLiệu 파일을 읽는다.
- UDP는 Java 루프백 및 lwIP/SLIP를 통한 giáTrịBênNgoài IPv4를 제공한다. dữLiệuThựcTế GENET/Wi-Fi/DNS/TLS/HTTP 전체는 없다. điệnDữLiệu 512바이트, giáTrịỔCắmMạng 8개, 소켓당 큐 4개. receive는 VM 가닥을 양보하며 대기하고 setSoTimeout을 적용하지만 전체 thựcThiLệnh 기한은 여전히 적용된다.
- long/float/double, invokedynamic/람다, enum/annotation, 다차원 giáTrịMảng, 완전한 giáTrịMảng 공변성·인터페이스 giáTrịTầng CácPhépKiểmTra, Reflection/JNI/JIT, NIO/ZIP API/Charset 전체, 보안/mậtMãHóaDữLiệu/국제화 전체, 전체 AWT/Swing/JavaFX는 미지원이다. Swing의 별도 giáTrịHỗTrợ 부분집합은 giáTrịĐáy 및 phátTriển 매뉴얼을 참고한다. giáTrịLớp Tệp 전체 검증기·mụcTruyCập giáTrịQuyền/보호된 멤버 검사는 아직 완전하지 않다. 손상된 입력은 EL0 bảoVệGiáTrị giáTrịRanhGiới 내에서 종료되도록 한다.

전체 OpenJDK를 목표로 하려면 다음은 별도의 주요 phầnCàiĐặt 단계다: 완전한 JVM giáTrị/thẩmĐịnh/giáTrịLớp 로더와 ngoạiLệ 모델 → 영속 VFS·mmap·ĐồngHồ·원자 giáTrịThaoTác·dữLiệuThựcTế 스레드/đồngBộHóa ABI → OpenJDK java.base 및 native thưViện ChuyểnNền → ThiếtBị 네트워크·TCP/IP → cửaSổ 시스템/giáTrịPhôngChữ/입력기·java.desktop → Java SE 호환성 KiểmThử. phầnMụcHiệnTại tựThân JVM의 일부 메서드를 더하는 것으로 이 작업이 완료되지는 않는다.

## thẩmĐịnh

`CôngCụ/thửJVM.py`는 같은 Java 8 class 파일의 출력을 Chủ OpenJDK `-Xverify:all`과 QEMU raspi4b tựThân 커널에서 비교한다. giáTrịĐốiTượng/상속/인터페이스·switch·giáTrịMảng, ngoạiLệ/finally, 컬렉션/GC, Thread/giáTrịKhóa, tiếngViệt UTF-8/Tệp/컬렉션, dữLiệuThựcTế UDP 루프백/giáTrịThờiGian 초과, 게스트 vănBảnHangul câyNguồn biênDịchNguồn, giáTrịMảng giáTrịKiểu/saoChépGiáTrị/Tệp giáTrịRanhGiới·vănBảnHangul 패키지의 9개 비교 시험과 잘못된 class 버전/giáTrịĐãCắtXén Tệp từChốiGiáTrị 시험을 실행한다. UDP gốcCâyDựÁn 실행에는 Chủ 루프백 giáTrịỔCắmMạng 권한이 필요하다.

`CôngCụ/ThửKhởiĐộng.py`는 giáTrịNhân bảoVệGiáTrị/회귀 시험과 별도로 tiếngViệt Java MànHình API가 dữLiệuThựcTế 픽셀을 그렸는지도 QMP MànHình 캡처로 검사한다. 보고서는 `build/verification/jvm/report.json`, `build/verification/report.json`이며 시험한 kernel8.img의 SHA-256을 기록한다. dữLiệuThựcTế Pi4 giáTrịPhầnCứng KhởiĐộng 시험과 전체 JDK 호환성 KiểmThử 결과는 아니다.


## JVM 0.3: 네트워크와 GUI giáTrịPhầnMởRộng

`Socket`/`ServerSocket` sinh·nốiKết·accept·양방향 InputStream/OutputStream·close·EOF·giáTrịThờiGian 제한과 UTF-8 `String.getBytes`를 추가했다. JVM 0.4에서는 giáTrịBênNgoài giáTrịChữSố IPv4 TCP도 lwIP/SLIP에 연결했다. 연결형 điểmKếtThúc 16개, Java 루프백 버퍼 1024바이트, giáTrịBênNgoài TCP 버퍼 4096바이트다. DNS·TLS는 없다.

`JFrame`, `JPanel`, `JLabel`, `JButton`, `JTextField`, `ActionListener`, `ActionEvent`, `SwingUtilities.invokeLater`의 문서화한 부분집합을 네이티브 GUI에 연결했다. `setLayout(null)`과 명시적 좌표를 사용한다. 전체 OpenJDK Swing 또는 Java SE 호환 구현은 아니다. tươngTác 이벤트 대기는 thựcThiLệnh 기한을 갱신하고 thiếtBịCuối chếĐộChuyển 시 프로세스 상태를 giáTrịCất·복원한다. 이벤트 콜백 자체는 기존 mãByte/CPU 기한을 따른다.

tiếngViệt `cửaSổ`, `ThànhTốGiaoDiện`, `vậnChuyểnKếtNối` 클래스를 giáTrịBảnPhânPhối JAR와 tựThân JVM 내장 자원에 추가했다. 상세 giáTrịPhươngThức·giáTrịGiớiHạn·câyNguồn·업로드 방법: [vănBảnHangul phátTriển 매뉴얼](HướngDẫnPhátTriển.md).

## tiếngViệt 객체의 직접 thựcThiLệnh

`cửaSổ`, `nhãn`, `TrườngVănBản`, `nút`, `HàngĐợiSựKiện`, `ThôngBáoHànhĐộng`, `bộLàmViệc`은
표준 GUI/Thread 객체를 보관하는 래퍼가 아니다. tựThân JVM의 giáTrịĐốiTượng sinh,
giáTrịĐịnhDạng CácPhépKiểmTra, MànHình gọiThựcHiện, sựKiện 큐, giáTrịLuồngChạy 스케줄러에 tiếngViệt 계약을 직접 구현했다.
표준 `javax.swing`·`Thread` 코드의 thựcThiLệnh 경로도 유지한다.
tiếngViệt 단추와 표준 JButton은 서로 다른 형식이며, 해당 instanceof 검사도 검증한다.

tựThân 실행기의 tiếngViệt 진입점은 `public static void chạy()`이다.
표준 `main(String[])`도 지원하며 giáTrịHai toánHạngThứBa 있으면 tiếngViệt 진입점을 우선한다.
명령행 인수는 `CácĐốiSố.sốLượngPhầnMục()`와 `CácĐốiSố.vănBản(chỉSốThứBậc)`으로 읽는다.
`example/java`의 다섯 예제는 이 규약을 사용한다. giáTrịTĩnh Tệp 예제는 게스트
javac로도 컴파일하며, GUI/giáTrịLuồngChạy 소스는 Chủ `javac --release 8`을 사용한다.
직접 GUI/giáTrịLuồngChạy API는 tựThân JVM 전용이다. 기존 OpenJDK 비교 시험과 별도로
tiếngViệt 가닥의 thựcThiLệnh·chờGiáTrị·중복 chạy từChốiGiáTrị, GUI sựKiện giáTrịGốc·sốHiệu·콜백을 검사한다.
전체 JDK 번역이나 모든 API의 jaot 지원을 뜻하지 않는다.

giáTrịPhươngThức 이름은 바이트코드에서도 유지된다. 이름과 참조를 같이 수정하면
tiếngViệt 클래스도 실행되지만, ChuỗiKýTự 리터럴·표준 thưViện 재정의·native
nốiKết·진입점은 각각 컴파일러와 실행기의 계약을 맞춰야 한다.
[상세 계약과 VíDụ](JavaTiếngViệt/HướngDẫn.md)를 참고한다.

## thiếtBịCuối giáTrịPhầnCon làmMới

giáTrịDiChuyển·cỡ 변경은 새 cửaSổ 영역과 phầnMụcTrướcĐó 자리에서 드러난 띠만 합성한다.
1920×32 điểmẢnh(240 KiB)의 giáTrịTạm 그림에서 배경·겹친 cửaSổ·giáTrịKýTự·GUI를 먼저
완성하고, phầnMụcHiệnTại hiệnGiáTrị 메모리와 비교하여 달라진 화소만 기록한다.
32줄보다 큰 영역은 여러 띠로 처리하므로 전체 프레임을 원자적으로
교체하거나 수직 동기에 맞추는 방식은 아니다. 전체 배경을 먼저 지우는
중간 화면은 표시하지 않는다. 좌표가 같으면 giáTrịThửLại 그리지 않는다.

`make test-redraw`는 dữLiệuThựcTế C mànHìnhTô 코드를 호스트의 dữLiệuBộNhớ 화면에 연결해
giáTrịDiChuyển 80회·cỡ đổiGiáTrị 40회·겹친 cửaSổ 4개를 전체 합성 결과와 điểmẢnh 단위로 대조한다.
giáTrịMiền 밖 NgườiDùng HìnhVẽ, 동일 điểmẢnh 무기록, conTrỏ 밑그림, dữLiệuThựcTế MànHình dòng 간격을
검사한다. 이 시험의 시간은 Chủ CPU 측정이며 Pi 4/QEMU 속도로 해석하지 않는다.
`make test-resize`는 QEMU/VNC의 640×480 및 1920×1080에서 bênTrái giáTrịGóc giáTrịKéo,
vănBảnHangul giáTrịVào·vi 미저장 giáTrịNộiDung·독립 cửaSổ 크기를 검사한다.
