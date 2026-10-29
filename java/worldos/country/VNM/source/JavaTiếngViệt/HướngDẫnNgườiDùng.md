# jkoros tiếngViệt thưViện HướngDẫnNgườiDùng

확인일: 2026-09-27. 대상은 `platforms/rpi4`의 **ARM64 Linux + OpenJDK 실행판**이며, QEMU에서도 같은 Java 라이브러리를 사용한다. `os/`의 tựThân x86 giáTrịNhân 및 `NguồnNềnTảng/`의 관리 giáTrịNhân 모형과 구분한다.

## 1. phầnMụcHiệnTại 제공하는 thưViện

패키지는 `tiếngViệt.Java`, HệĐiềuHành 안의 JAR 경로는 `/opt/jkoros/lib/JavaTiếngViệt.jar`toánHạngThứBa. **giáTrịPhụGiúp giáTrịLớp 5개, 공개 giáTrịTĩnh giáTrịPhươngThức 22개, 별도 GUI 프로그램인 KhôngGianLàmViệc 1개**toánHạngĐầuTiên 있다. JAR는 Java 11 이상을 대상으로 빌드하며 phầnMụcHiệnTại ARM64 배포판에는 OpenJDK 25가 포함돼 있다.

| giáTrịLớp | giáTrịPhươngThức trịSố | 기능 | mãNguồn |
|---|---:|---|---|
| `Tệp` | 9 | UTF-8 텍스트·giáTrịByte Tệp, giáTrịThưMục, danhSáchMục | [Tệp.java](mãNguồn/tiếngViệt/Java/Tệp.java) |
| `KýTự` | 5 | UTF-8 chuyểnĐổiGiáTrị, NFC chuẩnHóaGiáTrị, giáTrịMã 포인트, ChuỗiKýTự giáTrịRanhGiới | [KýTự.java](mãNguồn/tiếngViệt/Java/KýTự.java) |
| `TruyềnThông` | 2 | HTTP(S) GET, TCP nốiKết | [TruyềnThông.java](mãNguồn/tiếngViệt/Java/TruyềnThông.java) |
| `TácVụ` | 4 | 스레드 thựcThiLệnh·chờGiáTrị, 고정 cỡ TácVụ TrìnhKhởiChạyChươngTrình | [TácVụ.java](mãNguồn/tiếngViệt/Java/TácVụ.java) |
| `MànHình` | 2 | Swing 이벤트 mụcGiáTrịTiếnTrình 가닥에 TácVụ 예약, cửaSổ sinh | [MànHình.java](mãNguồn/tiếngViệt/Java/MànHình.java) |
| `KhôngGianLàmViệc` | điểmMục `main` | Java mãNguồn giáTrịSửa·giáTrịCất·biênDịchNguồn·thựcThiLệnh | [KhôngGianLàmViệc.java](mãNguồn/tiếngViệt/Java/KhôngGianLàmViệc.java) |

표준 JDK 전체를 한국어로 번역한 라이브러리는 아니다. Java 키워드와 `String`, `Path`, `Socket`, `JFrame`, `IOException` 같은 표준 kiểuDữLiệu·예외를 함께 사용한다. 이 도우미에 없는 기능은 OpenJDK의 표준 API 또는 별도 라이브러리로 구현한다. 예를 들어 HTTP POST, UDP, Swing nút·메뉴에는 각각 표준 Java API를 사용한다.

## 2. Java에서 bắtChạyTácVụ

게스트 운영체제의 TácVụ 폴더에서 `사용예.java`를 작성한다.

```java
import tiếngViệt.Java.*;
import java.nio.file.Path;

public class 사용예 {
    public static void main(String[] cácĐốiSố) throws Exception {
        Path giáTrịThưMục = Tệp.tạoThưMục(Tệp.đườngDẫn("사용예자료"));
        Path TàiLiệu = giáTrịThưMục.resolve("LờiChào.txt");
        Tệp.ghi(TàiLiệu, "vănBảnHangul 😀");
        String giáTrịNộiDung = Tệp.đọc(TàiLiệu);
        System.out.println(giáTrịNộiDung);
        System.out.println(KýTự.sốLượngĐiểmMã(giáTrịNộiDung)); // 한, vănBản, 공백, 😀 → 4
        Thread giáTrịViệc = TácVụ.chạy("LờiChào TácVụ", () -> System.out.println("TácVụ thựcThiLệnh"));
        TácVụ.đợi(giáTrịViệc);
    }
}
```

