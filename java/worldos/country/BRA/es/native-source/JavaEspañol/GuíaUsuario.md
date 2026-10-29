# jkoros español biblioteca GuíaUsuario

확인일: 2026-09-27. 대상은 `platforms/rpi4`의 **ARM64 Linux + OpenJDK 실행판**이며, QEMU에서도 같은 Java 라이브러리를 사용한다. `os/`의 propio x86 valorNúcleo 및 `FuentesFundamentales/`의 관리 valorNúcleo 모형과 구분한다.

## 1. elementoListaActual 제공하는 biblioteca

패키지는 `español.Java`, SistemaOperativo 안의 JAR 경로는 `/opt/jkoros/lib/JavaEspañol.jar`operandoTercero. **valorAyudante valorClase 5개, 공개 valorEstático valorMétodo 22개, 별도 GUI 프로그램인 EspacioTrabajo 1개**operandoPrimero 있다. JAR는 Java 11 이상을 대상으로 빌드하며 elementoListaActual ARM64 배포판에는 OpenJDK 25가 포함돼 있다.

| valorClase | valorMétodo númeroValor | 기능 | fuente |
|---|---:|---|---|
| `Archivo` | 9 | UTF-8 텍스트·valorByte Archivo, valorDirectorio, listaEntradaElemento | [Archivo.java](fuente/español/Java/Archivo.java) |
| `Caracteres` | 5 | UTF-8 convertirValor, NFC normalizarValor, valorCódigo 포인트, Cadena valorFrontera | [Caracteres.java](fuente/español/Java/Caracteres.java) |
| `Comunicación` | 2 | HTTP(S) GET, TCP conectar | [Comunicación.java](fuente/español/Java/Comunicación.java) |
| `Tarea` | 4 | 스레드 ejecutarComando·esperarValor, 고정 tamaño Tarea LanzadorPrograma | [Tarea.java](fuente/español/Java/Tarea.java) |
| `Pantalla` | 2 | Swing 이벤트 entradaElementoValorProceso 가닥에 Tarea 예약, ventana generar | [Pantalla.java](fuente/español/Java/Pantalla.java) |
| `EspacioTrabajo` | puntoEntradaElemento `main` | Java fuente valorEditar·valorAlmacenar·compilarFuente·ejecutarComando | [EspacioTrabajo.java](fuente/español/Java/EspacioTrabajo.java) |

표준 JDK 전체를 한국어로 번역한 라이브러리는 아니다. Java 키워드와 `String`, `Path`, `Socket`, `JFrame`, `IOException` 같은 표준 tipoDatos·예외를 함께 사용한다. 이 도우미에 없는 기능은 OpenJDK의 표준 API 또는 별도 라이브러리로 구현한다. 예를 들어 HTTP POST, UDP, Swing botón·메뉴에는 각각 표준 Java API를 사용한다.

## 2. Java에서 iniciarTarea

게스트 운영체제의 Tarea 폴더에서 `사용예.java`를 작성한다.

```java
import español.Java.*;
import java.nio.file.Path;

public class 사용예 {
    public static void main(String[] argumentos) throws Exception {
        Path valorDirectorio = Archivo.crearDirectorio(Archivo.ruta("사용예자료"));
        Path Documentación = valorDirectorio.resolve("Saludo.txt");
        Archivo.escribir(Documentación, "textoHangul 😀");
        String valorContenidoValor = Archivo.leer(Documentación);
        System.out.println(valorContenidoValor);
        System.out.println(Caracteres.númeroElementosPuntoCódigo(valorContenidoValor)); // 한, texto, 공백, 😀 → 4
        Thread valorTrabajo = Tarea.ponerEnMarcha("Saludo Tarea", () -> System.out.println("Tarea ejecutarComando"));
        Tarea.esperarFin(valorTrabajo);
    }
}
```

```sh
javac -encoding UTF-8 -cp /opt/jkoros/lib/JavaEspañol.jar 사용예.java
java -cp .:/opt/jkoros/lib/JavaEspañol.jar 사용예
```

로그인 환경에 valorPredeterminado `CLASSPATH`도 설정돼 있지만, 명시적인 `-cp`는 다른 ejecutarComando 환경에서도 경로를 분명하게 한다. 사용자가 `-cp`를 지정하면 필요한 JAR와 valorClase 폴더를 construirTodos 그 값에 포함해야 한다.

