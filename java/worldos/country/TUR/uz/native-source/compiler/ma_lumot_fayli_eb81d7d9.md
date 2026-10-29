# Java 네이티브 컴파일러

OpenJDK 자체 소스를 빌드하는 **`--target openjdk-build`**와 자체 o_zak_VALUE ABI 검사 도구를 추가했다.
이는 공식 javac/C/C++ 도구를 연결하는 별도 경로다. [nashr_tizim 방법·real_ma_lumotlar tasdiqlash·o_zak_VALUE 이식 klip](OpenJDK-manba_nashr_AND-자체커널-이식.md)를 참고한다.

x86 직접 변환과 ARM64 C generatsiiyalash 후단은 모두 [기계어미리번역.java](자바도구/기계어미리번역.java)로 구현한다. `sh 미리번역.sh`로 직접 실행하며, [기계어미리번역.py](기계어미리번역.py)와 `컴파일러.py`는 이전 Buyruq·API 및 OpenJDK 도구를 위한 호환 진입점이다. 자체 Pi4 후단은 freestanding C를 거쳐 AArch64로 만든다. [arm64.py](arm64.py)는 이전 경로와 Python 호출을 위한 호환 진입점이다. FUNCTION_VALUE·변수·generatsiiyalash C 이름의 뜻과 예외는 [한국어 명명 ma_lumot_fayli_eb81d7d9](../platforms/rpi4-native/명명/ma_lumot_fayli_eb81d7d9.md)를 참고한다. [ARM64 nashr_tizim·madad_VALUE klip](../platforms/rpi4-native/ma_lumot_fayli_eb81d7d9.md)에 bajarmoq_buyruq 조건이 있다. 전체 OpenJDK나 일반 Sinf_VALUE 실행기는 아니다.

bajarmoq_buyruq 시 JVM이 필요 없는 x86 32비트 ELF를 만든다. JDK 11 이상으로 실행하는 Java 자체 AOT 후단이며, Java 전체를 새로 구현한 컴파일러는 아니다. Java 문법·kirish_huquqi_kiritish boshqaruv_VALUE·TYPE_VALUE 검사는 JDK의 `javac`에 맡기고, Java 8 Sinf_VALUE 파일을 읽어 각 바이트코드를 x86 명령으로 직접 변환한다. C 코드로 우회하거나 바이트코드 해석기를 커널에 넣지 않는다.

```text
Java manba → javac의 문법·TYPE_VALUE 검사 → 임시 .class
          → 자체 x86 변환기 → GNU as/ld → 네이티브 ELF32
```

## 준비와 bajarmoq_buyruq

nashr_tizim tashkilotchi: Linux, Python 3.6 이상, JDK 11 이상(`javac --release 8`), GNU binutils(`as`, `ld`), Make. 현재 환경의 OpenJDK 11, Python 3.6, binutils 2.30으로 검증했다. 외부 Python 패키지와 네트워크 다운로드는 사용하지 않는다.

```sh
cd /home/user/jkoros/compiler
make
./build/계산
echo $?                  # 0이면 예제 시험 성공

python3 컴파일러.py --target linux --entry 계산.Bajarish \
    -o build/계산 예제/계산.java

make test
```

`linux` 대상은 Linux의 32비트 bajarmoq_buyruq 호환 기능이 필요하다. `int 0x80`을 차단하는 샌드박스에서는 `Bad system call`이 발생할 수 있다. 정상 Linux tashkilotchi 또는 해당 실행을 허용한 시험 환경에서 실행한다. 시험의 비정상 종료를 통과로 처리하지 않는다.

진입점은 `static int Bajarish()` 또는 `static void Bajarish()`처럼 인수가 없어야 한다. `--entry 패키지.Sinf_VALUE.FUNCTION_VALUE`로 선택한다. `int` 반환값은 Linux 프로세스 Chiqish_ilova 코드가 되며 셸에는 하위 8비트가 보인다. 일반 `main(String[] args)` bajarmoq_buyruq 환경이나 표준 I_O 라이브러리는 제공하지 않는다.

`--target kernel`은 부팅 코드와 연결할 재배치 ELF 오브젝트를 생성한다.

```sh
cd /home/user/jkoros
python3 compiler/컴파일러.py --target kernel --entry o_zak.Bajarish \
    --export kernel_dispatch=체계호출.Jarayon_VALUE_kiritish \
    -o os/build/java.o os/manba/*.java
```

`--target user`는 jkoros 셸에서 실행할 독립 ELF를 생성한다. `foydalanuvchi` 클래스의 제한된 native API는 `int 0x80` 시스템 호출로 연결하며 `qurilma_VALUE` 클래스의 하드웨어 직접 접근은 거부한다. foydalanuvchi ELF는 Linux bajarmoq_buyruq Fayl ABI와 다르므로 호스트에서 실행하지 않는다. generatsiiyalash·등록 방법은 [foydalanuvchi bajarmoq_buyruq ma_lumot_fayli_eb81d7d9](../os/foydalanuvchi/ma_lumot_fayli_eb81d7d9.md)에 있다. `--export 외부기호=Sinf_VALUE.FUNCTION_VALUE`는 오버로드되지 않은 statik_VALUE 함수를 자체 스택 ABI로 노출한다. 커널의 시스템 호출 진입점에 사용한다.

