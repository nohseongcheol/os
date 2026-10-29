# Java 네이티브 fordítóprogram

OpenJDK saját 소스를 빌드하는 **`--target openjdk-build`**와 saját kernel_ÉRTÉK ABI 검사 도구를 추가했다.
이는 공식 javac/C/C++ 도구를 연결하는 별도 경로다. [épít_Rendszer 방법·tényleges_adat ellenőriz·kernel_ÉRTÉK 이식 klip](OpenJDK-forrás_épít_ÉS-natív_kernel-이식.md)를 참고한다.

x86 직접 변환과 ARM64 C generálás 후단은 모두 [기계어미리번역.java](자바도구/기계어미리번역.java)로 구현한다. `sh 미리번역.sh`로 직접 실행하며, [기계어미리번역.py](기계어미리번역.py)와 `fordítóprogram.py`는 Előző_cikk Parancs·API 및 OpenJDK 도구를 위한 호환 진입점이다. saját Pi4 후단은 freestanding C를 거쳐 AArch64로 만든다. [arm64.py](arm64.py)는 Előző_cikk 경로와 Python 호출을 위한 호환 진입점이다. FÜGGVÉNY_ÉRTÉK·változó_ÉRTÉK·generálás C 이름의 뜻과 예외는 [magyar 명명 fontos_fájl_eb81d7d9](../platforms/rpi4-native/명명/fontos_fájl_eb81d7d9.md)를 참고한다. [ARM64 épít_Rendszer·támogat_ÉRTÉK klip](../platforms/rpi4-native/fontos_fájl_eb81d7d9.md)에 végrehajt_parancs 조건이 있다. 전체 OpenJDK나 일반 tanóra_ÉRTÉK 실행기는 아니다.

végrehajt_parancs 시 JVM이 필요 없는 x86 32비트 ELF를 만든다. JDK 11 이상으로 실행하는 Java saját AOT 후단이며, Java 전체를 새로 구현한 컴파일러는 아니다. Java 문법·hozzáfér_bejegyzés vezérlő_ÉRTÉK·beír_ÉRTÉK 검사는 JDK의 `javac`에 맡기고, Java 8 tanóra_ÉRTÉK 파일을 읽어 각 바이트코드를 x86 명령으로 직접 변환한다. C 코드로 우회하거나 바이트코드 해석기를 커널에 넣지 않는다.

```text
Java FORRÁS → javac의 문법·beír_ÉRTÉK 검사 → 임시 .class
          → saját x86 변환기 → GNU as/ld → 네이티브 ELF32
```

## 준비와 végrehajt_parancs

épít_Rendszer gazda: Linux, Python 3.6 이상, JDK 11 이상(`javac --release 8`), GNU binutils(`as`, `ld`), Make. aktuális_cikk 환경의 OpenJDK 11, Python 3.6, binutils 2.30으로 검증했다. külső_ÉRTÉK Python 패키지와 네트워크 다운로드는 사용하지 않는다.

```sh
cd /home/user/jkoros/compiler
make
./build/계산
echo $?                  # 0이면 예제 시험 성공

python3 fordítóprogram.py --target linux --entry 계산.Futtatás \
    -o build/계산 예제/계산.java

make test
```

`linux` 대상은 Linux의 32비트 végrehajt_parancs 호환 기능이 필요하다. `int 0x80`을 차단하는 샌드박스에서는 `Bad system call`이 발생할 szám 있다. informatikai_részleg_normál Linux gazda 또는 해당 실행을 허용한 시험 환경에서 실행한다. 시험의 비정상 종료를 통과로 처리하지 않는다.

진입점은 `static int Futtatás()` 또는 `static void Futtatás()`처럼 인수가 없어야 한다. `--entry 패키지.tanóra_ÉRTÉK.FÜGGVÉNY_ÉRTÉK`로 선택한다. `int` 반환값은 Linux 프로세스 kilép_app 코드가 되며 셸에는 하위 8비트가 보인다. 일반 `main(String[] args)` végrehajt_parancs 환경이나 표준 I_O 라이브러리는 제공하지 않는다.

