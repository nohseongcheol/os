# jkoros 안에서 Java épít_forrás·végrehajt_parancs

이 문서의 부팅·felület·tár_ÉRTÉK 명령은 **x86 verzió_ÉRTÉK** 기준이다. 공유 Java fordítóprogram/JVM은 [saját ARM64 Pi4 verzió_ÉRTÉK](../platforms/rpi4-native/README.md)에도 연결되어 있다. ARM64에서는 UTF-8 UART bevitel_ÉRTÉK·한글 fájlnév_SMS, `edit`의 단독 `.` tár_ÉRTÉK, 16개 RAM Fájl, 약 2초 végrehajt_parancs 제한을 사용한다.

`javac FILE.java`와 `java CLASS [ARGS]`를 네이티브 jkoros 셸에서 실행한다. 컴파일러와 JVM은 각각 독립 ELF로 적재되어 ring 3에서 동작한다. 소스를 게스트에서 읽어 tényleges_adat JVM `.class` 파일을 만들고, 그 파일의 바이트코드를 게스트 JVM이 해석한다. gazda épít_forrás 서버나 Linux 게스트는 사용하지 않는다.

**aktuális_cikk 구현은 saját 제한형 fordítóprogram·JVM이다. OpenJDK/JDK 전체를 이식하거나 설치한 것이 아니며 Java SE 호환 환경도 아니다.** 표준 라이브러리는 아래의 일부 호출을 구현한 것이다. `java -version`과 `javac -version`에도 이 범위를 표시한다. 일반 JAR, Maven/Gradle, 임의의 Java app_f5044b9b 실행은 아직 지원하지 않는다.

## 바로 végrehajt_parancs

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

ISO는 `os/build/kernel.iso`다. 기존 VirtualBox 실행기도 같은 ISO를 사용한다. végrehajt_parancs 중이거나 저장된 VM에는 새 ISO가 자동 반영되지 않는다. 새 부팅 절차는 [VirtualBox végrehajt_parancs fontos_fájl_eb81d7d9](가상상자실행.md)를 따른다. 이 변경의 Java 자동 시험은 QEMU에서 수행했다.

## 직접 작성

`edit`는 Fájl 전체를 새 내용으로 작성한다. 기존 내용의 Vonal szerkeszt_ÉRTÉK 기능은 아니다. `.save`로 저장하고 `.cancel`로 취소한다.

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

- `ls`: 파일과 bájt_ÉRTÉK szám bemutató_ÉRTÉK.
- `cat FILE`: Fájl Tartalom_ÉRTÉK bemutató_ÉRTÉK. 텍스트 소스에 사용한다.
- `rm FILE`: Memória_adat Fájl 삭제.
- `edit FILE`: 전체 내용을 새로 bevitel_ÉRTÉK. 빈 파일도 저장할 szám 있다.
- 구문·beír_ÉRTÉK 검사 hiba_ÉRTÉK 시 기존 `.class`는 유지된다. 소스를 고친 BACK_ÉRTÉK 컴파일이 실패했다면 Előző_cikk végrehajt_parancs 파일이 남아 있으므로 épít_forrás 성공 여부를 확인한다.

파일은 RAM에서 동작한다. 전용 tár_ÉRTÉK 매체가 없거나 `sync`하지 않은 내용은 재부팅하면 사라진다. `make -C os run-store`로 연결한 매체에는 `sync`로 forrás_fa·tanóra_ÉRTÉK·adat 파일을 보존할 szám 있다. 최대 8개, 파일마다 16KiB, Fájl 이름은 ASCII 1~63자다. forrás_fa 이름은 `.class` 확장자 CÍM_régió 때문에 최대 62자다. szerkeszt_ÉRTÉK 입력은 ASCII이고 한 Vonal 최대 128자다. Vonal 또는 Fájl 한도를 넘긴 편집은 `.save`에서 거부하여 기존 파일을 보존한다. kernel_ÉRTÉK/fordítóprogram/JVM 구현의 Java 식별자는 한국어이며, aktuális_cikk 게스트 bevitel_ÉRTÉK 제한 때문에 felhasználó 예제 이름은 ASCII로 작성한다.

