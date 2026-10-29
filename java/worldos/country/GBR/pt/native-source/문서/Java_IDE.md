# jkoros 안에서 Java compilar_fonte·Executar_comando

이 문서의 arranque_da_máquina·shell·Store_VALOR 명령은 **x86 versão_VALOR** 기준이다. 공유 Java compilador/JVM은 [nativo ARM64 Pi4 versão_VALOR](../platforms/rpi4-native/README.md)에도 연결되어 있다. ARM64에서는 UTF-8 UART entrada_VALOR·한글 nome_de_arquivo_SMS, `edit`의 단독 `.` Store_VALOR, 16개 RAM ficheiro, 약 2초 Executar_comando 제한을 사용한다.

`javac FILE.java`와 `java CLASS [ARGS]`를 네이티브 jkoros 셸에서 실행한다. 컴파일러와 JVM은 각각 독립 ELF로 적재되어 ring 3에서 동작한다. 소스를 게스트에서 읽어 real_dados JVM `.class` 파일을 만들고, 그 파일의 바이트코드를 게스트 JVM이 해석한다. host compilar_fonte 서버나 Linux 게스트는 사용하지 않는다.

**em_dia_item 구현은 nativo 제한형 compilador·JVM이다. OpenJDK/JDK 전체를 이식하거나 설치한 것이 아니며 Java SE 호환 환경도 아니다.** 표준 라이브러리는 아래의 일부 호출을 구현한 것이다. `java -version`과 `javac -version`에도 이 범위를 표시한다. 일반 JAR, Maven/Gradle, 임의의 Java app_f5044b9b 실행은 아직 지원하지 않는다.

## 바로 Executar_comando

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

ISO는 `os/build/kernel.iso`다. 기존 VirtualBox 실행기도 같은 ISO를 사용한다. Executar_comando 중이거나 저장된 VM에는 새 ISO가 자동 반영되지 않는다. 새 arranque_da_máquina 절차는 [VirtualBox Executar_comando LEIAME_eb81d7d9](가상상자실행.md)를 따른다. 이 변경의 Java 자동 시험은 QEMU에서 수행했다.

## 직접 작성

`edit`는 ficheiro 전체를 새 내용으로 작성한다. 기존 내용의 linha_de_entrada Editar_VALOR 기능은 아니다. `.save`로 저장하고 `.cancel`로 취소한다.

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

- `ls`: 파일과 byte_VALOR número mostrar_VALOR.
- `cat FILE`: ficheiro Conteúdo_VALOR mostrar_VALOR. 텍스트 소스에 사용한다.
- `rm FILE`: Memória_dados ficheiro 삭제.
- `edit FILE`: 전체 내용을 새로 entrada_VALOR. 빈 파일도 저장할 número 있다.
- 구문·TIPO_VALOR 검사 falha_VALOR 시 기존 `.class`는 유지된다. 소스를 고친 BACK_VALOR 컴파일이 실패했다면 Anterior_item Executar_comando 파일이 남아 있으므로 compilar_fonte 성공 여부를 확인한다.

파일은 RAM에서 동작한다. 전용 Store_VALOR 매체가 없거나 `sync`하지 않은 내용은 재부팅하면 사라진다. `make -C os run-store`로 연결한 매체에는 `sync`로 fonte_árvore·aula_VALOR·dados 파일을 보존할 número 있다. 최대 8개, 파일마다 16KiB, ficheiro 이름은 ASCII 1~63자다. fonte_árvore 이름은 `.class` 확장자 email_região 때문에 최대 62자다. Editar_VALOR 입력은 ASCII이고 한 linha_de_entrada 최대 128자다. linha_de_entrada 또는 ficheiro 한도를 넘긴 편집은 `.save`에서 거부하여 기존 파일을 보존한다. kernel_VALOR/compilador/JVM 구현의 Java 식별자는 한국어이며, em_dia_item 게스트 entrada_VALOR 제한 때문에 espaço_do_utilizador 예제 이름은 ASCII로 작성한다.

## externo_VALOR ficheiro 적재

호스트에서 만든 소스나 Suporte_VALOR recortar 안의 `.class`를 arranque_da_máquina 이미지에 포함할 número 있다. `JAVA_FILES`는 `게스트이름=호스트경로` 목록이다. 아래의 경로는 예시이며 real_dados 파일의 절대 경로로 바꾼다. 공백 없는 경로를 사용한다.

```sh
# host JDK로 컴파일한 클래스도 사용할 número 있다.
javac --release 8 /tmp/Demo.java
make -C /home/user/jkoros iso \
  JAVA_FILES='Demo.java=/tmp/Demo.java Demo.class=/tmp/Demo.class'
make -C /home/user/jkoros run \
  JAVA_FILES='Demo.java=/tmp/Demo.java Demo.class=/tmp/Demo.class'
```

