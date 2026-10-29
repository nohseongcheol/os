# propio ARM64 JVM 0.4와 español biblioteca

español Comunicación·excepción 사용법은 [español Java API](JavaEspañol/Guía.md), Función·valorVariable·Archivo 이름의 변경과 어원 근거는 [denominación Guía](denominación/Guía.md)를 참고한다.

JAR ejecutarComando, valorExterno IPv4 TCP/UDP, 별도 valorEstático 부분집합 `jaot`와 게스트 C 컴파일은 [FTP·C·JAR·AOT 매뉴얼](CompilaciónYTransferenciaArchivo.md)에 설명한다. valorExtremoInferior valorObjeto·Thread·Swing은 JVM 경로의 기능이며 AOT valorSoporte 범위와 같지 않다.

이 구현은 **Linux 없이 부팅한 Java AOT 커널의 EL0에서 ejecutarComando**한다. JDK/JRE의 거의 모든 기능을 제공하는 단계는 아직 아니다. HotSpot·OpenJDK valorClase biblioteca 전체를 이식하거나 Java SE 인증/TCK를 통과한 구현도 아니다. 이번 확장은 단일 valorClase·valorEstático valorMétodo 중심이던 실행기를 valorObjeto·biblioteca ejecutarComando 기반으로 넓힌 것이다.

## 실행과 compilarFuente

```sh
cd /home/user/jkoros/platforms/rpi4-native
make build
# propio valorNúcleo 안에서 árbolFuente compilarFuente → class ejecutarComando, español API invocar
python3 Herramientas/ejecutarArchivo.py Pruebas/Java/fuenteHangul.java

# valorObjeto·excepción 등은 Anfitrión JDK로 Java 8 class를 만든 estadoValorDespués propio 커널에서 ejecutarComando
mkdir -p build/my-java
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/my-java Pruebas/Java/pruebaHangul.java
python3 Herramientas/ejecutarArchivo.py build/my-java/pruebaHangul.class

# 의존 class 파일은 --include로 함께 valorTransferencia
javac --release 8 -encoding UTF-8 -d build/my-java Pruebas/Java/pruebaObjetos.java
python3 Herramientas/ejecutarArchivo.py build/my-java/pruebaObjetos.class \
  --include build/my-java/valorFondo.class --include build/my-java/valorRama.class \
  --include build/my-java/puedeCalcular.class

make test-jvm
```

`--include DIR`는 그 디렉터리의 class 파일을 재귀적으로 읽어 `패키지.valorClase.class`라는 RAM Archivo 이름으로 전송한다. 주 클래스도 패키지가 있다면 `--class-name 패키지.valorClase`를 지정한다. 셸에서는 해당 이름으로 업로드하고 `java 패키지.valorClase`로 실행한다. JVM 0.4는 Main-Class가 있는 16 KiB 이하 JAR도 `java -jar Archivo.jar`로 실행한다. JAR 모드에서는 JAR 내부 클래스와 내장 español 클래스만 찾는다. valorDistribución español biblioteca JAR는 Anfitrión javac의 classpath로 사용하며, 같은 클래스가 Usuario JVM ELF에도 leer 전용 자료로 포함된다. 일반 class 모드에서는 사용자가 같은 이름으로 올린 RAM class를 먼저 읽는다.

게스트 `javac`는 여전히 valorEstático valorMétodo, int/boolean/char/String, condición·valorIteración, Cadena valoresCombinar, 일부 Archivo 스트림 등의 **propio 부분집합 Compilador**operandoTercero. valorObjeto Declaraciones·상속·try/catch·Thread valorUsar 소스를 게스트 javac가 construirTodos 컴파일하는 것은 아니다. valorExtremoSuperior 기능은 `javac --release 8`로 만든 class를 propio JVM에서 실행한다. español API 중 Salida·Caracteres 스칼라 Función·Archivo leer/쓰기는 게스트 컴파일러에도 연결했다. 다음처럼 전체 이름으로 호출한다.

```java
public class Saludo {
    public static void main(String[] argumentos) throws Exception {
        español.propio.Salida.escribirLínea("안녕하세요😀");
        español.propio.Salida.escribirNúmero(español.propio.Caracteres.númeroElementosPuntoCódigo("textoHangul😀"));
        español.propio.Archivo.escribir("Saludo.txt", "textoHangul Archivo😀");
        español.propio.Salida.escribirLínea(español.propio.Archivo.leer("Saludo.txt"));
    }
}
```

