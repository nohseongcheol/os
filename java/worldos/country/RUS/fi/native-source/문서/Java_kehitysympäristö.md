# jkoros 안에서 Java kääntää_lähde·Suorita_komento

이 문서의 koneen_käynnistys·liittymä·Store_ARVO 명령은 **x86 versio_ARVO** 기준이다. 공유 Java kääntäjä/JVM은 [oma ARM64 Pi4 versio_ARVO](../platforms/rpi4-native/README.md)에도 연결되어 있다. ARM64에서는 UTF-8 UART syöte_ARVO·한글 tiedostonimi_SMS, `edit`의 단독 `.` Store_ARVO, 16개 RAM tiedoston_nimi, 약 2초 Suorita_komento 제한을 사용한다.

`javac FILE.java`와 `java CLASS [ARGS]`를 네이티브 jkoros 셸에서 실행한다. 컴파일러와 JVM은 각각 독립 ELF로 적재되어 ring 3에서 동작한다. 소스를 게스트에서 읽어 todellinen_data JVM `.class` 파일을 만들고, 그 파일의 바이트코드를 게스트 JVM이 해석한다. isäntä kääntää_lähde 서버나 Linux 게스트는 사용하지 않는다.

**nykyinen_kohde 구현은 oma 제한형 kääntäjä·JVM이다. OpenJDK/JDK 전체를 이식하거나 설치한 것이 아니며 Java SE 호환 환경도 아니다.** 표준 라이브러리는 아래의 일부 호출을 구현한 것이다. `java -version`과 `javac -version`에도 이 범위를 표시한다. 일반 JAR, Maven/Gradle, 임의의 Java ohjelma_f5044b9b 실행은 아직 지원하지 않는다.

## 바로 Suorita_komento

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

ISO는 `os/build/kernel.iso`다. 기존 VirtualBox 실행기도 같은 ISO를 사용한다. Suorita_komento 중이거나 저장된 VM에는 새 ISO가 자동 반영되지 않는다. 새 koneen_käynnistys 절차는 [VirtualBox Suorita_komento Lueminut_eb81d7d9](가상상자실행.md)를 따른다. 이 변경의 Java 자동 시험은 QEMU에서 수행했다.

## 직접 작성

`edit`는 tiedoston_nimi 전체를 새 내용으로 작성한다. 기존 내용의 syöterivi muutos_ARVO 기능은 아니다. `.save`로 저장하고 `.cancel`로 취소한다.

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

- `ls`: 파일과 tavu_ARVO numero näyttää_ARVO.
- `cat FILE`: tiedoston_nimi Sisältö_ARVO näyttää_ARVO. 텍스트 소스에 사용한다.
- `rm FILE`: Muisti_data tiedoston_nimi 삭제.
- `edit FILE`: 전체 내용을 새로 syöte_ARVO. 빈 파일도 저장할 numero 있다.
- 구문·TYYPPI_ARVO 검사 virhe_ARVO 시 기존 `.class`는 유지된다. 소스를 고친 BACK_ARVO 컴파일이 실패했다면 Edellinen_kohde Suorita_komento 파일이 남아 있으므로 kääntää_lähde 성공 여부를 확인한다.

파일은 RAM에서 동작한다. 전용 Store_ARVO 매체가 없거나 `sync`하지 않은 내용은 재부팅하면 사라진다. `make -C os run-store`로 연결한 매체에는 `sync`로 lähde_puu·Luokka_ARVO·data 파일을 보존할 numero 있다. 최대 8개, 파일마다 16KiB, tiedoston_nimi 이름은 ASCII 1~63자다. lähde_puu 이름은 `.class` 확장자 OSOITE_alue 때문에 최대 62자다. muutos_ARVO 입력은 ASCII이고 한 syöterivi 최대 128자다. syöterivi 또는 tiedoston_nimi 한도를 넘긴 편집은 `.save`에서 거부하여 기존 파일을 보존한다. ydin_ARVO/kääntäjä/JVM 구현의 Java 식별자는 한국어이며, nykyinen_kohde 게스트 syöte_ARVO 제한 때문에 käyttäjätila 예제 이름은 ASCII로 작성한다.

