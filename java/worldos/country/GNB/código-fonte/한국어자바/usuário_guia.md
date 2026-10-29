# jkoros Português biblioteca usuário_guia

확인일: 2026-09-27. 대상은 `platforms/rpi4`의 **ARM64 Linux + OpenJDK 실행판**이며, QEMU에서도 같은 Java 라이브러리를 사용한다. `os/`의 nativo x86 kernel_VALOR 및 `herdado_fonte/`의 관리 kernel_VALOR 모형과 구분한다.

## 1. em_dia_item 제공하는 biblioteca

패키지는 `Português.자바`, SO 안의 JAR 경로는 `/opt/jkoros/lib/한국어자바.jar`다. **auxiliar_VALOR aula_VALOR 5개, 공개 estático_VALOR método_VALOR 22개, 별도 GUI 프로그램인 workspace 1개**가 있다. JAR는 Java 11 이상을 대상으로 빌드하며 em_dia_item ARM64 배포판에는 OpenJDK 25가 포함돼 있다.

| aula_VALOR | método_VALOR número | 기능 | códigoFonte |
|---|---:|---|---|
| `ficheiro` | 9 | UTF-8 텍스트·byte_VALOR ficheiro, Diretório_VALOR, entrada_Lista_f07b3200 | [ficheiro.java](códigoFonte/Português/자바/ficheiro.java) |
| `문자` | 5 | UTF-8 CONVERTER_VALOR, NFC normalizar_VALOR, valor_do_código 포인트, cadeia_VALOR limite_VALOR | [문자.java](códigoFonte/Português/자바/문자.java) |
| `comunicação` | 2 | HTTP(S) GET, TCP Ligar | [comunicação.java](códigoFonte/Português/자바/comunicação.java) |
| `작업` | 4 | 스레드 Executar_comando·aguarde_VALOR, 고정 Tamanho 작업 app_Launcher | [작업.java](códigoFonte/Português/자바/작업.java) |
| `tela` | 2 | Swing 이벤트 Processo_VALOR_entrada 가닥에 작업 예약, Janela gerar | [tela.java](códigoFonte/Português/자바/tela.java) |
| `workspace` | ponto_de_entrada `main` | Java códigoFonte Editar_VALOR·Store_VALOR·compilar_fonte·Executar_comando | [workspace.java](códigoFonte/Português/자바/workspace.java) |

표준 JDK 전체를 한국어로 번역한 라이브러리는 아니다. Java 키워드와 `String`, `Path`, `Socket`, `JFrame`, `IOException` 같은 표준 tipo_de_dados·예외를 함께 사용한다. 이 도우미에 없는 기능은 OpenJDK의 표준 API 또는 별도 라이브러리로 구현한다. 예를 들어 HTTP POST, UDP, Swing botão·메뉴에는 각각 표준 Java API를 사용한다.

## 2. Java에서 START_Tarefa

게스트 운영체제의 작업 폴더에서 `사용예.java`를 작성한다.

```java
import Português.자바.*;
import java.nio.file.Path;

public class 사용예 {
    public static void main(String[] argumentos) throws Exception {
        Path Diretório_VALOR = ficheiro.Criar_Diretório(ficheiro.caminho("사용예자료"));
        Path 문서 = Diretório_VALOR.resolve("saudação_ae353e94.txt");
        ficheiro.Escrita(문서, "한글 😀");
        String Conteúdo_VALOR = ficheiro.Leitura(문서);
        System.out.println(Conteúdo_VALOR);
        System.out.println(문자.ponto_de_código_CONT_NÚM(Conteúdo_VALOR)); // 한, texto, 공백, 😀 → 4
        Thread Trabalho_VALOR = 작업.iniciar("saudação_ae353e94 작업", () -> System.out.println("작업 Executar_comando"));
        작업.기다리기(Trabalho_VALOR);
    }
}
```

```sh
javac -encoding UTF-8 -cp /opt/jkoros/lib/한국어자바.jar 사용예.java
java -cp .:/opt/jkoros/lib/한국어자바.jar 사용예
```

로그인 환경에 valor_padrão `CLASSPATH`도 설정돼 있지만, 명시적인 `-cp`는 다른 Executar_comando 환경에서도 경로를 분명하게 한다. 사용자가 `-cp`를 지정하면 필요한 JAR와 aula_VALOR 폴더를 모두 그 값에 포함해야 한다.

