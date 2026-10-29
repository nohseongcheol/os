# Java 네이티브 kääntäjä

OpenJDK oma 소스를 빌드하는 **`--target openjdk-build`**와 oma ydin_ARVO ABI 검사 도구를 추가했다.
이는 공식 javac/C/C++ 도구를 연결하는 별도 경로다. [kääntää_Järjestelmä 방법·todellinen_data vahvista·ydin_ARVO 이식 leikata](OpenJDK-lähde_kääntää_JA-alkuperäinen_ydin-이식.md)를 참고한다.

x86 직접 변환과 ARM64 C generoida 후단은 모두 [기계어미리번역.java](자바도구/기계어미리번역.java)로 구현한다. `sh 미리번역.sh`로 직접 실행하며, [기계어미리번역.py](기계어미리번역.py)와 `kääntäjä.py`는 Edellinen_kohde komento·API 및 OpenJDK 도구를 위한 호환 진입점이다. oma Pi4 후단은 freestanding C를 거쳐 AArch64로 만든다. [arm64.py](arm64.py)는 Edellinen_kohde 경로와 Python 호출을 위한 호환 진입점이다. funktio_ARVO·muuttuja_ARVO·generoida C 이름의 뜻과 예외는 [suomi 명명 Lueminut_eb81d7d9](../platforms/rpi4-native/명명/Lueminut_eb81d7d9.md)를 참고한다. [ARM64 kääntää_Järjestelmä·Tuki_ARVO leikata](../platforms/rpi4-native/Lueminut_eb81d7d9.md)에 Suorita_komento 조건이 있다. 전체 OpenJDK나 일반 Luokka_ARVO 실행기는 아니다.

Suorita_komento 시 JVM이 필요 없는 x86 32비트 ELF를 만든다. JDK 11 이상으로 실행하는 Java oma AOT 후단이며, Java 전체를 새로 구현한 컴파일러는 아니다. Java 문법·pääsy_merkintä_68aed533 ohjain_ARVO·TYYPPI_ARVO 검사는 JDK의 `javac`에 맡기고, Java 8 Luokka_ARVO 파일을 읽어 각 바이트코드를 x86 명령으로 직접 변환한다. C 코드로 우회하거나 바이트코드 해석기를 커널에 넣지 않는다.

```text
Java lähdetiedosto → javac의 문법·TYYPPI_ARVO 검사 → 임시 .class
          → oma x86 변환기 → GNU as/ld → 네이티브 ELF32
```

## 준비와 Suorita_komento

kääntää_Järjestelmä isäntä: Linux, Python 3.6 이상, JDK 11 이상(`javac --release 8`), GNU binutils(`as`, `ld`), Make. nykyinen_kohde 환경의 OpenJDK 11, Python 3.6, binutils 2.30으로 검증했다. ulkoinen_ARVO Python 패키지와 네트워크 다운로드는 사용하지 않는다.

```sh
cd /home/user/jkoros/compiler
make
./build/계산
echo $?                  # 0이면 예제 testit 성공

python3 kääntäjä.py --target linux --entry 계산.Suorita_2 \
    -o build/계산 예제/계산.java

make test
```

`linux` 대상은 Linux의 32비트 Suorita_komento 호환 기능이 필요하다. `int 0x80`을 차단하는 샌드박스에서는 `Bad system call`이 발생할 numero 있다. tietojärjestelmät_normaali Linux isäntä 또는 해당 실행을 허용한 testit 환경에서 실행한다. 시험의 비정상 종료를 통과로 처리하지 않는다.

진입점은 `static int Suorita_2()` 또는 `static void Suorita_2()`처럼 인수가 없어야 한다. `--entry 패키지.Luokka_ARVO.funktio_ARVO`로 선택한다. `int` 반환값은 Linux 프로세스 Lopeta_ohjelma 코드가 되며 셸에는 하위 8비트가 보인다. 일반 `main(String[] args)` Suorita_komento 환경이나 표준 I_O 라이브러리는 제공하지 않는다.

`--target kernel`은 koneen_käynnistys 코드와 연결할 재배치 ELF 오브젝트를 생성한다.

```sh
cd /home/user/jkoros
python3 compiler/kääntäjä.py --target kernel --entry ydin.Suorita_2 \
    --export kernel_dispatch=järjestelmäkutsu.prosessi_ARVO_merkintä \
    -o os/build/java.o os/lähdetiedosto/*.java
```

`--target user`는 jkoros 셸에서 실행할 독립 ELF를 생성한다. `käyttäjätila` 클래스의 제한된 native API는 `int 0x80` 시스템 호출로 연결하며 `laite_ARVO` 클래스의 laitteisto_ARVO 직접 접근은 거부한다. käyttäjätila ELF는 Linux Suorita_komento tiedoston_nimi ABI와 다르므로 호스트에서 실행하지 않는다. generoida·rekisteri_merkintä 방법은 [käyttäjätila Suorita_komento Lueminut_eb81d7d9](../os/käyttäjätila/Lueminut_eb81d7d9.md)에 있다. `--export 외부기호=Luokka_ARVO.funktio_ARVO`는 오버로드되지 않은 staattinen_ARVO 함수를 oma operandi_Pino ABI로 노출한다. 커널의 시스템 호출 진입점에 사용한다.

Java 파일은 필요한 클래스들을 한꺼번에 전달한다. tulostuspaikka 옆의 `.s`는 생성된 어셈블리, `.json`은 lähdetiedosto SHA-256 및 네이티브 symboli↔Java funktio_ARVO 대응표다. suomi 함수명은 원문과 대응표에 보존하고 ELF 내부에는 충돌 방지용 kone 기호를 쓴다. kääntää_lähde·kääntää_ARVO·Yhdistä 중 실패하면 기존 TULOS 파일을 덮어쓰지 않는다.

