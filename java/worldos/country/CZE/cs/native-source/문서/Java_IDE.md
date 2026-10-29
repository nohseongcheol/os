# jkoros 안에서 Java kompilovat_zdroj·Provést_příkaz

이 문서의 spuštění_stroje·prostředí·Store_HODNOTA 명령은 **x86 verze_HODNOTA** 기준이다. 공유 Java kompilátor/JVM은 [vlastní ARM64 Pi4 verze_HODNOTA](../platforms/rpi4-native/README.md)에도 연결되어 있다. ARM64에서는 UTF-8 UART vstup_HODNOTA·한글 název_souboru_SMS, `edit`의 단독 `.` Store_HODNOTA, 16개 RAM název_souboru, 약 2초 Provést_příkaz 제한을 사용한다.

`javac FILE.java`와 `java CLASS [ARGS]`를 네이티브 jkoros 셸에서 실행한다. 컴파일러와 JVM은 각각 독립 ELF로 적재되어 ring 3에서 동작한다. 소스를 게스트에서 읽어 skutečný_data JVM `.class` 파일을 만들고, 그 파일의 바이트코드를 게스트 JVM이 해석한다. hostit kompilovat_zdroj 서버나 Linux 게스트는 사용하지 않는다.

**dobrá_zboží 구현은 vlastní 제한형 kompilátor·JVM이다. OpenJDK/JDK 전체를 이식하거나 설치한 것이 아니며 Java SE 호환 환경도 아니다.** 표준 라이브러리는 아래의 일부 호출을 구현한 것이다. `java -version`과 `javac -version`에도 이 범위를 표시한다. 일반 JAR, Maven/Gradle, 임의의 Java program_f5044b9b 실행은 아직 지원하지 않는다.

## 바로 Provést_příkaz

호스트에서:

```sh
cd /home/user/jkoros
make iso
make run
```

게스트에서:

```text
jkoros> javac -version
jkoros> java -version
jkoros> ls
jkoros> cat Hello.java
jkoros> javac Hello.java
Compiled: Hello.class (JVM class version 49)
Exit: 0
jkoros> java Hello
Hello from jkoros JVM!
55
Exit: 0
```

ISO는 `os/build/kernel.iso`다. 기존 VirtualBox 실행기도 같은 ISO를 사용한다. Provést_příkaz 중이거나 저장된 VM에는 새 ISO가 자동 반영되지 않는다. 새 spuštění_stroje 절차는 [VirtualBox Provést_příkaz 안내](가상상자실행.md)를 따른다. 이 변경의 Java 자동 시험은 QEMU에서 수행했다.

## 직접 작성

`edit`는 název_souboru 전체를 새 내용으로 작성한다. 기존 내용의 vstupní_řádek úprava_HODNOTA 기능은 아니다. `.save`로 저장하고 `.cancel`로 취소한다.

```text
jkoros> edit Demo.java
...> public class Demo {
...>  public static int square(int n) { return n * n; }
...>  public static void main(String[] args) {
...>   int n = Integer.parseInt(args[0]);
...>   System.out.println("square=" + square(n));
...>  }
...> }
...> .save
jkoros> javac Demo.java
jkoros> java Demo 12
square=144
Exit: 0
```

- `ls`: 파일과 bajt_HODNOTA číslo zobrazit_HODNOTA.
- `cat FILE`: název_souboru Obsah_HODNOTA zobrazit_HODNOTA. 텍스트 소스에 사용한다.
- `rm FILE`: Paměť_data název_souboru 삭제.
- `edit FILE`: 전체 내용을 새로 vstup_HODNOTA. 빈 파일도 저장할 číslo 있다.
- 구문·TYP_HODNOTA 검사 selhání_HODNOTA 시 기존 `.class`는 유지된다. 소스를 고친 BACK_HODNOTA 컴파일이 실패했다면 Předchozí_zboží Provést_příkaz 파일이 남아 있으므로 kompilovat_zdroj 성공 여부를 확인한다.