host 저장소에서는 다음처럼 construir·실행한다. host 경로와 게스트의 `/opt/...` 경로는 서로 다르다.

```sh
cd /home/user/jkoros/한국어자바
make
javac -encoding UTF-8 -cp build/한국어자바.jar 예제/saudação_ae353e94.java
java -cp build/한국어자바.jar:예제 saudação_ae353e94
```

## 3. 전체 auxiliar_VALOR API

아래 메서드는 모두 `public static`이며, 객체를 만들지 않고 `ficheiro.Leitura(...)`처럼 호출한다. 표의 이름은 real_dados fonte_árvore 및 JAR의 `javap -public` 결과와 대조했다. 선언된 검사 exceção 외에도 잘못된 argumentos 등에 대한 표준 Java Executar_comando 시 예외가 발생할 número 있다.

### ficheiro: `Português.자바.ficheiro`

`Path`는 `java.nio.file.Path`, `List`는 `java.util.List`다.

| método_VALOR | tipo_de_retorno | Acção·doença |
|---|---|---|
| `caminho(String Nome)` | `Path` | 이름을 caminho 객체로 CONVERTER_VALOR. real_dados 파일을 만들지는 않음 |
| `Leitura(Path caminho)` | `String` | ficheiro 전체를 UTF-8 텍스트로 leitura_RC |
| `Escrita(Path caminho, String Conteúdo_VALOR)` | `Path` | UTF-8 Store_VALOR. 파일이 없으면 생성하고, 있으면 기존 내용을 비움 |
| `leitura_byte_VALOR(Path caminho)` | `byte[]` | ficheiro 전체를 byte_VALOR 배열로 leitura_RC |
| `gravar_byte_VALOR(Path caminho, byte[] Conteúdo_VALOR)` | `Path` | byte_VALOR Store_VALOR. 없으면 생성하고, 있으면 기존 내용을 비움 |
| `Criar_Diretório(Path caminho)` | `Path` | 필요한 상위 폴더까지 gerar |
| `있는가(Path caminho)` | `boolean` | 존재 여부 verificar. 확인할 número 없는 경우도 `false`Trabalho_VALOR número 있음 |
| `apagar_entrada(Path caminho)` | `boolean` | 삭제했으면 `true`, 없으면 `false`. 폴더의 재귀 삭제는 아님 |
| `entrada_Lista_f07b3200(Path caminho)` | `List<Path>` | 바로 아래 항목을 caminho alinhar_VALOR 순서로 devolver_RC. 재귀 탐색은 아님 |

`caminho`, `있는가`를 제외한 위 메서드는 `IOException`을 선언한다. `Escrita`와 `gravar_byte_VALOR`는 상위 폴더를 자동으로 만들거나 내용을 이어 쓰지 않는다. 필요한 폴더는 먼저 생성한다. 큰 파일은 전체 내용을 메모리에 담는 대신 표준 Java 스트림·Canal_VALOR API를 사용하는 방식으로 작성할 número 있다.

### 문자: `Português.자바.문자`

| método_VALOR | tipo_de_retorno | Acção·doença |
|---|---|---|
| `codificar(String Conteúdo_VALOR)` | `byte[]` | 문자열을 UTF-8 바이트로 CONVERTER_VALOR |
| `descriptografar_dados(byte[] Conteúdo_VALOR)` | `String` | UTF-8 바이트를 문자열로 CONVERTER_VALOR. 잘못된 입력은 대체 문자로 Processo_VALOR_entrada |
| `normalizar_VALOR(String Conteúdo_VALOR)` | `String` | UNICODE_VALOR NFC normalizar_VALOR. 예: composição_VALOR 자모 `ᄀ` + `ᅡ` → `가` |
| `ponto_de_código_CONT_NÚM(String Conteúdo_VALOR)` | `int` | UTF-16 valor_do_código 단위가 아닌 UNICODE_VALOR valor_do_código 포인트 número |
| `낱말(String Conteúdo_VALOR, Locale Idioma)` | `List<String>` | ceder_VALOR 언어의 `BreakIterator` 낱말 경계로 나눈 SMS_alcance |

