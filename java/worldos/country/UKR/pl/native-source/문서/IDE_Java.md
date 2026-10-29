# jkoros 안에서 Java kompilować_źródło·Wykonaj_polecenie

이 문서의 rozruch_maszyny·powłoka·Store_WARTOŚĆ 명령은 **x86 wersja_WARTOŚĆ** 기준이다. 공유 Java kompilator/JVM은 [własny ARM64 Pi4 wersja_WARTOŚĆ](../platforms/rpi4-native/README.md)에도 연결되어 있다. ARM64에서는 UTF-8 UART wejście_WARTOŚĆ·한글 nazwa_pliku_SMS, `edit`의 단독 `.` Store_WARTOŚĆ, 16개 RAM nazwa_pliku, 약 2초 Wykonaj_polecenie 제한을 사용한다.

`javac FILE.java`와 `java CLASS [ARGS]`를 네이티브 jkoros 셸에서 실행한다. 컴파일러와 JVM은 각각 독립 ELF로 적재되어 ring 3에서 동작한다. 소스를 게스트에서 읽어 rzeczywisty_dane JVM `.class` 파일을 만들고, 그 파일의 바이트코드를 게스트 JVM이 해석한다. host kompilować_źródło 서버나 Linux 게스트는 사용하지 않는다.

**bieżący_towar 구현은 własny 제한형 kompilator·JVM이다. OpenJDK/JDK 전체를 이식하거나 설치한 것이 아니며 Java SE 호환 환경도 아니다.** 표준 라이브러리는 아래의 일부 호출을 구현한 것이다. `java -version`과 `javac -version`에도 이 범위를 표시한다. 일반 JAR, Maven/Gradle, 임의의 Java program_f5044b9b 실행은 아직 지원하지 않는다.

## 바로 Wykonaj_polecenie

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

ISO는 `os/build/kernel.iso`다. 기존 VirtualBox 실행기도 같은 ISO를 사용한다. Wykonaj_polecenie 중이거나 저장된 VM에는 새 ISO가 자동 반영되지 않는다. 새 rozruch_maszyny 절차는 [VirtualBox Wykonaj_polecenie plik_README_eb81d7d9](가상상자실행.md)를 따른다. 이 변경의 Java 자동 시험은 QEMU에서 수행했다.

## 직접 작성

`edit`는 nazwa_pliku 전체를 새 내용으로 작성한다. 기존 내용의 wiersz_wejścia Edytuj_WARTOŚĆ 기능은 아니다. `.save`로 저장하고 `.cancel`로 취소한다.

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

- `ls`: 파일과 bajt_WARTOŚĆ identyfikator program_WARTOŚĆ.
- `cat FILE`: nazwa_pliku treść_WARTOŚĆ_cb0f2404 program_WARTOŚĆ. 텍스트 소스에 사용한다.
- `rm FILE`: Pamięć_dane nazwa_pliku 삭제.
- `edit FILE`: 전체 내용을 새로 wejście_WARTOŚĆ. 빈 파일도 저장할 identyfikator 있다.
- 구문·TYP_WARTOŚĆ 검사 awaria_WARTOŚĆ 시 기존 `.class`는 유지된다. 소스를 고친 BACK_WARTOŚĆ 컴파일이 실패했다면 Wstecz_towar Wykonaj_polecenie 파일이 남아 있으므로 kompilować_źródło 성공 여부를 확인한다.

파일은 RAM에서 동작한다. 전용 Store_WARTOŚĆ 매체가 없거나 `sync`하지 않은 내용은 재부팅하면 사라진다. `make -C os run-store`로 연결한 매체에는 `sync`로 źródło_drzewo·Klasa_WARTOŚĆ·dane 파일을 보존할 identyfikator 있다. 최대 8개, 파일마다 16KiB, nazwa_pliku 이름은 ASCII 1~63자다. źródło_drzewo 이름은 `.class` 확장자 ADRES_region 때문에 최대 62자다. Edytuj_WARTOŚĆ 입력은 ASCII이고 한 wiersz_wejścia 최대 128자다. wiersz_wejścia 또는 nazwa_pliku 한도를 넘긴 편집은 `.save`에서 거부하여 기존 파일을 보존한다. jądro_WARTOŚĆ/kompilator/JVM 구현의 Java 식별자는 한국어이며, bieżący_towar 게스트 wejście_WARTOŚĆ 제한 때문에 przestrzeń_użytkownika 예제 이름은 ASCII로 작성한다.