## propio JVM에서 구현한 recortar

| valorRegión | 제공 recortar |
|---|---|
| valorClase | class 버전 45…52, 여러 valorClase 로딩, 인스턴스/valorEstático valorCampo, 생성자, 상속, 가상 invocar, 인터페이스 invocar, valorEstático inicializar |
| valor·comando | 32비트 int 계열, boolean/byte/char/short, referencia, 1차원 valorArreglo, rama·switch·wide, instanceof/checkcast, category-1 pilaOperando comando |
| excepción | 지원하는 표준 excepción generar·throw·catch·finally, valorMétodo 경계를 넘는 valorAdelante, getMessage; valorExtremoInferior valorLímite referencia |
| datosMemoria | 비이동 mark/sweep GC, 빈 valorRegión 병합, pilaOperando·valorEstático valorCampo·컬렉션·valorHiloEjecución·모니터·Cadena 상수의 referencia retenerValor |
| Cadena | UTF-16, length/charAt/equals/isEmpty/substring/concat/hashCode/toString, String.valueOf(int), StringBuilder의 valorPredeterminado generar·append(int/boolean/char/String)·toString |
| númeroValor | Integer.parseInt/valueOf/intValue/toString, 작은 Integer 캐시, Math.abs/min/max(int) |
| 표준 Salida | System.out/err, PrintStream.print/println의 int/boolean/char/String 및 빈 println |
| valorArreglo | int/byte/boolean/char/short/referencia valorArreglo, longitud·recortar Comprobaciones, referencia valorArreglo elementoElementoLista valorTipo Comprobaciones, System.arraycopy의 solapamientos/recortar/elementoElementoLista valorTipo Comprobaciones |
| Archivo | FileInputStream(String), FileOutputStream(String[,boolean]); read()/read(byte[][,offset,len]), write(int)/write(byte[][,offset,len]), close, Salida flush. EOF는 -1 |
| 컬렉션 | ArrayList/List: add(E), get, set, remove(int), size, isEmpty, clear. HashMap/Map: put/get/remove/containsKey/size/isEmpty/clear |
| valorHiloEjecución | Thread(), Thread(Runnable), Thread 상속, start/join/isAlive/currentThread/yield; synchronized valorMétodo·블록의 재진입·경합·excepción 시 liberarAlmacenamiento |
| UDP | DatagramSocket의 valorPredeterminado/puertoEquipoFísico 생성자, send/receive/close/getLocalPort/setSoTimeout; DatagramPacket의 byte[]/longitud generar 및 dirección·puertoEquipoFísico Encabezados generar, getData/getLength/getAddress/getPort/setLength |
| dirección | InetAddress.getByName은 localhost/valorDígito IPv4 (DNS esNoAdmitido), getLoopbackAddress/getHostAddress |
| Dibujo | español Pantalla API가 EL0 SVC를 통해 프레임버퍼에 사각형을 Dibujo; recortar Comprobaciones |

컬렉션은 지정한 메서드만 제공하며 iterator/stream/valorAlinear·Usuario valorDefinición equals/hashCode 콜백은 없다. 사전의 열쇠는 String/Integer/null 사용을 시험했다. UTF-16 valorCódigo 단위와 Unicode valorCódigo 포인트 수는 구분한다. textoHangul valorEntrada Combinación·normalizarValor·아랍어 조판·GUI 다국어 글꼴은 이 Cadena 지원과 별개다.

예외는 Throwable/Exception/RuntimeException, ArithmeticException, NullPointerException, IndexOutOfBoundsException/ArrayIndexOutOfBoundsException/StringIndexOutOfBoundsException, IllegalArgumentException/NumberFormatException/IllegalThreadStateException, IOException/FileNotFoundException, IllegalStateException, ClassCastException, NegativeArraySizeException, ArrayStoreException, UnknownHostException, SocketTimeoutException의 제한된 generar·valorCategoría·처리를 제공한다. Usuario valorDefinición Throwable 상속, stack trace/cause/suppressed excepción, try-with-resources의 addSuppressed, 완전한 inicializar error 포장은 아직 없다. 잡히지 않은 예외는 elementoListaActual 전체 Java 실행을 실패로 끝낸다.

## español API