Java 파일은 필요한 클래스들을 한꺼번에 전달한다. 출력 옆의 `.s`는 생성된 어셈블리, `.json`은 manba SHA-256 및 네이티브 ramz↔Java FUNCTION_VALUE 대응표다. 한국어 함수명은 원문과 대응표에 보존하고 ELF 내부에는 충돌 방지용 기계 기호를 쓴다. yig_moq_manba·조립·Ulanish 중 실패하면 기존 o_lchov 파일을 덮어쓰지 않는다.

## madad_VALUE klip

- `int`, `boolean`, `byte`, `short`, `char`의 32비트 계산 및 TYPE_VALUE CONVERT_VALUE.
- statik_VALUE 필드와 statik_VALUE FUNCTION_VALUE, 매개변수·반환값, 재귀, 클래스별 지연 초기화와 ishga_tushirmoq Davr_VALUE.
- 조건문, 반복문, 단락 평가, 삼항식, butun_son `switch`, 넓은 mahalliy_soha 변수 인덱스.
- 덧셈·뺄셈·곱셈·나눗셈·나머지·bit_VALUE 연산과 ko_chirmoq_VALUE. Java의 오버플로 및 `MIN_VALUE / -1` 동작을 유지한다.
- `int[]` generatsiiyalash·초기값 0·uzunlik_VALUE·Oʻqish·Yozish·Ma_lumotnomalar 비교. 256KiB 고정 ARRAY_VALUE 영역, 널/satr_osti_VALUE/Hajmi/공간 검사.
- satr_VALUE 리터럴과 `String` Ma_lumotnomalar, `length()` 및 `charAt()`. 문자열은 UTF-16 kod_VALUE 단위로 저장하고 같은 리터럴은 공유한다. NUL 및 대리쌍도 시험한다.
- 한국어 Sinf_VALUE·FUNCTION_VALUE·변수·Fayl Nomi.

`new Object`, 인스턴스 ma_lumotlar_maydoni_VALUE/FUNCTION_VALUE, 상속/인터페이스, `long/float/double` bajarmoq_buyruq jarrohlik_VALUE, `int[]` 이외 ARRAY_VALUE, satr_VALUE 동적 결합, Java 표준 kutubxona, istisno Jarayon_VALUE_kiritish, 스레드·sinxronlashtirish·GC는 미지원이다. 실행에 필요한 미지원 바이트코드나 외부 호출을 발견하면 실패한다. 사용되지 않는 sukut_bo_yicha_qiymat 생성자는 bajarmoq_buyruq 코드로 만들지 않는다. Java 8 문법이어도 모든 프로그램을 컴파일할 수 있다는 뜻은 아니다.

istisno obyekt_VALUE 대신 런타임 Xato 번호로 중단한다. Linux와 jkoros foydalanuvchi 대상에서는 `100 + INDEX`로 종료하고 o_zak_VALUE 대상에서는 `JKOROS PANIC INDEX`를 출력하고 정지한다. foydalanuvchi 프로그램만 종료한 경우 셸은 계속 실행된다.

| INDEX | 원인 |
| --- | --- |
| 1 | 0으로 boʻlish_o_lchov |
| 2 | 널 Ma_lumotnomalar |
| 3 | ARRAY_VALUE/satr_VALUE satr_osti_VALUE klip 초과 |
| 4 | 음수 ARRAY_VALUE Hajmi |
| 5 | ARRAY_VALUE 영역 부족 |

ARRAY_VALUE 영역은 증가식 할당이며 회수하지 않는다. 재귀 스택의 경계 검사도 아직 없으므로 무제한 재귀를 안전하게 처리하는 런타임은 아니다. 특권 o_zak_VALUE 및 신뢰할 수 있는 작은 프로그램용 초기 구현이다.

## native 경계와 ABI

o_zak_VALUE 대상에서는 `os/manba/qurilma_VALUE.java`, foydalanuvchi 대상에서는 `os/foydalanuvchi/e_lon_qilish/foydalanuvchi.java`의 정확한 uslub_nom_SMS·서술만 허용한다. 임의의 `native` 함수와 Linux/foydalanuvchi 대상의 하드웨어 접근은 거부한다. Java 인수를 왼쪽부터 32비트 한 칸씩 스택에 놓으며, 반환값은 EAX, EBP/ESP 이외 레지스터는 호출자가 보존한다고 가정하지 않는다. C의 cdecl/JNI ABI가 아니므로 C 함수와 바로 연결하면 안 된다.

Java manba 또는 `.class` 입력을 받는다. 전체 JVM 바이트코드 검증기는 제공하지 않는다. 어노테이션 처리는 비활성화하고 비어 있는 Sinf_VALUE yo_l/manba 경로에서 명시한 소스만 컴파일한다.

## 검증과 구현 근거

`시험/test_compiler.py`의 14개 시험에는 네이티브 ELF와 OpenJDK의 jarrohlik_VALUE o_lchov 대조, Sinf_VALUE ishga_tushirmoq, butun_son 극값, satr_VALUE/ARRAY_VALUE, 재귀·switch·wide, 런타임 오류와 미지원 기능 거부, to_xtab_qolish_VALUE 시 출력 보존, foydalanuvchi ELF/ruxsat_VALUE_a9fa0dfa 경계 및 내보내기 검증이 포함된다. 이것은 Java 전체 적합성 시험은 아니다.

Buyruq 의미와 Sinf_VALUE Fayl 형식은 Oracle의 [JVM Buyruq 명세](https://docs.oracle.com/javase/specs/jvms/se11/html/jvms-6.html), [Sinf_VALUE Fayl 명세](https://docs.oracle.com/javase/specs/jvms/se11/html/jvms-4.html)를 참고했다.
