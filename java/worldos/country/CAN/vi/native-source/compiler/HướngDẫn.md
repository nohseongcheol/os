# Java 네이티브 TrìnhBiênDịch

OpenJDK tựThân 소스를 빌드하는 **`--target openjdk-build`**와 tựThân giáTrịNhân ABI CácPhépKiểmTra 도구를 추가했다.
이는 공식 javac/C/C++ 도구를 연결하는 별도 경로다. [xâyDựngHệThống 방법·dữLiệuThựcTế thẩmĐịnh·giáTrịNhân ChuyểnNền cắtXén](OpenJDK-VàXâyDựngNguồn-NhânBảnĐịa-ChuyểnNền.md)를 참고한다.

x86 직접 변환과 ARM64 C sinh 후단은 xâyDựngTấtCả [BiênDịchTrước.java](CôngCụJava/BiênDịchTrước.java)로 구현한다. `sh thờiGianCủaTrước.sh`로 직접 실행하며, [BiênDịchTrước.py](BiênDịchTrước.py)와 `TrìnhBiênDịch.py`는 phầnMụcTrướcĐó lệnh·API 및 OpenJDK 도구를 위한 호환 진입점이다. tựThân Pi4 후단은 freestanding C를 거쳐 AArch64로 만든다. [arm64.py](arm64.py)는 phầnMụcTrướcĐó 경로와 Python 호출을 위한 호환 진입점이다. Hàm·giáTrịBiến·sinh C 이름의 뜻과 예외는 [tiếngViệt cáchĐặtTên HướngDẫn](../platforms/rpi4-native/cáchĐặtTên/HướngDẫn.md)를 참고한다. [ARM64 xâyDựngHệThống·giáTrịHỗTrợ cắtXén](../platforms/rpi4-native/HướngDẫn.md)에 thựcThiLệnh 조건이 있다. 전체 OpenJDK나 일반 giáTrịLớp 실행기는 아니다.

thựcThiLệnh 시 JVM이 giáTrịCầnĐến 없는 x86 32비트 ELF를 만든다. JDK 11 이상으로 실행하는 Java tựThân AOT 후단이며, Java 전체를 새로 구현한 컴파일러는 아니다. Java 문법·mụcTruyCập giáTrịĐiềuKhiển·giáTrịKiểu 검사는 JDK의 `javac`에 맡기고, Java 8 giáTrịLớp 파일을 읽어 각 바이트코드를 x86 명령으로 직접 변환한다. C 코드로 우회하거나 mãByte 해석기를 커널에 넣지 않는다.

```text
Java mãNguồn → javac의 문법·giáTrịKiểu CácPhépKiểmTra → giáTrịTạm .class
          → tựThân x86 변환기 → GNU as/ld → 네이티브 ELF32
```

## 준비와 thựcThiLệnh

xâyDựngHệThống Chủ: Linux, Python 3.6 이상, JDK 11 이상(`javac --release 8`), GNU binutils(`as`, `ld`), Make. phầnMụcHiệnTại 환경의 OpenJDK 11, Python 3.6, binutils 2.30으로 검증했다. giáTrịBênNgoài Python 패키지와 네트워크 다운로드는 사용하지 않는다.

```sh
cd /home/user/jkoros/compiler
make
./build/phépTính
echo $?                  # 0이면 VíDụ KiểmThử giáTrịThànhCông

python3 TrìnhBiênDịch.py --target linux --entry phépTính.chạy \
    -o build/phépTính VíDụ/phépTính.java

make test
```

`linux` 대상은 Linux의 32비트 thựcThiLệnh 호환 기능이 필요하다. `int 0x80`을 차단하는 샌드박스에서는 `Bad system call`이 발생할 trịSố 있다. làBìnhThường Linux Chủ 또는 해당 실행을 허용한 KiểmThử 환경에서 실행한다. 시험의 비정상 종료를 통과로 처리하지 않는다.