파일은 RAM에서 동작한다. 전용 Store_HODNOTA 매체가 없거나 `sync`하지 않은 내용은 재부팅하면 사라진다. `make -C os run-store`로 연결한 매체에는 `sync`로 zdroj_strom·Třída_HODNOTA·data 파일을 보존할 číslo 있다. 최대 8개, 파일마다 16KiB, název_souboru 이름은 ASCII 1~63자다. zdroj_strom 이름은 `.class` 확장자 ODKAZ_oblast 때문에 최대 62자다. úprava_HODNOTA 입력은 ASCII이고 한 vstupní_řádek 최대 128자다. vstupní_řádek 또는 název_souboru 한도를 넘긴 편집은 `.save`에서 거부하여 기존 파일을 보존한다. jádro_HODNOTA/kompilátor/JVM 구현의 Java 식별자는 한국어이며, dobrá_zboží 게스트 vstup_HODNOTA 제한 때문에 uživatelský_prostor 예제 이름은 ASCII로 작성한다.

## externí_HODNOTA název_souboru 적재

호스트에서 만든 소스나 vzpěra_HODNOTA oříznout 안의 `.class`를 spuštění_stroje 이미지에 포함할 číslo 있다. `JAVA_FILES`는 `게스트이름=호스트경로` 목록이다. 아래의 경로는 예시이며 skutečný_data 파일의 절대 경로로 바꾼다. 공백 없는 경로를 사용한다.

```sh
# hostit JDK로 컴파일한 클래스도 사용할 číslo 있다.
javac --release 8 /tmp/Demo.java
make -C /home/user/jkoros iso \
  JAVA_FILES='Demo.java=/tmp/Demo.java Demo.class=/tmp/Demo.class'
make -C /home/user/jkoros run \
  JAVA_FILES='Demo.java=/tmp/Demo.java Demo.class=/tmp/Demo.class'
```

새 spuštění_stroje 후 `java Demo 12`를 실행한다. 소스만 넣었으면 게스트에서 `javac Demo.java`부터 실행한다. `JAVA_FILES`를 생략한 Další_zboží 빌드에서는 Připojit_položka 파일을 포함하지 않는다. název_souboru Obsah_HODNOTA 변경과 položka_Seznam 제거도 Další_zboží 빌드에 반영된다. 원본 hostit 파일에는 쓰지 않는다. výchozí_hodnota `Hello.java`까지 합해 8개이며, 같은 이름을 명시하면 výchozí_hodnota 예제를 대체한다. 새 `.class`를 저장할 빈 슬롯도 남겨 둔다.

`--release 8`은 Třída_HODNOTA název_souboru 버전을 맞추는 옵션이다. 사용하는 문법·바이트코드·라이브러리도 아래 vzpěra_HODNOTA oříznout 안에 있어야 한다.

## vzpěra_HODNOTA oříznout

| 기능 | 게스트 javac | 게스트 JVM |
| --- | --- | --- |
| Třída_HODNOTA | 패키지 없는 단일 Třída_HODNOTA, statický_HODNOTA funkce_HODNOTA, 재귀, argumenty/Vratka_KV | 실행마다 단일 Třída_HODNOTA 적재, public static main(String[]) |
| výchozí_hodnota HODNOTA | int, boolean, char, String, main의 String[] argumenty | integer·odkaz operand_Štos, String, int[], String[], 내부 StringBuilder |
| výpis_HODNOTA | 초기값 있는 místní_obor deklarace_4f4f026b, zadání_HODNOTA, `+=`, `-=`, `*=`, `/=`, `%=`, 후위 ++/--, 블록, if/else, while, for, return | 해당 integer·odkaz 바이트코드와 podmínka větev |
| výraz_HODNOTA | 십진 integer, UTF-8 소스의 řetězec_HODNOTA/문자, + - * / %, 비교, ==/!=, !/&&/\|\|, řetězec_HODNOTA 결합 | integer operace_HODNOTA·bit_HODNOTA operace_HODNOTA·TYP_HODNOTA CONVERT_HODNOTA, 단락 평가, pole_HODNOTA přístup_položka |
| název_souboru | FileInputStream(String), FileOutputStream(String[, boolean]), read()/write(int)/close() | skutečný_data jádro_HODNOTA 파일서술자와 Připojit, generovat·vymazat_Obsah·이어쓰기·EOF |
| výstupní_pozice | System.out.print/println: int/boolean/char/String, println() | 동일 |
| řetězec_HODNOTA/argumenty | String.length(), args.length, args[index], Integer.parseInt | 추가로 String.charAt(), řetězec_HODNOTA 상수의 modified UTF-8 해독 |

