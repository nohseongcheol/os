# Java 네이티브 kompilerare

OpenJDK eget 소스를 빌드하는 **`--target openjdk-build`**와 eget kärna_värde ABI 검사 도구를 추가했다.
이는 공식 javac/C/C++ 도구를 연결하는 별도 경로다. [version_System 방법·verklig_data validera·kärna_värde 이식 klipp](OpenJDK-källa_version_AND-ursprunglig_kärna-이식.md)를 참고한다.

x86 직접 변환과 ARM64 C generera 후단은 모두 [기계어미리번역.java](자바도구/기계어미리번역.java)로 구현한다. `sh 미리번역.sh`로 직접 실행하며, [기계어미리번역.py](기계어미리번역.py)와 `kompilerare.py`는 Föregående_objekt kommando·API 및 OpenJDK 도구를 위한 호환 진입점이다. eget Pi4 후단은 freestanding C를 거쳐 AArch64로 만든다. [arm64.py](arm64.py)는 Föregående_objekt 경로와 Python 호출을 위한 호환 진입점이다. FUNKTION_värde·variabel_värde·generera C 이름의 뜻과 예외는 [Svenska 명명 VIKTIGT_eb81d7d9](../platforms/rpi4-native/명명/VIKTIGT_eb81d7d9.md)를 참고한다. [ARM64 version_System·stöd_värde klipp](../platforms/rpi4-native/VIKTIGT_eb81d7d9.md)에 köra_kommando 조건이 있다. 전체 OpenJDK나 일반 Kurs_värde 실행기는 아니다.

köra_kommando 시 JVM이 필요 없는 x86 32비트 ELF를 만든다. JDK 11 이상으로 실행하는 Java eget AOT 후단이며, Java 전체를 새로 구현한 컴파일러는 아니다. Java 문법·ansluta_post kontroll_värde·Typ_värde 검사는 JDK의 `javac`에 맡기고, Java 8 Kurs_värde 파일을 읽어 각 바이트코드를 x86 명령으로 직접 변환한다. C 코드로 우회하거나 바이트코드 해석기를 커널에 넣지 않는다.

```text
Java källfil → javac의 문법·Typ_värde 검사 → 임시 .class
          → eget x86 변환기 → GNU as/ld → 네이티브 ELF32
```

## 준비와 köra_kommando

version_System värd: Linux, Python 3.6 이상, JDK 11 이상(`javac --release 8`), GNU binutils(`as`, `ld`), Make. aktuellt_objekt 환경의 OpenJDK 11, Python 3.6, binutils 2.30으로 검증했다. extern_värde Python 패키지와 네트워크 다운로드는 사용하지 않는다.

```sh
cd /home/user/jkoros/compiler
make
./build/계산
echo $?                  # 0이면 예제 tester 성공

python3 kompilerare.py --target linux --entry 계산.Kör \
    -o build/계산 예제/계산.java

make test
```

`linux` 대상은 Linux의 32비트 köra_kommando 호환 기능이 필요하다. `int 0x80`을 차단하는 샌드박스에서는 `Bad system call`이 발생할 nummer 있다. informationsteknik_normal Linux värd 또는 해당 실행을 허용한 tester 환경에서 실행한다. 시험의 비정상 종료를 통과로 처리하지 않는다.

진입점은 `static int Kör()` 또는 `static void Kör()`처럼 인수가 없어야 한다. `--entry 패키지.Kurs_värde.FUNKTION_värde`로 선택한다. `int` 반환값은 Linux 프로세스 Utgång_app 코드가 되며 셸에는 하위 8비트가 보인다. 일반 `main(String[] args)` köra_kommando 환경이나 표준 indata_utleverans 라이브러리는 제공하지 않는다.

`--target kernel`은 maskinstart 코드와 연결할 재배치 ELF 오브젝트를 생성한다.

```sh
cd /home/user/jkoros
python3 compiler/kompilerare.py --target kernel --entry kärna.Kör \
    --export kernel_dispatch=systemanrop.Process_värde_post \
    -o os/build/java.o os/källfil/*.java
```

`--target user`는 jkoros 셸에서 실행할 독립 ELF를 생성한다. `användarutrymme` 클래스의 제한된 native API는 `int 0x80` 시스템 호출로 연결하며 `enhet_värde` 클래스의 maskinvara_värde 직접 접근은 거부한다. användarutrymme ELF는 Linux köra_kommando filnamn ABI와 다르므로 호스트에서 실행하지 않는다. generera·register_post 방법은 [användarutrymme köra_kommando VIKTIGT_eb81d7d9](../os/användarutrymme/VIKTIGT_eb81d7d9.md)에 있다. `--export 외부기호=Kurs_värde.FUNKTION_värde`는 오버로드되지 않은 statisk_värde 함수를 eget operand_Stack ABI로 노출한다. 커널의 시스템 호출 진입점에 사용한다.