진입점은 `static int chạy()` 또는 `static void chạy()`처럼 인수가 없어야 한다. `--entry 패키지.giáTrịLớp.Hàm`로 선택한다. `int` 반환값은 Linux 프로세스 chươngTrìnhRa 코드가 되며 셸에는 하위 8비트가 보인다. 일반 `main(String[] args)` thựcThiLệnh 환경이나 표준 đầuRaĐầuVào 라이브러리는 제공하지 않는다.

`--target kernel`은 KhởiĐộng 코드와 연결할 재배치 ELF 오브젝트를 생성한다.

```sh
cd /home/user/jkoros
python3 compiler/TrìnhBiênDịch.py --target kernel --entry Nhân.chạy \
    --export kernel_dispatch=LờiGọiHệThống.mụcGiáTrịTiếnTrình \
    -o os/build/java.o os/mãNguồn/*.java
```

`--target user`는 jkoros 셸에서 실행할 독립 ELF를 생성한다. `NgườiDùng` 클래스의 제한된 native API는 `int 0x80` 시스템 호출로 연결하며 `ThiếtBị` 클래스의 giáTrịPhầnCứng 직접 접근은 거부한다. NgườiDùng ELF는 Linux thựcThiLệnh Tệp ABI와 다르므로 호스트에서 실행하지 않는다. sinh·thanhGhiMục 방법은 [NgườiDùng thựcThiLệnh HướngDẫn](../os/NgườiDùng/HướngDẫn.md)에 있다. `--export 외부기호=giáTrịLớp.Hàm`는 오버로드되지 않은 giáTrịTĩnh 함수를 tựThân ngănXếpToánHạng ABI로 노출한다. 커널의 시스템 gọiThựcHiện 진입점에 사용한다.

Java 파일은 필요한 클래스들을 한꺼번에 전달한다. ĐầuRa 옆의 `.s`는 생성된 어셈블리, `.json`은 mãNguồn SHA-256 및 네이티브 kýHiệu↔Java Hàm 대응표다. tiếngViệt 함수명은 원문과 대응표에 보존하고 ELF 내부에는 충돌 방지용 máy 기호를 쓴다. biênDịchNguồn·hợpDịchGiáTrị·nốiKết 중 실패하면 기존 kếtQuả 파일을 덮어쓰지 않는다.

## giáTrịHỗTrợ cắtXén

- `int`, `boolean`, `byte`, `short`, `char`의 32비트 phépTính 및 giáTrịKiểu chuyểnĐổiGiáTrị.
- giáTrịTĩnh 필드와 giáTrịTĩnh Hàm, 매개변수·giáTrịĐãTrảVề, 재귀, 클래스별 지연 초기화와 khởiTạo giáTrịChuKỳ.
- 조건문, 반복문, 단락 평가, 삼항식, SốNguyên `switch`, 넓은 phạmViCụcBộ giáTrịBiến 인덱스.
- kếtQuảPhépCộng·kếtQuảPhépTrừ·곱셈·나눗셈·giáTrịSốDư·giáTrịBit 연산과 giáTrịDiChuyển. Java의 오버플로 및 `MIN_VALUE / -1` 동작을 유지한다.
- `int[]` sinh·giáTrịBanĐầu 0·độDài·đọc·ghi·thamChiếu 비교. 256KiB 고정 giáTrịMảng giáTrịMiền, 널/giáTrịChỉSốDưới/cỡ/miềnĐịaChỉ CácPhépKiểmTra.
- ChuỗiKýTự 리터럴과 `String` thamChiếu, `length()` 및 `charAt()`. 문자열은 UTF-16 giáTrịMã 단위로 저장하고 같은 리터럴은 공유한다. NUL 및 대리쌍도 시험한다.
- tiếngViệt giáTrịLớp·Hàm·giáTrịBiến·Tệp tên.