선언은 지원하는 문법만 허용한다. 여러 변수를 한 선언에 나열하기, 초기값 없는 místní_obor deklarace_4f4f026b, 오버로드, 임의 TYP_HODNOTA CONVERT_HODNOTA, pole_HODNOTA generovat zdrojový_soubor, 8/16진 리터럴, Unicode zdroj_strom 이스케이프 등은 미지원이다. `char`는 문자 리터럴로 초기화하며 일반 JDK의 모든 konstanta_HODNOTA 축소 변환을 구현하지 않는다. externí_HODNOTA `.class`의 `int[]` generovat/Čtení/쓰기는 지원하므로 hostit `javac --release 8`로 만든 pole_HODNOTA 예제는 실행할 číslo 있다.

objekt_HODNOTA hodnota_pole·일반 objekt_HODNOTA generovat·상속·인터페이스·여러 Třída_HODNOTA Připojit, long/float/double, výjimka Proces_HODNOTA_položka, 스레드·모니터, 리플렉션, JNI, JIT, GC, 위 표에 없는 `java.io`와 `java.nio`/`java.net` 일반 API, 컬렉션, JAR와 클래스패스는 미지원이다. 런타임 오류는 Java výjimka 객체를 던지지 않고 진단 후 dobrá_zboží 프로그램을 종료한다. 객체와 řetězec_HODNOTA Store_HODNOTA 공간은 Provést_příkaz Konec_program 시 uživatelský_prostor oblast_HODNOTA_0e9a97ab 전체와 함께 회수한다. 지속 Provést_příkaz 중 GC는 없다.

## Provést_příkaz 한도와 chyba

| zdroj_HODNOTA | 한도 |
| --- | --- |
| zdroj_strom/Třída_HODNOTA název_souboru | 각각 16KiB |
| kompilátor | token_HODNOTA 2,047개, generovat KÓD_HODNOTA 4KiB, konstanta_HODNOTA 풀 4KiB |
| funkce_HODNOTA/argumenty | 클래스당 32함수, 함수당 16인수 |
| JVM konstanta_HODNOTA | 511개 |
| JVM funkce_HODNOTA KÓD_HODNOTA | 함수당 8KiB |
| JVM 호출/operand_Štos/místní_obor proměnná_HODNOTA | 32프레임, 프레임당 operand_Štos 128칸·místní_obor 128칸 |
| JVM objekt_HODNOTA Store_HODNOTA ODKAZ_oblast | 8,192개 32비트 přihrádka_položka, 헤더 deklarace 약 32KiB |
| Provést_příkaz | 최대 500,000 příkaz, 기존 커널의 약 3초 CPU Provést_příkaz 상한도 적용 |

게스트 컴파일러는 버전 49.0 `.class`를 생성하며 JVM은 45.0~52.0 중 vzpěra_HODNOTA 명령으로 구성된 파일을 읽는다. 스택맵을 이용한 완전한 JVM slovník 검증기를 구현한 것은 아니다. název_souboru/hodnota_atributu délka_HODNOTA, konstanta_HODNOTA odkaz, příkaz·větev 경계를 검사하고, Provést_příkaz 중 operand_Štos formát_HODNOTA·místní_obor inicializovat·pole_HODNOTA dolní_index_HODNOTA·objekt_HODNOTA 참조를 검사한다. uživatelský_prostor 코드의 페이지·hardware_port 접근은 기존 ring 3 경계로 보호한다.

일반 성공은 `Exit: 0`, kompilovat_zdroj·JVM 오류는 `Exit: 1`, příkaz argumenty 오류는 `Exit: 2`다. CPU časová_hodnota 상한은 기존 `Exit: 124`이며, uživatelský_prostor ELF 자체의 CPU/런타임 오류는 기존 Konec_program 코드를 따른다. selhání_HODNOTA 후 셸에서 다른 프로그램을 계속 실행할 číslo 있다.

## implementace 위치와 zkoušky

