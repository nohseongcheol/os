# jkoros 안에서 Java kompilere_kilde·Utfør_kommando

이 문서의 부팅·Shell·Store_VERDI 명령은 **x86 versjon_VERDI** 기준이다. 공유 Java kompilator/JVM은 [eget ARM64 Pi4 versjon_VERDI](../platforms/rpi4-native/README.md)에도 연결되어 있다. ARM64에서는 UTF-8 UART inndata_VERDI·한글 filnavn_SMS, `edit`의 단독 `.` Store_VERDI, 16개 RAM Fil, 약 2초 Utfør_kommando 제한을 사용한다.

`javac FILE.java`와 `java CLASS [ARGS]`를 네이티브 jkoros 셸에서 실행한다. 컴파일러와 JVM은 각각 독립 ELF로 적재되어 ring 3에서 동작한다. 소스를 게스트에서 읽어 faktisk_data JVM `.class` 파일을 만들고, 그 파일의 바이트코드를 게스트 JVM이 해석한다. vert kompilere_kilde 서버나 Linux 게스트는 사용하지 않는다.

**betalt_vare 구현은 eget 제한형 kompilator·JVM이다. OpenJDK/JDK 전체를 이식하거나 설치한 것이 아니며 Java SE 호환 환경도 아니다.** 표준 라이브러리는 아래의 일부 호출을 구현한 것이다. `java -version`과 `javac -version`에도 이 범위를 표시한다. 일반 JAR, Maven/Gradle, 임의의 Java app_f5044b9b 실행은 아직 지원하지 않는다.

## 바로 Utfør_kommando

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

ISO는 `os/build/kernel.iso`다. 기존 VirtualBox 실행기도 같은 ISO를 사용한다. Utfør_kommando 중이거나 저장된 VM에는 새 ISO가 자동 반영되지 않는다. 새 부팅 절차는 [VirtualBox Utfør_kommando Viktig_fil_eb81d7d9](가상상자실행.md)를 따른다. 이 변경의 Java 자동 시험은 QEMU에서 수행했다.

## 직접 작성

`edit`는 Fil 전체를 새 내용으로 작성한다. 기존 내용의 Linje Rediger_VERDI 기능은 아니다. `.save`로 저장하고 `.cancel`로 취소한다.

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

- `ls`: 파일과 byte_VERDI nummer vise_VERDI_487749b8.
- `cat FILE`: Fil Innhold_VERDI vise_VERDI_487749b8. 텍스트 소스에 사용한다.
- `rm FILE`: Minne_data Fil 삭제.
- `edit FILE`: 전체 내용을 새로 inndata_VERDI. 빈 파일도 저장할 nummer 있다.
- 구문·Type_VERDI 검사 feil_VERDI 시 기존 `.class`는 유지된다. 소스를 고친 TILBAKE_VERDI 컴파일이 실패했다면 Forrige_vare Utfør_kommando 파일이 남아 있으므로 kompilere_kilde 성공 여부를 확인한다.

파일은 RAM에서 동작한다. 전용 Store_VERDI 매체가 없거나 `sync`하지 않은 내용은 재부팅하면 사라진다. `make -C os run-store`로 연결한 매체에는 `sync`로 kilde_tre·time_VERDI·data 파일을 보존할 nummer 있다. 최대 8개, 파일마다 16KiB, Fil 이름은 ASCII 1~63자다. kilde_tre 이름은 `.class` 확장자 e_post_område 때문에 최대 62자다. Rediger_VERDI 입력은 ASCII이고 한 Linje 최대 128자다. Linje 또는 Fil 한도를 넘긴 편집은 `.save`에서 거부하여 기존 파일을 보존한다. kjerne_VERDI/kompilator/JVM 구현의 Java 식별자는 한국어이며, betalt_vare 게스트 inndata_VERDI 제한 때문에 bruker 예제 이름은 ASCII로 작성한다.

## ekstern_VERDI Fil 적재

호스트에서 만든 소스나 støtte_VERDI klippe 안의 `.class`를 부팅 이미지에 포함할 nummer 있다. `JAVA_FILES`는 `게스트이름=호스트경로` 목록이다. 아래의 경로는 예시이며 faktisk_data 파일의 절대 경로로 바꾼다. 공백 없는 경로를 사용한다.

```sh
# vert JDK로 컴파일한 클래스도 사용할 nummer 있다.
javac --release 8 /tmp/Demo.java
make -C /home/user/jkoros iso \
  JAVA_FILES='Demo.java=/tmp/Demo.java Demo.class=/tmp/Demo.class'
make -C /home/user/jkoros run \
  JAVA_FILES='Demo.java=/tmp/Demo.java Demo.class=/tmp/Demo.class'
```