## ulkoinen_ARVO tiedoston_nimi 적재

호스트에서 만든 소스나 Tuki_ARVO leikata 안의 `.class`를 koneen_käynnistys 이미지에 포함할 numero 있다. `JAVA_FILES`는 `게스트이름=호스트경로` 목록이다. 아래의 경로는 예시이며 todellinen_data 파일의 절대 경로로 바꾼다. 공백 없는 경로를 사용한다.

```sh
# isäntä JDK로 컴파일한 클래스도 사용할 numero 있다.
javac --release 8 /tmp/Demo.java
make -C /home/user/jkoros iso \
  JAVA_FILES='Demo.java=/tmp/Demo.java Demo.class=/tmp/Demo.class'
make -C /home/user/jkoros run \
  JAVA_FILES='Demo.java=/tmp/Demo.java Demo.class=/tmp/Demo.class'
```

새 koneen_käynnistys 후 `java Demo 12`를 실행한다. 소스만 넣었으면 게스트에서 `javac Demo.java`부터 실행한다. `JAVA_FILES`를 생략한 Seuraava_kohde 빌드에서는 liitä_merkintä 파일을 포함하지 않는다. tiedoston_nimi Sisältö_ARVO 변경과 merkintä_luettelo 제거도 Seuraava_kohde 빌드에 반영된다. 원본 isäntä 파일에는 쓰지 않는다. oletusarvo `Hello.java`까지 합해 8개이며, 같은 이름을 명시하면 oletusarvo 예제를 대체한다. 새 `.class`를 저장할 빈 슬롯도 남겨 둔다.

`--release 8`은 Luokka_ARVO tiedoston_nimi 버전을 맞추는 옵션이다. 사용하는 문법·바이트코드·라이브러리도 아래 Tuki_ARVO leikata 안에 있어야 한다.

## Tuki_ARVO leikata

| 기능 | 게스트 javac | 게스트 JVM |
| --- | --- | --- |
| Luokka_ARVO | 패키지 없는 단일 Luokka_ARVO, staattinen_ARVO funktio_ARVO, 재귀, argumentit/palauttaa_KR | 실행마다 단일 Luokka_ARVO 적재, public static main(String[]) |
| oletusarvo ARVO | int, boolean, char, String, main의 String[] argumentit | kokonaisluku·viite operandi_Pino, String, int[], String[], 내부 StringBuilder |
| lauseke_ARVO | 초기값 있는 paikallinen_laajuus esittely, tehtävä_ARVO, `+=`, `-=`, `*=`, `/=`, `%=`, 후위 ++/--, 블록, if/else, while, for, return | 해당 kokonaisluku·viite 바이트코드와 ehto haara |
| lauseke_ARVO_eb3593ac | 십진 kokonaisluku, UTF-8 소스의 merkkijono_ARVO/문자, + - * / %, 비교, ==/!=, !/&&/\|\|, merkkijono_ARVO 결합 | kokonaisluku leikkaus_ARVO·bitti_ARVO leikkaus_ARVO·TYYPPI_ARVO MUUNNA_ARVO, 단락 평가, MATRIISI_ARVO pääsy_merkintä_68aed533 |
| tiedoston_nimi | FileInputStream(String), FileOutputStream(String[, boolean]), read()/write(int)/close() | todellinen_data ydin_ARVO 파일서술자와 Yhdistä, generoida·selvittää_Sisällys·이어쓰기·EOF |
| tulostuspaikka | System.out.print/println: int/boolean/char/String, println() | 동일 |
| merkkijono_ARVO/argumentit | String.length(), args.length, args[index], Integer.parseInt | 추가로 String.charAt(), merkkijono_ARVO 상수의 modified UTF-8 해독 |