`--target kernel`은 부팅 코드와 연결할 재배치 ELF 오브젝트를 생성한다.

```sh
cd /home/user/jkoros
python3 compiler/fordítóprogram.py --target kernel --entry kernel.Futtatás \
    --export kernel_dispatch=체계호출.folyamat_ÉRTÉK_bejegyzés \
    -o os/build/java.o os/FORRÁS/*.java
```

`--target user`는 jkoros 셸에서 실행할 독립 ELF를 생성한다. `felhasználó` 클래스의 제한된 native API는 `int 0x80` 시스템 호출로 연결하며 `mobil_ÉRTÉK` 클래스의 hardver_ÉRTÉK 직접 접근은 거부한다. felhasználó ELF는 Linux végrehajt_parancs Fájl ABI와 다르므로 호스트에서 실행하지 않는다. generálás·jegyzék_bejegyzés 방법은 [felhasználó végrehajt_parancs fontos_fájl_eb81d7d9](../os/felhasználó/fontos_fájl_eb81d7d9.md)에 있다. `--export 외부기호=tanóra_ÉRTÉK.FÜGGVÉNY_ÉRTÉK`는 오버로드되지 않은 statikus_ÉRTÉK 함수를 saját operandus_Sor ABI로 노출한다. 커널의 시스템 호출 진입점에 사용한다.

Java 파일은 필요한 클래스들을 한꺼번에 전달한다. Kimenet 옆의 `.s`는 생성된 어셈블리, `.json`은 FORRÁS SHA-256 및 네이티브 szimbólum↔Java FÜGGVÉNY_ÉRTÉK 대응표다. magyar 함수명은 원문과 대응표에 보존하고 ELF 내부에는 충돌 방지용 gép 기호를 쓴다. épít_forrás·fordít_ÉRTÉK·Kapcsolódás 중 실패하면 기존 KR 파일을 덮어쓰지 않는다.

## támogat_ÉRTÉK klip

- `int`, `boolean`, `byte`, `short`, `char`의 32비트 계산 및 beír_ÉRTÉK konvertál_ÉRTÉK.
- statikus_ÉRTÉK 필드와 statikus_ÉRTÉK FÜGGVÉNY_ÉRTÉK, 매개변수·반환값, 재귀, 클래스별 지연 초기화와 inicializál Ciklus_ÉRTÉK.
- 조건문, 반복문, 단락 평가, 삼항식, egész_szám `switch`, 넓은 helyi_hatókör változó_ÉRTÉK 인덱스.
- 덧셈·뺄셈·곱셈·나눗셈·나머지·bit_ÉRTÉK 연산과 áthelyez_ÉRTÉK. Java의 오버플로 및 `MIN_VALUE / -1` 동작을 유지한다.
- `int[]` generálás·초기값 0·hossz_ÉRTÉK·Olvasás·Írás·hivatkozik 비교. 256KiB 고정 TÖMB_ÉRTÉK régió_ÉRTÉK, 널/alsó_index_ÉRTÉK/Méret/CÍM_régió 검사.
- sztring_ÉRTÉK 리터럴과 `String` hivatkozik, `length()` 및 `charAt()`. 문자열은 UTF-16 KÓD_ÉRTÉK 단위로 저장하고 같은 리터럴은 공유한다. NUL 및 대리쌍도 시험한다.
- magyar tanóra_ÉRTÉK·FÜGGVÉNY_ÉRTÉK·változó_ÉRTÉK·Fájl Név.