`낱말`은 공백·문장부호 구간도 반환한다. 자연어 형태소 분석기나 공백을 제거한 Word_VALOR entrada_Lista_f07b3200 API는 아니다. `normalizar_VALOR`는 입력기나 mover_fonte 기능이 아니다. valor_do_código 포인트 número 역시 사람이 보는 caractere_VALOR 수와 항상 같지는 않다. 여러 valor_do_código 포인트로 이루어진 결합 문자·가족 이모지 등을 구분해야 한다.

### comunicação: `Português.자바.comunicação`

| método_VALOR | tipo_de_retorno | Acção·doença |
|---|---|---|
| `PEGAR_VALOR(URI Endereço, Duration limite_de_tempo)` | `HttpResponse<String>` | HTTP(S) GET. Ligar 및 solicitação limite_de_tempo Definições. resposta 본문을 UTF-8로 analisar_VALOR |
| `Connect_Endpoint(String Endereço, int hardware_porta, int 제한밀리초)` | `Socket` | TCP Ligar 후 같은 값으로 Leitura 제한시간도 Definições |

`PEGAR_VALOR`는 `IOException`, `InterruptedException`을 선언한다. 제한시간은 양수다. 404·500 같은 HTTP erro 상태도 응답으로 반환하므로 `statusCode()`로 판단하고 `body()`로 본문을 읽는다. em_dia_item 구현은 호출마다 HTTP 클라이언트를 만들며 자동 리다이렉트 설정을 추가하지 않는다.

`Connect_Endpoint`는 `IOException`을 선언한다. 연결된 소켓은 호출자가 `close()` 또는 try-with-resources로 닫아야 한다. 제한밀리초의 0은 제한 없음이며, Escrita 전체의 data_limite_VALOR 시간을 보장하는 옵션은 아니다.

```java
var resposta = comunicação.PEGAR_VALOR(
    java.net.URI.create("http://127.0.0.1:8000/"),
    java.time.Duration.ofSeconds(5));
System.out.println(resposta.statusCode());
System.out.println(resposta.body());
```

위 조각은 método_VALOR 안에서 실행하며 별도로 해당 주소의 서버를 실행해야 한다. Java exceção 처리가 필요하다.

### 작업: `Português.자바.작업`

| método_VALOR | tipo_de_retorno | Acção·doença |
|---|---|---|
| `iniciar(String Nome, Runnable Acção)` | `Thread` | 이름을 지정한 스레드를 만들고 즉시 iniciar |
| `기다리기(Thread thread_VALOR)` | `void` | 해당 스레드가 종료할 때까지 `join()` |
| `쉬기(long 밀리초)` | `void` | 호출한 스레드를 ceder_VALOR valor_temporal 동안 `sleep()` |
| `Workbench_VALOR(int contagem_de_threads)` | `ExecutorService` | 고정 Tamanho 작업 app_Launcher gerar. 가닥수는 양수 |

`기다리기`, `쉬기`는 `InterruptedException`을 선언한다. 작업 실행기는 uso_VALOR 후 `shutdown()`으로 종료하고 필요하면 `awaitTermination(...)`으로 완료를 기다린다. Swing 이벤트 Processo_VALOR_entrada 가닥에서 긴 작업이나 `기다리기`를 실행하면 화면이 멈출 número 있다.

### tela: `Português.자바.tela`

| método_VALOR | tipo_de_retorno | Acção·doença |
|---|---|---|
| `나중에(Runnable Acção)` | `void` | Swing 이벤트 Processo_VALOR_entrada 가닥에 실행을 예약하고 devolver_RC |
| `Janela(String janela_Título, JComponent Conteúdo_VALOR, int 너비, int altura_VALOR)` | `JFrame` | Conteúdo_VALOR·크기를 지정한 창을 생성해 mostrar_VALOR |

`Janela`을 Swing 이벤트 Processo_VALOR_entrada thread_VALOR 밖에서 부르면 `IllegalStateException`이 발생한다. 그래픽 세션도 필요하다. QEMU에서는 VNC 데스크톱의 터미널에서 실행한다.

```java
tela.나중에(() -> tela.Janela(
    "Português tela", new javax.swing.JLabel("안녕하세요"), 500, 180));
```

