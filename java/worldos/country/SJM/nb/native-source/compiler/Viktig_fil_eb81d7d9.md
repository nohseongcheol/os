# Java 네이티브 kompilator

OpenJDK eget 소스를 빌드하는 **`--target openjdk-build`**와 eget kjerne_VERDI ABI 검사 도구를 추가했다.
이는 공식 javac/C/C++ 도구를 연결하는 별도 경로다. [bygg_System 방법·faktisk_data bekrefte_5fb2b747·kjerne_VERDI 이식 klippe](OpenJDK-kilde_bygg_OG-opprinnelig_kjerne-이식.md)를 참고한다.

x86 직접 변환과 ARM64 C generere 후단은 모두 [기계어미리번역.java](자바도구/기계어미리번역.java)로 구현한다. `sh 미리번역.sh`로 직접 실행하며, [기계어미리번역.py](기계어미리번역.py)와 `kompilator.py`는 Forrige_vare Kommando·API 및 OpenJDK 도구를 위한 호환 진입점이다. eget Pi4 후단은 freestanding C를 거쳐 AArch64로 만든다. [arm64.py](arm64.py)는 Forrige_vare 경로와 Python 호출을 위한 호환 진입점이다. FUNKSJON_VERDI·variabel_VERDI·generere C 이름의 뜻과 예외는 [norsk 명명 Viktig_fil_eb81d7d9](../platforms/rpi4-native/명명/Viktig_fil_eb81d7d9.md)를 참고한다. [ARM64 bygg_System·støtte_VERDI klippe](../platforms/rpi4-native/Viktig_fil_eb81d7d9.md)에 Utfør_kommando 조건이 있다. 전체 OpenJDK나 일반 time_VERDI 실행기는 아니다.

Utfør_kommando 시 JVM이 필요 없는 x86 32비트 ELF를 만든다. JDK 11 이상으로 실행하는 Java eget AOT 후단이며, Java 전체를 새로 구현한 컴파일러는 아니다. Java 문법·tilgang_oppføring kontroll_VERDI·Type_VERDI 검사는 JDK의 `javac`에 맡기고, Java 8 time_VERDI 파일을 읽어 각 바이트코드를 x86 명령으로 직접 변환한다. C 코드로 우회하거나 바이트코드 해석기를 커널에 넣지 않는다.

```text
Java KILDE → javac의 문법·Type_VERDI 검사 → 임시 .class
          → eget x86 변환기 → GNU as/ld → 네이티브 ELF32
```

## 준비와 Utfør_kommando

bygg_System vert: Linux, Python 3.6 이상, JDK 11 이상(`javac --release 8`), GNU binutils(`as`, `ld`), Make. betalt_vare 환경의 OpenJDK 11, Python 3.6, binutils 2.30으로 검증했다. ekstern_VERDI Python 패키지와 네트워크 다운로드는 사용하지 않는다.

```sh
cd /home/user/jkoros/compiler
make
./build/계산
echo $?                  # 0이면 예제 시험 성공

python3 kompilator.py --target linux --entry 계산.Kjør_2 \
    -o build/계산 예제/계산.java

make test
```

`linux` 대상은 Linux의 32비트 Utfør_kommando 호환 기능이 필요하다. `int 0x80`을 차단하는 샌드박스에서는 `Bad system call`이 발생할 nummer 있다. informasjonssystemer_normal Linux vert 또는 해당 실행을 허용한 시험 환경에서 실행한다. 시험의 비정상 종료를 통과로 처리하지 않는다.

진입점은 `static int Kjør_2()` 또는 `static void Kjør_2()`처럼 인수가 없어야 한다. `--entry 패키지.time_VERDI.FUNKSJON_VERDI`로 선택한다. `int` 반환값은 Linux 프로세스 Utgang_app 코드가 되며 셸에는 하위 8비트가 보인다. 일반 `main(String[] args)` Utfør_kommando 환경이나 표준 I_U 라이브러리는 제공하지 않는다.

`--target kernel`은 부팅 코드와 연결할 재배치 ELF 오브젝트를 생성한다.

```sh
cd /home/user/jkoros
python3 compiler/kompilator.py --target kernel --entry kjerne.Kjør_2 \
    --export kernel_dispatch=체계호출.Prosess_VERDI_oppføring \
    -o os/build/java.o os/KILDE/*.java
```

`--target user`는 jkoros 셸에서 실행할 독립 ELF를 생성한다. `bruker` 클래스의 제한된 native API는 `int 0x80` 시스템 호출로 연결하며 `enhet_VERDI` 클래스의 maskinvare_VERDI 직접 접근은 거부한다. bruker ELF는 Linux Utfør_kommando Fil ABI와 다르므로 호스트에서 실행하지 않는다. generere·register_oppføring 방법은 [bruker Utfør_kommando Viktig_fil_eb81d7d9](../os/bruker/Viktig_fil_eb81d7d9.md)에 있다. `--export 외부기호=time_VERDI.FUNKSJON_VERDI`는 오버로드되지 않은 statisk_VERDI 함수를 eget operand_stakk ABI로 노출한다. 커널의 시스템 호출 진입점에 사용한다.