```sh
javac -encoding UTF-8 -cp /opt/jkoros/lib/JavaTiếngViệt.jar 사용예.java
java -cp .:/opt/jkoros/lib/JavaTiếngViệt.jar 사용예
```

로그인 환경에 giáTrịMặcĐịnh `CLASSPATH`도 설정돼 있지만, 명시적인 `-cp`는 다른 thựcThiLệnh 환경에서도 경로를 분명하게 한다. 사용자가 `-cp`를 지정하면 필요한 JAR와 giáTrịLớp 폴더를 xâyDựngTấtCả 그 값에 포함해야 한다.

Chủ 저장소에서는 다음처럼 xâyDựngHệThống·실행한다. Chủ 경로와 게스트의 `/opt/...` 경로는 서로 다르다.

```sh
cd /home/user/jkoros/JavaTiếngViệt
make
javac -encoding UTF-8 -cp build/JavaTiếngViệt.jar VíDụ/LờiChào.java
java -cp build/JavaTiếngViệt.jar:VíDụ LờiChào
```

## 3. 전체 giáTrịPhụGiúp API

giáTrịĐáy 메서드는 xâyDựngTấtCả `public static`이며, 객체를 만들지 않고 `Tệp.đọc(...)`처럼 호출한다. 표의 이름은 dữLiệuThựcTế câyNguồn 및 JAR의 `javap -public` 결과와 대조했다. 선언된 CácPhépKiểmTra ngoạiLệ 외에도 잘못된 cácĐốiSố 등에 대한 표준 Java thựcThiLệnh 시 예외가 발생할 trịSố 있다.

### Tệp: `tiếngViệt.Java.Tệp`

`Path`는 `java.nio.file.Path`, `List`는 `java.util.List`toánHạngThứBa.

| giáTrịPhươngThức | kiểuTrảVề | hànhĐộng·điềuKiện |
|---|---|---|
| `đườngDẫn(String tên)` | `Path` | 이름을 đườngDẫn 객체로 chuyểnĐổiGiáTrị. dữLiệuThựcTế 파일을 만들지는 않음 |
| `đọc(Path đườngDẫn)` | `String` | Tệp 전체를 UTF-8 텍스트로 đọcKếtQuả |
| `ghi(Path đườngDẫn, String giáTrịNộiDung)` | `Path` | UTF-8 giáTrịCất. 파일이 없으면 생성하고, 있으면 기존 내용을 비움 |
| `đọcGiáTrịByte(Path đườngDẫn)` | `byte[]` | Tệp 전체를 giáTrịByte 배열로 đọcKếtQuả |
| `ghiGiáTrịByte(Path đườngDẫn, byte[] giáTrịNộiDung)` | `Path` | giáTrịByte giáTrịCất. 없으면 생성하고, 있으면 기존 내용을 비움 |
| `tạoThưMục(Path đườngDẫn)` | `Path` | 필요한 상위 폴더까지 sinh |
| `thựcHiệnĐượcTồnTại(Path đườngDẫn)` | `boolean` | 존재 여부 xácMinh. 확인할 trịSố 없는 경우도 `false`giáTrịViệc trịSố 있음 |
| `xóaMục(Path đườngDẫn)` | `boolean` | 삭제했으면 `true`, 없으면 `false`. 폴더의 재귀 삭제는 아님 |
| `danhSáchMục(Path đườngDẫn)` | `List<Path>` | 바로 giáTrịĐáy 항목을 đườngDẫn giáTrịCănChỉnh 순서로 kếtQuảTrảVề. 재귀 탐색은 아님 |

`đườngDẫn`, `thựcHiệnĐượcTồnTại`를 제외한 giáTrịĐỉnh 메서드는 `IOException`을 선언한다. `ghi`와 `ghiGiáTrịByte`는 상위 폴더를 자동으로 만들거나 내용을 giáTrịSựTiếpDiễn 쓰지 않는다. 필요한 폴더는 먼저 생성한다. 큰 파일은 전체 내용을 메모리에 담는 대신 표준 Java 스트림·giáTrịKênh API를 사용하는 방식으로 작성할 trịSố 있다.