반환된 `JFrame`에 표준 Swing API를 추가로 사용할 número 있다. 창의 Fechar 동작은 `DISPOSE_ON_CLOSE`다. `tela.나중에`가 반환됐다고 Janela 생성이 이미 끝난 것은 아니다.

### workspace: Editar_VALOR·compilar_fonte GUI

```sh
java -cp /opt/jkoros/lib/한국어자바.jar Português.자바.workspace
```

`~/workspace`의 원문을 Abrir·저장하고, `javac`로 컴파일해 `java`로 실행한다. Executar_comando ficheiro 만들기는 `jclassc --target openjdk` 경로를 사용한다. 작업마당은 개발용 프로그램이며 별도의 ficheiro·문자 API 클래스가 아니다. 생성하는 Executar_comando ficheiro 방식은 [compilador 설명](../compiler/OpenJDK-executável.md)을 따른다.

## 4. Python과 C++에서 사용할 número 있는가?

| método_MODO | em_dia_item declarações Estado_VALOR | 호출 가능 recortar |
|---|---|---|
| Java → Português JAR | valor_padrão declarações | 위 22개 메서드와 workspace |
| Python → `java` filho_VALOR 프로세스 | Python·Java valor_padrão declarações | 작은 Java 진입점을 통해 호출하고 표준 saídaTexto·ficheiro 등으로 resultado Avançar_VALOR |
| Python → JPype → JVM | JPype는 valor_padrão 배포에 없음 | 별도 instalar_VALOR 후 Java aula_VALOR·método_VALOR 호출 가능. 이 배포판의 ARM64/musl/Python 3.14 조합은 Acrescentar_entrada validar 필요 |
| C++ → JNI → JVM | `g++`, JNI 헤더, `libjvm.so` declarações | JVM을 생성하고 Português aula_VALOR·메서드를 직접 호출할 número 있음 |
| Python용 독립 Português biblioteca | em_dia_item valor_padrão 제공 없음 | 필요하면 Python 표준 라이브러리를 감싸는 Português 모듈을 별도로 작성 |
| C/C++용 독립 Português biblioteca | nativo x86 `posix-kor`와 nativo ARM64 커널용 estado_inicial RAM ficheiro 연결이 별도로 존재 | 둘 다 이 Linux/OpenJDK 실행판의 libc 라이브러리는 아님 |

Python의 일반 `import`SEGUNDO_operando `ctypes.CDLL`로 JAR를 바로 읽을 수는 없다. C++의 `#include`SEGUNDO_operando 일반 네이티브 링커만으로 Java 메서드를 연결할 수도 없다. JVM 프로세스 또는 JVM Ligar 계층을 거쳐야 한다.

### Python: Acrescentar_entrada 패키지 없이 호출