## zewnętrzny_WARTOŚĆ nazwa_pliku 적재

호스트에서 만든 소스나 wsparcie_WARTOŚĆ obcinać 안의 `.class`를 rozruch_maszyny 이미지에 포함할 identyfikator 있다. `JAVA_FILES`는 `게스트이름=호스트경로` 목록이다. 아래의 경로는 예시이며 rzeczywisty_dane 파일의 절대 경로로 바꾼다. 공백 없는 경로를 사용한다.

```sh
# host JDK로 컴파일한 클래스도 사용할 identyfikator 있다.
javac --release 8 /tmp/Demo.java
make -C /home/user/jkoros iso \
  JAVA_FILES='Demo.java=/tmp/Demo.java Demo.class=/tmp/Demo.class'
make -C /home/user/jkoros run \
  JAVA_FILES='Demo.java=/tmp/Demo.java Demo.class=/tmp/Demo.class'
```

새 rozruch_maszyny 후 `java Demo 12`를 실행한다. 소스만 넣었으면 게스트에서 `javac Demo.java`부터 실행한다. `JAVA_FILES`를 생략한 Dalej_towar 빌드에서는 dołączać_wpis 파일을 포함하지 않는다. nazwa_pliku treść_WARTOŚĆ_cb0f2404 변경과 wpis_Lista 제거도 Dalej_towar 빌드에 반영된다. 원본 host 파일에는 쓰지 않는다. wartość_domyślna `Hello.java`까지 합해 8개이며, 같은 이름을 명시하면 wartość_domyślna 예제를 대체한다. 새 `.class`를 저장할 빈 슬롯도 남겨 둔다.

`--release 8`은 Klasa_WARTOŚĆ nazwa_pliku 버전을 맞추는 옵션이다. 사용하는 문법·바이트코드·라이브러리도 아래 wsparcie_WARTOŚĆ obcinać 안에 있어야 한다.

## wsparcie_WARTOŚĆ obcinać

| 기능 | 게스트 javac | 게스트 JVM |
| --- | --- | --- |
| Klasa_WARTOŚĆ | 패키지 없는 단일 Klasa_WARTOŚĆ, statyczny_WARTOŚĆ FUNKCJA_WARTOŚĆ, 재귀, argumenty/Zwrot_KR | 실행마다 단일 Klasa_WARTOŚĆ 적재, public static main(String[]) |
| wartość_domyślna WARTOŚĆ | int, boolean, char, String, main의 String[] argumenty | liczba_całkowita·odwołanie operand_Stos, String, int[], String[], 내부 StringBuilder |
| wyciąg_WARTOŚĆ | 초기값 있는 lokalny_Scope deklaracja, zadanie_WARTOŚĆ, `+=`, `-=`, `*=`, `/=`, `%=`, 후위 ++/--, 블록, if/else, while, for, return | 해당 liczba_całkowita·odwołanie 바이트코드와 choroba gałąź_22e01337 |
| wyrażenie_WARTOŚĆ | 십진 liczba_całkowita, UTF-8 소스의 ciąg_WARTOŚĆ/문자, + - * / %, 비교, ==/!=, !/&&/\|\|, ciąg_WARTOŚĆ 결합 | liczba_całkowita zabieg_WARTOŚĆ·bit_WARTOŚĆ zabieg_WARTOŚĆ·TYP_WARTOŚĆ KONWERTUJ_WARTOŚĆ, 단락 평가, TABLICA_WARTOŚĆ dostęp_wpis |
| nazwa_pliku | FileInputStream(String), FileOutputStream(String[, boolean]), read()/write(int)/close() | rzeczywisty_dane jądro_WARTOŚĆ 파일서술자와 Połącz, generować·czyścić_Spis_treści·이어쓰기·EOF |
| pozycja_wyjścia | System.out.print/println: int/boolean/char/String, println() | 동일 |
| ciąg_WARTOŚĆ/argumenty | String.length(), args.length, args[index], Integer.parseInt | 추가로 String.charAt(), ciąg_WARTOŚĆ 상수의 modified UTF-8 해독 |