새 부팅 후 `java Demo 12`를 실행한다. 소스만 넣었으면 게스트에서 `javac Demo.java`부터 실행한다. `JAVA_FILES`를 생략한 Neste_vare 빌드에서는 Tilføye_oppføring 파일을 포함하지 않는다. Fil Innhold_VERDI 변경과 oppføring_Liste 제거도 Neste_vare 빌드에 반영된다. 원본 vert 파일에는 쓰지 않는다. standardverdi `Hello.java`까지 합해 8개이며, 같은 이름을 명시하면 standardverdi 예제를 대체한다. 새 `.class`를 저장할 빈 슬롯도 남겨 둔다.

`--release 8`은 time_VERDI Fil 버전을 맞추는 옵션이다. 사용하는 문법·바이트코드·라이브러리도 아래 støtte_VERDI klippe 안에 있어야 한다.

## støtte_VERDI klippe

| 기능 | 게스트 javac | 게스트 JVM |
| --- | --- | --- |
| time_VERDI | 패키지 없는 단일 time_VERDI, statisk_VERDI FUNKSJON_VERDI, 재귀, Argumenter/return_KR | 실행마다 단일 time_VERDI 적재, public static main(String[]) |
| standardverdi VERDI | int, boolean, char, String, main의 String[] Argumenter | heltall·referere operand_stakk, String, int[], String[], 내부 StringBuilder |
| kontoutdrag_VERDI | 초기값 있는 lokal_Omfang erklæring, oppgave_VERDI, `+=`, `-=`, `*=`, `/=`, `%=`, 후위 ++/--, 블록, if/else, while, for, return | 해당 heltall·referere 바이트코드와 vilkår gren |
| uttrykk_VERDI | 십진 heltall, UTF-8 소스의 streng_VERDI/문자, + - * / %, 비교, ==/!=, !/&&/\|\|, streng_VERDI 결합 | heltall operasjon_VERDI·bit_VERDI operasjon_VERDI·Type_VERDI KONVERTER_VERDI, 단락 평가, MATRISE_VERDI tilgang_oppføring |
| Fil | FileInputStream(String), FileOutputStream(String[, boolean]), read()/write(int)/close() | faktisk_data kjerne_VERDI 파일서술자와 Koble_til, generere·tømme_Innhold·이어쓰기·EOF |
| Utgang | System.out.print/println: int/boolean/char/String, println() | 동일 |
| streng_VERDI/Argumenter | String.length(), args.length, args[index], Integer.parseInt | 추가로 String.charAt(), streng_VERDI 상수의 modified UTF-8 해독 |

선언은 지원하는 문법만 허용한다. 여러 변수를 한 선언에 나열하기, 초기값 없는 lokal_Omfang erklæring, 오버로드, 임의 Type_VERDI KONVERTER_VERDI, MATRISE_VERDI generere KILDE, 8/16진 리터럴, Unicode kilde_tre 이스케이프 등은 미지원이다. `char`는 문자 리터럴로 초기화하며 일반 JDK의 모든 konstant_VERDI 축소 변환을 구현하지 않는다. ekstern_VERDI `.class`의 `int[]` generere/Les/쓰기는 지원하므로 vert `javac --release 8`로 만든 MATRISE_VERDI 예제는 실행할 nummer 있다.

objekt_VERDI feltverdi·일반 objekt_VERDI generere·상속·인터페이스·여러 time_VERDI Koble_til, long/float/double, unntak Prosess_VERDI_oppføring, 스레드·모니터, 리플렉션, JNI, JIT, GC, 위 표에 없는 `java.io`와 `java.nio`/`java.net` 일반 API, 컬렉션, JAR와 클래스패스는 미지원이다. 런타임 오류는 Java unntak 객체를 던지지 않고 진단 후 betalt_vare 프로그램을 종료한다. 객체와 streng_VERDI Store_VERDI 공간은 Utfør_kommando Utgang_app 시 bruker område_VERDI_0e9a97ab 전체와 함께 회수한다. 지속 Utfør_kommando 중 GC는 없다.

## Utfør_kommando 한도와 feil

| ressurs_VERDI | 한도 |
| --- | --- |
| kilde_tre/time_VERDI Fil | 각각 16KiB |
| kompilator | token_VERDI 2,047개, generere KODE_VERDI 4KiB, konstant_VERDI 풀 4KiB |
| FUNKSJON_VERDI/Argumenter | 클래스당 32함수, 함수당 16인수 |
| JVM konstant_VERDI | 511개 |
| JVM FUNKSJON_VERDI KODE_VERDI | 함수당 8KiB |
| JVM 호출/operand_stakk/lokal_Omfang variabel_VERDI | 32프레임, 프레임당 operand_stakk 128칸·lokal_Omfang 128칸 |
| JVM objekt_VERDI Store_VERDI e_post_område | 8,192개 32비트 åpning_oppføring, 헤더 포함 약 32KiB |
| Utfør_kommando | 최대 500,000 Kommando, 기존 커널의 약 3초 CPU Utfør_kommando 상한도 적용 |