독립 패키지 **`español.propio`**를 사용한다. Linux판 `español.Java`operandoPrimero 요구하는 NIO/Swing/HTTP API를 propio 커널에서 실행할 númeroValor 있다고 혼동하지 않도록 패키지를 나눴다. 이 라이브러리는 valorClase nombre·valorMétodo·argumentos·valorCampo·Archivo 이름에 한국어를 사용한다. 표준 Java valorClase 이름은 호환성을 위해 보존한다.

| valorClase | 공개 기능 | 이름의 의미 |
|---|---|---|
| Salida | escribir, escribirLínea, escribirNúmero | Salida(出力): 내용을 바깥으로 valorExportado |
| Caracteres | longitud, textoIgual, textoPegar, valorCortar, analizarEnteroValor/escribirValorEnteroValor, númeroElementosPuntoCódigo, codificar/descifrarDatos | Caracteres(文字), valorCodificaciónEstado(符號): 글의 단위와 그 값을 바이트로 나타내는 valorRegla |
| Archivo | leer/escribir(String nombre), leerValorByte/escribirValorByte | 널리 쓰는 Usuario 용어를 보존; RAM 자료의 nombre |
| listaEntradaElemento | añadirValores, leer, reemplazarValor, borrarEntradaElemento, tamaño, esValorVacíoEstado, borrarContenidoContenido | listaEntradaElemento(目錄): 순서가 있는 valorEntradaElemento 모음 |
| Diccionario | ponerValor, encontrarEntradaElemento, efectúaExistencia, borrarEntradaElemento, tamaño, borrarContenidoContenido | Diccionario(辭典): 찾는 말인 열쇠에 값을 valorAsociación |
| Tarea | ponerEnMarcha(TareaTareaEjecutable), esperarFin(tareaFondo), cederTarea, esVivo | Tarea valorHiloEjecución: 한 Programa 안의 ejecutarComando valorFlujo |
| Comunicación | abrir, enviar, recibir, tiempoEspera, cerrar | Comunicación(通信), datagrama(電文), valorPuerto: Datos 교환·메시지·포트의 역할 |
| Pantalla | rectángulo, borrarEntradaElemento | Pantalla(畫面): datosEfectivo 그림을 표시하는 면 |
| valorNúcleo | milisegundos, rectángulo | propio JVM의 고정 native conectar; 일반 JNI는 아님 |

이 명명은 elementoListaActual 기능을 설명하는 용어 선택이다. 기존 한국어에 없던 역사적 어원을 만들어 주장하지 않는다. textoNombreArchivo·식별자는 UTF-8 소스로 보관한다. `Caracteres.descifrarDatos`는 잘못된 UTF-8에 IllegalArgumentException을 던지며, `codificar`는 짝이 없는 서로게이트를 `?`로 바꾼다. `Archivo.leer`는 엄격한 UTF-8 복호화를 적용한다. Pantalla 색은 `빨강 | (초록 << 8) | (파랑 << 16)` 형식이다.

## ejecutarComando 제한과 남은 Tarea