- `os/uživatelský_prostor/자바/자바컴파일러.java`: 게스트 어휘·구문·TYP_HODNOTA 검사, konstanta_HODNOTA 풀 및 바이트코드 generovat.
- `os/uživatelský_prostor/자바/자바가상기계.java`: Třída_HODNOTA 적재, operand_Štos·프레임·objekt_HODNOTA Store_HODNOTA, příkaz 해석과 제한된 표준 호출.
- `os/zdrojový_soubor/Paměť_systém_souborů.java`: Paměť_data systém_souborů, úprava_HODNOTA, spuštění_stroje název_souboru 적재.
- `os/zdrojový_soubor/systémové_volání.java`, `compiler/START_uživatel_program.s`: název_souboru/문자 výstupní_pozice API와 uživatelský_prostor ukazatel 검사.
- `os/nástroje/자바파일묶기.py`: hostit vstup_HODNOTA název_souboru ověřit_5fb2b747·spuštění_stroje Skupina_HODNOTA generovat.

```sh
make test-java
make test
```

`os/zkoušky/자바시험.py`는 ELF/ISO spuštění_stroje, 게스트 kompilovat_zdroj·Provést_příkaz, uživatelský_prostor vstup_HODNOTA, 재귀·반복문·integer 극값·řetězec_HODNOTA 결합·단락 평가, 재실행, zdroj_strom chyba 후 기존 Třída_HODNOTA 보존, pole_HODNOTA/číslo 해독 chyba, 무한 sprint_HODNOTA 제한, úprava_HODNOTA 넘침과 název_souboru 부족을 검사한다. 게스트 generovat 클래스의 바이트를 QEMU 메모리에서 꺼내 OpenJDK `java -Xverify:all`로 실행하고 결과를 대조한다. 반대 방향으로 hostit OpenJDK의 Třída_HODNOTA, integer 배열과 한글 상수를 게스트에 적재하며, 손상된 název_souboru značka_HODNOTA_7e8f90bd·버전·konstanta_HODNOTA číslo·větev·스택을 거부하는지도 검사한다. 기록은 `os/build/자바시험.json`에 남는다. 디스크 없는 별도 zkoušky VM만 생성하고 종료한다.

implementace 형식의 참고 data: Oracle [JVM Třída_HODNOTA název_souboru 명세](https://docs.oracle.com/javase/specs/jvms/se8/html/jvms-4.html), [JVM příkaz 명세](https://docs.oracle.com/javase/specs/jvms/se8/html/jvms-6.html).

## Java název_souboru vstup_a_výstup

[FileDemo.java](../posix-kor/자바예제/FileDemo.java)는 일반 Java 표준 Třída_HODNOTA 이름을 사용한다. 소스를 `edit FileDemo.java`로 입력하거나 `JAVA_FILES`로 spuštění_stroje 이미지에 넣은 BACK_HODNOTA `javac FileDemo.java`, `java FileDemo`를 실행한다. 결과는 `65`, `255`, `66`, `-1`, `JAVA FILE IO PASS`다. `write(int)`는 하위 8비트를 쓰고 `read()`는 0~255 또는 EOF -1을 반환한다. výchozí_hodnota výstupní_pozice 생성자는 내용을 비우고, boolean 인수가 true이면 이어쓴다.

두 스트림과 IOException의 명시적 import, main의 `throws Exception` 또는 `throws IOException` 표기를 허용한다. výjimka objekt_HODNOTA·try/catch·try-with-resources는 지원하지 않으며 název_souboru 오류를 진단하고 프로그램을 종료한다. pole_HODNOTA vstup_a_výstup, InputStream/OutputStream으로의 다형성, Reader/Writer, getFD, 일반 název_souboru 메타데이터 API는 아직 없다. close는 열린 서술자를 닫고, 재부팅 보존에는 prostředí `sync`가 필요하다. 예제의 název_souboru 이름은 dobrá_zboží 셸과 파일체계에 맞춰 ASCII로 쓴다.

`os/zkoušky/자바파일시험.py`는 skutečný_data 게스트 kompilovat_zdroj 결과를 OpenJDK `-Xverify:all`로 zkusit_znovu_HODNOTA 실행해 název_souboru 바이트와 출력을 대조한다. 범위와 Store_HODNOTA média_HODNOTA 사용법은 [posix-kor 안내](../posix-kor/안내.md)를 참고한다. 참고한 표준 API는 Oracle [FileOutputStream](https://docs.oracle.com/javase/8/docs/api/java/io/FileOutputStream.html)이다.