새 arranque_da_máquina 후 `java Demo 12`를 실행한다. 소스만 넣었으면 게스트에서 `javac Demo.java`부터 실행한다. `JAVA_FILES`를 생략한 Avançar_item 빌드에서는 Acrescentar_entrada 파일을 포함하지 않는다. ficheiro Conteúdo_VALOR 변경과 entrada_Lista_f07b3200 제거도 Avançar_item 빌드에 반영된다. 원본 host 파일에는 쓰지 않는다. valor_padrão `Hello.java`까지 합해 8개이며, 같은 이름을 명시하면 valor_padrão 예제를 대체한다. 새 `.class`를 저장할 빈 슬롯도 남겨 둔다.

`--release 8`은 aula_VALOR ficheiro 버전을 맞추는 옵션이다. 사용하는 문법·바이트코드·라이브러리도 아래 Suporte_VALOR recortar 안에 있어야 한다.

## Suporte_VALOR recortar

| 기능 | 게스트 javac | 게스트 JVM |
| --- | --- | --- |
| aula_VALOR | 패키지 없는 단일 aula_VALOR, estático_VALOR FUNÇÃO_VALOR, 재귀, argumentos/devolver_RC | 실행마다 단일 aula_VALOR 적재, public static main(String[]) |
| valor_padrão VALOR | int, boolean, char, String, main의 String[] argumentos | inteiro·Referência operando_pilha, String, int[], String[], 내부 StringBuilder |
| instrução_VALOR | 초기값 있는 local_Scope declaração, tarefa_VALOR, `+=`, `-=`, `*=`, `/=`, `%=`, 후위 ++/--, 블록, if/else, while, for, return | 해당 inteiro·Referência 바이트코드와 doença branch |
| expressão_VALOR | 십진 inteiro, UTF-8 소스의 cadeia_VALOR/문자, + - * / %, 비교, ==/!=, !/&&/\|\|, cadeia_VALOR 결합 | inteiro cirurgia_VALOR·bit_VALOR cirurgia_VALOR·TIPO_VALOR CONVERTER_VALOR, 단락 평가, MATRIZ_VALOR acesso_entrada |
| ficheiro | FileInputStream(String), FileOutputStream(String[, boolean]), read()/write(int)/close() | real_dados kernel_VALOR 파일서술자와 Ligar, gerar·limpar_Sumário·이어쓰기·EOF |
| saídaTexto | System.out.print/println: int/boolean/char/String, println() | 동일 |
| cadeia_VALOR/argumentos | String.length(), args.length, args[index], Integer.parseInt | 추가로 String.charAt(), cadeia_VALOR 상수의 modified UTF-8 해독 |

선언은 지원하는 문법만 허용한다. 여러 변수를 한 선언에 나열하기, 초기값 없는 local_Scope declaração, 오버로드, 임의 TIPO_VALOR CONVERTER_VALOR, MATRIZ_VALOR gerar códigoFonte, 8/16진 리터럴, Unicode fonte_árvore 이스케이프 등은 미지원이다. `char`는 문자 리터럴로 초기화하며 일반 JDK의 모든 constante_VALOR 축소 변환을 구현하지 않는다. externo_VALOR `.class`의 `int[]` gerar/Leitura/쓰기는 지원하므로 host `javac --release 8`로 만든 MATRIZ_VALOR 예제는 실행할 número 있다.

objeto_VALOR valor_do_campo·일반 objeto_VALOR gerar·상속·인터페이스·여러 aula_VALOR Ligar, long/float/double, exceção Processo_VALOR_entrada, 스레드·모니터, 리플렉션, JNI, JIT, GC, 위 표에 없는 `java.io`와 `java.nio`/`java.net` 일반 API, 컬렉션, JAR와 클래스패스는 미지원이다. 런타임 오류는 Java exceção 객체를 던지지 않고 진단 후 em_dia_item 프로그램을 종료한다. 객체와 cadeia_VALOR Store_VALOR 공간은 Executar_comando sair_app 시 espaço_do_utilizador região_VALOR 전체와 함께 회수한다. 지속 Executar_comando 중 GC는 없다.

## Executar_comando 한도와 erro

| recurso_VALOR | 한도 |
| --- | --- |
| fonte_árvore/aula_VALOR ficheiro | 각각 16KiB |
| compilador | token_VALOR 2,047개, gerar valor_do_código 4KiB, constante_VALOR 풀 4KiB |
| FUNÇÃO_VALOR/argumentos | 클래스당 32함수, 함수당 16인수 |
| JVM constante_VALOR | 511개 |
| JVM FUNÇÃO_VALOR valor_do_código | 함수당 8KiB |
| JVM 호출/operando_pilha/local_Scope variável_VALOR | 32프레임, 프레임당 operando_pilha 128칸·local_Scope 128칸 |
| JVM objeto_VALOR Store_VALOR email_região | 8,192개 32비트 slot_entrada, 헤더 declarações 약 32KiB |
| Executar_comando | 최대 500,000 comando, 기존 커널의 약 3초 CPU Executar_comando 상한도 적용 |

게스트 컴파일러는 버전 49.0 `.class`를 생성하며 JVM은 45.0~52.0 중 Suporte_VALOR 명령으로 구성된 파일을 읽는다. 스택맵을 이용한 완전한 JVM dicionário 검증기를 구현한 것은 아니다. ficheiro/valor_do_atributo duração_VALOR, constante_VALOR Referência, comando·branch 경계를 검사하고, Executar_comando 중 operando_pilha formato_VALOR·local_Scope inicializar·MATRIZ_VALOR subscrito_VALOR·objeto_VALOR 참조를 검사한다. espaço_do_utilizador 코드의 페이지·hardware_porta 접근은 기존 ring 3 경계로 보호한다.