Java 파일은 필요한 클래스들을 한꺼번에 전달한다. Utgang 옆의 `.s`는 생성된 어셈블리, `.json`은 KILDE SHA-256 및 네이티브 symbol↔Java FUNKSJON_VERDI 대응표다. norsk 함수명은 원문과 대응표에 보존하고 ELF 내부에는 충돌 방지용 maskin 기호를 쓴다. kompilere_kilde·조립·Koble_til 중 실패하면 기존 KR 파일을 덮어쓰지 않는다.

## støtte_VERDI klippe

- `int`, `boolean`, `byte`, `short`, `char`의 32비트 계산 및 Type_VERDI KONVERTER_VERDI.
- statisk_VERDI 필드와 statisk_VERDI FUNKSJON_VERDI, 매개변수·반환값, 재귀, 클래스별 지연 초기화와 starte Krets_VERDI.
- 조건문, 반복문, 단락 평가, 삼항식, heltall `switch`, 넓은 lokal_Omfang variabel_VERDI 인덱스.
- 덧셈·뺄셈·곱셈·나눗셈·나머지·bit_VERDI 연산과 flytte_VERDI_83b651b8. Java의 오버플로 및 `MIN_VALUE / -1` 동작을 유지한다.
- `int[]` generere·초기값 0·lengde_VERDI·Les·Skriv·referere 비교. 256KiB 고정 MATRISE_VERDI område_VERDI_0e9a97ab, 널/senket_skrift_VERDI/Størrelse/e_post_område 검사.
- streng_VERDI 리터럴과 `String` referere, `length()` 및 `charAt()`. 문자열은 UTF-16 KODE_VERDI 단위로 저장하고 같은 리터럴은 공유한다. NUL 및 대리쌍도 시험한다.
- norsk time_VERDI·FUNKSJON_VERDI·variabel_VERDI·Fil Navn.

`new Object`, 인스턴스 feltverdi/FUNKSJON_VERDI, 상속/인터페이스, `long/float/double` Utfør_kommando operasjon_VERDI, `int[]` 이외 MATRISE_VERDI, streng_VERDI 동적 결합, Java 표준 bibliotek, unntak Prosess_VERDI_oppføring, 스레드·synkronisere·GC는 미지원이다. 실행에 필요한 미지원 바이트코드나 ekstern_VERDI 호출을 발견하면 실패한다. 사용되지 않는 standardverdi 생성자는 Utfør_kommando 코드로 만들지 않는다. Java 8 문법이어도 모든 프로그램을 컴파일할 nummer 있다는 뜻은 아니다.

unntak objekt_VERDI 대신 런타임 feil 번호로 중단한다. Linux와 jkoros bruker 대상에서는 `100 + INDEKS`로 종료하고 kjerne_VERDI 대상에서는 `JKOROS PANIC INDEKS`를 출력하고 정지한다. bruker 프로그램만 종료한 경우 셸은 계속 실행된다.

| INDEKS | 원인 |
| --- | --- |
| 1 | 0으로 Divisjon_KR |
| 2 | 널 referere |
| 3 | MATRISE_VERDI/streng_VERDI senket_skrift_VERDI klippe 초과 |
| 4 | 음수 MATRISE_VERDI Størrelse |
| 5 | MATRISE_VERDI område_VERDI_0e9a97ab 부족 |

MATRISE_VERDI 영역은 증가식 할당이며 회수하지 않는다. 재귀 스택의 grense_VERDI 검사도 아직 없으므로 무제한 재귀를 안전하게 처리하는 런타임은 아니다. 특권 kjerne_VERDI 및 신뢰할 nummer 있는 작은 프로그램용 opprinnelig_tilstand 구현이다.

## native 경계와 ABI

kjerne_VERDI 대상에서는 `os/KILDE/enhet_VERDI.java`, bruker 대상에서는 `os/bruker/erklæring/bruker.java`의 정확한 metode_navn_SMS·서술만 허용한다. 임의의 `native` 함수와 Linux/bruker 대상의 maskinvare_VERDI 접근은 거부한다. Java 인수를 왼쪽부터 32비트 한 칸씩 스택에 놓으며, 반환값은 EAX, EBP/ESP 이외 레지스터는 호출자가 보존한다고 가정하지 않는다. C의 cdecl/JNI ABI가 아니므로 C 함수와 바로 연결하면 안 된다.

Java KILDE 또는 `.class` 입력을 받는다. 전체 JVM 바이트코드 검증기는 제공하지 않는다. 어노테이션 처리는 비활성화하고 비어 있는 time_VERDI Sti/KILDE 경로에서 명시한 소스만 컴파일한다.

## 검증과 구현 근거

`시험/test_compiler.py`의 14개 시험에는 네이티브 ELF와 OpenJDK의 operasjon_VERDI KR 대조, time_VERDI starte, heltall 극값, streng_VERDI/MATRISE_VERDI, 재귀·switch·wide, 런타임 오류와 미지원 기능 avvise_VERDI, feil_VERDI 시 Utgang 보존, bruker ELF/tillatelse_VERDI grense_VERDI 및 내보내기 검증이 포함된다. 이것은 Java 전체 적합성 시험은 아니다.

Kommando 의미와 time_VERDI Fil 형식은 Oracle의 [JVM Kommando 명세](https://docs.oracle.com/javase/specs/jvms/se11/html/jvms-6.html), [time_VERDI Fil 명세](https://docs.oracle.com/javase/specs/jvms/se11/html/jvms-4.html)를 참고했다.
