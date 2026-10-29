# Java 네이티브 컴파일러

OpenJDK 자체 소스를 빌드하는 **`--target openjdk-build`**와 자체 aaluude_njaru ABI 검사 도구를 추가했다.
이는 공식 javac/C/C++ 도구를 연결하는 별도 경로다. [tafde_yuɓɓo 방법·laatii_keɓe 검증·aaluude_njaru 이식 kilip](OpenJDK-소스빌드와-자체커널-이식.md)를 참고한다.

x86 직접 변환과 ARM64 C 생성 후단은 모두 [기계어미리번역.java](자바도구/기계어미리번역.java)로 구현한다. `sh 미리번역.sh`로 직접 실행하며, [기계어미리번역.py](기계어미리번역.py)와 `컴파일러.py`는 이전 ginol·API 및 OpenJDK 도구를 위한 호환 진입점이다. 자체 Pi4 후단은 freestanding C를 거쳐 AArch64로 만든다. [arm64.py](arm64.py)는 이전 경로와 Python 호출을 위한 호환 진입점이다. juɓɓol_njaru·변수·생성 C 이름의 뜻과 예외는 [한국어 명명 TARƊOO_eb81d7d9](../platforms/rpi4-native/명명/TARƊOO_eb81d7d9.md)를 참고한다. [ARM64 tafde_yuɓɓo·ballital_njaru kilip](../platforms/rpi4-native/TARƊOO_eb81d7d9.md)에 실행 조건이 있다. 전체 OpenJDK나 일반 fedde_njaru 실행기는 아니다.

실행 시 JVM이 필요 없는 x86 32비트 ELF를 만든다. JDK 11 이상으로 실행하는 Java 자체 AOT 후단이며, Java 전체를 새로 구현한 컴파일러는 아니다. Java 문법·naatde_naatnugol yuurnitorde_njaru·형 검사는 JDK의 `javac`에 맡기고, Java 8 fedde_njaru 파일을 읽어 각 바이트코드를 x86 명령으로 직접 변환한다. C 코드로 우회하거나 바이트코드 해석기를 커널에 넣지 않는다.

```text
Java sewnde → javac의 문법·형 검사 → 임시 .class
          → 자체 x86 변환기 → GNU as/ld → 네이티브 ELF32
```

## 준비와 실행

tafde_yuɓɓo njaatigi: Linux, Python 3.6 이상, JDK 11 이상(`javac --release 8`), GNU binutils(`as`, `ld`), Make. 현재 환경의 OpenJDK 11, Python 3.6, binutils 2.30으로 검증했다. 외부 Python 패키지와 네트워크 다운로드는 사용하지 않는다.

```sh
cd /home/user/jkoros/compiler
make
./build/계산
echo $?                  # 0이면 예제 시험 성공

python3 컴파일러.py --target linux --entry 계산.huutoraade \
    -o build/계산 예제/계산.java

make test
```

`linux` 대상은 Linux의 32비트 실행 호환 기능이 필요하다. `int 0x80`을 차단하는 샌드박스에서는 `Bad system call`이 발생할 수 있다. 정상 Linux njaatigi 또는 해당 실행을 허용한 시험 환경에서 실행한다. 시험의 비정상 종료를 통과로 처리하지 않는다.

진입점은 `static int huutoraade()` 또는 `static void huutoraade()`처럼 인수가 없어야 한다. `--entry 패키지.fedde_njaru.juɓɓol_njaru`로 선택한다. `int` 반환값은 Linux 프로세스 yaltude_tafirde 코드가 되며 셸에는 하위 8비트가 보인다. 일반 `main(String[] args)` 실행 환경이나 표준 I_O 라이브러리는 제공하지 않는다.

`--target kernel`은 부팅 코드와 연결할 재배치 ELF 오브젝트를 생성한다.

```sh
cd /home/user/jkoros
python3 compiler/컴파일러.py --target kernel --entry aaluude.huutoraade \
    --export kernel_dispatch=체계호출.Yuɓɓo_golle_njaru_naatnugol \
    -o os/build/java.o os/sewnde/*.java
```

`--target user`는 jkoros 셸에서 실행할 독립 ELF를 생성한다. `kuutoro` 클래스의 제한된 native API는 `int 0x80` 시스템 호출로 연결하며 `kaɓirgal_njaru` 클래스의 하드웨어 직접 접근은 거부한다. kuutoro ELF는 Linux 실행 fiilde ABI와 다르므로 호스트에서 실행하지 않는다. 생성·등록 방법은 [kuutoro 실행 TARƊOO_eb81d7d9](../os/kuutoro/TARƊOO_eb81d7d9.md)에 있다. `--export 외부기호=fedde_njaru.juɓɓol_njaru`는 오버로드되지 않은 ñiiɓ_njaru 함수를 자체 스택 ABI로 노출한다. 커널의 시스템 호출 진입점에 사용한다.

