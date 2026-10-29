# tiếngViệt Java TruyềnThông·đầuRaĐầuVào·ngoạiLệ API

패키지는 `tiếngViệt.tựThân`toánHạngThứBa. Chủ `javac --release 8`로 컴파일한 class를
tựThân ARM64 커널의 JVM에서 실행한다. TruyềnThông·Tệp·ngoạiLệ API는 OpenJDK와 대조한다. 아래의 직접 구현한 MànHình·TácVụ giáTrịLuồngChạy API는 tựThân JVM 전용이다.
기존 표준 Java thưViện 전체의 tiếngViệt 번역판은 아니다.

```java
import tiếngViệt.tựThân.*;

public class mạng {
    public static void main(String[] cácĐốiSố) throws NgoạiLệĐầuRaĐầuVào {
        KếtNối nốiKết = KếtNối.mở("10.0.2.2", 9000);
        try {
            nốiKết.hếtGiờ(700);
            nốiKết.ĐầuRa().ghi(KýTự.mãHóa("안녕하세요\n"));
            LuồngĐầuVào giáTrịVào = nốiKết.giáTrịVào();
            ĐầuRa.ghiSố(giáTrịVào.đọc());
        } catch (NgoạiLệHếtGiờChờ lỗi) {
            ĐầuRa.ghiDòng(lỗi.môTả());
        } finally {
            nốiKết.đóng();
        }
    }
}
```

`Socket`, `getOutputStream`, `write`, `getInputStream`, `read`, `close`를
NgườiDùng 예제에서 직접 호출할 필요가 없다. `try/catch/throws` 등 Java 문법은 유지한다. `String`은 예약어가 아니라 javac가 ChuỗiKýTự 리터럴에 사용하는 표준 클래스다. tựThân 실행기는 `public static void chạy()`도 진입점으로 받는다.

## 통신과 giáTrịLuồng

| giáTrịLớp | tiếngViệt gọiThựcHiện |
|---|---|
| KếtNối | `mở(địaChỉ, sốCổng)`, `giáTrịVào()`, `ĐầuRa()`, `hếtGiờ(miliGiây)`, `sốCổng()`, `sốCổngCụcBộ()`, `đãKếtNối()`, `làĐãĐóng()`, `đóng()` |
| nhậnCổng | `mở(sốCổng)`, `nhận()`, `sốCổng()`, `hếtGiờ(miliGiây)`, `làĐãĐóng()`, `đóng()` |
| LuồngĐầuVào | `đọc()`, `đọc(byte[])`, `đọc(byte[], chạy, độDài)`, `đóng()` |
| LuồngĐầuRa | `ghi(int)`, `ghi(byte[])`, `ghi(byte[], chạy, độDài)`, `phátGiáTrị()`, `đóng()` |
| KênhĐiệnDữLiệu | `mở(sốCổng)`, `gửi(địaChỉ, sốCổng, vănBản)`, `nhận()`, `hếtGiờ(miliGiây)`, `sốCổng()`, `làĐãĐóng()`, `đóng()` |
| vậnChuyểnKếtNối | `mở(...)`, `mởBộNhận(...)`는 giáTrịĐỉnh tiếngViệt 객체를 kếtQuảTrảVề |
| CácPhépKiểmTra | `đòiHỏi(điềuKiện, giáTrịNguyênNhân)` |

TCP 입력은 한 번에 요청한 모든 바이트가 도착한다고 가정하지 않는다.
`đọc()`의 Tệp 끝은 -1, giáTrịMảng 읽기의 반환값은 dữLiệuThựcTế 읽은 길이다.
네트워크 흐름을 닫으면 연결도 닫힌다. sốCổng 0은 빈 번호를 자동 배정한다.
UDP 전문은 phầnMụcHiệnTại tựThân 커널에서 512바이트까지 받으며, 주소는 giáTrịChữSố IPv4를 사용한다.
`localhost` 루프백 외의 tên 풀이(DNS)는 tựThân 커널에 아직 없다.