Anfitrión 저장소에서는 다음처럼 construirSistema·실행한다. Anfitrión 경로와 게스트의 `/opt/...` 경로는 서로 다르다.

```sh
cd /home/user/jkoros/JavaEspañol
make
javac -encoding UTF-8 -cp build/JavaEspañol.jar Ejemplos/Saludo.java
java -cp build/JavaEspañol.jar:Ejemplos Saludo
```

## 3. 전체 valorAyudante API

valorExtremoInferior 메서드는 construirTodos `public static`이며, 객체를 만들지 않고 `Archivo.leer(...)`처럼 호출한다. 표의 이름은 datosEfectivo árbolFuente 및 JAR의 `javap -public` 결과와 대조했다. 선언된 Comprobaciones excepción 외에도 잘못된 argumentos 등에 대한 표준 Java ejecutarComando 시 예외가 발생할 númeroValor 있다.

### Archivo: `español.Java.Archivo`

`Path`는 `java.nio.file.Path`, `List`는 `java.util.List`operandoTercero.

| valorMétodo | tipoRetornar | acción·condición |
|---|---|---|
| `ruta(String nombre)` | `Path` | 이름을 ruta 객체로 convertirValor. datosEfectivo 파일을 만들지는 않음 |
| `leer(Path ruta)` | `String` | Archivo 전체를 UTF-8 텍스트로 leerResultado |
| `escribir(Path ruta, String valorContenidoValor)` | `Path` | UTF-8 valorAlmacenar. 파일이 없으면 생성하고, 있으면 기존 내용을 비움 |
| `leerValorByte(Path ruta)` | `byte[]` | Archivo 전체를 valorByte 배열로 leerResultado |
| `escribirValorByte(Path ruta, byte[] valorContenidoValor)` | `Path` | valorByte valorAlmacenar. 없으면 생성하고, 있으면 기존 내용을 비움 |
| `crearDirectorio(Path ruta)` | `Path` | 필요한 상위 폴더까지 generar |
| `efectúaExistencia(Path ruta)` | `boolean` | 존재 여부 verificar. 확인할 númeroValor 없는 경우도 `false`valorTrabajo númeroValor 있음 |
| `borrarEntradaElemento(Path ruta)` | `boolean` | 삭제했으면 `true`, 없으면 `false`. 폴더의 재귀 삭제는 아님 |
| `listaEntradaElemento(Path ruta)` | `List<Path>` | 바로 valorExtremoInferior 항목을 ruta valorAlinear 순서로 resultadoRetornar. 재귀 탐색은 아님 |

`ruta`, `efectúaExistencia`를 제외한 valorExtremoSuperior 메서드는 `IOException`을 선언한다. `escribir`와 `escribirValorByte`는 상위 폴더를 자동으로 만들거나 내용을 valorContinuación 쓰지 않는다. 필요한 폴더는 먼저 생성한다. 큰 파일은 전체 내용을 메모리에 담는 대신 표준 Java 스트림·valorCanal API를 사용하는 방식으로 작성할 númeroValor 있다.

### Caracteres: `español.Java.Caracteres`

| valorMétodo | tipoRetornar | acción·condición |
|---|---|---|
| `codificar(String valorContenidoValor)` | `byte[]` | 문자열을 UTF-8 바이트로 convertirValor |
| `descifrarDatos(byte[] valorContenidoValor)` | `String` | UTF-8 바이트를 문자열로 convertirValor. 잘못된 입력은 대체 문자로 entradaElementoValorProceso |
| `normalizarValor(String valorContenidoValor)` | `String` | valorUnicode NFC normalizarValor. 예: Combinación valorLetraHangul `ᄀ` + `ᅡ` → `operandoPrimero` |
| `númeroElementosPuntoCódigo(String valorContenidoValor)` | `int` | UTF-16 valorCódigo 단위가 아닌 valorUnicode valorCódigo 포인트 númeroValor |
| `palabraLéxico(String valorContenidoValor, Locale Lengua)` | `List<String>` | valorAsignar 언어의 `BreakIterator` palabraLéxico 경계로 나눈 rangoTexto |

