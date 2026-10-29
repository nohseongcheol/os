# Java 네이티브 컴파일러

OpenJDK 자체 소스를 빌드하는 **`--target openjdk-build`**와 자체 kākano_uara_0611a8a8 ABI 검사 도구를 추가했다.
이는 공식 javac/C/C++ 도구를 연결하는 별도 경로다. [hanga_pūnaha 방법·tūturu_raraunga whakamana·kākano_uara_0611a8a8 이식 topenga](OpenJDK-pūtake_hanga_AND-자체커널-이식.md)를 참고한다.

x86 직접 변환과 ARM64 C waihanga 후단은 모두 [기계어미리번역.java](자바도구/기계어미리번역.java)로 구현한다. `sh 미리번역.sh`로 직접 실행하며, [기계어미리번역.py](기계어미리번역.py)와 `컴파일러.py`는 이전 tono·API 및 OpenJDK 도구를 위한 호환 진입점이다. 자체 Pi4 후단은 freestanding C를 거쳐 AArch64로 만든다. [arm64.py](arm64.py)는 이전 경로와 Python 호출을 위한 호환 진입점이다. TAUMAHI_uara·변수·waihanga C 이름의 뜻과 예외는 [Reo_Māori 명명 PĀNUIMAI_eb81d7d9](../platforms/rpi4-native/명명/PĀNUIMAI_eb81d7d9.md)를 참고한다. [ARM64 hanga_pūnaha·Tautoko_uara topenga](../platforms/rpi4-native/PĀNUIMAI_eb81d7d9.md)에 kawe_tono 조건이 있다. 전체 OpenJDK나 일반 tauaha_uara 실행기는 아니다.

kawe_tono 시 JVM이 필요 없는 x86 32비트 ELF를 만든다. JDK 11 이상으로 실행하는 Java 자체 AOT 후단이며, Java 전체를 새로 구현한 컴파일러는 아니다. Java 문법·uru_tāurunga mana_uara·TYPE_uara 검사는 JDK의 `javac`에 맡기고, Java 8 tauaha_uara 파일을 읽어 각 바이트코드를 x86 명령으로 직접 변환한다. C 코드로 우회하거나 바이트코드 해석기를 커널에 넣지 않는다.

```text
Java pūtake → javac의 문법·TYPE_uara 검사 → 임시 .class
          → 자체 x86 변환기 → GNU as/ld → 네이티브 ELF32
```

## 준비와 kawe_tono

hanga_pūnaha taurima: Linux, Python 3.6 이상, JDK 11 이상(`javac --release 8`), GNU binutils(`as`, `ld`), Make. 현재 환경의 OpenJDK 11, Python 3.6, binutils 2.30으로 검증했다. 외부 Python 패키지와 네트워크 다운로드는 사용하지 않는다.

```sh
cd /home/user/jkoros/compiler
make
./build/계산
echo $?                  # 0이면 예제 시험 성공

python3 컴파일러.py --target linux --entry 계산.whakahaere \
    -o build/계산 예제/계산.java

make test
```

`linux` 대상은 Linux의 32비트 kawe_tono 호환 기능이 필요하다. `int 0x80`을 차단하는 샌드박스에서는 `Bad system call`이 발생할 수 있다. 정상 Linux taurima 또는 해당 실행을 허용한 시험 환경에서 실행한다. 시험의 비정상 종료를 통과로 처리하지 않는다.

진입점은 `static int whakahaere()` 또는 `static void whakahaere()`처럼 인수가 없어야 한다. `--entry 패키지.tauaha_uara.TAUMAHI_uara`로 선택한다. `int` 반환값은 Linux 프로세스 Putaatu_kaupapa 코드가 되며 셸에는 하위 8비트가 보인다. 일반 `main(String[] args)` kawe_tono 환경이나 표준 I_O 라이브러리는 제공하지 않는다.

`--target kernel`은 부팅 코드와 연결할 재배치 ELF 오브젝트를 생성한다.

```sh
cd /home/user/jkoros
python3 compiler/컴파일러.py --target kernel --entry kākano.whakahaere \
    --export kernel_dispatch=체계호출.Hātepe_uara_tāurunga \
    -o os/build/java.o os/pūtake/*.java
```

`--target user`는 jkoros 셸에서 실행할 독립 ELF를 생성한다. `kaiwhakamahi` 클래스의 제한된 native API는 `int 0x80` 시스템 호출로 연결하며 `pūkoro_uara` 클래스의 하드웨어 직접 접근은 거부한다. kaiwhakamahi ELF는 Linux kawe_tono Kōnae ABI와 다르므로 호스트에서 실행하지 않는다. waihanga·rēhita_tāurunga 방법은 [kaiwhakamahi kawe_tono PĀNUIMAI_eb81d7d9](../os/kaiwhakamahi/PĀNUIMAI_eb81d7d9.md)에 있다. `--export 외부기호=tauaha_uara.TAUMAHI_uara`는 오버로드되지 않은 pateko_uara 함수를 자체 스택 ABI로 노출한다. 커널의 시스템 호출 진입점에 사용한다.