`new Object`, 인스턴스 mezőérték/FÜGGVÉNY_ÉRTÉK, 상속/인터페이스, `long/float/double` végrehajt_parancs műtét_ÉRTÉK, `int[]` 이외 TÖMB_ÉRTÉK, sztring_ÉRTÉK 동적 결합, Java 표준 kódtár, kivétel folyamat_ÉRTÉK_bejegyzés, 스레드·szinkronizál·GC는 미지원이다. 실행에 필요한 미지원 바이트코드나 külső_ÉRTÉK 호출을 발견하면 실패한다. 사용되지 않는 alapértelmezett_érték 생성자는 végrehajt_parancs 코드로 만들지 않는다. Java 8 문법이어도 모든 프로그램을 컴파일할 szám 있다는 뜻은 아니다.

kivétel objektum_ÉRTÉK 대신 런타임 HIBA 번호로 중단한다. Linux와 jkoros felhasználó 대상에서는 `100 + INDEX`로 종료하고 kernel_ÉRTÉK 대상에서는 `JKOROS PANIC INDEX`를 출력하고 정지한다. felhasználó 프로그램만 종료한 경우 셸은 계속 실행된다.

| INDEX | 원인 |
| --- | --- |
| 1 | 0으로 osztás_KR |
| 2 | 널 hivatkozik |
| 3 | TÖMB_ÉRTÉK/sztring_ÉRTÉK alsó_index_ÉRTÉK klip 초과 |
| 4 | 음수 TÖMB_ÉRTÉK Méret |
| 5 | TÖMB_ÉRTÉK régió_ÉRTÉK 부족 |

TÖMB_ÉRTÉK 영역은 증가식 할당이며 회수하지 않는다. 재귀 스택의 határ_ÉRTÉK 검사도 아직 없으므로 무제한 재귀를 안전하게 처리하는 런타임은 아니다. 특권 kernel_ÉRTÉK 및 신뢰할 szám 있는 작은 프로그램용 kiinduló_állapot 구현이다.

## native 경계와 ABI

kernel_ÉRTÉK 대상에서는 `os/FORRÁS/mobil_ÉRTÉK.java`, felhasználó 대상에서는 `os/felhasználó/bevallás/felhasználó.java`의 정확한 metódus_név_SMS·서술만 허용한다. 임의의 `native` 함수와 Linux/felhasználó 대상의 hardver_ÉRTÉK 접근은 거부한다. Java 인수를 왼쪽부터 32비트 한 칸씩 스택에 놓으며, 반환값은 EAX, EBP/ESP 이외 레지스터는 호출자가 보존한다고 가정하지 않는다. C의 cdecl/JNI ABI가 아니므로 C 함수와 바로 연결하면 안 된다.

Java FORRÁS 또는 `.class` 입력을 받는다. 전체 JVM 바이트코드 검증기는 제공하지 않는다. 어노테이션 처리는 비활성화하고 비어 있는 tanóra_ÉRTÉK ÚTVONAL/FORRÁS 경로에서 명시한 소스만 컴파일한다.

## 검증과 구현 근거

`시험/test_compiler.py`의 14개 시험에는 네이티브 ELF와 OpenJDK의 műtét_ÉRTÉK KR 대조, tanóra_ÉRTÉK inicializál, egész_szám 극값, sztring_ÉRTÉK/TÖMB_ÉRTÉK, 재귀·switch·wide, 런타임 오류와 미지원 기능 elutasít_ÉRTÉK, hiba_ÉRTÉK 시 Kimenet 보존, felhasználó ELF/engedély_ÉRTÉK határ_ÉRTÉK 및 내보내기 검증이 포함된다. 이것은 Java 전체 적합성 시험은 아니다.

Parancs 의미와 tanóra_ÉRTÉK Fájl 형식은 Oracle의 [JVM Parancs 명세](https://docs.oracle.com/javase/specs/jvms/se11/html/jvms-6.html), [tanóra_ÉRTÉK Fájl 명세](https://docs.oracle.com/javase/specs/jvms/se11/html/jvms-4.html)를 참고했다.
