# jkoros 안에서 Java biênDịchNguồn·thựcThiLệnh

이 문서의 KhởiĐộng·vỏLệnh·giáTrịCất 명령은 **x86 giáTrịPhiênBản** 기준이다. 공유 Java TrìnhBiênDịch/JVM은 [tựThân ARM64 Pi4 giáTrịPhiênBản](../platforms/rpi4-native/README.md)에도 연결되어 있다. ARM64에서는 UTF-8 UART giáTrịVào·vănBảnHangul vănBảnTênTệp, `edit`의 단독 `.` giáTrịCất, 16개 RAM Tệp, 약 2초 thựcThiLệnh 제한을 사용한다.

`javac FILE.java`와 `java CLASS [ARGS]`를 네이티브 jkoros 셸에서 실행한다. 컴파일러와 JVM은 각각 독립 ELF로 적재되어 ring 3에서 동작한다. 소스를 게스트에서 읽어 dữLiệuThựcTế JVM `.class` 파일을 만들고, 그 파일의 바이트코드를 게스트 JVM이 해석한다. Chủ biênDịchNguồn 서버나 Linux 게스트는 사용하지 않는다.

**phầnMụcHiệnTại 구현은 tựThân 제한형 TrìnhBiênDịch·JVM이다. OpenJDK/JDK 전체를 이식하거나 설치한 것이 아니며 Java SE 호환 환경도 아니다.** 표준 라이브러리는 아래의 일부 호출을 구현한 것이다. `java -version`과 `javac -version`에도 이 범위를 표시한다. 일반 JAR, Maven/Gradle, 임의의 Java ChươngTrình 실행은 아직 지원하지 않는다.

## 바로 thựcThiLệnh

호스트에서:

```sh
cd /home/user/jkoros
make iso
make run
```

게스트에서:

```text
jkoros> javac -version
jkoros> java -version
jkoros> ls
jkoros> cat Hello.java
jkoros> javac Hello.java
Compiled: Hello.class (JVM class version 49)
Exit: 0
jkoros> java Hello
Hello from jkoros JVM!
55
Exit: 0
```

ISO는 `os/build/kernel.iso`toánHạngThứBa. 기존 VirtualBox 실행기도 같은 ISO를 사용한다. thựcThiLệnh 중이거나 저장된 VM에는 새 ISO가 자동 반영되지 않는다. 새 KhởiĐộng 절차는 [VirtualBox thựcThiLệnh HướngDẫn](ChạyVirtualBox.md)를 따른다. 이 변경의 Java 자동 시험은 QEMU에서 수행했다.

## 직접 작성

`edit`는 Tệp 전체를 새 내용으로 작성한다. 기존 내용의 dòng giáTrịSửa 기능은 아니다. `.save`로 저장하고 `.cancel`로 취소한다.

```text
jkoros> edit Demo.java
...> public class Demo {
...>  public static int square(int n) { return n * n; }
...>  public static void main(String[] args) {
...>   int n = Integer.parseInt(args[0]);
...>   System.out.println("square=" + square(n));
...>  }
...> }
...> .save
jkoros> javac Demo.java
jkoros> java Demo 12
square=144
Exit: 0
```

- `ls`: 파일과 giáTrịByte trịSố hiệnGiáTrị.
- `cat FILE`: Tệp giáTrịNộiDung hiệnGiáTrị. 텍스트 소스에 사용한다.
- `rm FILE`: dữLiệuBộNhớ Tệp 삭제.
- `edit FILE`: 전체 내용을 새로 giáTrịVào. 빈 파일도 저장할 trịSố 있다.
- 구문·giáTrịKiểu CácPhépKiểmTra giáTrịSựThấtBại 시 기존 `.class`는 유지된다. 소스를 고친 giáTrịLùi 컴파일이 실패했다면 phầnMụcTrướcĐó thựcThiLệnh 파일이 남아 있으므로 biênDịchNguồn giáTrịThànhCông 여부를 확인한다.

파일은 RAM에서 동작한다. 전용 giáTrịCất 매체가 없거나 `sync`하지 않은 내용은 재부팅하면 사라진다. `make -C os run-store`로 연결한 매체에는 `sync`로 câyNguồn·giáTrịLớp·DữLiệu 파일을 보존할 trịSố 있다. giáTrịTốiĐa 8개, 파일마다 16KiB, Tệp 이름은 ASCII 1~63자다. câyNguồn 이름은 `.class` 확장자 miềnĐịaChỉ 때문에 giáTrịTốiĐa 62자다. giáTrịSửa 입력은 ASCII이고 한 dòng giáTrịTốiĐa 128자다. dòng 또는 Tệp 한도를 넘긴 편집은 `.save`에서 거부하여 기존 파일을 보존한다. giáTrịNhân/TrìnhBiênDịch/JVM 구현의 Java 식별자는 한국어이며, phầnMụcHiệnTại 게스트 giáTrịVào giáTrịGiớiHạn 때문에 NgườiDùng VíDụ 이름은 ASCII로 작성한다.