### KýTự: `tiếngViệt.Java.KýTự`

| giáTrịPhươngThức | kiểuTrảVề | hànhĐộng·điềuKiện |
|---|---|---|
| `mãHóa(String giáTrịNộiDung)` | `byte[]` | 문자열을 UTF-8 바이트로 chuyểnĐổiGiáTrị |
| `giảiMậtMãDữLiệu(byte[] giáTrịNộiDung)` | `String` | UTF-8 바이트를 문자열로 chuyểnĐổiGiáTrị. 잘못된 입력은 대체 문자로 mụcGiáTrịTiếnTrình |
| `chuẩnHóaGiáTrị(String giáTrịNộiDung)` | `String` | giáTrịUnicode NFC chuẩnHóaGiáTrị. 예: PhốiHợp giáTrịJamo `ᄀ` + `ᅡ` → `toánHạngĐầuTiên` |
| `sốLượngĐiểmMã(String giáTrịNộiDung)` | `int` | UTF-16 giáTrịMã 단위가 아닌 giáTrịUnicode giáTrịMã 포인트 trịSố |
| `từTừVựng(String giáTrịNộiDung, Locale NgônNgữ)` | `List<String>` | giáTrịGán 언어의 `BreakIterator` từTừVựng 경계로 나눈 khoảngVănBản |

`từTừVựng`은 공백·문장부호 구간도 반환한다. 자연어 형태소 분석기나 공백을 제거한 giáTrịTừ danhSáchMục API는 아니다. `chuẩnHóaGiáTrị`는 입력기나 dịchThuậtNguồn 기능이 아니다. giáTrịMã 포인트 trịSố 역시 사람이 보는 giáTrịKýTự 수와 항상 같지는 않다. 여러 giáTrịMã 포인트로 이루어진 cácGiáTrịKếtHợp KýTự·가족 이모지 등을 구분해야 한다.

### TruyềnThông: `tiếngViệt.Java.TruyềnThông`

| giáTrịPhươngThức | kiểuTrảVề | hànhĐộng·điềuKiện |
|---|---|---|
| `giáTrịThu(URI địaChỉ, Duration giớiHạnThờiGian)` | `HttpResponse<String>` | HTTP(S) GET. nốiKết 및 yêuCầu giớiHạnThờiGian cácThiếtLập. lờiĐáp 본문을 UTF-8로 phânTíchCúPhápGiáTrị |
| `kếtNốiĐiểmCuối(String địaChỉ, int cổngPhầnCứng, int miliGiâyGiớiHạn)` | `Socket` | TCP nốiKết trạngTháiSau 같은 값으로 đọc 제한시간도 cácThiếtLập |

`giáTrịThu`는 `IOException`, `InterruptedException`을 선언한다. 제한시간은 양수다. 404·500 같은 HTTP lỗi 상태도 응답으로 반환하므로 `statusCode()`로 판단하고 `body()`로 본문을 읽는다. phầnMụcHiệnTại 구현은 호출마다 HTTP 클라이언트를 만들며 자동 리다이렉트 설정을 추가하지 않는다.

`kếtNốiĐiểmCuối`는 `IOException`을 선언한다. 연결된 소켓은 호출자가 `close()` 또는 try-with-resources로 닫아야 한다. 제한밀리초의 0은 giáTrịGiớiHạn 없음이며, ghi 전체의 giáTrịHạnChót 시간을 보장하는 옵션은 아니다.

```java
var lờiĐáp = TruyềnThông.giáTrịThu(
    java.net.URI.create("http://127.0.0.1:8000/"),
    java.time.Duration.ofSeconds(5));
System.out.println(lờiĐáp.statusCode());
System.out.println(lờiĐáp.body());
```

giáTrịĐỉnh 조각은 giáTrịPhươngThức 안에서 실행하며 별도로 해당 주소의 서버를 실행해야 한다. Java ngoạiLệ 처리가 필요하다.

### TácVụ: `tiếngViệt.Java.TácVụ`