Java 파일은 필요한 클래스들을 한꺼번에 전달한다. 출력 옆의 `.s`는 생성된 어셈블리, `.json`은 pūtake SHA-256 및 네이티브 tohu↔Java TAUMAHI_uara 대응표다. Reo_Māori 함수명은 원문과 대응표에 보존하고 ELF 내부에는 충돌 방지용 mīhini 기호를 쓴다. hanga_pūtake·조립·TŪHONO 중 실패하면 기존 mēhua 파일을 덮어쓰지 않는다.

## Tautoko_uara topenga

- `int`, `boolean`, `byte`, `short`, `char`의 32비트 계산 및 TYPE_uara CONVERT_uara.
- pateko_uara 필드와 pateko_uara TAUMAHI_uara, 매개변수·반환값, 재귀, 클래스별 지연 초기화와 arawhiti Porohita_uara.
- 조건문, 반복문, 단락 평가, 삼항식, tau_tōpū `switch`, 넓은 paetata_whānuitanga 변수 인덱스.
- 덧셈·뺄셈·곱셈·나눗셈·나머지·moka_uara 연산과 nuku_uara. Java의 오버플로 및 `MIN_VALUE / -1` 동작을 유지한다.
- `int[]` waihanga·초기값 0·roa_uara·Pānuitia·Tuhia·Pūranga_kōrero 비교. 256KiB 고정 HUĀNGA_uara 영역, 널/hauraro_uara/rahi/공간 검사.
- aho_uara 리터럴과 `String` Pūranga_kōrero, `length()` 및 `charAt()`. 문자열은 UTF-16 CODE_uara 단위로 저장하고 같은 리터럴은 공유한다. NUL 및 대리쌍도 시험한다.
- Reo_Māori tauaha_uara·TAUMAHI_uara·변수·Kōnae Ingoa.

`new Object`, 인스턴스 āpure_uara/TAUMAHI_uara, 상속/인터페이스, `long/float/double` kawe_tono mahi_uara, `int[]` 이외 HUĀNGA_uara, aho_uara 동적 결합, Java 표준 puna, 예외 Hātepe_uara_tāurunga, 스레드·tukutahi·GC는 미지원이다. 실행에 필요한 미지원 바이트코드나 외부 호출을 발견하면 실패한다. 사용되지 않는 uara_taunoa 생성자는 kawe_tono 코드로 만들지 않는다. Java 8 문법이어도 모든 프로그램을 컴파일할 수 있다는 뜻은 아니다.

예외 ahanoa_uara 대신 런타임 Pōhēhē 번호로 중단한다. Linux와 jkoros kaiwhakamahi 대상에서는 `100 + INDEX`로 종료하고 kākano_uara_0611a8a8 대상에서는 `JKOROS PANIC INDEX`를 출력하고 정지한다. kaiwhakamahi 프로그램만 종료한 경우 셸은 계속 실행된다.

| INDEX | 원인 |
| --- | --- |
| 1 | 0으로 whakawehenga_mēhua |
| 2 | 널 Pūranga_kōrero |
| 3 | HUĀNGA_uara/aho_uara hauraro_uara topenga 초과 |
| 4 | 음수 HUĀNGA_uara rahi |
| 5 | HUĀNGA_uara 영역 부족 |

HUĀNGA_uara 영역은 증가식 할당이며 회수하지 않는다. 재귀 스택의 경계 검사도 아직 없으므로 무제한 재귀를 안전하게 처리하는 런타임은 아니다. 특권 kākano_uara_0611a8a8 및 신뢰할 수 있는 작은 프로그램용 초기 구현이다.

## native 경계와 ABI

kākano_uara_0611a8a8 대상에서는 `os/pūtake/pūkoro_uara.java`, kaiwhakamahi 대상에서는 `os/kaiwhakamahi/선언/kaiwhakamahi.java`의 정확한 aratuka_ingoa_TEXT·서술만 허용한다. 임의의 `native` 함수와 Linux/kaiwhakamahi 대상의 하드웨어 접근은 거부한다. Java 인수를 왼쪽부터 32비트 한 칸씩 스택에 놓으며, 반환값은 EAX, EBP/ESP 이외 레지스터는 호출자가 보존한다고 가정하지 않는다. C의 cdecl/JNI ABI가 아니므로 C 함수와 바로 연결하면 안 된다.

Java pūtake 또는 `.class` 입력을 받는다. 전체 JVM 바이트코드 검증기는 제공하지 않는다. 어노테이션 처리는 비활성화하고 비어 있는 tauaha_uara ara/pūtake 경로에서 명시한 소스만 컴파일한다.

## 검증과 구현 근거

`시험/test_compiler.py`의 14개 시험에는 네이티브 ELF와 OpenJDK의 mahi_uara mēhua 대조, tauaha_uara arawhiti, tau_tōpū 극값, aho_uara/HUĀNGA_uara, 재귀·switch·wide, 런타임 오류와 미지원 기능 거부, rahunga_uara 시 출력 보존, kaiwhakamahi ELF/mana_uru_uara 경계 및 내보내기 검증이 포함된다. 이것은 Java 전체 적합성 시험은 아니다.

tono 의미와 tauaha_uara Kōnae 형식은 Oracle의 [JVM tono 명세](https://docs.oracle.com/javase/specs/jvms/se11/html/jvms-6.html), [tauaha_uara Kōnae 명세](https://docs.oracle.com/javase/specs/jvms/se11/html/jvms-4.html)를 참고했다.