일반 성공은 `Exit: 0`, compilar_fonte·JVM 오류는 `Exit: 1`, comando argumentos 오류는 `Exit: 2`다. CPU valor_temporal 상한은 기존 `Exit: 124`이며, espaço_do_utilizador ELF 자체의 CPU/런타임 오류는 기존 sair_app 코드를 따른다. falha_VALOR 후 셸에서 다른 프로그램을 계속 실행할 número 있다.

## implementação 위치와 testes

- `os/espaço_do_utilizador/자바/자바컴파일러.java`: 게스트 어휘·구문·TIPO_VALOR 검사, constante_VALOR 풀 및 바이트코드 gerar.
- `os/espaço_do_utilizador/자바/자바가상기계.java`: aula_VALOR 적재, operando_pilha·프레임·objeto_VALOR Store_VALOR, comando 해석과 제한된 표준 호출.
- `os/códigoFonte/Memória_sistema_de_arquivos.java`: Memória_dados sistema_de_arquivos, Editar_VALOR, arranque_da_máquina ficheiro 적재.
- `os/códigoFonte/chamada_ao_sistema.java`, `compiler/START_usuário_app.s`: ficheiro/문자 saídaTexto API와 espaço_do_utilizador ponteiro 검사.
- `os/ferramentas/자바파일묶기.py`: host entrada_VALOR ficheiro validar·arranque_da_máquina Grupo_VALOR gerar.

```sh
make test-java
make test
```

`os/testes/자바시험.py`는 ELF/ISO arranque_da_máquina, 게스트 compilar_fonte·Executar_comando, espaço_do_utilizador entrada_VALOR, 재귀·반복문·inteiro 극값·cadeia_VALOR 결합·단락 평가, 재실행, fonte_árvore erro 후 기존 aula_VALOR 보존, MATRIZ_VALOR/número 해독 erro, 무한 sprint_VALOR 제한, Editar_VALOR 넘침과 ficheiro 부족을 검사한다. 게스트 gerar 클래스의 바이트를 QEMU 메모리에서 꺼내 OpenJDK `java -Xverify:all`로 실행하고 결과를 대조한다. 반대 방향으로 host OpenJDK의 aula_VALOR, inteiro 배열과 한글 상수를 게스트에 적재하며, 손상된 ficheiro favorito_VALOR·버전·constante_VALOR número·branch·스택을 거부하는지도 검사한다. 기록은 `os/build/자바시험.json`에 남는다. 디스크 없는 별도 testes VM만 생성하고 종료한다.

implementação 형식의 참고 dados: Oracle [JVM aula_VALOR ficheiro especificação](https://docs.oracle.com/javase/specs/jvms/se8/html/jvms-4.html), [JVM comando especificação](https://docs.oracle.com/javase/specs/jvms/se8/html/jvms-6.html).

## Java ficheiro E_S

[FileDemo.java](../posix-kor/자바예제/FileDemo.java)는 일반 Java 표준 aula_VALOR 이름을 사용한다. 소스를 `edit FileDemo.java`로 입력하거나 `JAVA_FILES`로 arranque_da_máquina 이미지에 넣은 BACK_VALOR `javac FileDemo.java`, `java FileDemo`를 실행한다. 결과는 `65`, `255`, `66`, `-1`, `JAVA FILE IO PASS`다. `write(int)`는 하위 8비트를 쓰고 `read()`는 0~255 또는 EOF -1을 반환한다. valor_padrão saídaTexto 생성자는 내용을 비우고, boolean 인수가 true이면 이어쓴다.

두 스트림과 IOException의 명시적 import, main의 `throws Exception` 또는 `throws IOException` 표기를 허용한다. exceção objeto_VALOR·try/catch·try-with-resources는 지원하지 않으며 ficheiro 오류를 진단하고 프로그램을 종료한다. MATRIZ_VALOR E_S, InputStream/OutputStream으로의 다형성, Reader/Writer, getFD, 일반 ficheiro 메타데이터 API는 아직 없다. close는 열린 서술자를 닫고, 재부팅 보존에는 shell `sync`가 필요하다. 예제의 ficheiro 이름은 em_dia_item 셸과 파일체계에 맞춰 ASCII로 쓴다.

`os/testes/자바파일시험.py`는 real_dados 게스트 compilar_fonte 결과를 OpenJDK `-Xverify:all`로 repetir_VALOR 실행해 ficheiro 바이트와 출력을 대조한다. 범위와 Store_VALOR Mídia_VALOR 사용법은 [posix-kor LEIAME_eb81d7d9](../posix-kor/LEIAME_eb81d7d9.md)를 참고한다. 참고한 표준 API는 Oracle [FileOutputStream](https://docs.oracle.com/javase/8/docs/api/java/io/FileOutputStream.html)이다.