| giáTrịPhươngThức | kiểuTrảVề | hànhĐộng·điềuKiện |
|---|---|---|
| `chạy(String tên, Runnable hànhĐộng)` | `Thread` | 이름을 지정한 스레드를 만들고 즉시 chạy |
| `đợi(Thread giáTrịLuồngChạy)` | `void` | 해당 스레드가 종료할 때까지 `join()` |
| `ngắnPhầnCòn(long miliGiây)` | `void` | 호출한 스레드를 giáTrịGán giáTrịThờiGian 동안 `sleep()` |
| `giáTrịBànLàmViệc(int sốLượngLuồngChạy)` | `ExecutorService` | 고정 cỡ TácVụ TrìnhKhởiChạyChươngTrình sinh. 가닥수는 양수 |

`đợi`, `ngắnPhầnCòn`는 `InterruptedException`을 선언한다. TácVụ 실행기는 giáTrịDùng trạngTháiSau `shutdown()`으로 종료하고 필요하면 `awaitTermination(...)`으로 완료를 기다린다. Swing 이벤트 mụcGiáTrịTiếnTrình 가닥에서 긴 작업이나 `đợi`를 실행하면 화면이 멈출 trịSố 있다.

### MànHình: `tiếngViệt.Java.MànHình`

| giáTrịPhươngThức | kiểuTrảVề | hànhĐộng·điềuKiện |
|---|---|---|
| `giáTrịVềSau(Runnable hànhĐộng)` | `void` | Swing 이벤트 mụcGiáTrịTiếnTrình 가닥에 실행을 예약하고 kếtQuảTrảVề |
| `cửaSổ(String tiêuĐềCửaSổ, JComponent giáTrịNộiDung, int giáTrịRộng, int giáTrịCao)` | `JFrame` | giáTrịNộiDung·크기를 지정한 창을 생성해 hiệnGiáTrị |

`cửaSổ`을 Swing 이벤트 mụcGiáTrịTiếnTrình giáTrịLuồngChạy 밖에서 부르면 `IllegalStateException`이 발생한다. 그래픽 세션도 필요하다. QEMU에서는 VNC 데스크톱의 터미널에서 실행한다.

```java
MànHình.giáTrịVềSau(() -> MànHình.cửaSổ(
    "tiếngViệt MànHình", new javax.swing.JLabel("안녕하세요"), 500, 180));
```

반환된 `JFrame`에 표준 Swing API를 추가로 사용할 trịSố 있다. 창의 đóng 동작은 `DISPOSE_ON_CLOSE`toánHạngThứBa. `MànHình.giáTrịVềSau`toánHạngĐầuTiên 반환됐다고 cửaSổ 생성이 이미 끝난 것은 아니다.

### KhôngGianLàmViệc: giáTrịSửa·biênDịchNguồn GUI

```sh
java -cp /opt/jkoros/lib/JavaTiếngViệt.jar tiếngViệt.Java.KhôngGianLàmViệc
```

`~/workspace`의 원문을 mở·저장하고, `javac`로 컴파일해 `java`로 실행한다. thựcThiLệnh Tệp 만들기는 `jclassc --target openjdk` 경로를 사용한다. 작업마당은 개발용 프로그램이며 별도의 Tệp·KýTự API 클래스가 아니다. 생성하는 thựcThiLệnh Tệp 방식은 [TrìnhBiênDịch môTả](../compiler/OpenJDK-tệpTệpThựcThi.md)을 따른다.

## 4. Python과 C++에서 사용할 trịSố thựcHiệnĐượcTồnTại?