## giáTrịBênNgoài Tệp 적재

호스트에서 만든 소스나 giáTrịHỗTrợ cắtXén 안의 `.class`를 KhởiĐộng 이미지에 포함할 trịSố 있다. `JAVA_FILES`는 `게스트이름=호스트경로` 목록이다. 아래의 경로는 예시이며 dữLiệuThựcTế 파일의 절대 경로로 바꾼다. 공백 없는 경로를 사용한다.

```sh
# Chủ JDK로 컴파일한 클래스도 사용할 trịSố 있다.
javac --release 8 /tmp/Demo.java
make -C /home/user/jkoros iso \
  JAVA_FILES='Demo.java=/tmp/Demo.java Demo.class=/tmp/Demo.class'
make -C /home/user/jkoros run \
  JAVA_FILES='Demo.java=/tmp/Demo.java Demo.class=/tmp/Demo.class'
```

새 KhởiĐộng trạngTháiSau `java Demo 12`를 실행한다. 소스만 넣었으면 게스트에서 `javac Demo.java`부터 실행한다. `JAVA_FILES`를 생략한 phầnMụcKếTiếp 빌드에서는 thêmCuốiMục 파일을 포함하지 않는다. Tệp giáTrịNộiDung 변경과 danhSáchMục 제거도 phầnMụcKếTiếp 빌드에 반영된다. nguyênBản Chủ 파일에는 쓰지 않는다. giáTrịMặcĐịnh `Hello.java`đếnKhi 합해 8개이며, 같은 이름을 명시하면 giáTrịMặcĐịnh 예제를 대체한다. 새 `.class`를 저장할 빈 슬롯도 남겨 둔다.

`--release 8`은 giáTrịLớp Tệp 버전을 맞추는 옵션이다. 사용하는 문법·mãByte·라이브러리도 giáTrịĐáy giáTrịHỗTrợ cắtXén 안에 있어야 한다.

## giáTrịHỗTrợ cắtXén

| 기능 | 게스트 javac | 게스트 JVM |
| --- | --- | --- |
| giáTrịLớp | 패키지 없는 단일 giáTrịLớp, giáTrịTĩnh Hàm, 재귀, cácĐốiSố/kếtQuảTrảVề | 실행마다 단일 giáTrịLớp 적재, public static main(String[]) |
| giáTrịMặcĐịnh giáTrị | int, boolean, char, String, main의 String[] cácĐốiSố | SốNguyên·thamChiếu ngănXếpToánHạng, String, int[], String[], 내부 StringBuilder |
| giáTrịCâuLệnh | giáTrịBanĐầu 있는 phạmViCụcBộ KhaiBáo, giáTrịPhépGán, `+=`, `-=`, `*=`, `/=`, `%=`, 후위 ++/--, 블록, if/else, while, for, return | 해당 SốNguyên·thamChiếu 바이트코드와 điềuKiện nhánh |
| giáTrịBiểuThức | 십진 SốNguyên, UTF-8 소스의 ChuỗiKýTự/KýTự, + - * / %, 비교, ==/!=, !/&&/\|\|, ChuỗiKýTự cácGiáTrịKếtHợp | SốNguyên giáTrịThaoTác·giáTrịBit giáTrịThaoTác·giáTrịKiểu chuyểnĐổiGiáTrị, 단락 평가, giáTrịMảng mụcTruyCập |
| Tệp | FileInputStream(String), FileOutputStream(String[, boolean]), read()/write(int)/close() | dữLiệuThựcTế giáTrịNhân 파일서술자와 nốiKết, sinh·xóaSạchCácNộiDung·thêmCuốiSựTiếpDiễn·EOF |
| ĐầuRa | System.out.print/println: int/boolean/char/String, println() | 동일 |
| ChuỗiKýTự/cácĐốiSố | String.length(), args.length, args[index], Integer.parseInt | 추가로 String.charAt(), ChuỗiKýTự 상수의 modified UTF-8 해독 |