## külső_ÉRTÉK Fájl 적재

호스트에서 만든 소스나 támogat_ÉRTÉK klip 안의 `.class`를 부팅 이미지에 포함할 szám 있다. `JAVA_FILES`는 `게스트이름=호스트경로` 목록이다. 아래의 경로는 예시이며 tényleges_adat 파일의 절대 경로로 바꾼다. 공백 없는 경로를 사용한다.

```sh
# gazda JDK로 컴파일한 클래스도 사용할 szám 있다.
javac --release 8 /tmp/Demo.java
make -C /home/user/jkoros iso \
  JAVA_FILES='Demo.java=/tmp/Demo.java Demo.class=/tmp/Demo.class'
make -C /home/user/jkoros run \
  JAVA_FILES='Demo.java=/tmp/Demo.java Demo.class=/tmp/Demo.class'
```

새 부팅 후 `java Demo 12`를 실행한다. 소스만 넣었으면 게스트에서 `javac Demo.java`부터 실행한다. `JAVA_FILES`를 생략한 Tovább_cikk 빌드에서는 hozzáfűz_bejegyzés 파일을 포함하지 않는다. Fájl Tartalom_ÉRTÉK 변경과 bejegyzés_Lista 제거도 Tovább_cikk 빌드에 반영된다. 원본 gazda 파일에는 쓰지 않는다. alapértelmezett_érték `Hello.java`까지 합해 8개이며, 같은 이름을 명시하면 alapértelmezett_érték 예제를 대체한다. 새 `.class`를 저장할 빈 슬롯도 남겨 둔다.

`--release 8`은 tanóra_ÉRTÉK Fájl 버전을 맞추는 옵션이다. 사용하는 문법·바이트코드·라이브러리도 아래 támogat_ÉRTÉK klip 안에 있어야 한다.

## támogat_ÉRTÉK klip

| 기능 | 게스트 javac | 게스트 JVM |
| --- | --- | --- |
| tanóra_ÉRTÉK | 패키지 없는 단일 tanóra_ÉRTÉK, statikus_ÉRTÉK FÜGGVÉNY_ÉRTÉK, 재귀, Argumentumok/visszaküld_KR | 실행마다 단일 tanóra_ÉRTÉK 적재, public static main(String[]) |
| alapértelmezett_érték ÉRTÉK | int, boolean, char, String, main의 String[] Argumentumok | egész_szám·hivatkozik operandus_Sor, String, int[], String[], 내부 StringBuilder |
| utasítás_ÉRTÉK | 초기값 있는 helyi_hatókör bevallás, labor_ÉRTÉK, `+=`, `-=`, `*=`, `/=`, `%=`, 후위 ++/--, 블록, if/else, while, for, return | 해당 egész_szám·hivatkozik 바이트코드와 állapot ág |
| kifejezés_ÉRTÉK | 십진 egész_szám, UTF-8 소스의 sztring_ÉRTÉK/문자, + - * / %, 비교, ==/!=, !/&&/\|\|, sztring_ÉRTÉK 결합 | egész_szám műtét_ÉRTÉK·bit_ÉRTÉK műtét_ÉRTÉK·beír_ÉRTÉK konvertál_ÉRTÉK, 단락 평가, TÖMB_ÉRTÉK hozzáfér_bejegyzés |
| Fájl | FileInputStream(String), FileOutputStream(String[, boolean]), read()/write(int)/close() | tényleges_adat kernel_ÉRTÉK 파일서술자와 Kapcsolódás, generálás·töröl_Tartalom·이어쓰기·EOF |
| Kimenet | System.out.print/println: int/boolean/char/String, println() | 동일 |
| sztring_ÉRTÉK/Argumentumok | String.length(), args.length, args[index], Integer.parseInt | 추가로 String.charAt(), sztring_ÉRTÉK 상수의 modified UTF-8 해독 |