| chếĐộPhươngThức | phầnMụcHiệnTại TệpĐầuMục giáTrịTrạngThái | gọiThựcHiện 가능 cắtXén |
|---|---|---|
| Java → tiếngViệt JAR | giáTrịMặcĐịnh TệpĐầuMục | giáTrịĐỉnh 22개 메서드와 KhôngGianLàmViệc |
| Python → `java` giáTrịCon 프로세스 | Python·Java giáTrịMặcĐịnh TệpĐầuMục | 작은 Java 진입점을 통해 호출하고 표준 ĐầuRa·Tệp 등으로 kếtQuả giáTrịTiến |
| Python → JPype → JVM | JPype는 giáTrịMặcĐịnh 배포에 phươngThứcThiếu | 별도 càiĐặtGiáTrị trạngTháiSau Java giáTrịLớp·giáTrịPhươngThức gọiThựcHiện 가능. 이 배포판의 ARM64/musl/Python 3.14 조합은 thêmCuốiMục thẩmĐịnh giáTrịCầnĐến |
| C++ → JNI → JVM | `g++`, JNI 헤더, `libjvm.so` TệpĐầuMục | JVM을 생성하고 tiếngViệt giáTrịLớp·메서드를 직접 호출할 trịSố 있음 |
| Python용 독립 tiếngViệt thưViện | phầnMụcHiệnTại giáTrịMặcĐịnh 제공 phươngThứcThiếu | 필요하면 Python 표준 라이브러리를 감싸는 tiếngViệt 모듈을 별도로 작성 |
| C/C++용 독립 tiếngViệt thưViện | tựThân x86 `posix-kor`와 tựThân ARM64 커널용 trạngTháiBanĐầu RAM Tệp 연결이 별도로 존재 | giáTrịHai toánHạngThứBa 이 Linux/OpenJDK 실행판의 libc 라이브러리는 아님 |

Python의 일반 `import`toánHạngThứHai `ctypes.CDLL`로 JAR를 바로 읽을 수는 없다. C++의 `#include`toánHạngThứHai 일반 네이티브 링커만으로 Java 메서드를 연결할 수도 없다. JVM 프로세스 또는 JVM nốiKết 계층을 거쳐야 한다.

### Python: thêmCuốiMục 패키지 없이 gọiThựcHiện

