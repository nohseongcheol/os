# Java 네이티브 컴파일러

OpenJDK 자체 소스를 빌드하는 **`--target openjdk-build`**와 자체 eithne_VALUE ABI 검사 도구를 추가했다.
이는 공식 javac/C/C++ 도구를 연결하는 별도 경로다. [tóg_córas 방법·iarbhír_sonraí bailíochtaigh·eithne_VALUE 이식 gearrthóg](OpenJDK-foinse_tóg_AND-자체커널-이식.md)를 참고한다.

x86 직접 변환과 ARM64 C giniúint 후단은 모두 [기계어미리번역.java](자바도구/기계어미리번역.java)로 구현한다. `sh 미리번역.sh`로 직접 실행하며, [기계어미리번역.py](기계어미리번역.py)와 `컴파일러.py`는 이전 Ordú·API 및 OpenJDK 도구를 위한 호환 진입점이다. 자체 Pi4 후단은 freestanding C를 거쳐 AArch64로 만든다. [arm64.py](arm64.py)는 이전 경로와 Python 호출을 위한 호환 진입점이다. feidhm_VALUE·변수·giniúint C 이름의 뜻과 예외는 [Gaeilge 명명 LÉIGHMÉ_eb81d7d9](../platforms/rpi4-native/명명/LÉIGHMÉ_eb81d7d9.md)를 참고한다. [ARM64 tóg_córas·Tacaíocht_VALUE gearrthóg](../platforms/rpi4-native/LÉIGHMÉ_eb81d7d9.md)에 Rith_ordú 조건이 있다. 전체 OpenJDK나 일반 aicme_VALUE 실행기는 아니다.

Rith_ordú 시 JVM이 필요 없는 x86 32비트 ELF를 만든다. JDK 11 이상으로 실행하는 Java 자체 AOT 후단이며, Java 전체를 새로 구현한 컴파일러는 아니다. Java 문법·rochtain_iontráil rialú_VALUE·TYPE_VALUE 검사는 JDK의 `javac`에 맡기고, Java 8 aicme_VALUE 파일을 읽어 각 바이트코드를 x86 명령으로 직접 변환한다. C 코드로 우회하거나 바이트코드 해석기를 커널에 넣지 않는다.

```text
Java FOINSE → javac의 문법·TYPE_VALUE 검사 → 임시 .class
          → 자체 x86 변환기 → GNU as/ld → 네이티브 ELF32
```

## 준비와 Rith_ordú

tóg_córas óstach: Linux, Python 3.6 이상, JDK 11 이상(`javac --release 8`), GNU binutils(`as`, `ld`), Make. 현재 환경의 OpenJDK 11, Python 3.6, binutils 2.30으로 검증했다. 외부 Python 패키지와 네트워크 다운로드는 사용하지 않는다.

```sh
cd /home/user/jkoros/compiler
make
./build/계산
echo $?                  # 0이면 예제 시험 성공

python3 컴파일러.py --target linux --entry 계산.Rith_2 \
    -o build/계산 예제/계산.java

make test
```

`linux` 대상은 Linux의 32비트 Rith_ordú 호환 기능이 필요하다. `int 0x80`을 차단하는 샌드박스에서는 `Bad system call`이 발생할 수 있다. 정상 Linux óstach 또는 해당 실행을 허용한 시험 환경에서 실행한다. 시험의 비정상 종료를 통과로 처리하지 않는다.

진입점은 `static int Rith_2()` 또는 `static void Rith_2()`처럼 인수가 없어야 한다. `--entry 패키지.aicme_VALUE.feidhm_VALUE`로 선택한다. `int` 반환값은 Linux 프로세스 scoir_clár 코드가 되며 셸에는 하위 8비트가 보인다. 일반 `main(String[] args)` Rith_ordú 환경이나 표준 I_O 라이브러리는 제공하지 않는다.

`--target kernel`은 부팅 코드와 연결할 재배치 ELF 오브젝트를 생성한다.

```sh
cd /home/user/jkoros
python3 compiler/컴파일러.py --target kernel --entry eithne.Rith_2 \
    --export kernel_dispatch=체계호출.Próiseas_VALUE_iontráil \
    -o os/build/java.o os/FOINSE/*.java
```

`--target user`는 jkoros 셸에서 실행할 독립 ELF를 생성한다. `úsáideoir` 클래스의 제한된 native API는 `int 0x80` 시스템 호출로 연결하며 `gléas_VALUE` 클래스의 하드웨어 직접 접근은 거부한다. úsáideoir ELF는 Linux Rith_ordú Comhad ABI와 다르므로 호스트에서 실행하지 않는다. giniúint·cláraigh_iontráil 방법은 [úsáideoir Rith_ordú LÉIGHMÉ_eb81d7d9](../os/úsáideoir/LÉIGHMÉ_eb81d7d9.md)에 있다. `--export 외부기호=aicme_VALUE.feidhm_VALUE`는 오버로드되지 않은 statach_VALUE 함수를 자체 스택 ABI로 노출한다. 커널의 시스템 호출 진입점에 사용한다.

Java 파일은 필요한 클래스들을 한꺼번에 전달한다. Aschur 옆의 `.s`는 생성된 어셈블리, `.json`은 FOINSE SHA-256 및 네이티브 siombail↔Java feidhm_VALUE 대응표다. Gaeilge 함수명은 원문과 대응표에 보존하고 ELF 내부에는 충돌 방지용 meaisín 기호를 쓴다. tóg_foinse·조립·Nasc 중 실패하면 기존 tomhas 파일을 덮어쓰지 않는다.