선언은 지원하는 문법만 허용한다. 여러 변수를 한 선언에 나열하기, 초기값 없는 helyi_hatókör bevallás, 오버로드, 임의 beír_ÉRTÉK konvertál_ÉRTÉK, TÖMB_ÉRTÉK generálás FORRÁS, 8/16진 리터럴, Unicode forrás_fa 이스케이프 등은 미지원이다. `char`는 문자 리터럴로 초기화하며 일반 JDK의 모든 állandó_ÉRTÉK 축소 변환을 구현하지 않는다. külső_ÉRTÉK `.class`의 `int[]` generálás/Olvasás/쓰기는 지원하므로 gazda `javac --release 8`로 만든 TÖMB_ÉRTÉK 예제는 실행할 szám 있다.

objektum_ÉRTÉK mezőérték·일반 objektum_ÉRTÉK generálás·상속·인터페이스·여러 tanóra_ÉRTÉK Kapcsolódás, long/float/double, kivétel folyamat_ÉRTÉK_bejegyzés, 스레드·모니터, 리플렉션, JNI, JIT, GC, 위 표에 없는 `java.io`와 `java.nio`/`java.net` 일반 API, 컬렉션, JAR와 클래스패스는 미지원이다. 런타임 오류는 Java kivétel 객체를 던지지 않고 진단 후 aktuális_cikk 프로그램을 종료한다. 객체와 sztring_ÉRTÉK tár_ÉRTÉK 공간은 végrehajt_parancs kilép_app 시 felhasználó régió_ÉRTÉK 전체와 함께 회수한다. 지속 végrehajt_parancs 중 GC는 없다.

## végrehajt_parancs 한도와 HIBA

| erőforrás_ÉRTÉK | 한도 |
| --- | --- |
| forrás_fa/tanóra_ÉRTÉK Fájl | 각각 16KiB |
| fordítóprogram | kód_ÉRTÉK 2,047개, generálás KÓD_ÉRTÉK 4KiB, állandó_ÉRTÉK 풀 4KiB |
| FÜGGVÉNY_ÉRTÉK/Argumentumok | 클래스당 32함수, 함수당 16인수 |
| JVM állandó_ÉRTÉK | 511개 |
| JVM FÜGGVÉNY_ÉRTÉK KÓD_ÉRTÉK | 함수당 8KiB |
| JVM 호출/operandus_Sor/helyi_hatókör változó_ÉRTÉK | 32프레임, 프레임당 operandus_Sor 128칸·helyi_hatókör 128칸 |
| JVM objektum_ÉRTÉK tár_ÉRTÉK CÍM_régió | 8,192개 32비트 tárolóhely_bejegyzés, 헤더 포함 약 32KiB |
| végrehajt_parancs | 최대 500,000 Parancs, 기존 커널의 약 3초 CPU végrehajt_parancs 상한도 적용 |

게스트 컴파일러는 버전 49.0 `.class`를 생성하며 JVM은 45.0~52.0 중 támogat_ÉRTÉK 명령으로 구성된 파일을 읽는다. 스택맵을 이용한 완전한 JVM szótár 검증기를 구현한 것은 아니다. Fájl/attribútum_ÉRTÉK hossz_ÉRTÉK, állandó_ÉRTÉK hivatkozik, Parancs·ág 경계를 검사하고, végrehajt_parancs 중 operandus_Sor formáz_ÉRTÉK·helyi_hatókör inicializál·TÖMB_ÉRTÉK alsó_index_ÉRTÉK·objektum_ÉRTÉK 참조를 검사한다. felhasználó 코드의 페이지·hardver_port 접근은 기존 ring 3 경계로 보호한다.

일반 성공은 `Exit: 0`, épít_forrás·JVM 오류는 `Exit: 1`, Parancs Argumentumok 오류는 `Exit: 2`다. CPU IDŐ_ÉRTÉK 상한은 기존 `Exit: 124`이며, felhasználó ELF 자체의 CPU/런타임 오류는 기존 kilép_app 코드를 따른다. hiba_ÉRTÉK 후 셸에서 다른 프로그램을 계속 실행할 szám 있다.

## 구현 위치와 시험

