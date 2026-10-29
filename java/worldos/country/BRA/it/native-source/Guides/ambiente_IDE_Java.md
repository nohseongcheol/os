# jkoros 안에서 Java compilare_fonte·Esegui_comando

이 문서의 avvio_macchina·Shell·Store_VALORE 명령은 **x86 versione_VALORE** 기준이다. 공유 Java compilatore/JVM은 [nativo ARM64 Pi4 versione_VALORE](../platforms/rpi4-native/README.md)에도 연결되어 있다. ARM64에서는 UTF-8 UART input_VALORE·한글 nome_file_SMS, `edit`의 단독 `.` Store_VALORE, 16개 RAM file, 약 2초 Esegui_comando 제한을 사용한다.

`javac FILE.java`와 `java CLASS [ARGS]`를 네이티브 jkoros 셸에서 실행한다. 컴파일러와 JVM은 각각 독립 ELF로 적재되어 ring 3에서 동작한다. 소스를 게스트에서 읽어 effettivo_dati JVM `.class` 파일을 만들고, 그 파일의 바이트코드를 게스트 JVM이 해석한다. host compilare_fonte 서버나 Linux 게스트는 사용하지 않는다.

**Regolari_articolo 구현은 nativo 제한형 compilatore·JVM이다. OpenJDK/JDK 전체를 이식하거나 설치한 것이 아니며 Java SE 호환 환경도 아니다.** 표준 라이브러리는 아래의 일부 호출을 구현한 것이다. `java -version`과 `javac -version`에도 이 범위를 표시한다. 일반 JAR, Maven/Gradle, 임의의 Java app_f5044b9b 실행은 아직 지원하지 않는다.

## 바로 Esegui_comando

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

ISO는 `os/build/kernel.iso`다. 기존 VirtualBox 실행기도 같은 ISO를 사용한다. Esegui_comando 중이거나 저장된 VM에는 새 ISO가 자동 반영되지 않는다. 새 avvio_macchina 절차는 [VirtualBox Esegui_comando README_eb81d7d9](가상상자실행.md)를 따른다. 이 변경의 Java 자동 시험은 QEMU에서 수행했다.

## 직접 작성

`edit`는 file 전체를 새 내용으로 작성한다. 기존 내용의 riga_di_ingresso Modifica_VALORE 기능은 아니다. `.save`로 저장하고 `.cancel`로 취소한다.

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

- `ls`: 파일과 byte_VALORE numero mostrare_VALORE.
- `cat FILE`: file Contenuto_VALORE mostrare_VALORE. 텍스트 소스에 사용한다.
- `rm FILE`: Memoria_dati file 삭제.
- `edit FILE`: 전체 내용을 새로 input_VALORE. 빈 파일도 저장할 numero 있다.
- 구문·TIPO_VALORE 검사 errore_VALORE 시 기존 `.class`는 유지된다. 소스를 고친 BACK_VALORE 컴파일이 실패했다면 Indietro_articolo Esegui_comando 파일이 남아 있으므로 compilare_fonte 성공 여부를 확인한다.

파일은 RAM에서 동작한다. 전용 Store_VALORE 매체가 없거나 `sync`하지 않은 내용은 재부팅하면 사라진다. `make -C os run-store`로 연결한 매체에는 `sync`로 fonte_albero·Corso_VALORE·dati 파일을 보존할 numero 있다. 최대 8개, 파일마다 16KiB, file 이름은 ASCII 1~63자다. fonte_albero 이름은 `.class` 확장자 e_mail_area 때문에 최대 62자다. Modifica_VALORE 입력은 ASCII이고 한 riga_di_ingresso 최대 128자다. riga_di_ingresso 또는 file 한도를 넘긴 편집은 `.save`에서 거부하여 기존 파일을 보존한다. kernel_VALORE/compilatore/JVM 구현의 Java 식별자는 한국어이며, Regolari_articolo 게스트 input_VALORE 제한 때문에 spazio_utente 예제 이름은 ASCII로 작성한다.

## esterno_VALORE file 적재

호스트에서 만든 소스나 Supporto_VALORE ritagliare 안의 `.class`를 avvio_macchina 이미지에 포함할 numero 있다. `JAVA_FILES`는 `게스트이름=호스트경로` 목록이다. 아래의 경로는 예시이며 effettivo_dati 파일의 절대 경로로 바꾼다. 공백 없는 경로를 사용한다.

```sh
# host JDK로 컴파일한 클래스도 사용할 numero 있다.
javac --release 8 /tmp/Demo.java
make -C /home/user/jkoros iso \
  JAVA_FILES='Demo.java=/tmp/Demo.java Demo.class=/tmp/Demo.class'
make -C /home/user/jkoros run \
  JAVA_FILES='Demo.java=/tmp/Demo.java Demo.class=/tmp/Demo.class'
```