기존 `vậnChuyểnKếtNối.nốiKết/lắngNgheĐiểmCuối/nhận`, `TruyềnThông.mở/gửi/nhận`는 표준 Java 객체를
사용하던 코드와의 연결용이다. 새 코드는 `KếtNối`, `nhậnCổng`, `KênhĐiệnDữLiệu`를 쓴다.

## tiếngViệt ngoạiLệ

모든 giáTrịĐáy 클래스는 giáTrịMặcĐịnh 생성자, `새예외("môTả")` 형태의 ChuỗiKýTự 생성자와
`môTả()`을 제공한다. dữLiệuThựcTế sinh 문법은 `new NgoạiLệHếtGiờChờ("chờTrạngThái phầnKết")`이다.

| tiếngViệt ngoạiLệ | 상위 giáTrịLớp / 용도 |
|---|---|
| ngoạiLệ | `java.lang.Exception`, 직접 던지는 일반 CácPhépKiểmTra ngoạiLệ |
| NgoạiLệViệcThựcThi | `java.lang.RuntimeException` |
| NgoạiLệĐầuRaĐầuVào | `java.io.IOException`, tiếngViệt Tệp·TruyềnThông API의 CácPhépKiểmTra ngoạiLệ |
| NgoạiLệHếtGiờChờ | `NgoạiLệĐầuRaĐầuVào`, TruyềnThông hếtGiờ 초과 |
| NgoạiLệTraCứuĐịaChỉ | `NgoạiLệĐầuRaĐầuVào`, địaChỉ xácMinh giáTrịSựThấtBại |
| NgoạiLệTệpThiếu | `NgoạiLệĐầuRaĐầuVào`, Tệp mở giáTrịSựThấtBại |
| NgoạiLệTruyềnThông | `NgoạiLệĐầuRaĐầuVào`, 표준 SocketException chuyểnĐổiGiáTrị |
| NgoạiLệĐốiSốKhôngHợpLệ | `java.lang.IllegalArgumentException` |
| SựThấtBạiĐịnhDạngSố | `NgoạiLệĐốiSốKhôngHợpLệ` |
| NgoạiLệCácCận | `java.lang.IndexOutOfBoundsException` |
| NgoạiLệCácCậnMảng / NgoạiLệCácCậnChuỗi | `NgoạiLệCácCận` |
| NgoạiLệThamChiếuRỗngThamChiếu | `java.lang.NullPointerException` |
| SựThấtBạiSốHọc | `java.lang.ArithmeticException` |
| NgoạiLệTrạngThái | `java.lang.IllegalStateException` |
| NgoạiLệÉpKiểuKiểu | `java.lang.ClassCastException` |
| SựThấtBạiCỡMảngÂm | `java.lang.NegativeArraySizeException` |
| SựThấtBạiCấtMảng | `java.lang.ArrayStoreException` |
| NgoạiLệTrạngTháiLuồngChạy | `java.lang.IllegalThreadStateException` |
| NgoạiLệĐãBịNgắtChờ | `java.lang.InterruptedException`, `TácVụ.đợi`의 chờGiáTrị 중단 |

`ngoạiLệ`와 `NgoạiLệViệcThựcThi`는 모든 tiếngViệt 예외의 giáTrịChung 부모가 아니다. giáTrịĐỉnh 상속 관계를
사용하며, Tệp·TruyềnThông 전체를 잡으려면 `catch (NgoạiLệĐầuRaĐầuVào lỗi)`를 쓴다.
tiếngViệt API가 표준 đầuRaĐầuVào 오류를 tiếngViệt 예외로 변환한다.
기존 tiếngViệt TruyềnThông 호출에서 `SocketTimeoutException`을 잡던 코드는
`NgoạiLệHếtGiờChờ`를 잡도록 옮긴다. 표준 `java.net`을 직접 사용하는 코드의
ngoạiLệ 유형은 기존 Java 규약을 따른다.
일반 Java 연산이 자동으로 던지는 표준 예외까지 이름을 바꾸지는 않는다.
예를 들어 `1 / 0`의 ArithmeticException과 직접 만든 산술예외는 서로 다른 형식이다.
phầnMụcHiệnTại tựThân JVM에 이 20종을 추가했다. 임의의 NgườiDùng Throwable 하위 giáTrịLớp 전체를
지원하도록 확장했다는 뜻은 아니다.