- `os/felhasználó/자바/자바컴파일러.java`: 게스트 어휘·구문·beír_ÉRTÉK 검사, állandó_ÉRTÉK 풀 및 바이트코드 generálás.
- `os/felhasználó/자바/자바가상기계.java`: tanóra_ÉRTÉK 적재, operandus_Sor·프레임·objektum_ÉRTÉK tár_ÉRTÉK, Parancs 해석과 제한된 표준 호출.
- `os/FORRÁS/Memória_fájlrendszer.java`: Memória_adat fájlrendszer, szerkeszt_ÉRTÉK, 부팅 Fájl 적재.
- `os/FORRÁS/체계호출.java`, `compiler/START_felhasználó_app.s`: Fájl/문자 Kimenet API와 felhasználó mutató 검사.
- `os/Eszközök/자바파일묶기.py`: gazda bevitel_ÉRTÉK Fájl ellenőriz·부팅 Csoport_ÉRTÉK generálás.

```sh
make test-java
make test
```

`os/시험/자바시험.py`는 ELF/ISO 부팅, 게스트 épít_forrás·végrehajt_parancs, felhasználó bevitel_ÉRTÉK, 재귀·반복문·egész_szám 극값·sztring_ÉRTÉK 결합·단락 평가, 재실행, forrás_fa HIBA 후 기존 tanóra_ÉRTÉK 보존, TÖMB_ÉRTÉK/szám 해독 HIBA, 무한 futam_ÉRTÉK 제한, szerkeszt_ÉRTÉK 넘침과 Fájl 부족을 검사한다. 게스트 generálás 클래스의 바이트를 QEMU 메모리에서 꺼내 OpenJDK `java -Xverify:all`로 실행하고 결과를 대조한다. 반대 방향으로 gazda OpenJDK의 tanóra_ÉRTÉK, egész_szám 배열과 한글 상수를 게스트에 적재하며, 손상된 Fájl jelölő_ÉRTÉK·버전·állandó_ÉRTÉK szám·ág·스택을 거부하는지도 검사한다. 기록은 `os/build/자바시험.json`에 남는다. 디스크 없는 별도 시험 VM만 생성하고 종료한다.

구현 형식의 참고 adat: Oracle [JVM tanóra_ÉRTÉK Fájl 명세](https://docs.oracle.com/javase/specs/jvms/se8/html/jvms-4.html), [JVM Parancs 명세](https://docs.oracle.com/javase/specs/jvms/se8/html/jvms-6.html).

## Java Fájl I_O

[FileDemo.java](../posix-kor/자바예제/FileDemo.java)는 일반 Java 표준 tanóra_ÉRTÉK 이름을 사용한다. 소스를 `edit FileDemo.java`로 입력하거나 `JAVA_FILES`로 부팅 이미지에 넣은 BACK_ÉRTÉK `javac FileDemo.java`, `java FileDemo`를 실행한다. 결과는 `65`, `255`, `66`, `-1`, `JAVA FILE IO PASS`다. `write(int)`는 하위 8비트를 쓰고 `read()`는 0~255 또는 EOF -1을 반환한다. alapértelmezett_érték Kimenet 생성자는 내용을 비우고, boolean 인수가 true이면 이어쓴다.

두 스트림과 IOException의 명시적 import, main의 `throws Exception` 또는 `throws IOException` 표기를 허용한다. kivétel objektum_ÉRTÉK·try/catch·try-with-resources는 지원하지 않으며 Fájl 오류를 진단하고 프로그램을 종료한다. TÖMB_ÉRTÉK I_O, InputStream/OutputStream으로의 다형성, Reader/Writer, getFD, 일반 Fájl 메타데이터 API는 아직 없다. close는 열린 서술자를 닫고, 재부팅 보존에는 felület `sync`가 필요하다. 예제의 Fájl 이름은 aktuális_cikk 셸과 파일체계에 맞춰 ASCII로 쓴다.

`os/시험/자바파일시험.py`는 tényleges_adat 게스트 épít_forrás 결과를 OpenJDK `-Xverify:all`로 újrapróbál_ÉRTÉK 실행해 Fájl 바이트와 출력을 대조한다. 범위와 tár_ÉRTÉK Multimédia_ÉRTÉK 사용법은 [posix-kor fontos_fájl_eb81d7d9](../posix-kor/fontos_fájl_eb81d7d9.md)를 참고한다. 참고한 표준 API는 Oracle [FileOutputStream](https://docs.oracle.com/javase/8/docs/api/java/io/FileOutputStream.html)이다.