선언은 지원하는 문법만 허용한다. 여러 변수를 한 선언에 나열하기, 초기값 없는 lokalny_Scope deklaracja, 오버로드, 임의 TYP_WARTOŚĆ KONWERTUJ_WARTOŚĆ, TABLICA_WARTOŚĆ generować plik_źródłowy, 8/16진 리터럴, Unicode źródło_drzewo 이스케이프 등은 미지원이다. `char`는 문자 리터럴로 초기화하며 일반 JDK의 모든 stała_WARTOŚĆ 축소 변환을 구현하지 않는다. zewnętrzny_WARTOŚĆ `.class`의 `int[]` generować/Odczyt/쓰기는 지원하므로 host `javac --release 8`로 만든 TABLICA_WARTOŚĆ 예제는 실행할 identyfikator 있다.

obiekt_WARTOŚĆ wartość_pola·일반 obiekt_WARTOŚĆ generować·상속·인터페이스·여러 Klasa_WARTOŚĆ Połącz, long/float/double, wyjątek Proces_WARTOŚĆ_wpis, 스레드·모니터, 리플렉션, JNI, JIT, GC, 위 표에 없는 `java.io`와 `java.nio`/`java.net` 일반 API, 컬렉션, JAR와 클래스패스는 미지원이다. 런타임 오류는 Java wyjątek 객체를 던지지 않고 진단 후 bieżący_towar 프로그램을 종료한다. 객체와 ciąg_WARTOŚĆ Store_WARTOŚĆ 공간은 Wykonaj_polecenie wyjść_program 시 przestrzeń_użytkownika region_WARTOŚĆ 전체와 함께 회수한다. 지속 Wykonaj_polecenie 중 GC는 없다.

## Wykonaj_polecenie 한도와 błąd

| zasób_WARTOŚĆ | 한도 |
| --- | --- |
| źródło_drzewo/Klasa_WARTOŚĆ nazwa_pliku | 각각 16KiB |
| kompilator | token_WARTOŚĆ 2,047개, generować KOD_WARTOŚĆ 4KiB, stała_WARTOŚĆ 풀 4KiB |
| FUNKCJA_WARTOŚĆ/argumenty | 클래스당 32함수, 함수당 16인수 |
| JVM stała_WARTOŚĆ | 511개 |
| JVM FUNKCJA_WARTOŚĆ KOD_WARTOŚĆ | 함수당 8KiB |
| JVM 호출/operand_Stos/lokalny_Scope zmienna_WARTOŚĆ | 32프레임, 프레임당 operand_Stos 128칸·lokalny_Scope 128칸 |
| JVM obiekt_WARTOŚĆ Store_WARTOŚĆ ADRES_region | 8,192개 32비트 gniazdo_wpis, 헤더 deklaracje 약 32KiB |
| Wykonaj_polecenie | 최대 500,000 polecenie, 기존 커널의 약 3초 CPU Wykonaj_polecenie 상한도 적용 |

게스트 컴파일러는 버전 49.0 `.class`를 생성하며 JVM은 45.0~52.0 중 wsparcie_WARTOŚĆ 명령으로 구성된 파일을 읽는다. 스택맵을 이용한 완전한 JVM słownik 검증기를 구현한 것은 아니다. nazwa_pliku/wartość_atrybutu długość_WARTOŚĆ, stała_WARTOŚĆ odwołanie, polecenie·gałąź_22e01337 경계를 검사하고, Wykonaj_polecenie 중 operand_Stos format_WARTOŚĆ·lokalny_Scope inicjuj·TABLICA_WARTOŚĆ indeks_dolny_WARTOŚĆ·obiekt_WARTOŚĆ 참조를 검사한다. przestrzeń_użytkownika 코드의 페이지·sprzęt_port 접근은 기존 ring 3 경계로 보호한다.

일반 성공은 `Exit: 0`, kompilować_źródło·JVM 오류는 `Exit: 1`, polecenie argumenty 오류는 `Exit: 2`다. CPU wartość_czasu 상한은 기존 `Exit: 124`이며, przestrzeń_użytkownika ELF 자체의 CPU/런타임 오류는 기존 wyjść_program 코드를 따른다. awaria_WARTOŚĆ 후 셸에서 다른 프로그램을 계속 실행할 identyfikator 있다.

## implementacja 위치와 testy

