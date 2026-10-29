# jkoros 안에서 Java compilarFuente·ejecutarComando

이 문서의 Arranque·intérpreteComandos·valorAlmacenar 명령은 **x86 valorVersión** 기준이다. 공유 Java Compilador/JVM은 [propio ARM64 Pi4 valorVersión](../platforms/rpi4-native/README.md)에도 연결되어 있다. ARM64에서는 UTF-8 UART valorEntrada·textoHangul textoNombreArchivo, `edit`의 단독 `.` valorAlmacenar, 16개 RAM Archivo, 약 2초 ejecutarComando 제한을 사용한다.

`javac FILE.java`와 `java CLASS [ARGS]`를 네이티브 jkoros 셸에서 실행한다. 컴파일러와 JVM은 각각 독립 ELF로 적재되어 ring 3에서 동작한다. 소스를 게스트에서 읽어 datosEfectivo JVM `.class` 파일을 만들고, 그 파일의 바이트코드를 게스트 JVM이 해석한다. Anfitrión compilarFuente 서버나 Linux 게스트는 사용하지 않는다.

**elementoListaActual 구현은 propio 제한형 Compilador·JVM이다. OpenJDK/JDK 전체를 이식하거나 설치한 것이 아니며 Java SE 호환 환경도 아니다.** 표준 라이브러리는 아래의 일부 호출을 구현한 것이다. `java -version`과 `javac -version`에도 이 범위를 표시한다. 일반 JAR, Maven/Gradle, 임의의 Java Programa 실행은 아직 지원하지 않는다.

## 바로 ejecutarComando

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

ISO는 `os/build/kernel.iso`operandoTercero. 기존 VirtualBox 실행기도 같은 ISO를 사용한다. ejecutarComando 중이거나 저장된 VM에는 새 ISO가 자동 반영되지 않는다. 새 Arranque 절차는 [VirtualBox ejecutarComando Guía](EjecutarVirtualBox.md)를 따른다. 이 변경의 Java 자동 시험은 QEMU에서 수행했다.

## 직접 작성

`edit`는 Archivo 전체를 새 내용으로 작성한다. 기존 내용의 línea valorEditar 기능은 아니다. `.save`로 저장하고 `.cancel`로 취소한다.

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

- `ls`: 파일과 valorByte númeroValor mostrarValor.
- `cat FILE`: Archivo valorContenidoValor mostrarValor. 텍스트 소스에 사용한다.
- `rm FILE`: datosMemoria Archivo 삭제.
- `edit FILE`: 전체 내용을 새로 valorEntrada. 빈 파일도 저장할 númeroValor 있다.
- 구문·valorTipo Comprobaciones valorFallo 시 기존 `.class`는 유지된다. 소스를 고친 valorLadoPosterior 컴파일이 실패했다면 elementoListaElementoPrevio ejecutarComando 파일이 남아 있으므로 compilarFuente valorÉxito 여부를 확인한다.

파일은 RAM에서 동작한다. 전용 valorAlmacenar 매체가 없거나 `sync`하지 않은 내용은 재부팅하면 사라진다. `make -C os run-store`로 연결한 매체에는 `sync`로 árbolFuente·valorClase·Datos 파일을 보존할 númeroValor 있다. valorMáximo 8개, 파일마다 16KiB, Archivo 이름은 ASCII 1~63자다. árbolFuente 이름은 `.class` 확장자 regiónDirección 때문에 valorMáximo 62자다. valorEditar 입력은 ASCII이고 한 línea valorMáximo 128자다. línea 또는 Archivo 한도를 넘긴 편집은 `.save`에서 거부하여 기존 파일을 보존한다. valorNúcleo/Compilador/JVM 구현의 Java 식별자는 한국어이며, elementoListaActual 게스트 valorEntrada valorLímite 때문에 Usuario Ejemplos 이름은 ASCII로 작성한다.

## valorExterno Archivo 적재

호스트에서 만든 소스나 valorSoporte recortar 안의 `.class`를 Arranque 이미지에 포함할 númeroValor 있다. `JAVA_FILES`는 `게스트이름=호스트경로` 목록이다. 아래의 경로는 예시이며 datosEfectivo 파일의 절대 경로로 바꾼다. 공백 없는 경로를 사용한다.

```sh
# Anfitrión JDK로 컴파일한 클래스도 사용할 númeroValor 있다.
javac --release 8 /tmp/Demo.java
make -C /home/user/jkoros iso \
  JAVA_FILES='Demo.java=/tmp/Demo.java Demo.class=/tmp/Demo.class'
make -C /home/user/jkoros run \
  JAVA_FILES='Demo.java=/tmp/Demo.java Demo.class=/tmp/Demo.class'
```