새 avvio_macchina 후 `java Demo 12`를 실행한다. 소스만 넣었으면 게스트에서 `javac Demo.java`부터 실행한다. `JAVA_FILES`를 생략한 Avanti_articolo 빌드에서는 Aggiunta_voce 파일을 포함하지 않는다. file Contenuto_VALORE 변경과 voce_elenco 제거도 Avanti_articolo 빌드에 반영된다. 원본 host 파일에는 쓰지 않는다. valore_predefinito `Hello.java`까지 합해 8개이며, 같은 이름을 명시하면 valore_predefinito 예제를 대체한다. 새 `.class`를 저장할 빈 슬롯도 남겨 둔다.

`--release 8`은 Corso_VALORE file 버전을 맞추는 옵션이다. 사용하는 문법·바이트코드·라이브러리도 아래 Supporto_VALORE ritagliare 안에 있어야 한다.

## Supporto_VALORE ritagliare

| 기능 | 게스트 javac | 게스트 JVM |
| --- | --- | --- |
| Corso_VALORE | 패키지 없는 단일 Corso_VALORE, statico_VALORE FUNZIONE_VALORE, 재귀, argomenti/Reso_KR | 실행마다 단일 Corso_VALORE 적재, public static main(String[]) |
| valore_predefinito VALORE | int, boolean, char, String, main의 String[] argomenti | intero·fonti operando_Pila, String, int[], String[], 내부 StringBuilder |
| istruzione_VALORE | 초기값 있는 locale_Scope dichiarazione, lab_VALORE, `+=`, `-=`, `*=`, `/=`, `%=`, 후위 ++/--, 블록, if/else, while, for, return | 해당 intero·fonti 바이트코드와 condizione ramo |
| espressione_VALORE | 십진 intero, UTF-8 소스의 stringa_VALORE/문자, + - * / %, 비교, ==/!=, !/&&/\|\|, stringa_VALORE 결합 | intero operazione_VALORE·bit_VALORE operazione_VALORE·TIPO_VALORE CONVERTI_VALORE, 단락 평가, array_VALORE accesso_voce |
| file | FileInputStream(String), FileOutputStream(String[, boolean]), read()/write(int)/close() | effettivo_dati kernel_VALORE 파일서술자와 Connetti, generare·liquidare_Sommario·이어쓰기·EOF |
| uscitaTesto | System.out.print/println: int/boolean/char/String, println() | 동일 |
| stringa_VALORE/argomenti | String.length(), args.length, args[index], Integer.parseInt | 추가로 String.charAt(), stringa_VALORE 상수의 modified UTF-8 해독 |

선언은 지원하는 문법만 허용한다. 여러 변수를 한 선언에 나열하기, 초기값 없는 locale_Scope dichiarazione, 오버로드, 임의 TIPO_VALORE CONVERTI_VALORE, array_VALORE generare codiceSorgente, 8/16진 리터럴, Unicode fonte_albero 이스케이프 등은 미지원이다. `char`는 문자 리터럴로 초기화하며 일반 JDK의 모든 costante_VALORE 축소 변환을 구현하지 않는다. esterno_VALORE `.class`의 `int[]` generare/Lettura/쓰기는 지원하므로 host `javac --release 8`로 만든 array_VALORE 예제는 실행할 numero 있다.

oggetto_VALORE valore_del_campo·일반 oggetto_VALORE generare·상속·인터페이스·여러 Corso_VALORE Connetti, long/float/double, eccezione Processi_VALORE_voce, 스레드·모니터, 리플렉션, JNI, JIT, GC, 위 표에 없는 `java.io`와 `java.nio`/`java.net` 일반 API, 컬렉션, JAR와 클래스패스는 미지원이다. 런타임 오류는 Java eccezione 객체를 던지지 않고 진단 후 Regolari_articolo 프로그램을 종료한다. 객체와 stringa_VALORE Store_VALORE 공간은 Esegui_comando Esci_app 시 spazio_utente area_VALORE 전체와 함께 회수한다. 지속 Esegui_comando 중 GC는 없다.

## Esegui_comando 한도와 errore

| risorsa_VALORE | 한도 |
| --- | --- |
| fonte_albero/Corso_VALORE file | 각각 16KiB |
| compilatore | token_VALORE 2,047개, generare CODICE_VALORE 4KiB, costante_VALORE 풀 4KiB |
| FUNZIONE_VALORE/argomenti | 클래스당 32함수, 함수당 16인수 |
| JVM costante_VALORE | 511개 |
| JVM FUNZIONE_VALORE CODICE_VALORE | 함수당 8KiB |
| JVM 호출/operando_Pila/locale_Scope variabile_VALORE | 32프레임, 프레임당 operando_Pila 128칸·locale_Scope 128칸 |
| JVM oggetto_VALORE Store_VALORE e_mail_area | 8,192개 32비트 slot_voce, 헤더 dichiarazioni 약 32KiB |
| Esegui_comando | 최대 500,000 comando, 기존 커널의 약 3초 CPU Esegui_comando 상한도 적용 |