Executar_comando 가능한 예제 원문은 [문자명령.java](예제/다른언어/문자명령.java), [PYTHON_Chamadas.py](예제/다른언어/PYTHON_Chamadas.py)다. Python이 Java 진입점을 실행하고 `문자.ponto_de_código_CONT_NÚM`의 inteiro 결과를 받는다. argumentos 목록을 사용하며 shell comando 문자열을 조립하지 않는다. `subprocess.run`의 프로세스 Executar_comando·sair_app valor_do_código·saídaTexto Processo_VALOR_entrada 방식은 [Python 공식 문서](https://docs.python.org/3/library/subprocess.html)를 따른다.

두 예제 파일을 게스트의 같은 폴더에 복사한 BACK_VALOR 그 폴더에서 실행한다. 예제 ficheiro 자체는 valor_padrão 시스템 이미지에 자동 설치돼 있지 않다.

```sh
mkdir -p classes
javac -encoding UTF-8 -cp /opt/jkoros/lib/한국어자바.jar -d classes 문자명령.java
python3 PYTHON_Chamadas.py --text '한글 😀'
```

saídaTexto: `Python → Português.자바.문자.ponto_de_código_CONT_NÚM: 4`

이 예제의 Python FUNÇÃO_VALOR `ponto_de_código_CONT_NÚM`는 이번 문서의 Ligar 예제이며 기존에 설치된 Python 라이브러리는 아니다. em_dia_item 예제는 호출할 때마다 JVM 프로세스를 시작한다. Java objeto_VALOR 자체를 Python으로 가져오는 방식은 아니며, 다른 메서드를 사용하려면 진입점의 argumentos·resultado 형식을 확장한다.

### Python: JPype로 같은 프로세스에서 호출

JPype를 별도 설치한 환경에서는 Avançar_item 형태로 연결할 número 있다. **아래는 seleção_VALOR 가능한 Ligar 방법이며, em_dia_item 배포판에 JPype가 설치돼 있거나 Executar_comando 검증됐다는 뜻은 아니다.** JVM 시작과 `JClass`를 통한 aula_VALOR 접근은 [JPype 공식 설명](https://jpype.readthedocs.io/en/latest/userguide.html)을 참고한다.

```python
import jpype

jpype.startJVM(
    "/usr/lib/jvm/java-25-openjdk/lib/server/libjvm.so",
    classpath=["/opt/jkoros/lib/한국어자바.jar"])
try:
    문자 = jpype.JClass("Português.자바.문자")
    print(문자.ponto_de_código_CONT_NÚM(jpype.JString("한글 😀")))
finally:
    jpype.shutdownJVM()
```

Python·JVM·Ligar 모듈의 CPU 아키텍처가 맞아야 한다. 이 실행판은 ARM64 + musl이므로 일반 x86_64/glibc용 바이너리를 그대로 설치하는 방식은 맞지 않는다. JPype instalar_VALOR·패키지 빌드는 이번 문서 작업에서 수행하지 않았다.

### C++: JNI로 직접 호출

[자바호출.cpp](예제/다른언어/자바호출.cpp)는 real_dados Executar_comando 가능한 예제다. JVM을 작업 스레드에서 생성하고 Avançar_item 메서드를 찾는다.

```cpp
jclass type = env->FindClass("Português/자바/문자");
jmethodID method = env->GetStaticMethodID(
    type, "ponto_de_código_CONT_NÚM", "(Ljava/lang/String;)I");
```

JVM gerar·종료와 스레드 연결은 [JNI Invocation API](https://docs.oracle.com/en/java/javase/25/docs/specs/jni/invocation.html)의 방식이다. `JNIEnv*`는 gerar·연결된 스레드에서 사용해야 한다. 예제는 Java 예외를 확인하고 JVM 종료까지 처리한다.

게스트에 `자바호출.cpp`를 복사한 BACK_VALOR 컴파일한다. 로그인 환경의 `JAVA_HOME`은 `/usr/lib/jvm/java-25-openjdk`다.

```sh
g++ -std=c++11 -Wall -Wextra -pthread \
  -I"$JAVA_HOME/include" -I"$JAVA_HOME/include/linux" \
  자바호출.cpp -L"$JAVA_HOME/lib/server" \
  -Wl,-rpath,"$JAVA_HOME/lib/server" -ljvm -o 자바호출
./자바호출 /opt/jkoros/lib/한국어자바.jar
```

saídaTexto: `C++ → Português.자바.문자.ponto_de_código_CONT_NÚM: 4`

예제는 `한글 😀`을 UTF-16으로 만들어 `NewString`에 전달한다. `NewStringUTF`가 받는 modified UTF-8은 일반 UTF-8과 차이가 있으므로, 일반 UTF-8 이모지 바이트를 그대로 넘기는 예제로 작성하지 않았다. [JNI cadeia_VALOR formato_VALOR](https://docs.oracle.com/en/java/javase/25/docs/specs/jni/types.html#modified-utf-8-strings)

다른 Português 메서드도 JNI 서명과 argumentos 자료형을 맞춰 호출할 número 있다. 예를 들어 `Path`를 받는 ficheiro API는 먼저 `ficheiro.caminho`로 Java caminho 객체를 얻어 전달한다. Swing 호출에는 그래픽 세션과 이벤트 Processo_VALOR_entrada thread_VALOR 규칙도 그대로 적용된다. JNI는 Java 실행을 기계어로 대체하는 기능이 아니며 JVM이 계속 필요하다.

### 기존 posix-kor와의 관계

추가된 [nativo ARM64 Ligar](../posix-kor/arm64-native/LEIAME_eb81d7d9.md)은 C++에서 AOT Java 커널의 RAM ficheiro API를 직접 호출하며, 별도 EL0 espaço_do_utilizador 라이브러리로 ficheiro/UDP 루프백 SVC 호출도 제공한다. JNI를 사용하지 않는다. 이 문서의 ARM64 **Linux** 및 Português Java JAR와는 다른 Executar_comando 기반이며 nativo 커널은 별도 제한형 Java compilador/JVM과 MicroPython 1.24.1을 실행한다. MicroPython의 `import jkoros`로 Java kernel_VALOR ficheiro·UDP 루프백·retângulo 호출이 가능하지만 이 문서의 JAR를 가져오는 기능은 아니다. nativo 커널의 전체 OpenJDK/JRE/CPython 이식은 아직 미완성이다.

[posix-kor](../posix-kor/LEIAME_eb81d7d9.md)에는 `abrir_Arquivo`, `leitura_Arquivo_dados`, `gravar_Arquivo_dados`, `Close_Arquivo`, `Criar_empresa`, `enviar_datagrama_dados` 등의 Português C 별칭이 있다. 그러나 구현은 **nativo jkoros i386 커널의 `int 0x80` 호출 규약용**이다.

이 `libposix-kor.a`와 nativo `sys/stat.h` 등의 헤더는 em_dia_item ARM64 Linux 실행판의 libc/C++용 라이브러리가 아니다. 해당 헤더·바이너리를 ARM64 Linux 프로그램에 그대로 연결해서는 ABI가 맞지 않는다. C++용 Português aula_VALOR 라이브러리나 Python용 바인딩을 valor_padrão 제공하는 상태도 아니다. em_dia_item Linux 실행판에서 그와 같은 독립 API를 제공하려면 Linux 표준 라이브러리를 대상으로 별도로 implementação·빌드해야 한다.

## 5. verificar 범위와 재현

패키지 declarações 여부는 [distribuição_VALOR 패키지 entrada_Lista_f07b3200](../platforms/rpi4/dist/packages.lock.json) 및 construir 루트의 real_dados 파일로 확인했다. JNI 헤더는 JDK의 `include/jni.h`, `include/linux/jni_md.h`, JVM 라이브러리는 `lib/server/libjvm.so`에 있다. 사용자가 이후 별도로 설치한 패키지는 이 valor_padrão distribuição_VALOR 목록과 다를 número 있다.

이번에 **host x86_64/OpenJDK 11에서** Python filho_VALOR 프로세스 호출과 C++ JNI 직접 호출을 compilar_fonte·실행해 각각 resultado 4를 확인했다. JAR 공개 메서드도 소스와 대조했다. Python Ligar 예제는 Acrescentar_entrada 패키지를 설치하지 않는다.

문서의 Java uso_VALOR 예제도 compilar_fonte·실행했고, 22개 메서드의 문서 declarações 여부와 로컬 문서 링크를 확인했다. [예제 validar LOG_linha](build/다른언어/validação_relatar.json)

기존 ARM64 QEMU에서는 Java의 ficheiro·UNICODE_VALOR·스레드·HTTP 및 Swing testes 결과가 있다. 이번 Python/C++ Ligar 예제의 **ARM64 게스트 실행과 JPype 설치는 별도 검증하지 않았다.** 이미지와 Executar_comando 중인 espaço_do_utilizador 환경은 이 문서 작업에서 변경하지 않았다. [기존 SO validar LOG_linha](../platforms/rpi4/VERIFICATION.md)

호스트에서 Python 예제를 재현하려면:

```sh
cd /home/user/jkoros/한국어자바
make
mkdir -p build/다른언어
javac -encoding UTF-8 --release 11 -cp build/한국어자바.jar \
  -d build/다른언어 예제/다른언어/문자명령.java
python3 예제/다른언어/PYTHON_Chamadas.py \
  --jar build/한국어자바.jar --classes build/다른언어
```

host C++ 예제는 위 JNI compilar_fonte 명령의 JDK 경로를 **host JDK caminho**로 바꾸고, códigoFonte `예제/다른언어/자바호출.cpp`와 JAR `build/한국어자바.jar`를 지정한다. ARM64 게스트 JDK의 헤더·biblioteca 경로를 host x86_64 링크 명령에 섞지 않는다.