`palabraLéxico`은 공백·문장부호 구간도 반환한다. 자연어 형태소 분석기나 공백을 제거한 valorPalabra listaEntradaElemento API는 아니다. `normalizarValor`는 입력기나 traducirFuente 기능이 아니다. valorCódigo 포인트 númeroValor 역시 사람이 보는 valorCarácter 수와 항상 같지는 않다. 여러 valorCódigo 포인트로 이루어진 valoresCombinar Caracteres·가족 이모지 등을 구분해야 한다.

### Comunicación: `español.Java.Comunicación`

| valorMétodo | tipoRetornar | acción·condición |
|---|---|---|
| `valorTomar(URI dirección, Duration límiteTiempo)` | `HttpResponse<String>` | HTTP(S) GET. conectar 및 petición límiteTiempo ajustes. respuesta 본문을 UTF-8로 analizarValor |
| `conectarExtremo(String dirección, int puertoEquipoFísico, int milisegundosLímite)` | `Socket` | TCP conectar estadoValorDespués 같은 값으로 leer 제한시간도 ajustes |

`valorTomar`는 `IOException`, `InterruptedException`을 선언한다. 제한시간은 양수다. 404·500 같은 HTTP error 상태도 응답으로 반환하므로 `statusCode()`로 판단하고 `body()`로 본문을 읽는다. elementoListaActual 구현은 호출마다 HTTP 클라이언트를 만들며 자동 리다이렉트 설정을 추가하지 않는다.

`conectarExtremo`는 `IOException`을 선언한다. 연결된 소켓은 호출자가 `close()` 또는 try-with-resources로 닫아야 한다. 제한밀리초의 0은 valorLímite 없음이며, escribir 전체의 valorPlazo 시간을 보장하는 옵션은 아니다.

```java
var respuesta = Comunicación.valorTomar(
    java.net.URI.create("http://127.0.0.1:8000/"),
    java.time.Duration.ofSeconds(5));
System.out.println(respuesta.statusCode());
System.out.println(respuesta.body());
```

valorExtremoSuperior 조각은 valorMétodo 안에서 실행하며 별도로 해당 주소의 서버를 실행해야 한다. Java excepción 처리가 필요하다.

### Tarea: `español.Java.Tarea`

| valorMétodo | tipoRetornar | acción·condición |
|---|---|---|
| `ponerEnMarcha(String nombre, Runnable acción)` | `Thread` | 이름을 지정한 스레드를 만들고 즉시 ponerEnMarcha |
| `esperarFin(Thread valorHiloEjecución)` | `void` | 해당 스레드가 종료할 때까지 `join()` |
| `brevementeRestanteParte(long milisegundos)` | `void` | 호출한 스레드를 valorAsignar valorTiempo 동안 `sleep()` |
| `valorBancoTrabajo(int númeroElementosHiloEjecución)` | `ExecutorService` | 고정 tamaño Tarea LanzadorPrograma generar. 가닥수는 양수 |

`esperarFin`, `brevementeRestanteParte`는 `InterruptedException`을 선언한다. Tarea 실행기는 valorUsar estadoValorDespués `shutdown()`으로 종료하고 필요하면 `awaitTermination(...)`으로 완료를 기다린다. Swing 이벤트 entradaElementoValorProceso 가닥에서 긴 작업이나 `esperarFin`를 실행하면 화면이 멈출 númeroValor 있다.

### Pantalla: `español.Java.Pantalla`

| valorMétodo | tipoRetornar | acción·condición |
|---|---|---|
| `valorPosterior(Runnable acción)` | `void` | Swing 이벤트 entradaElementoValorProceso 가닥에 실행을 예약하고 resultadoRetornar |
| `ventana(String títuloVentana, JComponent valorContenidoValor, int valorAnchura, int valorAltura)` | `JFrame` | valorContenidoValor·크기를 지정한 창을 생성해 mostrarValor |

`ventana`을 Swing 이벤트 entradaElementoValorProceso valorHiloEjecución 밖에서 부르면 `IllegalStateException`이 발생한다. 그래픽 세션도 필요하다. QEMU에서는 VNC 데스크톱의 터미널에서 실행한다.

```java
Pantalla.valorPosterior(() -> Pantalla.ventana(
    "español Pantalla", new javax.swing.JLabel("안녕하세요"), 500, 180));
```

반환된 `JFrame`에 표준 Swing API를 추가로 사용할 númeroValor 있다. 창의 cerrar 동작은 `DISPOSE_ON_CLOSE`operandoTercero. `Pantalla.valorPosterior`operandoPrimero 반환됐다고 ventana 생성이 이미 끝난 것은 아니다.

