# Java 네이티브 compiler

OpenJDK Eigen 소스를 빌드하는 **`--target openjdk-build`**와 Eigen kernel_WAARDE ABI 검사 도구를 추가했다.
이는 공식 javac/C/C++ 도구를 연결하는 별도 경로다. [bouwen 방법·werkelijk_gegevens valideren·kernel_WAARDE 이식 clip](OpenJDK-bron_build_EN-systeemeigen_kernel-이식.md)를 참고한다.

x86 직접 변환과 ARM64 C genereren 후단은 모두 [기계어미리번역.java](자바도구/기계어미리번역.java)로 구현한다. `sh 미리번역.sh`로 직접 실행하며, [기계어미리번역.py](기계어미리번역.py)와 `compiler.py`는 Vorige_item opdracht·API 및 OpenJDK 도구를 위한 호환 진입점이다. Eigen Pi4 후단은 freestanding C를 거쳐 AArch64로 만든다. [arm64.py](arm64.py)는 Vorige_item 경로와 Python 호출을 위한 호환 진입점이다. FUNCTIE_WAARDE·variabele_WAARDE·genereren C 이름의 뜻과 예외는 [Nederlands 명명 LEESMIJ_eb81d7d9](../platforms/rpi4-native/명명/LEESMIJ_eb81d7d9.md)를 참고한다. [ARM64 bouwen·steun_WAARDE clip](../platforms/rpi4-native/LEESMIJ_eb81d7d9.md)에 Uitvoeren_opdracht 조건이 있다. 전체 OpenJDK나 일반 les_WAARDE 실행기는 아니다.

Uitvoeren_opdracht 시 JVM이 필요 없는 x86 32비트 ELF를 만든다. JDK 11 이상으로 실행하는 Java Eigen AOT 후단이며, Java 전체를 새로 구현한 컴파일러는 아니다. Java 문법·toegang_invoer controle_WAARDE·TYPE_WAARDE 검사는 JDK의 `javac`에 맡기고, Java 8 les_WAARDE 파일을 읽어 각 바이트코드를 x86 명령으로 직접 변환한다. C 코드로 우회하거나 바이트코드 해석기를 커널에 넣지 않는다.

```text
Java broncode → javac의 문법·TYPE_WAARDE 검사 → 임시 .class
          → Eigen x86 변환기 → GNU as/ld → 네이티브 ELF32
```

## 준비와 Uitvoeren_opdracht

bouwen host: Linux, Python 3.6 이상, JDK 11 이상(`javac --release 8`), GNU binutils(`as`, `ld`), Make. actueel_item 환경의 OpenJDK 11, Python 3.6, binutils 2.30으로 검증했다. extern_WAARDE Python 패키지와 네트워크 다운로드는 사용하지 않는다.

```sh
cd /home/user/jkoros/compiler
make
./build/계산
echo $?                  # 0이면 예제 tests 성공

python3 compiler.py --target linux --entry 계산.starten \
    -o build/계산 예제/계산.java

make test
```

`linux` 대상은 Linux의 32비트 Uitvoeren_opdracht 호환 기능이 필요하다. `int 0x80`을 차단하는 샌드박스에서는 `Bad system call`이 발생할 nummer 있다. informatie_normaal Linux host 또는 해당 실행을 허용한 tests 환경에서 실행한다. 시험의 비정상 종료를 통과로 처리하지 않는다.

진입점은 `static int starten()` 또는 `static void starten()`처럼 인수가 없어야 한다. `--entry 패키지.les_WAARDE.FUNCTIE_WAARDE`로 선택한다. `int` 반환값은 Linux 프로세스 Einde_app 코드가 되며 셸에는 하위 8비트가 보인다. 일반 `main(String[] args)` Uitvoeren_opdracht 환경이나 표준 I_O 라이브러리는 제공하지 않는다.

`--target kernel`은 machineopstart 코드와 연결할 재배치 ELF 오브젝트를 생성한다.

```sh
cd /home/user/jkoros
python3 compiler/compiler.py --target kernel --entry Kern.starten \
    --export kernel_dispatch=systeemaanroep.Proces_WAARDE_invoer \
    -o os/build/java.o os/broncode/*.java
```

`--target user`는 jkoros 셸에서 실행할 독립 ELF를 생성한다. `gebruikersruimte` 클래스의 제한된 native API는 `int 0x80` 시스템 호출로 연결하며 `mobiel_WAARDE` 클래스의 hardware_WAARDE 직접 접근은 거부한다. gebruikersruimte ELF는 Linux Uitvoeren_opdracht bestand ABI와 다르므로 호스트에서 실행하지 않는다. genereren·register_invoer 방법은 [gebruikersruimte Uitvoeren_opdracht LEESMIJ_eb81d7d9](../os/gebruikersruimte/LEESMIJ_eb81d7d9.md)에 있다. `--export 외부기호=les_WAARDE.FUNCTIE_WAARDE`는 오버로드되지 않은 statisch_WAARDE 함수를 Eigen operand_stack ABI로 노출한다. 커널의 시스템 호출 진입점에 사용한다.

Java 파일은 필요한 클래스들을 한꺼번에 전달한다. tekstuitvoer 옆의 `.s`는 생성된 어셈블리, `.json`은 broncode SHA-256 및 네이티브 symbool↔Java FUNCTIE_WAARDE 대응표다. Nederlands 함수명은 원문과 대응표에 보존하고 ELF 내부에는 충돌 방지용 machine 기호를 쓴다. compileren_bron·조립·Verbinden 중 실패하면 기존 resultaat 파일을 덮어쓰지 않는다.