선언은 지원하는 문법만 허용한다. 여러 변수를 한 선언에 나열하기, giáTrịBanĐầu 없는 phạmViCụcBộ KhaiBáo, 오버로드, 임의 giáTrịKiểu chuyểnĐổiGiáTrị, giáTrịMảng sinh mãNguồn, 8/16진 리터럴, Unicode câyNguồn 이스케이프 등은 미지원이다. `char`는 KýTự 리터럴로 초기화하며 일반 JDK의 모든 giáTrịHằng 축소 변환을 구현하지 않는다. giáTrịBênNgoài `.class`의 `int[]` sinh/đọc/쓰기는 지원하므로 Chủ `javac --release 8`로 만든 giáTrịMảng 예제는 실행할 trịSố 있다.

giáTrịĐốiTượng giáTrịTrường·일반 giáTrịĐốiTượng sinh·상속·인터페이스·여러 giáTrịLớp nốiKết, long/float/double, ngoạiLệ mụcGiáTrịTiếnTrình, 스레드·모니터, 리플렉션, JNI, JIT, GC, giáTrịĐỉnh 표에 없는 `java.io`와 `java.nio`/`java.net` 일반 API, 컬렉션, JAR와 클래스패스는 미지원이다. 런타임 오류는 Java ngoạiLệ 객체를 던지지 않고 giáTrịChẩnĐoán trạngTháiSau phầnMụcHiệnTại 프로그램을 종료한다. 객체와 ChuỗiKýTự giáTrịCất 공간은 thựcThiLệnh chươngTrìnhRa 시 NgườiDùng giáTrịMiền 전체와 함께 회수한다. 지속 thựcThiLệnh 중 GC는 없다.

## thựcThiLệnh 한도와 lỗi

| giáTrịTàiNguyên | giớiHạnSứcChứa |
| --- | --- |
| câyNguồn/giáTrịLớp Tệp | 각각 16KiB |
| TrìnhBiênDịch | giáTrịTừTố 2,047개, sinh giáTrịMã 4KiB, giáTrịHằng 풀 4KiB |
| Hàm/cácĐốiSố | 클래스당 32함수, 함수당 16인수 |
| JVM giáTrịHằng | 511개 |
| JVM Hàm giáTrịMã | 함수당 8KiB |
| JVM gọiThựcHiện/ngănXếpToánHạng/phạmViCụcBộ giáTrịBiến | 32프레임, 프레임당 ngănXếpToánHạng 128칸·phạmViCụcBộ 128칸 |
| JVM giáTrịĐốiTượng giáTrịCất miềnĐịaChỉ | 8,192개 32비트 mụcÔ, 헤더 TệpĐầuMục 약 32KiB |
| thựcThiLệnh | giáTrịTốiĐa 500,000 lệnh, 기존 커널의 약 3초 CPU thựcThiLệnh 상한도 적용 |

게스트 컴파일러는 버전 49.0 `.class`를 생성하며 JVM은 45.0~52.0 중 giáTrịHỗTrợ 명령으로 구성된 파일을 읽는다. 스택맵을 이용한 완전한 JVM TừĐiển 검증기를 구현한 것은 아니다. Tệp/giáTrịThuộcTính độDài, giáTrịHằng thamChiếu, lệnh·nhánh 경계를 검사하고, thựcThiLệnh 중 ngănXếpToánHạng giáTrịĐịnhDạng·phạmViCụcBộ khởiTạo·giáTrịMảng giáTrịChỉSốDưới·giáTrịĐốiTượng 참조를 검사한다. NgườiDùng 코드의 페이지·cổngPhầnCứng 접근은 기존 ring 3 경계로 보호한다.

일반 성공은 `Exit: 0`, biênDịchNguồn·JVM 오류는 `Exit: 1`, lệnh cácĐốiSố 오류는 `Exit: 2`toánHạngThứBa. CPU giáTrịThờiGian 상한은 기존 `Exit: 124`이며, NgườiDùng ELF 자체의 CPU/런타임 오류는 기존 chươngTrìnhRa 코드를 따른다. giáTrịSựThấtBại trạngTháiSau 셸에서 다른 프로그램을 việcXửLýTiếpTục 실행할 trịSố 있다.

## phầnCàiĐặt 위치와 KiểmThử