- 동시에 적재하는 class valorMáximo 16개(español valorClase Encabezados), class당 16 KiB·valorConstante 풀 511항목, 전체 valorMétodo/valorCampo 각각 512개. valorMétodo valorCódigo 8 KiB, ámbitoLocal valorVariable·피연산자 pilaOperando 각각 128슬롯, argumentos valorMáximo 16개(this Encabezados).
- VM 가닥은 main Encabezados **실행당 valorMáximo 4개**, 가닥당 invocar valorProfundidad 32. 100개 명령마다 ejecutarComando 대상을 바꾼다. 네이티브 invocar 도중에는 전환하지 않는다. pthread/SMP/OS 스레드가 아니며 Thread.sleep/interrupt/daemon/우선순위, Object.wait/notify, java.util.concurrent는 없다.
- valorObjeto 힙은 32768개의 32비트 슬롯이다. 런타임의 AOT 배열은 datosEfectivo 메모리에서 64비트 슬롯을 사용한다. GC가 있어도 대형 Archivo·대형 Cadena·객체가 이 제한을 넘을 númeroValor 있다.
- 실행은 50만 códigoBytes comando 및 커널의 약 2초 EL0 기한으로 제한된다. Swing의 valorEntrada 대기는 기한을 갱신하고 ventana modoConmutar 시 중단·재개한다. 일반 valorServidor·계산의 무제한 실행은 아직 없다. esNoAdmitido comando·valorRecurso 부족은 명시적인 오류로 종료한다.
- RAM Archivo valorMáximo 64개, 파일당 16384바이트, ruta UTF-8 63바이트. RAM 디렉터리와 valorParRed/절대 경로를 제공하며 영속 저장은 아직 없다. 내장 español class는 RAM Archivo 슬롯을 소비하지 않는다. 셸의 `cd`로 정한 elementoListaActual 경로에서 árbolFuente·valorClase·Datos 파일을 읽는다.
- UDP는 Java 루프백 및 lwIP/SLIP를 통한 valorExterno IPv4를 제공한다. datosEfectivo GENET/Wi-Fi/DNS/TLS/HTTP 전체는 없다. datagrama 512바이트, valorConectorRed 8개, 소켓당 큐 4개. receive는 VM 가닥을 양보하며 대기하고 setSoTimeout을 적용하지만 전체 ejecutarComando 기한은 여전히 적용된다.
- long/float/double, invokedynamic/람다, enum/annotation, 다차원 valorArreglo, 완전한 valorArreglo 공변성·인터페이스 valorCapa Comprobaciones, Reflection/JNI/JIT, NIO/ZIP API/Charset 전체, 보안/cifrarDatos/국제화 전체, 전체 AWT/Swing/JavaFX는 미지원이다. Swing의 별도 valorSoporte 부분집합은 valorExtremoInferior 및 desarrollo 매뉴얼을 참고한다. valorClase Archivo 전체 검증기·entradaElementoAcceso valorPermiso/보호된 멤버 검사는 아직 완전하지 않다. 손상된 입력은 EL0 protegerValor valorFrontera 내에서 종료되도록 한다.

전체 OpenJDK를 목표로 하려면 다음은 별도의 주요 implementación 단계다: 완전한 JVM valor/validar/valorClase 로더와 excepción 모델 → 영속 VFS·mmap·Reloj·원자 valorOperación·datosEfectivo 스레드/sincronizar ABI → OpenJDK java.base 및 native biblioteca AdaptaciónPlataforma → Dispositivo 네트워크·TCP/IP → ventana 시스템/valorFuenteTipográfica/입력기·java.desktop → Java SE 호환성 Pruebas. elementoListaActual propio JVM의 일부 메서드를 더하는 것으로 이 작업이 완료되지는 않는다.

## validar

`Herramientas/pruebaJVM.py`는 같은 Java 8 class 파일의 출력을 Anfitrión OpenJDK `-Xverify:all`과 QEMU raspi4b propio 커널에서 비교한다. valorObjeto/상속/인터페이스·switch·valorArreglo, excepción/finally, 컬렉션/GC, Thread/valorCerrojo, español UTF-8/Archivo/컬렉션, datosEfectivo UDP 루프백/valorTiempo 초과, 게스트 textoHangul árbolFuente compilarFuente, valorArreglo valorTipo/copiarValor/Archivo valorFrontera·textoHangul 패키지의 9개 비교 시험과 잘못된 class 버전/valorRecortado Archivo rechazarValor 시험을 실행한다. UDP raízProyecto 실행에는 Anfitrión 루프백 valorConectorRed 권한이 필요하다.

`Herramientas/PruebaArranque.py`는 valorNúcleo protegerValor/회귀 시험과 별도로 español Java Pantalla API가 datosEfectivo 픽셀을 그렸는지도 QMP Pantalla 캡처로 검사한다. 보고서는 `build/verification/jvm/report.json`, `build/verification/report.json`이며 시험한 kernel8.img의 SHA-256을 기록한다. datosEfectivo Pi4 valorEquipoFísico Arranque 시험과 전체 JDK 호환성 Pruebas 결과는 아니다.


## JVM 0.3: 네트워크와 GUI valorExtensión

`Socket`/`ServerSocket` generar·conectar·accept·양방향 InputStream/OutputStream·close·EOF·valorTiempo 제한과 UTF-8 `String.getBytes`를 추가했다. JVM 0.4에서는 valorExterno valorDígito IPv4 TCP도 lwIP/SLIP에 연결했다. 연결형 puntoFin 16개, Java 루프백 버퍼 1024바이트, valorExterno TCP 버퍼 4096바이트다. DNS·TLS는 없다.