게스트 컴파일러는 버전 49.0 `.class`를 생성하며 JVM은 45.0~52.0 중 støtte_VERDI 명령으로 구성된 파일을 읽는다. 스택맵을 이용한 완전한 JVM ordliste 검증기를 구현한 것은 아니다. Fil/attributtverdi lengde_VERDI, konstant_VERDI referere, Kommando·gren 경계를 검사하고, Utfør_kommando 중 operand_stakk format_VERDI·lokal_Omfang starte·MATRISE_VERDI senket_skrift_VERDI·objekt_VERDI 참조를 검사한다. bruker 코드의 페이지·maskinvare_port 접근은 기존 ring 3 경계로 보호한다.

일반 성공은 `Exit: 0`, kompilere_kilde·JVM 오류는 `Exit: 1`, Kommando Argumenter 오류는 `Exit: 2`다. CPU TID_VERDI 상한은 기존 `Exit: 124`이며, bruker ELF 자체의 CPU/런타임 오류는 기존 Utgang_app 코드를 따른다. feil_VERDI 후 셸에서 다른 프로그램을 계속 실행할 nummer 있다.

## 구현 위치와 시험

- `os/bruker/자바/자바컴파일러.java`: 게스트 어휘·구문·Type_VERDI 검사, konstant_VERDI 풀 및 바이트코드 generere.
- `os/bruker/자바/자바가상기계.java`: time_VERDI 적재, operand_stakk·프레임·objekt_VERDI Store_VERDI, Kommando 해석과 제한된 표준 호출.
- `os/KILDE/Minne_filsystem.java`: Minne_data filsystem, Rediger_VERDI, 부팅 Fil 적재.
- `os/KILDE/체계호출.java`, `compiler/START_bruker_app.s`: Fil/문자 Utgang API와 bruker peker 검사.
- `os/Verktøy/자바파일묶기.py`: vert inndata_VERDI Fil bekrefte_5fb2b747·부팅 gruppe_VERDI generere.

```sh
make test-java
make test
```

`os/시험/자바시험.py`는 ELF/ISO 부팅, 게스트 kompilere_kilde·Utfør_kommando, bruker inndata_VERDI, 재귀·반복문·heltall 극값·streng_VERDI 결합·단락 평가, 재실행, kilde_tre feil 후 기존 time_VERDI 보존, MATRISE_VERDI/nummer 해독 feil, 무한 sprint_VERDI 제한, Rediger_VERDI 넘침과 Fil 부족을 검사한다. 게스트 generere 클래스의 바이트를 QEMU 메모리에서 꺼내 OpenJDK `java -Xverify:all`로 실행하고 결과를 대조한다. 반대 방향으로 vert OpenJDK의 time_VERDI, heltall 배열과 한글 상수를 게스트에 적재하며, 손상된 Fil tusj_VERDI·버전·konstant_VERDI nummer·gren·스택을 거부하는지도 검사한다. 기록은 `os/build/자바시험.json`에 남는다. 디스크 없는 별도 시험 VM만 생성하고 종료한다.

구현 형식의 참고 data: Oracle [JVM time_VERDI Fil 명세](https://docs.oracle.com/javase/specs/jvms/se8/html/jvms-4.html), [JVM Kommando 명세](https://docs.oracle.com/javase/specs/jvms/se8/html/jvms-6.html).

## Java Fil I_U

[FileDemo.java](../posix-kor/자바예제/FileDemo.java)는 일반 Java 표준 time_VERDI 이름을 사용한다. 소스를 `edit FileDemo.java`로 입력하거나 `JAVA_FILES`로 부팅 이미지에 넣은 TILBAKE_VERDI `javac FileDemo.java`, `java FileDemo`를 실행한다. 결과는 `65`, `255`, `66`, `-1`, `JAVA FILE IO PASS`다. `write(int)`는 하위 8비트를 쓰고 `read()`는 0~255 또는 EOF -1을 반환한다. standardverdi Utgang 생성자는 내용을 비우고, boolean 인수가 true이면 이어쓴다.

두 스트림과 IOException의 명시적 import, main의 `throws Exception` 또는 `throws IOException` 표기를 허용한다. unntak objekt_VERDI·try/catch·try-with-resources는 지원하지 않으며 Fil 오류를 진단하고 프로그램을 종료한다. MATRISE_VERDI I_U, InputStream/OutputStream으로의 다형성, Reader/Writer, getFD, 일반 Fil 메타데이터 API는 아직 없다. close는 열린 서술자를 닫고, 재부팅 보존에는 Shell `sync`가 필요하다. 예제의 Fil 이름은 betalt_vare 셸과 파일체계에 맞춰 ASCII로 쓴다.

`os/시험/자바파일시험.py`는 faktisk_data 게스트 kompilere_kilde 결과를 OpenJDK `-Xverify:all`로 prøve_på_nytt_VERDI 실행해 Fil 바이트와 출력을 대조한다. 범위와 Store_VERDI media_VERDI 사용법은 [posix-kor Viktig_fil_eb81d7d9](../posix-kor/Viktig_fil_eb81d7d9.md)를 참고한다. 참고한 표준 API는 Oracle [FileOutputStream](https://docs.oracle.com/javase/8/docs/api/java/io/FileOutputStream.html)이다.