선언은 지원하는 문법만 허용한다. 여러 변수를 한 선언에 나열하기, 초기값 없는 paikallinen_laajuus esittely, 오버로드, 임의 TYYPPI_ARVO MUUNNA_ARVO, MATRIISI_ARVO generoida lähdetiedosto, 8/16진 리터럴, Unicode lähde_puu 이스케이프 등은 미지원이다. `char`는 문자 리터럴로 초기화하며 일반 JDK의 모든 vakio_ARVO 축소 변환을 구현하지 않는다. ulkoinen_ARVO `.class`의 `int[]` generoida/Luku/쓰기는 지원하므로 isäntä `javac --release 8`로 만든 MATRIISI_ARVO 예제는 실행할 numero 있다.

objekti_ARVO kentän_arvo·일반 objekti_ARVO generoida·상속·인터페이스·여러 Luokka_ARVO Yhdistä, long/float/double, poikkeus prosessi_ARVO_merkintä, 스레드·모니터, 리플렉션, JNI, JIT, GC, 위 표에 없는 `java.io`와 `java.nio`/`java.net` 일반 API, 컬렉션, JAR와 클래스패스는 미지원이다. 런타임 오류는 Java poikkeus 객체를 던지지 않고 진단 후 nykyinen_kohde 프로그램을 종료한다. 객체와 merkkijono_ARVO Store_ARVO 공간은 Suorita_komento Lopeta_ohjelma 시 käyttäjätila alue_ARVO_0e9a97ab 전체와 함께 회수한다. 지속 Suorita_komento 중 GC는 없다.

## Suorita_komento 한도와 VIRHE

| resurssi_ARVO | 한도 |
| --- | --- |
| lähde_puu/Luokka_ARVO tiedoston_nimi | 각각 16KiB |
| kääntäjä | tunnus_ARVO_eb540501 2,047개, generoida KOODI_ARVO 4KiB, vakio_ARVO 풀 4KiB |
| funktio_ARVO/argumentit | 클래스당 32함수, 함수당 16인수 |
| JVM vakio_ARVO | 511개 |
| JVM funktio_ARVO KOODI_ARVO | 함수당 8KiB |
| JVM 호출/operandi_Pino/paikallinen_laajuus muuttuja_ARVO | 32프레임, 프레임당 operandi_Pino 128칸·paikallinen_laajuus 128칸 |
| JVM objekti_ARVO Store_ARVO OSOITE_alue | 8,192개 32비트 paikka_merkintä, 헤더 esittelyt 약 32KiB |
| Suorita_komento | 최대 500,000 komento, 기존 커널의 약 3초 CPU Suorita_komento 상한도 적용 |

게스트 컴파일러는 버전 49.0 `.class`를 생성하며 JVM은 45.0~52.0 중 Tuki_ARVO 명령으로 구성된 파일을 읽는다. 스택맵을 이용한 완전한 JVM sanakirja 검증기를 구현한 것은 아니다. tiedoston_nimi/määritteen_arvo kesto_ARVO, vakio_ARVO viite, komento·haara 경계를 검사하고, Suorita_komento 중 operandi_Pino muoto_ARVO·paikallinen_laajuus alustaa·MATRIISI_ARVO alaindeksi_ARVO·objekti_ARVO 참조를 검사한다. käyttäjätila 코드의 페이지·laitteisto_portti 접근은 기존 ring 3 경계로 보호한다.

일반 성공은 `Exit: 0`, kääntää_lähde·JVM 오류는 `Exit: 1`, komento argumentit 오류는 `Exit: 2`다. CPU AIKA_ARVO 상한은 기존 `Exit: 124`이며, käyttäjätila ELF 자체의 CPU/런타임 오류는 기존 Lopeta_ohjelma 코드를 따른다. virhe_ARVO 후 셸에서 다른 프로그램을 계속 실행할 numero 있다.

## toteutus 위치와 testit