`JFrame`, `JPanel`, `JLabel`, `JButton`, `JTextField`, `ActionListener`, `ActionEvent`, `SwingUtilities.invokeLater`의 문서화한 부분집합을 네이티브 GUI에 연결했다. `setLayout(null)`과 명시적 좌표를 사용한다. 전체 OpenJDK Swing 또는 Java SE 호환 구현은 아니다. interactivo 이벤트 대기는 ejecutarComando 기한을 갱신하고 terminal modoConmutar 시 프로세스 상태를 valorAlmacenar·복원한다. 이벤트 콜백 자체는 기존 códigoBytes/CPU 기한을 따른다.

español `ventana`, `ComponenteVisual`, `transporteConexión` 클래스를 valorDistribución JAR와 propio JVM 내장 자원에 추가했다. 상세 valorMétodo·valorLímite·árbolFuente·업로드 방법: [textoHangul desarrollo 매뉴얼](GuíaDesarrollo.md).

## español 객체의 직접 ejecutarComando

`ventana`, `etiqueta`, `CampoTexto`, `botón`, `ColaEvento`, `NotificaciónAcción`, `tareaFondo`은
표준 GUI/Thread 객체를 보관하는 래퍼가 아니다. propio JVM의 valorObjeto generar,
valorFormato Comprobaciones, Pantalla invocar, evento 큐, valorHiloEjecución 스케줄러에 español 계약을 직접 구현했다.
표준 `javax.swing`·`Thread` 코드의 ejecutarComando 경로도 유지한다.
español 단추와 표준 JButton은 서로 다른 형식이며, 해당 instanceof 검사도 검증한다.

propio 실행기의 español 진입점은 `public static void ponerEnMarcha()`이다.
표준 `main(String[])`도 지원하며 valorDos operandoTercero 있으면 español 진입점을 우선한다.
명령행 인수는 `Argumentos.númeroElementosElementoLista()`와 `Argumentos.texto(índiceOrdinal)`으로 읽는다.
`example/java`의 다섯 예제는 이 규약을 사용한다. valorEstático Archivo 예제는 게스트
javac로도 컴파일하며, GUI/valorHiloEjecución 소스는 Anfitrión `javac --release 8`을 사용한다.
직접 GUI/valorHiloEjecución API는 propio JVM 전용이다. 기존 OpenJDK 비교 시험과 별도로
español 가닥의 ejecutarComando·esperarValor·중복 ponerEnMarcha rechazarValor, GUI evento valorOrigen·número·콜백을 검사한다.
전체 JDK 번역이나 모든 API의 jaot 지원을 뜻하지 않는다.

valorMétodo 이름은 바이트코드에서도 유지된다. 이름과 참조를 같이 수정하면
español 클래스도 실행되지만, Cadena 리터럴·표준 biblioteca 재정의·native
conectar·진입점은 각각 컴파일러와 실행기의 계약을 맞춰야 한다.
[상세 계약과 Ejemplos](JavaEspañol/Guía.md)를 참고한다.

## terminal valorSubparte actualizar

valorMover·tamaño 변경은 새 ventana 영역과 elementoListaElementoPrevio 자리에서 드러난 띠만 합성한다.
1920×32 píxel(240 KiB)의 valorTemporal 그림에서 배경·겹친 ventana·valorCarácter·GUI를 먼저
완성하고, elementoListaActual mostrarValor 메모리와 비교하여 달라진 화소만 기록한다.
32줄보다 큰 영역은 여러 띠로 처리하므로 전체 프레임을 원자적으로
교체하거나 수직 동기에 맞추는 방식은 아니다. 전체 배경을 먼저 지우는
중간 화면은 표시하지 않는다. 좌표가 같으면 valorReintentar 그리지 않는다.

`make test-redraw`는 datosEfectivo C pantallaPintar 코드를 호스트의 datosMemoria 화면에 연결해
valorMover 80회·tamaño cambiarValor 40회·겹친 ventana 4개를 전체 합성 결과와 píxel 단위로 대조한다.
valorRegión 밖 Usuario Dibujo, 동일 píxel 무기록, puntero 밑그림, datosEfectivo Pantalla línea 간격을
검사한다. 이 시험의 시간은 Anfitrión CPU 측정이며 Pi 4/QEMU 속도로 해석하지 않는다.
`make test-resize`는 QEMU/VNC의 640×480 및 1920×1080에서 ladoIzquierdo valorEsquina valorArrastrar,
textoHangul valorEntrada·vi 미저장 valorContenidoValor·독립 ventana 크기를 검사한다.