### EspacioTrabajo: valorEditar·compilarFuente GUI

```sh
java -cp /opt/jkoros/lib/JavaEspañol.jar español.Java.EspacioTrabajo
```

`~/workspace`의 원문을 abrir·저장하고, `javac`로 컴파일해 `java`로 실행한다. ejecutarComando Archivo 만들기는 `jclassc --target openjdk` 경로를 사용한다. 작업마당은 개발용 프로그램이며 별도의 Archivo·Caracteres API 클래스가 아니다. 생성하는 ejecutarComando Archivo 방식은 [Compilador descripción](../compiler/OpenJDK-archivoCódigoEjecutable.md)을 따른다.

## 4. Python과 C++에서 사용할 númeroValor efectúaExistencia?

| modoMétodo | elementoListaActual Encabezados valorEstadoValor | invocar 가능 recortar |
|---|---|---|
| Java → español JAR | valorPredeterminado Encabezados | valorExtremoSuperior 22개 메서드와 EspacioTrabajo |
| Python → `java` valorHijo 프로세스 | Python·Java valorPredeterminado Encabezados | 작은 Java 진입점을 통해 호출하고 표준 Salida·Archivo 등으로 resultado valorAdelante |
| Python → JPype → JVM | JPype는 valorPredeterminado 배포에 métodoAusente | 별도 instalarValor estadoValorDespués Java valorClase·valorMétodo invocar 가능. 이 배포판의 ARM64/musl/Python 3.14 조합은 añadirFinalEntradaElemento validar valorNecesario |
| C++ → JNI → JVM | `g++`, JNI 헤더, `libjvm.so` Encabezados | JVM을 생성하고 español valorClase·메서드를 직접 호출할 númeroValor 있음 |
| Python용 독립 español biblioteca | elementoListaActual valorPredeterminado 제공 métodoAusente | 필요하면 Python 표준 라이브러리를 감싸는 español 모듈을 별도로 작성 |
| C/C++용 독립 español biblioteca | propio x86 `posix-kor`와 propio ARM64 커널용 estadoValorInicialValor RAM Archivo 연결이 별도로 존재 | valorDos operandoTercero 이 Linux/OpenJDK 실행판의 libc 라이브러리는 아님 |

Python의 일반 `import`operandoSegundo `ctypes.CDLL`로 JAR를 바로 읽을 수는 없다. C++의 `#include`operandoSegundo 일반 네이티브 링커만으로 Java 메서드를 연결할 수도 없다. JVM 프로세스 또는 JVM conectar 계층을 거쳐야 한다.

### Python: añadirFinalEntradaElemento 패키지 없이 invocar