- `os/käyttäjätila/자바/자바컴파일러.java`: 게스트 어휘·구문·TYYPPI_ARVO 검사, vakio_ARVO 풀 및 바이트코드 generoida.
- `os/käyttäjätila/자바/자바가상기계.java`: Luokka_ARVO 적재, operandi_Pino·프레임·objekti_ARVO Store_ARVO, komento 해석과 제한된 표준 호출.
- `os/lähdetiedosto/Muisti_tiedostojärjestelmä.java`: Muisti_data tiedostojärjestelmä, muutos_ARVO, koneen_käynnistys tiedoston_nimi 적재.
- `os/lähdetiedosto/järjestelmäkutsu.java`, `compiler/alku_käyttäjä_ohjelma.s`: tiedoston_nimi/문자 tulostuspaikka API와 käyttäjätila osoitin 검사.
- `os/työkalut/자바파일묶기.py`: isäntä syöte_ARVO tiedoston_nimi vahvista·koneen_käynnistys Ryhmä_ARVO generoida.

```sh
make test-java
make test
```

`os/testit/자바시험.py`는 ELF/ISO koneen_käynnistys, 게스트 kääntää_lähde·Suorita_komento, käyttäjätila syöte_ARVO, 재귀·반복문·kokonaisluku 극값·merkkijono_ARVO 결합·단락 평가, 재실행, lähde_puu VIRHE 후 기존 Luokka_ARVO 보존, MATRIISI_ARVO/numero 해독 VIRHE, 무한 sprintti_ARVO 제한, muutos_ARVO 넘침과 tiedoston_nimi 부족을 검사한다. 게스트 generoida 클래스의 바이트를 QEMU 메모리에서 꺼내 OpenJDK `java -Xverify:all`로 실행하고 결과를 대조한다. 반대 방향으로 isäntä OpenJDK의 Luokka_ARVO, kokonaisluku 배열과 한글 상수를 게스트에 적재하며, 손상된 tiedoston_nimi merkintä_ARVO·버전·vakio_ARVO numero·haara·스택을 거부하는지도 검사한다. 기록은 `os/build/자바시험.json`에 남는다. 디스크 없는 별도 testit VM만 생성하고 종료한다.

toteutus 형식의 참고 data: Oracle [JVM Luokka_ARVO tiedoston_nimi määritys](https://docs.oracle.com/javase/specs/jvms/se8/html/jvms-4.html), [JVM komento määritys](https://docs.oracle.com/javase/specs/jvms/se8/html/jvms-6.html).

## Java tiedoston_nimi I_O

[FileDemo.java](../posix-kor/자바예제/FileDemo.java)는 일반 Java 표준 Luokka_ARVO 이름을 사용한다. 소스를 `edit FileDemo.java`로 입력하거나 `JAVA_FILES`로 koneen_käynnistys 이미지에 넣은 BACK_ARVO `javac FileDemo.java`, `java FileDemo`를 실행한다. 결과는 `65`, `255`, `66`, `-1`, `JAVA FILE IO PASS`다. `write(int)`는 하위 8비트를 쓰고 `read()`는 0~255 또는 EOF -1을 반환한다. oletusarvo tulostuspaikka 생성자는 내용을 비우고, boolean 인수가 true이면 이어쓴다.

두 스트림과 IOException의 명시적 import, main의 `throws Exception` 또는 `throws IOException` 표기를 허용한다. poikkeus objekti_ARVO·try/catch·try-with-resources는 지원하지 않으며 tiedoston_nimi 오류를 진단하고 프로그램을 종료한다. MATRIISI_ARVO I_O, InputStream/OutputStream으로의 다형성, Reader/Writer, getFD, 일반 tiedoston_nimi 메타데이터 API는 아직 없다. close는 열린 서술자를 닫고, 재부팅 보존에는 liittymä `sync`가 필요하다. 예제의 tiedoston_nimi 이름은 nykyinen_kohde 셸과 파일체계에 맞춰 ASCII로 쓴다.

`os/testit/자바파일시험.py`는 todellinen_data 게스트 kääntää_lähde 결과를 OpenJDK `-Xverify:all`로 yrittää_uudelleen_ARVO 실행해 tiedoston_nimi 바이트와 출력을 대조한다. 범위와 Store_ARVO tietoväline_ARVO 사용법은 [posix-kor Lueminut_eb81d7d9](../posix-kor/Lueminut_eb81d7d9.md)를 참고한다. 참고한 표준 API는 Oracle [FileOutputStream](https://docs.oracle.com/javase/8/docs/api/java/io/FileOutputStream.html)이다.