## Tacaíocht_VALUE gearrthóg

- `int`, `boolean`, `byte`, `short`, `char`의 32비트 계산 및 TYPE_VALUE CONVERT_VALUE.
- statach_VALUE 필드와 statach_VALUE feidhm_VALUE, 매개변수·반환값, 재귀, 클래스별 지연 초기화와 túsaigh Timthriall_VALUE.
- 조건문, 반복문, 단락 평가, 삼항식, slánuimhir `switch`, 넓은 logánta_scóip 변수 인덱스.
- 덧셈·뺄셈·곱셈·나눗셈·나머지·giotán_VALUE 연산과 bog_VALUE. Java의 오버플로 및 `MIN_VALUE / -1` 동작을 유지한다.
- `int[]` giniúint·초기값 0·fad_VALUE·Léigh·Scríobh·Leabhair_thagartha 비교. 256KiB 고정 ARRAY_VALUE 영역, 널/foscript_VALUE/Méid/공간 검사.
- teaghrán_VALUE 리터럴과 `String` Leabhair_thagartha, `length()` 및 `charAt()`. 문자열은 UTF-16 CODE_VALUE 단위로 저장하고 같은 리터럴은 공유한다. NUL 및 대리쌍도 시험한다.
- Gaeilge aicme_VALUE·feidhm_VALUE·변수·Comhad Ainm.

`new Object`, 인스턴스 réimse_VALUE/feidhm_VALUE, 상속/인터페이스, `long/float/double` Rith_ordú oibríocht_VALUE, `int[]` 이외 ARRAY_VALUE, teaghrán_VALUE 동적 결합, Java 표준 leabharlann, eisceacht Próiseas_VALUE_iontráil, 스레드·sioncronaigh·GC는 미지원이다. 실행에 필요한 미지원 바이트코드나 외부 호출을 발견하면 실패한다. 사용되지 않는 luach_réamhshocraithe 생성자는 Rith_ordú 코드로 만들지 않는다. Java 8 문법이어도 모든 프로그램을 컴파일할 수 있다는 뜻은 아니다.

eisceacht oibiacht_VALUE 대신 런타임 ERREÁID 번호로 중단한다. Linux와 jkoros úsáideoir 대상에서는 `100 + INDEX`로 종료하고 eithne_VALUE 대상에서는 `JKOROS PANIC INDEX`를 출력하고 정지한다. úsáideoir 프로그램만 종료한 경우 셸은 계속 실행된다.

| INDEX | 원인 |
| --- | --- |
| 1 | 0으로 roinnt_tomhas |
| 2 | 널 Leabhair_thagartha |
| 3 | ARRAY_VALUE/teaghrán_VALUE foscript_VALUE gearrthóg 초과 |
| 4 | 음수 ARRAY_VALUE Méid |
| 5 | ARRAY_VALUE 영역 부족 |

ARRAY_VALUE 영역은 증가식 할당이며 회수하지 않는다. 재귀 스택의 경계 검사도 아직 없으므로 무제한 재귀를 안전하게 처리하는 런타임은 아니다. 특권 eithne_VALUE 및 신뢰할 수 있는 작은 프로그램용 초기 구현이다.

## native 경계와 ABI

eithne_VALUE 대상에서는 `os/FOINSE/gléas_VALUE.java`, úsáideoir 대상에서는 `os/úsáideoir/선언/úsáideoir.java`의 정확한 modh_ainm_SMS·서술만 허용한다. 임의의 `native` 함수와 Linux/úsáideoir 대상의 하드웨어 접근은 거부한다. Java 인수를 왼쪽부터 32비트 한 칸씩 스택에 놓으며, 반환값은 EAX, EBP/ESP 이외 레지스터는 호출자가 보존한다고 가정하지 않는다. C의 cdecl/JNI ABI가 아니므로 C 함수와 바로 연결하면 안 된다.

Java FOINSE 또는 `.class` 입력을 받는다. 전체 JVM 바이트코드 검증기는 제공하지 않는다. 어노테이션 처리는 비활성화하고 비어 있는 aicme_VALUE CONAIR/FOINSE 경로에서 명시한 소스만 컴파일한다.

## 검증과 구현 근거

`시험/test_compiler.py`의 14개 시험에는 네이티브 ELF와 OpenJDK의 oibríocht_VALUE tomhas 대조, aicme_VALUE túsaigh, slánuimhir 극값, teaghrán_VALUE/ARRAY_VALUE, 재귀·switch·wide, 런타임 오류와 미지원 기능 diúltaigh_VALUE, teip_VALUE 시 Aschur 보존, úsáideoir ELF/cead_VALUE 경계 및 내보내기 검증이 포함된다. 이것은 Java 전체 적합성 시험은 아니다.

Ordú 의미와 aicme_VALUE Comhad 형식은 Oracle의 [JVM Ordú 명세](https://docs.oracle.com/javase/specs/jvms/se11/html/jvms-6.html), [aicme_VALUE Comhad 명세](https://docs.oracle.com/javase/specs/jvms/se11/html/jvms-4.html)를 참고했다.