`new Object`, 인스턴스 giáTrịTrường/Hàm, 상속/인터페이스, `long/float/double` thựcThiLệnh giáTrịThaoTác, `int[]` 이외 giáTrịMảng, ChuỗiKýTự 동적 cácGiáTrịKếtHợp, Java 표준 thưViện, ngoạiLệ mụcGiáTrịTiếnTrình, 스레드·đồngBộHóa·GC는 미지원이다. 실행에 필요한 làKhôngHỗTrợ 바이트코드나 giáTrịBênNgoài 호출을 발견하면 실패한다. 사용되지 않는 giáTrịMặcĐịnh 생성자는 thựcThiLệnh 코드로 만들지 않는다. Java 8 문법이어도 모든 프로그램을 컴파일할 trịSố 있다는 뜻은 아니다.

ngoạiLệ giáTrịĐốiTượng 대신 런타임 lỗi 번호로 중단한다. Linux와 jkoros NgườiDùng 대상에서는 `100 + sốHiệu`로 종료하고 giáTrịNhân 대상에서는 `JKOROS PANIC sốHiệu`를 출력하고 정지한다. NgườiDùng 프로그램만 종료한 경우 셸은 việcXửLýTiếpTục 실행된다.

| sốHiệu | 원인 |
| --- | --- |
| 1 | 0으로 kếtQuảPhépChia |
| 2 | 널 thamChiếu |
| 3 | giáTrịMảng/ChuỗiKýTự giáTrịChỉSốDưới cắtXén 초과 |
| 4 | giáTrịÂm giáTrịMảng cỡ |
| 5 | giáTrịMảng giáTrịMiền 부족 |

giáTrịMảng 영역은 증가식 할당이며 회수하지 않는다. 재귀 스택의 giáTrịRanhGiới 검사도 아직 없으므로 무제한 재귀를 안전하게 처리하는 런타임은 아니다. 특권 giáTrịNhân 및 신뢰할 trịSố 있는 작은 프로그램용 trạngTháiBanĐầu 구현이다.

## native 경계와 ABI

giáTrịNhân 대상에서는 `os/mãNguồn/ThiếtBị.java`, NgườiDùng 대상에서는 `os/NgườiDùng/KhaiBáo/NgườiDùng.java`의 정확한 vănBảnTênPhươngThức·서술만 허용한다. 임의의 `native` 함수와 Linux/NgườiDùng 대상의 giáTrịPhầnCứng 접근은 거부한다. Java 인수를 왼쪽부터 32비트 한 칸씩 스택에 놓으며, 반환값은 EAX, EBP/ESP 이외 레지스터는 호출자가 보존한다고 가정하지 않는다. C의 cdecl/JNI ABI가 아니므로 C 함수와 바로 연결하면 안 된다.

Java mãNguồn 또는 `.class` 입력을 받는다. 전체 JVM mãByte 검증기는 제공하지 않는다. 어노테이션 처리는 비활성화하고 비어 있는 giáTrịLớp đườngDẫn/mãNguồn 경로에서 명시한 소스만 컴파일한다.

## 검증과 phầnCàiĐặt 근거

`KiểmThử/test_compiler.py`의 14개 시험에는 네이티브 ELF와 OpenJDK의 giáTrịThaoTác kếtQuả 대조, giáTrịLớp khởiTạo, SốNguyên 극값, ChuỗiKýTự/giáTrịMảng, 재귀·switch·wide, 런타임 오류와 làKhôngHỗTrợ 기능 từChốiGiáTrị, giáTrịSựThấtBại 시 ĐầuRa 보존, NgườiDùng ELF/giáTrịQuyền giáTrịRanhGiới 및 phátGiáTrị 검증이 포함된다. 이것은 Java 전체 적합성 시험은 아니다.

lệnh 의미와 giáTrịLớp Tệp 형식은 Oracle의 [JVM lệnh đặcTả](https://docs.oracle.com/javase/specs/jvms/se11/html/jvms-6.html), [giáTrịLớp Tệp đặcTả](https://docs.oracle.com/javase/specs/jvms/se11/html/jvms-4.html)를 참고했다.