## biênDịchNguồn·thựcThiLệnh

```sh
cd /home/user/jkoros/platforms/rpi4-native
make xâyDựngHệThống
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/한국어사용 KiểmThử/Java/thửKếtNốiMạngTiếngHàn.java
python3 CôngCụ/thựcThiTệp.py build/한국어사용/thửKếtNốiMạngTiếngHàn.class
make test-jvm
```

내장 라이브러리는 NgườiDùng JVM ELF 안에 탑재된다. `.jar`는 Chủ javac의
giáTrịLớp 경로로 사용한다. câyNguồn 묶음은 `dist/jkoros-native-korean-sources.zip`이다.
게스트의 제한형 `javac`는 tiếngViệt 예외의 `throws` 선언과 그 import를 인식한다.
tựThân JVM의 Thread.interrupt 동작을 새로 구현한 것은 아니다.
try/catch·giáTrịĐốiTượng·giáTrịỔCắmMạng VíDụ 전체의 câyNguồn 컴파일은 Chủ javac를 사용한다.
`/example/java/VíDụTệp.java`는 게스트 javac로도 컴파일할 trịSố 있다.

dữLiệuThựcTế TCP/UDP 예제는 [VíDụMạng.java](../../../example/java/VíDụMạng.java),
thựcThiLệnh 절차는 [example HướngDẫn](../../../example/README.md),
câyNguồn cáchĐặtTên 원칙은 [cáchĐặtTên HướngDẫn](../cáchĐặtTên/HướngDẫn.md)에 있다.

## Swing cửaSổ VíDụ

`/example/java/VíDụCửaSổ.java`와 컴파일된 `.class`toánHạngĐầuTiên KhởiĐộng 시 준비된다.
`cd /example/java` phầnMụcKếTiếp `java VíDụCửaSổ`로 연다. tên giáTrịVào, chào 버튼,
인사말과 giáTrịNhấnChuột sốLượngSựLặp làmMới, X 닫기를 지원한다.

| 기능 | tiếngViệt 직접 API |
|---|---|
| Runnable / run | `TácVụChạyĐược.thựcThiTácVụ()` |
| ActionListener / actionPerformed | `BộNhậnHànhĐộng.nhậnHànhĐộng(ThôngBáoHànhĐộng thôngBáo)` |
| ActionEvent | `ThôngBáoHànhĐộng.vănBảnLệnh()`, `nguồnSựKiện()`, `sốHiệu()` |
| JFrame | `cửaSổ(tiêuĐềCửaSổ, khoảngTrảiRộng, giáTrịCao)`, `thêmPhầnTử(PhầnTửMànHình)`, `hiệnCửaSổ()`, `đóng()`, `làHiệnĐược()` |
| JButton | `nút(vănBản, vịTríNgang, vịTríDọc, khoảngTrảiRộng, giáTrịCao, giáTrịBộNhận)`, `đặtGiáTrịBộNhậnHànhĐộng(giáTrịBộNhận)` |
| JLabel / JTextField | `nhãn(...)`, `TrườngVănBản(...)` |
| giáTrịChung MànHình giáTrịPhầnTử | `PhầnTửMànHình.đọcVănBản()`, `ghiVănBản(vănBản)`, `đặtGiáTrịCácCận(vịTríNgang, vịTríDọc, khoảngTrảiRộng, giáTrịCao)` |
| SwingUtilities.invokeLater | `HàngĐợiSựKiện.gọiThựcHiệnVềSau(TácVụChạyĐược)`, `làĐangĐiềuPhốiSựKiện()` |
| Thread | `bộLàmViệc(TácVụChạyĐược)`, `bắtChạyTácVụ()`, `đợi()`, `làCònSống()`, `nhườngTácVụ()` |
| 명령행 | `chạy()`, `CácĐốiSố.sốLượngPhầnMục()`, `CácĐốiSố.vănBản(chỉSốThứBậc)` |