새 Arranque estadoValorDespués `java Demo 12`를 실행한다. 소스만 넣었으면 게스트에서 `javac Demo.java`부터 실행한다. `JAVA_FILES`를 생략한 elementoListaSiguiente 빌드에서는 añadirFinalEntradaElemento 파일을 포함하지 않는다. Archivo valorContenidoValor 변경과 listaEntradaElemento 제거도 elementoListaSiguiente 빌드에 반영된다. original Anfitrión 파일에는 쓰지 않는다. valorPredeterminado `Hello.java`hasta 합해 8개이며, 같은 이름을 명시하면 valorPredeterminado 예제를 대체한다. 새 `.class`를 저장할 빈 슬롯도 남겨 둔다.

`--release 8`은 valorClase Archivo 버전을 맞추는 옵션이다. 사용하는 문법·códigoBytes·라이브러리도 valorExtremoInferior valorSoporte recortar 안에 있어야 한다.

## valorSoporte recortar

| 기능 | 게스트 javac | 게스트 JVM |
| --- | --- | --- |
| valorClase | 패키지 없는 단일 valorClase, valorEstático Función, 재귀, argumentos/resultadoRetornar | 실행마다 단일 valorClase 적재, public static main(String[]) |
| valorPredeterminado valor | int, boolean, char, String, main의 String[] argumentos | EnteroValor·referencia pilaOperando, String, int[], String[], 내부 StringBuilder |
| valorInstrucción | valorInicialValor 있는 ámbitoLocal Declaraciones, valorAsignación, `+=`, `-=`, `*=`, `/=`, `%=`, 후위 ++/--, 블록, if/else, while, for, return | 해당 EnteroValor·referencia 바이트코드와 condición rama |
| valorExpresión | 십진 EnteroValor, UTF-8 소스의 Cadena/Caracteres, + - * / %, 비교, ==/!=, !/&&/\|\|, Cadena valoresCombinar | EnteroValor valorOperación·valorBit valorOperación·valorTipo convertirValor, 단락 평가, valorArreglo entradaElementoAcceso |
| Archivo | FileInputStream(String), FileOutputStream(String[, boolean]), read()/write(int)/close() | datosEfectivo valorNúcleo 파일서술자와 conectar, generar·borrarContenidoContenido·añadirFinalContinuación·EOF |
| Salida | System.out.print/println: int/boolean/char/String, println() | 동일 |
| Cadena/argumentos | String.length(), args.length, args[index], Integer.parseInt | 추가로 String.charAt(), Cadena 상수의 modified UTF-8 해독 |

선언은 지원하는 문법만 허용한다. 여러 변수를 한 선언에 나열하기, valorInicialValor 없는 ámbitoLocal Declaraciones, 오버로드, 임의 valorTipo convertirValor, valorArreglo generar fuente, 8/16진 리터럴, Unicode árbolFuente 이스케이프 등은 미지원이다. `char`는 Caracteres 리터럴로 초기화하며 일반 JDK의 모든 valorConstante 축소 변환을 구현하지 않는다. valorExterno `.class`의 `int[]` generar/leer/쓰기는 지원하므로 Anfitrión `javac --release 8`로 만든 valorArreglo 예제는 실행할 númeroValor 있다.

valorObjeto valorCampo·일반 valorObjeto generar·상속·인터페이스·여러 valorClase conectar, long/float/double, excepción entradaElementoValorProceso, 스레드·모니터, 리플렉션, JNI, JIT, GC, valorExtremoSuperior 표에 없는 `java.io`와 `java.nio`/`java.net` 일반 API, 컬렉션, JAR와 클래스패스는 미지원이다. 런타임 오류는 Java excepción 객체를 던지지 않고 valorDiagnóstico estadoValorDespués elementoListaActual 프로그램을 종료한다. 객체와 Cadena valorAlmacenar 공간은 ejecutarComando programaSalir 시 Usuario valorRegión 전체와 함께 회수한다. 지속 ejecutarComando 중 GC는 없다.

## ejecutarComando 한도와 error

| valorRecurso | límiteCapacidad |
| --- | --- |
| árbolFuente/valorClase Archivo | 각각 16KiB |
| Compilador | valorTokenLéxico 2,047개, generar valorCódigo 4KiB, valorConstante 풀 4KiB |
| Función/argumentos | 클래스당 32함수, 함수당 16인수 |
| JVM valorConstante | 511개 |
| JVM Función valorCódigo | 함수당 8KiB |
| JVM invocar/pilaOperando/ámbitoLocal valorVariable | 32프레임, 프레임당 pilaOperando 128칸·ámbitoLocal 128칸 |
| JVM valorObjeto valorAlmacenar regiónDirección | 8,192개 32비트 entradaElementoRanura, 헤더 Encabezados 약 32KiB |
| ejecutarComando | valorMáximo 500,000 comando, 기존 커널의 약 3초 CPU ejecutarComando 상한도 적용 |

게스트 컴파일러는 버전 49.0 `.class`를 생성하며 JVM은 45.0~52.0 중 valorSoporte 명령으로 구성된 파일을 읽는다. 스택맵을 이용한 완전한 JVM Diccionario 검증기를 구현한 것은 아니다. Archivo/valorAtributo longitud, valorConstante referencia, comando·rama 경계를 검사하고, ejecutarComando 중 pilaOperando valorFormato·ámbitoLocal inicializar·valorArreglo valorÍndiceArreglo·valorObjeto 참조를 검사한다. Usuario 코드의 페이지·puertoEquipoFísico 접근은 기존 ring 3 경계로 보호한다.