thựcThiLệnh 가능한 VíDụ 원문은 [LệnhVănBản.java](VíDụ/NgônNgữKhác/LệnhVănBản.java), [GọiPython.py](VíDụ/NgônNgữKhác/GọiPython.py)toánHạngThứBa. Python이 Java 진입점을 실행하고 `KýTự.sốLượngĐiểmMã`의 SốNguyên 결과를 받는다. cácĐốiSố 목록을 사용하며 vỏLệnh lệnh 문자열을 조립하지 않는다. `subprocess.run`의 프로세스 thựcThiLệnh·chươngTrìnhRa giáTrịMã·ĐầuRa mụcGiáTrịTiếnTrình 방식은 [Python 공식 TàiLiệu](https://docs.python.org/3/library/subprocess.html)를 따른다.

두 VíDụ 파일을 게스트의 같은 폴더에 복사한 giáTrịLùi 그 폴더에서 실행한다. VíDụ Tệp 자체는 giáTrịMặcĐịnh 시스템 이미지에 자동 설치돼 있지 않다.

```sh
mkdir -p classes
javac -encoding UTF-8 -cp /opt/jkoros/lib/JavaTiếngViệt.jar -d classes LệnhVănBản.java
python3 GọiPython.py --text 'vănBảnHangul 😀'
```

ĐầuRa: `Python → tiếngViệt.Java.KýTự.sốLượngĐiểmMã: 4`

이 예제의 Python Hàm `sốLượngĐiểmMã`는 이번 문서의 nốiKết 예제이며 기존에 설치된 Python 라이브러리는 아니다. phầnMụcHiệnTại 예제는 호출할 때마다 JVM 프로세스를 시작한다. Java giáTrịĐốiTượng 자체를 Python으로 가져오는 방식은 아니며, 다른 메서드를 사용하려면 진입점의 cácĐốiSố·kếtQuả 형식을 확장한다.

### Python: JPype로 같은 프로세스에서 gọiThựcHiện

JPype를 별도 설치한 환경에서는 phầnMụcKếTiếp 형태로 연결할 trịSố 있다. **아래는 giáTrịViệcChọn 가능한 nốiKết 방법이며, phầnMụcHiệnTại 배포판에 JPype가 설치돼 있거나 thựcThiLệnh 검증됐다는 뜻은 아니다.** JVM 시작과 `JClass`를 통한 giáTrịLớp 접근은 [JPype 공식 môTả](https://jpype.readthedocs.io/en/latest/userguide.html)을 참고한다.

```python
import jpype

jpype.startJVM(
    "/usr/lib/jvm/java-25-openjdk/lib/server/libjvm.so",
    classpath=["/opt/jkoros/lib/JavaTiếngViệt.jar"])
try:
    KýTự = jpype.JClass("tiếngViệt.Java.KýTự")
    print(KýTự.sốLượngĐiểmMã(jpype.JString("vănBảnHangul 😀")))
finally:
    jpype.shutdownJVM()
```

Python·JVM·nốiKết 모듈의 CPU 아키텍처가 맞아야 한다. 이 실행판은 ARM64 + musl이므로 일반 x86_64/glibc용 바이너리를 그대로 설치하는 방식은 맞지 않는다. JPype càiĐặtGiáTrị·패키지 빌드는 이번 TàiLiệu 작업에서 수행하지 않았다.

### C++: JNI로 직접 gọiThựcHiện

[GọiJava.cpp](VíDụ/NgônNgữKhác/GọiJava.cpp)는 dữLiệuThựcTế thựcThiLệnh 가능한 예제다. JVM을 TácVụ 스레드에서 생성하고 phầnMụcKếTiếp 메서드를 찾는다.

```cpp
jclass type = env->FindClass("tiếngViệt/Java/KýTự");
jmethodID method = env->GetStaticMethodID(
    type, "sốLượngĐiểmMã", "(Ljava/lang/String;)I");
```

JVM sinh·종료와 스레드 연결은 [JNI Invocation API](https://docs.oracle.com/en/java/javase/25/docs/specs/jni/invocation.html)의 방식이다. `JNIEnv*`는 sinh·연결된 스레드에서 사용해야 한다. 예제는 Java 예외를 확인하고 JVM 종료까지 처리한다.

게스트에 `GọiJava.cpp`를 복사한 giáTrịLùi 컴파일한다. 로그인 환경의 `JAVA_HOME`은 `/usr/lib/jvm/java-25-openjdk`toánHạngThứBa.

```sh
g++ -std=c++11 -Wall -Wextra -pthread \
  -I"$JAVA_HOME/include" -I"$JAVA_HOME/include/linux" \
  GọiJava.cpp -L"$JAVA_HOME/lib/server" \
  -Wl,-rpath,"$JAVA_HOME/lib/server" -ljvm -o GọiJava
./GọiJava /opt/jkoros/lib/JavaTiếngViệt.jar
```

ĐầuRa: `C++ → tiếngViệt.Java.KýTự.sốLượngĐiểmMã: 4`

예제는 `vănBảnHangul 😀`을 UTF-16으로 만들어 `NewString`에 전달한다. `NewStringUTF`toánHạngĐầuTiên 받는 modified UTF-8은 일반 UTF-8과 차이가 있으므로, 일반 UTF-8 이모지 바이트를 그대로 넘기는 예제로 작성하지 않았다. [JNI ChuỗiKýTự giáTrịĐịnhDạng](https://docs.oracle.com/en/java/javase/25/docs/specs/jni/types.html#modified-utf-8-strings)

다른 tiếngViệt 메서드도 JNI 서명과 cácĐốiSố 자료형을 맞춰 호출할 trịSố 있다. 예를 들어 `Path`를 받는 Tệp API는 먼저 `Tệp.đườngDẫn`로 Java đườngDẫn 객체를 얻어 전달한다. Swing 호출에는 그래픽 세션과 이벤트 mụcGiáTrịTiếnTrình giáTrịLuồngChạy 규칙도 그대로 적용된다. JNI는 Java 실행을 기계어로 대체하는 기능이 아니며 JVM이 việcXửLýTiếpTục 필요하다.

### 기존 posix-kor와의 관계

추가된 [tựThân ARM64 nốiKết](../posix-kor/arm64-native/HướngDẫn.md)은 C++에서 AOT Java 커널의 RAM Tệp API를 직접 호출하며, 별도 EL0 NgườiDùng 라이브러리로 Tệp/UDP 루프백 SVC 호출도 제공한다. JNI를 사용하지 않는다. 이 문서의 ARM64 **Linux** 및 tiếngViệt Java JAR와는 다른 thựcThiLệnh 기반이며 tựThân 커널은 별도 제한형 Java TrìnhBiênDịch/JVM과 MicroPython 1.24.1을 실행한다. MicroPython의 `import jkoros`로 Java giáTrịNhân Tệp·UDP 루프백·hìnhChữNhật 호출이 가능하지만 이 문서의 JAR를 가져오는 기능은 아니다. tựThân 커널의 전체 OpenJDK/JRE/CPython 이식은 아직 미완성이다.

[posix-kor](../posix-kor/HướngDẫn.md)에는 `mởTệp`, `đọcDữLiệuTệp`, `ghiDữLiệuTệp`, `đóngTệp`, `tạoĐiểmCuối`, `gửiDữLiệuĐiệnDữLiệu` 등의 tiếngViệt C 별칭이 있다. 그러나 구현은 **tựThân jkoros i386 커널의 `int 0x80` gọiThựcHiện 규약용**이다.

이 `libposix-kor.a`와 tựThân `sys/stat.h` 등의 헤더는 phầnMụcHiệnTại ARM64 Linux 실행판의 libc/C++용 라이브러리가 아니다. 해당 헤더·바이너리를 ARM64 Linux 프로그램에 그대로 연결해서는 ABI가 맞지 않는다. C++용 tiếngViệt giáTrịLớp 라이브러리나 Python용 바인딩을 giáTrịMặcĐịnh 제공하는 상태도 아니다. phầnMụcHiệnTại Linux 실행판에서 그와 같은 독립 API를 제공하려면 Linux 표준 라이브러리를 대상으로 별도로 phầnCàiĐặt·빌드해야 한다.

## 5. xácMinh 범위와 재현

패키지 TệpĐầuMục 여부는 [giáTrịBảnPhânPhối 패키지 danhSáchMục](../platforms/rpi4/dist/packages.lock.json) 및 xâyDựngHệThống 루트의 dữLiệuThựcTế 파일로 확인했다. JNI 헤더는 JDK의 `include/jni.h`, `include/linux/jni_md.h`, JVM 라이브러리는 `lib/server/libjvm.so`에 있다. 사용자가 giáTrịSau 별도로 설치한 패키지는 이 giáTrịMặcĐịnh giáTrịBảnPhânPhối 목록과 다를 trịSố 있다.

이번에 **Chủ x86_64/OpenJDK 11에서** Python giáTrịCon 프로세스 호출과 C++ JNI 직접 호출을 biênDịchNguồn·실행해 각각 kếtQuả 4를 확인했다. JAR 공개 메서드도 소스와 대조했다. Python nốiKết 예제는 thêmCuốiMục 패키지를 설치하지 않는다.

문서의 Java giáTrịDùng 예제도 biênDịchNguồn·실행했고, 22개 메서드의 TàiLiệu TệpĐầuMục 여부와 로컬 TàiLiệu 링크를 확인했다. [VíDụ thẩmĐịnh bảnGhiNhậtKý](build/NgônNgữKhác/báoCáoViệcThẩmĐịnh.json)

기존 ARM64 QEMU에서는 Java의 Tệp·giáTrịUnicode·스레드·HTTP 및 Swing KiểmThử 결과가 있다. 이번 Python/C++ nốiKết 예제의 **ARM64 게스트 실행과 JPype 설치는 별도 검증하지 않았다.** 이미지와 thựcThiLệnh 중인 NgườiDùng 환경은 이 TàiLiệu 작업에서 변경하지 않았다. [기존 HệĐiềuHành thẩmĐịnh bảnGhiNhậtKý](../platforms/rpi4/VERIFICATION.md)

호스트에서 Python 예제를 재현하려면:

```sh
cd /home/user/jkoros/JavaTiếngViệt
make
mkdir -p build/NgônNgữKhác
javac -encoding UTF-8 --release 11 -cp build/JavaTiếngViệt.jar \
  -d build/NgônNgữKhác VíDụ/NgônNgữKhác/LệnhVănBản.java
python3 VíDụ/NgônNgữKhác/GọiPython.py \
  --jar build/JavaTiếngViệt.jar --classes build/NgônNgữKhác
```

Chủ C++ 예제는 giáTrịĐỉnh JNI biênDịchNguồn 명령의 JDK 경로를 **Chủ JDK đườngDẫn**로 바꾸고, mãNguồn `VíDụ/NgônNgữKhác/GọiJava.cpp`와 JAR `build/JavaTiếngViệt.jar`를 지정한다. ARM64 게스트 JDK의 헤더·thưViện 경로를 Chủ x86_64 링크 명령에 섞지 않는다.