giáTrịĐỉnh 클래스들은 `JButton`·`Thread` 등의 객체를 만들거나 보관하지 않는다.
tựThân JVM의 `gọiThựcHiệnMànHìnhTiếngHàn`, `luồngChạyTiếnTrình`toánHạngĐầuTiên tiếngViệt giáTrịLớp·giáTrịPhươngThức·서술자를
해석해 MànHình 요소와 thựcThiLệnh 가닥을 직접 만든다. hànhĐộng 알림도 tựThân 객체이며
콜백으로 `thựcThiTácVụ`와 `nhậnHànhĐộng`를 직접 찾는다. 표준 Swing/Thread를
사용하는 기존 프로그램의 thựcThiLệnh 경로는 별도로 남아 있다.

Java 소스의 `native` 선언은 tựThân JVM에 구현한 계약이다. 생성자의 예외는
이 계약이 없는 Chủ JVM에서 무동작 객체가 생기지 않도록 하는 từChốiGiáTrị 경로다.
tựThân JVM은 생성자를 직접 처리한다. 일반 OpenJDK에서는 이 직접 phầnCàiĐặt API를
실행할 trịSố 없다. Chủ javac로 컴파일한 giáTrịLùi tựThân JVM에서 실행한다.
`StringUtilities`라는 표준 Swing 클래스는 없으며, MànHình 큐 기능은 `SwingUtilities`에 해당한다.

```java
import tiếngViệt.tựThân.*;
public class 가닥예제 implements TácVụChạyĐược {
    public void thựcThiTácVụ() { ĐầuRa.ghiDòng("tiếngViệt TácVụ thựcThiLệnh"); }
    public static void chạy() throws NgoạiLệĐãBịNgắtChờ {
        bộLàmViệc giáTrịLuồngChạy = TácVụ.chạy(new 가닥예제());
        TácVụ.đợi(giáTrịLuồngChạy);
    }
}
```

`example/java`의 다섯 소스는 cácTừĐượcDànhTrước·리터럴 외 식별자를 한국어로 작성한다.
giáTrịMảng cácĐốiSố 대신 `CácĐốiSố`, 길이는 `KýTự.sốLượngByte`를 사용한다.
표준 Java의 `main(String[])`도 việcXửLýTiếpTục 지원한다. giáTrịHai toánHạngThứBa 정의되어 있으면
tựThân 실행기는 cácĐốiSố 없는 `chạy()`을 우선한다.
기존 tiếngViệt MànHình 래퍼의 표준 `Component`/`Runnable`/`ActionListener` 인수와
`TácVụ.chạy(Runnable)`을 사용하던 코드는 새 tiếngViệt 계약으로 수정하고 재컴파일한다.
이는 전체 AWT/Swing·Thread API giáTrịHỗTrợ 또는 모든 JDK 소스의 번역을 뜻하지 않는다.

바이트코드에도 giáTrịLớp·giáTrịPhươngThức 이름과 서술자가 남는다.
tiếngViệt tên 자체는 합법이지만, 다른 클래스에서 그 이름을 참조하는 giáTrịPhầnCon,
상속·giáTrịPhươngThức 재정의, native nốiKết, 런처의 진입점도 함께 맞춰야 한다.
근거는 [JLS giáTrịĐịnhDanh](https://docs.oracle.com/javase/specs/jls/se25/html/jls-3.html#jls-3.8)와
[JVMS giáTrịPhươngThức thamChiếu](https://docs.oracle.com/javase/specs/jvms/se25/html/jvms-4.html#jvms-4.4.2)toánHạngThứBa.