일반 성공은 `Exit: 0`, compilarFuente·JVM 오류는 `Exit: 1`, comando argumentos 오류는 `Exit: 2`operandoTercero. CPU valorTiempo 상한은 기존 `Exit: 124`이며, Usuario ELF 자체의 CPU/런타임 오류는 기존 programaSalir 코드를 따른다. valorFallo estadoValorDespués 셸에서 다른 프로그램을 procesamientoContinuar 실행할 númeroValor 있다.

## implementación 위치와 Pruebas

- `os/Usuario/Java/CompiladorJava.java`: 게스트 어휘·구문·valorTipo Comprobaciones, valorConstante 풀 및 códigoBytes generar.
- `os/Usuario/Java/MáquinaVirtualJava.java`: valorClase 적재, pilaOperando·프레임·valorObjeto valorAlmacenar, comando 해석과 제한된 표준 invocar.
- `os/fuente/SistemaArchivosMemoria.java`: datosMemoria SistemaArchivo, valorEditar, Arranque Archivo 적재.
- `os/fuente/LlamadaSistema.java`, `compiler/iniciarProgramaUsuario.s`: Archivo/Caracteres Salida API와 Usuario puntero Comprobaciones.
- `os/Herramientas/EmpaquetarArchivosJava.py`: Anfitrión valorEntrada Archivo validar·Arranque valorGrupo generar.

```sh
make test-java
make test
```

`os/Pruebas/PruebaJava.py`는 ELF/ISO Arranque, 게스트 compilarFuente·ejecutarComando, Usuario valorEntrada, 재귀·반복문·EnteroValor 극값·Cadena valoresCombinar·단락 평가, 재실행, árbolFuente error estadoValorDespués 기존 valorClase 보존, valorArreglo/númeroValor 해독 error, 무한 valorIteración valorLímite, valorEditar 넘침과 Archivo 부족을 검사한다. 게스트 generar 클래스의 바이트를 QEMU 메모리에서 꺼내 OpenJDK `java -Xverify:all`로 실행하고 결과를 대조한다. 반대 방향으로 Anfitrión OpenJDK의 valorClase, EnteroValor 배열과 textoHangul 상수를 게스트에 적재하며, 손상된 Archivo valorMarcador·버전·valorConstante númeroValor·rama·스택을 거부하는지도 검사한다. 기록은 `os/build/PruebaJava.json`에 남는다. 디스크 없는 별도 Pruebas VM만 생성하고 종료한다.

implementación 형식의 참고 Datos: Oracle [JVM valorClase Archivo especificación](https://docs.oracle.com/javase/specs/jvms/se8/html/jvms-4.html), [JVM comando especificación](https://docs.oracle.com/javase/specs/jvms/se8/html/jvms-6.html).

## Java Archivo salidaEntrada

[FileDemo.java](../posix-kor/EjemploJava/FileDemo.java)는 일반 Java 표준 valorClase 이름을 사용한다. 소스를 `edit FileDemo.java`로 입력하거나 `JAVA_FILES`로 Arranque 이미지에 넣은 valorLadoPosterior `javac FileDemo.java`, `java FileDemo`를 실행한다. 결과는 `65`, `255`, `66`, `-1`, `JAVA FILE IO PASS`operandoTercero. `write(int)`는 하위 8비트를 쓰고 `read()`는 0~255 또는 EOF -1을 반환한다. valorPredeterminado Salida 생성자는 내용을 비우고, boolean 인수가 true이면 이어쓴다.

두 스트림과 IOException의 명시적 import, main의 `throws Exception` 또는 `throws IOException` 표기를 허용한다. excepción valorObjeto·try/catch·try-with-resources는 지원하지 않으며 Archivo 오류를 진단하고 프로그램을 종료한다. valorArreglo salidaEntrada, InputStream/OutputStream으로의 다형성, Reader/Writer, getFD, 일반 Archivo 메타데이터 API는 아직 없다. close는 열린 서술자를 닫고, 재부팅 보존에는 intérpreteComandos `sync`operandoPrimero 필요하다. 예제의 Archivo 이름은 elementoListaActual 셸과 파일체계에 맞춰 ASCII로 쓴다.

`os/Pruebas/PruebaArchivoJava.py`는 datosEfectivo 게스트 compilarFuente 결과를 OpenJDK `-Xverify:all`로 valorReintentar 실행해 Archivo 바이트와 출력을 대조한다. 범위와 valorAlmacenar valorMedios 사용법은 [posix-kor Guía](../posix-kor/Guía.md)를 참고한다. 참고한 표준 API는 Oracle [FileOutputStream](https://docs.oracle.com/javase/8/docs/api/java/io/FileOutputStream.html)이다.