게스트 컴파일러는 버전 49.0 `.class`를 생성하며 JVM은 45.0~52.0 중 Supporto_VALORE 명령으로 구성된 파일을 읽는다. 스택맵을 이용한 완전한 JVM dizionario 검증기를 구현한 것은 아니다. file/valore_dell_attributo durata_VALORE, costante_VALORE fonti, comando·ramo 경계를 검사하고, Esegui_comando 중 operando_Pila formato_VALORE·locale_Scope inizializza·array_VALORE pedice_VALORE·oggetto_VALORE 참조를 검사한다. spazio_utente 코드의 페이지·hardware_porta 접근은 기존 ring 3 경계로 보호한다.

일반 성공은 `Exit: 0`, compilare_fonte·JVM 오류는 `Exit: 1`, comando argomenti 오류는 `Exit: 2`다. CPU valore 상한은 기존 `Exit: 124`이며, spazio_utente ELF 자체의 CPU/런타임 오류는 기존 Esci_app 코드를 따른다. errore_VALORE 후 셸에서 다른 프로그램을 계속 실행할 numero 있다.

## implementazione 위치와 prove

- `os/spazio_utente/자바/자바컴파일러.java`: 게스트 어휘·구문·TIPO_VALORE 검사, costante_VALORE 풀 및 바이트코드 generare.
- `os/spazio_utente/자바/자바가상기계.java`: Corso_VALORE 적재, operando_Pila·프레임·oggetto_VALORE Store_VALORE, comando 해석과 제한된 표준 호출.
- `os/codiceSorgente/Memoria_file_system.java`: Memoria_dati file_system, Modifica_VALORE, avvio_macchina file 적재.
- `os/codiceSorgente/chiamata_di_sistema.java`, `compiler/START_USER_app.s`: file/문자 uscitaTesto API와 spazio_utente puntatore 검사.
- `os/strumenti/자바파일묶기.py`: host input_VALORE file convalidare·avvio_macchina gruppo_VALORE generare.

```sh
make test-java
make test
```

`os/prove/자바시험.py`는 ELF/ISO avvio_macchina, 게스트 compilare_fonte·Esegui_comando, spazio_utente input_VALORE, 재귀·반복문·intero 극값·stringa_VALORE 결합·단락 평가, 재실행, fonte_albero errore 후 기존 Corso_VALORE 보존, array_VALORE/numero 해독 errore, 무한 sprint_VALORE 제한, Modifica_VALORE 넘침과 file 부족을 검사한다. 게스트 generare 클래스의 바이트를 QEMU 메모리에서 꺼내 OpenJDK `java -Xverify:all`로 실행하고 결과를 대조한다. 반대 방향으로 host OpenJDK의 Corso_VALORE, intero 배열과 한글 상수를 게스트에 적재하며, 손상된 file marcatore_VALORE·버전·costante_VALORE numero·ramo·스택을 거부하는지도 검사한다. 기록은 `os/build/자바시험.json`에 남는다. 디스크 없는 별도 prove VM만 생성하고 종료한다.

implementazione 형식의 참고 dati: Oracle [JVM Corso_VALORE file specifica](https://docs.oracle.com/javase/specs/jvms/se8/html/jvms-4.html), [JVM comando specifica](https://docs.oracle.com/javase/specs/jvms/se8/html/jvms-6.html).

## Java file I_O

[FileDemo.java](../posix-kor/자바예제/FileDemo.java)는 일반 Java 표준 Corso_VALORE 이름을 사용한다. 소스를 `edit FileDemo.java`로 입력하거나 `JAVA_FILES`로 avvio_macchina 이미지에 넣은 BACK_VALORE `javac FileDemo.java`, `java FileDemo`를 실행한다. 결과는 `65`, `255`, `66`, `-1`, `JAVA FILE IO PASS`다. `write(int)`는 하위 8비트를 쓰고 `read()`는 0~255 또는 EOF -1을 반환한다. valore_predefinito uscitaTesto 생성자는 내용을 비우고, boolean 인수가 true이면 이어쓴다.

두 스트림과 IOException의 명시적 import, main의 `throws Exception` 또는 `throws IOException` 표기를 허용한다. eccezione oggetto_VALORE·try/catch·try-with-resources는 지원하지 않으며 file 오류를 진단하고 프로그램을 종료한다. array_VALORE I_O, InputStream/OutputStream으로의 다형성, Reader/Writer, getFD, 일반 file 메타데이터 API는 아직 없다. close는 열린 서술자를 닫고, 재부팅 보존에는 Shell `sync`가 필요하다. 예제의 file 이름은 Regolari_articolo 셸과 파일체계에 맞춰 ASCII로 쓴다.

`os/prove/자바파일시험.py`는 effettivo_dati 게스트 compilare_fonte 결과를 OpenJDK `-Xverify:all`로 retry_VALORE 실행해 file 바이트와 출력을 대조한다. 범위와 Store_VALORE supporti_VALORE 사용법은 [posix-kor README_eb81d7d9](../posix-kor/README_eb81d7d9.md)를 참고한다. 참고한 표준 API는 Oracle [FileOutputStream](https://docs.oracle.com/javase/8/docs/api/java/io/FileOutputStream.html)이다.