- `os/przestrzeń_użytkownika/자바/자바컴파일러.java`: 게스트 어휘·구문·TYP_WARTOŚĆ 검사, stała_WARTOŚĆ 풀 및 바이트코드 generować.
- `os/przestrzeń_użytkownika/자바/자바가상기계.java`: Klasa_WARTOŚĆ 적재, operand_Stos·프레임·obiekt_WARTOŚĆ Store_WARTOŚĆ, polecenie 해석과 제한된 표준 호출.
- `os/plik_źródłowy/Pamięć_system_plików.java`: Pamięć_dane system_plików, Edytuj_WARTOŚĆ, rozruch_maszyny nazwa_pliku 적재.
- `os/plik_źródłowy/wywołanie_systemowe.java`, `compiler/START_użytkownik_program.s`: nazwa_pliku/문자 pozycja_wyjścia API와 przestrzeń_użytkownika wskaźnik 검사.
- `os/narzędzia/자바파일묶기.py`: host wejście_WARTOŚĆ nazwa_pliku walidować·rozruch_maszyny grupa_WARTOŚĆ generować.

```sh
make test-java
make test
```

`os/testy/자바시험.py`는 ELF/ISO rozruch_maszyny, 게스트 kompilować_źródło·Wykonaj_polecenie, przestrzeń_użytkownika wejście_WARTOŚĆ, 재귀·반복문·liczba_całkowita 극값·ciąg_WARTOŚĆ 결합·단락 평가, 재실행, źródło_drzewo błąd 후 기존 Klasa_WARTOŚĆ 보존, TABLICA_WARTOŚĆ/identyfikator 해독 błąd, 무한 iteracja_WARTOŚĆ 제한, Edytuj_WARTOŚĆ 넘침과 nazwa_pliku 부족을 검사한다. 게스트 generować 클래스의 바이트를 QEMU 메모리에서 꺼내 OpenJDK `java -Xverify:all`로 실행하고 결과를 대조한다. 반대 방향으로 host OpenJDK의 Klasa_WARTOŚĆ, liczba_całkowita 배열과 한글 상수를 게스트에 적재하며, 손상된 nazwa_pliku pisak_WARTOŚĆ·버전·stała_WARTOŚĆ identyfikator·gałąź_22e01337·스택을 거부하는지도 검사한다. 기록은 `os/build/자바시험.json`에 남는다. 디스크 없는 별도 testy VM만 생성하고 종료한다.

implementacja 형식의 참고 dane: Oracle [JVM Klasa_WARTOŚĆ nazwa_pliku 명세](https://docs.oracle.com/javase/specs/jvms/se8/html/jvms-4.html), [JVM polecenie 명세](https://docs.oracle.com/javase/specs/jvms/se8/html/jvms-6.html).

## Java nazwa_pliku We_Wy

[FileDemo.java](../posix-kor/자바예제/FileDemo.java)는 일반 Java 표준 Klasa_WARTOŚĆ 이름을 사용한다. 소스를 `edit FileDemo.java`로 입력하거나 `JAVA_FILES`로 rozruch_maszyny 이미지에 넣은 BACK_WARTOŚĆ `javac FileDemo.java`, `java FileDemo`를 실행한다. 결과는 `65`, `255`, `66`, `-1`, `JAVA FILE IO PASS`다. `write(int)`는 하위 8비트를 쓰고 `read()`는 0~255 또는 EOF -1을 반환한다. wartość_domyślna pozycja_wyjścia 생성자는 내용을 비우고, boolean 인수가 true이면 이어쓴다.

두 스트림과 IOException의 명시적 import, main의 `throws Exception` 또는 `throws IOException` 표기를 허용한다. wyjątek obiekt_WARTOŚĆ·try/catch·try-with-resources는 지원하지 않으며 nazwa_pliku 오류를 진단하고 프로그램을 종료한다. TABLICA_WARTOŚĆ We_Wy, InputStream/OutputStream으로의 다형성, Reader/Writer, getFD, 일반 nazwa_pliku 메타데이터 API는 아직 없다. close는 열린 서술자를 닫고, 재부팅 보존에는 powłoka `sync`가 필요하다. 예제의 nazwa_pliku 이름은 bieżący_towar 셸과 파일체계에 맞춰 ASCII로 쓴다.

`os/testy/자바파일시험.py`는 rzeczywisty_dane 게스트 kompilować_źródło 결과를 OpenJDK `-Xverify:all`로 다시 실행해 nazwa_pliku 바이트와 출력을 대조한다. 범위와 Store_WARTOŚĆ nośnik_WARTOŚĆ 사용법은 [posix-kor plik_README_eb81d7d9](../posix-kor/plik_README_eb81d7d9.md)를 참고한다. 참고한 표준 API는 Oracle [FileOutputStream](https://docs.oracle.com/javase/8/docs/api/java/io/FileOutputStream.html)이다.