- `os/NgườiDùng/Java/TrìnhBiênDịchJava.java`: 게스트 어휘·구문·giáTrịKiểu CácPhépKiểmTra, giáTrịHằng 풀 및 mãByte sinh.
- `os/NgườiDùng/Java/MáyẢoJava.java`: giáTrịLớp 적재, ngănXếpToánHạng·프레임·giáTrịĐốiTượng giáTrịCất, lệnh 해석과 제한된 표준 gọiThựcHiện.
- `os/mãNguồn/HệTệpBộNhớ.java`: dữLiệuBộNhớ HệThốngTệp, giáTrịSửa, KhởiĐộng Tệp 적재.
- `os/mãNguồn/LờiGọiHệThống.java`, `compiler/bắtChạyChươngTrìnhNgườiDùng.s`: Tệp/KýTự ĐầuRa API와 NgườiDùng conTrỏ CácPhépKiểmTra.
- `os/CôngCụ/GóiTệpJava.py`: Chủ giáTrịVào Tệp thẩmĐịnh·KhởiĐộng giáTrịNhóm sinh.

```sh
make test-java
make test
```

`os/KiểmThử/ThửJava.py`는 ELF/ISO KhởiĐộng, 게스트 biênDịchNguồn·thựcThiLệnh, NgườiDùng giáTrịVào, 재귀·반복문·SốNguyên 극값·ChuỗiKýTự cácGiáTrịKếtHợp·단락 평가, 재실행, câyNguồn lỗi trạngTháiSau 기존 giáTrịLớp 보존, giáTrịMảng/trịSố 해독 lỗi, 무한 giáTrịLầnLặp giáTrịGiớiHạn, giáTrịSửa 넘침과 Tệp 부족을 검사한다. 게스트 sinh 클래스의 바이트를 QEMU 메모리에서 꺼내 OpenJDK `java -Xverify:all`로 실행하고 결과를 대조한다. 반대 방향으로 Chủ OpenJDK의 giáTrịLớp, SốNguyên 배열과 vănBảnHangul 상수를 게스트에 적재하며, 손상된 Tệp giáTrịDấuMốc·버전·giáTrịHằng trịSố·nhánh·스택을 거부하는지도 검사한다. 기록은 `os/build/ThửJava.json`에 남는다. 디스크 없는 별도 KiểmThử VM만 생성하고 종료한다.

phầnCàiĐặt 형식의 참고 DữLiệu: Oracle [JVM giáTrịLớp Tệp đặcTả](https://docs.oracle.com/javase/specs/jvms/se8/html/jvms-4.html), [JVM lệnh đặcTả](https://docs.oracle.com/javase/specs/jvms/se8/html/jvms-6.html).

## Java Tệp đầuRaĐầuVào

[FileDemo.java](../posix-kor/VíDụJava/FileDemo.java)는 일반 Java 표준 giáTrịLớp 이름을 사용한다. 소스를 `edit FileDemo.java`로 입력하거나 `JAVA_FILES`로 KhởiĐộng 이미지에 넣은 giáTrịLùi `javac FileDemo.java`, `java FileDemo`를 실행한다. 결과는 `65`, `255`, `66`, `-1`, `JAVA FILE IO PASS`toánHạngThứBa. `write(int)`는 하위 8비트를 쓰고 `read()`는 0~255 또는 EOF -1을 반환한다. giáTrịMặcĐịnh ĐầuRa 생성자는 내용을 비우고, boolean 인수가 true이면 이어쓴다.

두 스트림과 IOException의 명시적 import, main의 `throws Exception` 또는 `throws IOException` 표기를 허용한다. ngoạiLệ giáTrịĐốiTượng·try/catch·try-with-resources는 지원하지 않으며 Tệp 오류를 진단하고 프로그램을 종료한다. giáTrịMảng đầuRaĐầuVào, InputStream/OutputStream으로의 다형성, Reader/Writer, getFD, 일반 Tệp 메타데이터 API는 아직 없다. close는 열린 서술자를 닫고, 재부팅 보존에는 vỏLệnh `sync`toánHạngĐầuTiên 필요하다. 예제의 Tệp 이름은 phầnMụcHiệnTại 셸과 파일체계에 맞춰 ASCII로 쓴다.

`os/KiểmThử/ThửTệpJava.py`는 dữLiệuThựcTế 게스트 biênDịchNguồn 결과를 OpenJDK `-Xverify:all`로 giáTrịThửLại 실행해 Tệp 바이트와 출력을 대조한다. 범위와 giáTrịCất giáTrịPhươngTiện 사용법은 [posix-kor HướngDẫn](../posix-kor/HướngDẫn.md)를 참고한다. 참고한 표준 API는 Oracle [FileOutputStream](https://docs.oracle.com/javase/8/docs/api/java/io/FileOutputStream.html)이다.