## steun_WAARDE clip

- `int`, `boolean`, `byte`, `short`, `char`의 32비트 계산 및 TYPE_WAARDE CONVERTEREN_WAARDE.
- statisch_WAARDE 필드와 statisch_WAARDE FUNCTIE_WAARDE, 매개변수·반환값, 재귀, 클래스별 지연 초기화와 initialiseren cyclus_WAARDE.
- 조건문, 반복문, 단락 평가, 삼항식, geheel_getal `switch`, 넓은 lokaal_scope variabele_WAARDE 인덱스.
- 덧셈·뺄셈·곱셈·나눗셈·나머지·bit_WAARDE 연산과 verplaatsen_WAARDE_83b651b8. Java의 오버플로 및 `MIN_VALUE / -1` 동작을 유지한다.
- `int[]` genereren·초기값 0·tijdsduur_WAARDE·Lezen·Schrijven·verwijzen 비교. 256KiB 고정 MATRIX_WAARDE regio_WAARDE, 널/subscript_WAARDE/Grootte/ADRES_regio 검사.
- tekenreeks_WAARDE 리터럴과 `String` verwijzen, `length()` 및 `charAt()`. 문자열은 UTF-16 CODE_WAARDE 단위로 저장하고 같은 리터럴은 공유한다. NUL 및 대리쌍도 시험한다.
- Nederlands les_WAARDE·FUNCTIE_WAARDE·variabele_WAARDE·bestand Naam.

`new Object`, 인스턴스 veldwaarde/FUNCTIE_WAARDE, 상속/인터페이스, `long/float/double` Uitvoeren_opdracht operatie_WAARDE, `int[]` 이외 MATRIX_WAARDE, tekenreeks_WAARDE 동적 결합, Java 표준 bibliotheek, uitzondering Proces_WAARDE_invoer, 스레드·synchroniseren·GC는 미지원이다. 실행에 필요한 미지원 바이트코드나 extern_WAARDE 호출을 발견하면 실패한다. 사용되지 않는 standaardwaarde 생성자는 Uitvoeren_opdracht 코드로 만들지 않는다. Java 8 문법이어도 모든 프로그램을 컴파일할 nummer 있다는 뜻은 아니다.

uitzondering object_WAARDE 대신 런타임 fout 번호로 중단한다. Linux와 jkoros gebruikersruimte 대상에서는 `100 + INDEX`로 종료하고 kernel_WAARDE 대상에서는 `JKOROS PANIC INDEX`를 출력하고 정지한다. gebruikersruimte 프로그램만 종료한 경우 셸은 계속 실행된다.

| INDEX | 원인 |
| --- | --- |
| 1 | 0으로 deling_HR |
| 2 | 널 verwijzen |
| 3 | MATRIX_WAARDE/tekenreeks_WAARDE subscript_WAARDE clip 초과 |
| 4 | 음수 MATRIX_WAARDE Grootte |
| 5 | MATRIX_WAARDE regio_WAARDE 부족 |

MATRIX_WAARDE 영역은 증가식 할당이며 회수하지 않는다. 재귀 스택의 grens_WAARDE 검사도 아직 없으므로 무제한 재귀를 안전하게 처리하는 런타임은 아니다. 특권 kernel_WAARDE 및 신뢰할 nummer 있는 작은 프로그램용 begintoestand 구현이다.

## native 경계와 ABI

kernel_WAARDE 대상에서는 `os/broncode/mobiel_WAARDE.java`, gebruikersruimte 대상에서는 `os/gebruikersruimte/aangifte/gebruikersruimte.java`의 정확한 methode_naam_sms·서술만 허용한다. 임의의 `native` 함수와 Linux/gebruikersruimte 대상의 hardware_WAARDE 접근은 거부한다. Java 인수를 왼쪽부터 32비트 한 칸씩 스택에 놓으며, 반환값은 EAX, EBP/ESP 이외 레지스터는 호출자가 보존한다고 가정하지 않는다. C의 cdecl/JNI ABI가 아니므로 C 함수와 바로 연결하면 안 된다.

Java broncode 또는 `.class` 입력을 받는다. 전체 JVM 바이트코드 검증기는 제공하지 않는다. 어노테이션 처리는 비활성화하고 비어 있는 les_WAARDE pad/broncode 경로에서 명시한 소스만 컴파일한다.

## 검증과 implementatie 근거

`tests/test_compiler.py`의 14개 시험에는 네이티브 ELF와 OpenJDK의 operatie_WAARDE resultaat 대조, les_WAARDE initialiseren, geheel_getal 극값, tekenreeks_WAARDE/MATRIX_WAARDE, 재귀·switch·wide, 런타임 오류와 미지원 기능 weigeren_WAARDE, fout_WAARDE 시 tekstuitvoer 보존, gebruikersruimte ELF/machtiging_WAARDE grens_WAARDE 및 내보내기 검증이 포함된다. 이것은 Java 전체 적합성 시험은 아니다.

opdracht 의미와 les_WAARDE bestand 형식은 Oracle의 [JVM opdracht specificatie](https://docs.oracle.com/javase/specs/jvms/se11/html/jvms-6.html), [les_WAARDE bestand specificatie](https://docs.oracle.com/javase/specs/jvms/se11/html/jvms-4.html)를 참고했다.