Java 파일은 필요한 클래스들을 한꺼번에 전달한다. 출력 옆의 `.s`는 생성된 어셈블리, `.json`은 sewnde SHA-256 및 네이티브 기호↔Java juɓɓol_njaru 대응표다. 한국어 함수명은 원문과 대응표에 보존하고 ELF 내부에는 충돌 방지용 기계 기호를 쓴다. tafde_sewnde·조립·seŋaade 중 실패하면 기존 결과 파일을 덮어쓰지 않는다.

## ballital_njaru kilip

- `int`, `boolean`, `byte`, `short`, `char`의 32비트 계산 및 형 변환.
- ñiiɓ_njaru 필드와 ñiiɓ_njaru juɓɓol_njaru, 매개변수·반환값, 재귀, 클래스별 지연 초기화와 ɓamtinde Yiildu_njaru.
- 조건문, 반복문, 단락 평가, 삼항식, 정수 `switch`, 넓은 nokkuwal_njaajeendi 변수 인덱스.
- 덧셈·뺄셈·곱셈·나눗셈·나머지·bitere_njaru 연산과 dirtinde_njaru. Java의 오버플로 및 `MIN_VALUE / -1` 동작을 유지한다.
- `int[]` 생성·초기값 0·njuuteendi_njaru·읽기·winndude·참조 비교. 256KiB 고정 배열 영역, 널/limtoore_sakkiinde_njaru/waylude_etannde/공간 검사.
- ɓoggol_njaru 리터럴과 `String` 참조, `length()` 및 `charAt()`. 문자열은 UTF-16 코드 단위로 저장하고 같은 리터럴은 공유한다. NUL 및 대리쌍도 시험한다.
- 한국어 fedde_njaru·juɓɓol_njaru·변수·fiilde innde.

`new Object`, 인스턴스 suudu_njaru/juɓɓol_njaru, 상속/인터페이스, `long/float/double` 실행 hiisoore_njaru, `int[]` 이외 배열, ɓoggol_njaru 동적 결합, Java 표준 defterdu, 예외 Yuɓɓo_golle_njaru_naatnugol, 스레드·sanngoɗinde·GC는 미지원이다. 실행에 필요한 미지원 바이트코드나 외부 호출을 발견하면 실패한다. 사용되지 않는 lasli_njaru 생성자는 실행 코드로 만들지 않는다. Java 8 문법이어도 모든 프로그램을 컴파일할 수 있다는 뜻은 아니다.

예외 huunde_njaru 대신 런타임 juumre 번호로 중단한다. Linux와 jkoros kuutoro 대상에서는 `100 + joopirdu`로 종료하고 aaluude_njaru 대상에서는 `JKOROS PANIC joopirdu`를 출력하고 정지한다. kuutoro 프로그램만 종료한 경우 셸은 계속 실행된다.

| joopirdu | 원인 |
| --- | --- |
| 1 | 0으로 나눔 |
| 2 | 널 참조 |
| 3 | 배열/ɓoggol_njaru limtoore_sakkiinde_njaru kilip 초과 |
| 4 | 음수 배열 waylude_etannde |
| 5 | 배열 영역 부족 |

배열 영역은 증가식 할당이며 회수하지 않는다. 재귀 스택의 경계 검사도 아직 없으므로 무제한 재귀를 안전하게 처리하는 런타임은 아니다. 특권 aaluude_njaru 및 신뢰할 수 있는 작은 프로그램용 초기 구현이다.

## native 경계와 ABI

aaluude_njaru 대상에서는 `os/sewnde/kaɓirgal_njaru.java`, kuutoro 대상에서는 `os/kuutoro/선언/kuutoro.java`의 정확한 함수명·서술만 허용한다. 임의의 `native` 함수와 Linux/kuutoro 대상의 하드웨어 접근은 거부한다. Java 인수를 왼쪽부터 32비트 한 칸씩 스택에 놓으며, 반환값은 EAX, EBP/ESP 이외 레지스터는 호출자가 보존한다고 가정하지 않는다. C의 cdecl/JNI ABI가 아니므로 C 함수와 바로 연결하면 안 된다.

Java sewnde 또는 `.class` 입력을 받는다. 전체 JVM 바이트코드 검증기는 제공하지 않는다. 어노테이션 처리는 비활성화하고 비어 있는 fedde_njaru laawol/sewnde 경로에서 명시한 소스만 컴파일한다.

## 검증과 구현 근거

`시험/test_compiler.py`의 14개 시험에는 네이티브 ELF와 OpenJDK의 hiisoore_njaru 결과 대조, fedde_njaru ɓamtinde, 정수 극값, ɓoggol_njaru/배열, 재귀·switch·wide, 런타임 오류와 미지원 기능 거부, ella_njaru 시 출력 보존, kuutoro ELF/권한 경계 및 내보내기 검증이 포함된다. 이것은 Java 전체 적합성 시험은 아니다.

ginol 의미와 fedde_njaru fiilde 형식은 Oracle의 [JVM ginol 명세](https://docs.oracle.com/javase/specs/jvms/se11/html/jvms-6.html), [fedde_njaru fiilde 명세](https://docs.oracle.com/javase/specs/jvms/se11/html/jvms-4.html)를 참고했다.