## Tuki_ARVO leikata

- `int`, `boolean`, `byte`, `short`, `char`의 32비트 계산 및 TYYPPI_ARVO MUUNNA_ARVO.
- staattinen_ARVO 필드와 staattinen_ARVO funktio_ARVO, 매개변수·반환값, 재귀, 클래스별 지연 초기화와 alustaa kehä_ARVO.
- 조건문, 반복문, 단락 평가, 삼항식, kokonaisluku `switch`, 넓은 paikallinen_laajuus muuttuja_ARVO 인덱스.
- 덧셈·뺄셈·곱셈·나눗셈·나머지·bitti_ARVO 연산과 siirrä_ARVO_83b651b8. Java의 오버플로 및 `MIN_VALUE / -1` 동작을 유지한다.
- `int[]` generoida·초기값 0·kesto_ARVO·Luku·Kirjoitus·viite 비교. 256KiB 고정 MATRIISI_ARVO alue_ARVO_0e9a97ab, 널/alaindeksi_ARVO/Koko/OSOITE_alue 검사.
- merkkijono_ARVO 리터럴과 `String` viite, `length()` 및 `charAt()`. 문자열은 UTF-16 KOODI_ARVO 단위로 저장하고 같은 리터럴은 공유한다. NUL 및 대리쌍도 시험한다.
- suomi Luokka_ARVO·funktio_ARVO·muuttuja_ARVO·tiedoston_nimi Nimi.

`new Object`, 인스턴스 kentän_arvo/funktio_ARVO, 상속/인터페이스, `long/float/double` Suorita_komento leikkaus_ARVO, `int[]` 이외 MATRIISI_ARVO, merkkijono_ARVO 동적 결합, Java 표준 kirjasto, poikkeus prosessi_ARVO_merkintä, 스레드·synkronoi·GC는 미지원이다. 실행에 필요한 미지원 바이트코드나 ulkoinen_ARVO 호출을 발견하면 실패한다. 사용되지 않는 oletusarvo 생성자는 Suorita_komento 코드로 만들지 않는다. Java 8 문법이어도 모든 프로그램을 컴파일할 numero 있다는 뜻은 아니다.

poikkeus objekti_ARVO 대신 런타임 VIRHE 번호로 중단한다. Linux와 jkoros käyttäjätila 대상에서는 `100 + INDEKSI`로 종료하고 ydin_ARVO 대상에서는 `JKOROS PANIC INDEKSI`를 출력하고 정지한다. käyttäjätila 프로그램만 종료한 경우 셸은 계속 실행된다.

| INDEKSI | 원인 |
| --- | --- |
| 1 | 0으로 jako_KR |
| 2 | 널 viite |
| 3 | MATRIISI_ARVO/merkkijono_ARVO alaindeksi_ARVO leikata 초과 |
| 4 | 음수 MATRIISI_ARVO Koko |
| 5 | MATRIISI_ARVO alue_ARVO_0e9a97ab 부족 |

MATRIISI_ARVO 영역은 증가식 할당이며 회수하지 않는다. 재귀 스택의 rajattu_alue_ARVO 검사도 아직 없으므로 무제한 재귀를 안전하게 처리하는 런타임은 아니다. 특권 ydin_ARVO 및 신뢰할 numero 있는 작은 프로그램용 alkutila 구현이다.

## native 경계와 ABI

ydin_ARVO 대상에서는 `os/lähdetiedosto/laite_ARVO.java`, käyttäjätila 대상에서는 `os/käyttäjätila/esittely/käyttäjätila.java`의 정확한 menetelmä_nimi_SMS·서술만 허용한다. 임의의 `native` 함수와 Linux/käyttäjätila 대상의 laitteisto_ARVO 접근은 거부한다. Java 인수를 왼쪽부터 32비트 한 칸씩 스택에 놓으며, 반환값은 EAX, EBP/ESP 이외 레지스터는 호출자가 보존한다고 가정하지 않는다. C의 cdecl/JNI ABI가 아니므로 C 함수와 바로 연결하면 안 된다.

Java lähdetiedosto 또는 `.class` 입력을 받는다. 전체 JVM 바이트코드 검증기는 제공하지 않는다. 어노테이션 처리는 비활성화하고 비어 있는 Luokka_ARVO polku_2/lähdetiedosto 경로에서 명시한 소스만 컴파일한다.

## 검증과 toteutus 근거

`testit/test_compiler.py`의 14개 시험에는 네이티브 ELF와 OpenJDK의 leikkaus_ARVO TULOS 대조, Luokka_ARVO alustaa, kokonaisluku 극값, merkkijono_ARVO/MATRIISI_ARVO, 재귀·switch·wide, 런타임 오류와 미지원 기능 hylkää_ARVO_e3ecc00b, virhe_ARVO 시 tulostuspaikka 보존, käyttäjätila ELF/lupa_ARVO rajattu_alue_ARVO 및 내보내기 검증이 포함된다. 이것은 Java 전체 적합성 시험은 아니다.

komento 의미와 Luokka_ARVO tiedoston_nimi 형식은 Oracle의 [JVM komento määritys](https://docs.oracle.com/javase/specs/jvms/se11/html/jvms-6.html), [Luokka_ARVO tiedoston_nimi määritys](https://docs.oracle.com/javase/specs/jvms/se11/html/jvms-4.html)를 참고했다.