ejecutarComando 가능한 Ejemplos 원문은 [ComandoTexto.java](Ejemplos/OtrasLenguas/ComandoTexto.java), [LlamadaPython.py](Ejemplos/OtrasLenguas/LlamadaPython.py)operandoTercero. Python이 Java 진입점을 실행하고 `Caracteres.númeroElementosPuntoCódigo`의 EnteroValor 결과를 받는다. argumentos 목록을 사용하며 intérpreteComandos comando 문자열을 조립하지 않는다. `subprocess.run`의 프로세스 ejecutarComando·programaSalir valorCódigo·Salida entradaElementoValorProceso 방식은 [Python 공식 Documentación](https://docs.python.org/3/library/subprocess.html)를 따른다.

두 Ejemplos 파일을 게스트의 같은 폴더에 복사한 valorLadoPosterior 그 폴더에서 실행한다. Ejemplos Archivo 자체는 valorPredeterminado 시스템 이미지에 자동 설치돼 있지 않다.

```sh
mkdir -p classes
javac -encoding UTF-8 -cp /opt/jkoros/lib/JavaEspañol.jar -d classes ComandoTexto.java
python3 LlamadaPython.py --text 'textoHangul 😀'
```

Salida: `Python → español.Java.Caracteres.númeroElementosPuntoCódigo: 4`

이 예제의 Python Función `númeroElementosPuntoCódigo`는 이번 문서의 conectar 예제이며 기존에 설치된 Python 라이브러리는 아니다. elementoListaActual 예제는 호출할 때마다 JVM 프로세스를 시작한다. Java valorObjeto 자체를 Python으로 가져오는 방식은 아니며, 다른 메서드를 사용하려면 진입점의 argumentos·resultado 형식을 확장한다.

### Python: JPype로 같은 프로세스에서 invocar

JPype를 별도 설치한 환경에서는 elementoListaSiguiente 형태로 연결할 númeroValor 있다. **아래는 valorSelección 가능한 conectar 방법이며, elementoListaActual 배포판에 JPype가 설치돼 있거나 ejecutarComando 검증됐다는 뜻은 아니다.** JVM 시작과 `JClass`를 통한 valorClase 접근은 [JPype 공식 descripción](https://jpype.readthedocs.io/en/latest/userguide.html)을 참고한다.

```python
import jpype

jpype.startJVM(
    "/usr/lib/jvm/java-25-openjdk/lib/server/libjvm.so",
    classpath=["/opt/jkoros/lib/JavaEspañol.jar"])
try:
    Caracteres = jpype.JClass("español.Java.Caracteres")
    print(Caracteres.númeroElementosPuntoCódigo(jpype.JString("textoHangul 😀")))
finally:
    jpype.shutdownJVM()
```

Python·JVM·conectar 모듈의 CPU 아키텍처가 맞아야 한다. 이 실행판은 ARM64 + musl이므로 일반 x86_64/glibc용 바이너리를 그대로 설치하는 방식은 맞지 않는다. JPype instalarValor·패키지 빌드는 이번 Documentación 작업에서 수행하지 않았다.

### C++: JNI로 직접 invocar

[LlamadaJava.cpp](Ejemplos/OtrasLenguas/LlamadaJava.cpp)는 datosEfectivo ejecutarComando 가능한 예제다. JVM을 Tarea 스레드에서 생성하고 elementoListaSiguiente 메서드를 찾는다.

```cpp
jclass type = env->FindClass("español/Java/Caracteres");
jmethodID method = env->GetStaticMethodID(
    type, "númeroElementosPuntoCódigo", "(Ljava/lang/String;)I");
```

JVM generar·종료와 스레드 연결은 [JNI Invocation API](https://docs.oracle.com/en/java/javase/25/docs/specs/jni/invocation.html)의 방식이다. `JNIEnv*`는 generar·연결된 스레드에서 사용해야 한다. 예제는 Java 예외를 확인하고 JVM 종료까지 처리한다.

게스트에 `LlamadaJava.cpp`를 복사한 valorLadoPosterior 컴파일한다. 로그인 환경의 `JAVA_HOME`은 `/usr/lib/jvm/java-25-openjdk`operandoTercero.

```sh
g++ -std=c++11 -Wall -Wextra -pthread \
  -I"$JAVA_HOME/include" -I"$JAVA_HOME/include/linux" \
  LlamadaJava.cpp -L"$JAVA_HOME/lib/server" \
  -Wl,-rpath,"$JAVA_HOME/lib/server" -ljvm -o LlamadaJava
./LlamadaJava /opt/jkoros/lib/JavaEspañol.jar
```

Salida: `C++ → español.Java.Caracteres.númeroElementosPuntoCódigo: 4`

예제는 `textoHangul 😀`을 UTF-16으로 만들어 `NewString`에 전달한다. `NewStringUTF`operandoPrimero 받는 modified UTF-8은 일반 UTF-8과 차이가 있으므로, 일반 UTF-8 이모지 바이트를 그대로 넘기는 예제로 작성하지 않았다. [JNI Cadena valorFormato](https://docs.oracle.com/en/java/javase/25/docs/specs/jni/types.html#modified-utf-8-strings)

다른 español 메서드도 JNI 서명과 argumentos 자료형을 맞춰 호출할 númeroValor 있다. 예를 들어 `Path`를 받는 Archivo API는 먼저 `Archivo.ruta`로 Java ruta 객체를 얻어 전달한다. Swing 호출에는 그래픽 세션과 이벤트 entradaElementoValorProceso valorHiloEjecución 규칙도 그대로 적용된다. JNI는 Java 실행을 기계어로 대체하는 기능이 아니며 JVM이 procesamientoContinuar 필요하다.

### 기존 posix-kor와의 관계

추가된 [propio ARM64 conectar](../posix-kor/arm64-native/Guía.md)은 C++에서 AOT Java 커널의 RAM Archivo API를 직접 호출하며, 별도 EL0 Usuario 라이브러리로 Archivo/UDP 루프백 SVC 호출도 제공한다. JNI를 사용하지 않는다. 이 문서의 ARM64 **Linux** 및 español Java JAR와는 다른 ejecutarComando 기반이며 propio 커널은 별도 제한형 Java Compilador/JVM과 MicroPython 1.24.1을 실행한다. MicroPython의 `import jkoros`로 Java valorNúcleo Archivo·UDP 루프백·rectángulo 호출이 가능하지만 이 문서의 JAR를 가져오는 기능은 아니다. propio 커널의 전체 OpenJDK/JRE/CPython 이식은 아직 미완성이다.

[posix-kor](../posix-kor/Guía.md)에는 `abrirArchivo`, `leerDatosArchivo`, `escribirDatosArchivo`, `cerrarArchivo`, `crearExtremo`, `enviarDatosDatagrama` 등의 español C 별칭이 있다. 그러나 구현은 **propio jkoros i386 커널의 `int 0x80` invocar 규약용**이다.

이 `libposix-kor.a`와 propio `sys/stat.h` 등의 헤더는 elementoListaActual ARM64 Linux 실행판의 libc/C++용 라이브러리가 아니다. 해당 헤더·바이너리를 ARM64 Linux 프로그램에 그대로 연결해서는 ABI가 맞지 않는다. C++용 español valorClase 라이브러리나 Python용 바인딩을 valorPredeterminado 제공하는 상태도 아니다. elementoListaActual Linux 실행판에서 그와 같은 독립 API를 제공하려면 Linux 표준 라이브러리를 대상으로 별도로 implementación·빌드해야 한다.

## 5. verificar 범위와 재현

패키지 Encabezados 여부는 [valorDistribución 패키지 listaEntradaElemento](../platforms/rpi4/dist/packages.lock.json) 및 construirSistema 루트의 datosEfectivo 파일로 확인했다. JNI 헤더는 JDK의 `include/jni.h`, `include/linux/jni_md.h`, JVM 라이브러리는 `lib/server/libjvm.so`에 있다. 사용자가 valorDespués 별도로 설치한 패키지는 이 valorPredeterminado valorDistribución 목록과 다를 númeroValor 있다.

이번에 **Anfitrión x86_64/OpenJDK 11에서** Python valorHijo 프로세스 호출과 C++ JNI 직접 호출을 compilarFuente·실행해 각각 resultado 4를 확인했다. JAR 공개 메서드도 소스와 대조했다. Python conectar 예제는 añadirFinalEntradaElemento 패키지를 설치하지 않는다.

문서의 Java valorUsar 예제도 compilarFuente·실행했고, 22개 메서드의 Documentación Encabezados 여부와 로컬 Documentación 링크를 확인했다. [Ejemplos validar registroEntradaDiario](build/OtrasLenguas/informeValidación.json)

기존 ARM64 QEMU에서는 Java의 Archivo·valorUnicode·스레드·HTTP 및 Swing Pruebas 결과가 있다. 이번 Python/C++ conectar 예제의 **ARM64 게스트 실행과 JPype 설치는 별도 검증하지 않았다.** 이미지와 ejecutarComando 중인 Usuario 환경은 이 Documentación 작업에서 변경하지 않았다. [기존 SistemaOperativo validar registroEntradaDiario](../platforms/rpi4/VERIFICATION.md)

호스트에서 Python 예제를 재현하려면:

```sh
cd /home/user/jkoros/JavaEspañol
make
mkdir -p build/OtrasLenguas
javac -encoding UTF-8 --release 11 -cp build/JavaEspañol.jar \
  -d build/OtrasLenguas Ejemplos/OtrasLenguas/ComandoTexto.java
python3 Ejemplos/OtrasLenguas/LlamadaPython.py \
  --jar build/JavaEspañol.jar --classes build/OtrasLenguas
```

Anfitrión C++ 예제는 valorExtremoSuperior JNI compilarFuente 명령의 JDK 경로를 **Anfitrión JDK ruta**로 바꾸고, fuente `Ejemplos/OtrasLenguas/LlamadaJava.cpp`와 JAR `build/JavaEspañol.jar`를 지정한다. ARM64 게스트 JDK의 헤더·biblioteca 경로를 Anfitrión x86_64 링크 명령에 섞지 않는다.