Java 파일은 필요한 클래스들을 한꺼번에 전달한다. utmatningsposition 옆의 `.s`는 생성된 어셈블리, `.json`은 källfil SHA-256 및 네이티브 symbol↔Java FUNKTION_värde 대응표다. Svenska 함수명은 원문과 대응표에 보존하고 ELF 내부에는 충돌 방지용 dator 기호를 쓴다. kompilera_källa·assemblera_värde·Anslut 중 실패하면 기존 RESULTAT 파일을 덮어쓰지 않는다.

## stöd_värde klipp

- `int`, `boolean`, `byte`, `short`, `char`의 32비트 계산 및 Typ_värde KONVERTERA_värde.
- statisk_värde 필드와 statisk_värde FUNKTION_värde, 매개변수·반환값, 재귀, 클래스별 지연 초기화와 starta cykel_värde.
- 조건문, 반복문, 단락 평가, 삼항식, heltal `switch`, 넓은 lokal_scope variabel_värde 인덱스.
- 덧셈·뺄셈·곱셈·나눗셈·나머지·bit_värde 연산과 flytta_värde. Java의 오버플로 및 `MIN_VALUE / -1` 동작을 유지한다.
- `int[]` generera·초기값 0·längd_värde·Läs·Skriv·referens 비교. 256KiB 고정 MATRIS_värde område_värde_0e9a97ab, 널/nedsänkt_text_värde/Storlek/ADRESS_område 검사.
- sträng_värde 리터럴과 `String` referens, `length()` 및 `charAt()`. 문자열은 UTF-16 KOD_värde 단위로 저장하고 같은 리터럴은 공유한다. NUL 및 대리쌍도 시험한다.
- Svenska Kurs_värde·FUNKTION_värde·variabel_värde·filnamn Namn.

`new Object`, 인스턴스 fältvärde/FUNKTION_värde, 상속/인터페이스, `long/float/double` köra_kommando åtgärd_värde, `int[]` 이외 MATRIS_värde, sträng_värde 동적 결합, Java 표준 bibliotek, fel_31f743d2 Process_värde_post, 스레드·synka·GC는 미지원이다. 실행에 필요한 미지원 바이트코드나 extern_värde 호출을 발견하면 실패한다. 사용되지 않는 standardvärde 생성자는 köra_kommando 코드로 만들지 않는다. Java 8 문법이어도 모든 프로그램을 컴파일할 nummer 있다는 뜻은 아니다.

fel_31f743d2 objekt_värde 대신 런타임 fel 번호로 중단한다. Linux와 jkoros användarutrymme 대상에서는 `100 + INDEX`로 종료하고 kärna_värde 대상에서는 `JKOROS PANIC INDEX`를 출력하고 정지한다. användarutrymme 프로그램만 종료한 경우 셸은 계속 실행된다.

| INDEX | 원인 |
| --- | --- |
| 1 | 0으로 Division_KR |
| 2 | 널 referens |
| 3 | MATRIS_värde/sträng_värde nedsänkt_text_värde klipp 초과 |
| 4 | 음수 MATRIS_värde Storlek |
| 5 | MATRIS_värde område_värde_0e9a97ab 부족 |

MATRIS_värde 영역은 증가식 할당이며 회수하지 않는다. 재귀 스택의 gräns_värde 검사도 아직 없으므로 무제한 재귀를 안전하게 처리하는 런타임은 아니다. 특권 kärna_värde 및 신뢰할 nummer 있는 작은 프로그램용 starttillstånd 구현이다.

## native 경계와 ABI

kärna_värde 대상에서는 `os/källfil/enhet_värde.java`, användarutrymme 대상에서는 `os/användarutrymme/deklaration/användarutrymme.java`의 정확한 metod_namn_SMS·서술만 허용한다. 임의의 `native` 함수와 Linux/användarutrymme 대상의 maskinvara_värde 접근은 거부한다. Java 인수를 왼쪽부터 32비트 한 칸씩 스택에 놓으며, 반환값은 EAX, EBP/ESP 이외 레지스터는 호출자가 보존한다고 가정하지 않는다. C의 cdecl/JNI ABI가 아니므로 C 함수와 바로 연결하면 안 된다.

Java källfil 또는 `.class` 입력을 받는다. 전체 JVM 바이트코드 검증기는 제공하지 않는다. 어노테이션 처리는 비활성화하고 비어 있는 Kurs_värde sökväg_2/källfil 경로에서 명시한 소스만 컴파일한다.

## 검증과 implementation 근거

`tester/test_compiler.py`의 14개 시험에는 네이티브 ELF와 OpenJDK의 åtgärd_värde RESULTAT 대조, Kurs_värde starta, heltal 극값, sträng_värde/MATRIS_värde, 재귀·switch·wide, 런타임 오류와 미지원 기능 avvisa_värde, fel_värde 시 utmatningsposition 보존, användarutrymme ELF/behörighet_värde gräns_värde 및 내보내기 검증이 포함된다. 이것은 Java 전체 적합성 시험은 아니다.

kommando 의미와 Kurs_värde filnamn 형식은 Oracle의 [JVM kommando 명세](https://docs.oracle.com/javase/specs/jvms/se11/html/jvms-6.html), [Kurs_värde filnamn 명세](https://docs.oracle.com/javase/specs/jvms/se11/html/jvms-4.html)를 참고했다.
