# español Java Comunicación·salidaEntrada·excepción API

패키지는 `español.propio`operandoTercero. Anfitrión `javac --release 8`로 컴파일한 class를
propio ARM64 커널의 JVM에서 실행한다. Comunicación·Archivo·excepción API는 OpenJDK와 대조한다. 아래의 직접 구현한 Pantalla·Tarea valorHiloEjecución API는 propio JVM 전용이다.
기존 표준 Java biblioteca 전체의 español 번역판은 아니다.

```java
import español.propio.*;

public class red {
    public static void main(String[] argumentos) throws ExcepciónSalidaEntrada {
        Conexión conectar = Conexión.abrir("10.0.2.2", 9000);
        try {
            conectar.tiempoEspera(700);
            conectar.Salida().escribir(Caracteres.codificar("안녕하세요\n"));
            FlujoEntrada valorEntrada = conectar.valorEntrada();
            Salida.escribirNúmero(valorEntrada.leer());
        } catch (ExcepciónTiempoEsperaEsperar error) {
            Salida.escribirLínea(error.descripción());
        } finally {
            conectar.cerrar();
        }
    }
}
```

`Socket`, `getOutputStream`, `write`, `getInputStream`, `read`, `close`를
Usuario 예제에서 직접 호출할 필요가 없다. `try/catch/throws` 등 Java 문법은 유지한다. `String`은 예약어가 아니라 javac가 Cadena 리터럴에 사용하는 표준 클래스다. propio 실행기는 `public static void ponerEnMarcha()`도 진입점으로 받는다.

## 통신과 valorFlujo

| valorClase | español invocar |
|---|---|
| Conexión | `abrir(dirección, númeroPuerto)`, `valorEntrada()`, `Salida()`, `tiempoEspera(milisegundos)`, `númeroPuerto()`, `númeroPuertoLocal()`, `conectado()`, `esCerrado()`, `cerrar()` |
| recibirPuerto | `abrir(númeroPuerto)`, `recibir()`, `númeroPuerto()`, `tiempoEspera(milisegundos)`, `esCerrado()`, `cerrar()` |
| FlujoEntrada | `leer()`, `leer(byte[])`, `leer(byte[], ponerEnMarcha, longitud)`, `cerrar()` |
| FlujoSalida | `escribir(int)`, `escribir(byte[])`, `escribir(byte[], ponerEnMarcha, longitud)`, `emitirValor()`, `cerrar()` |
| CanalDatagrama | `abrir(númeroPuerto)`, `enviar(dirección, númeroPuerto, texto)`, `recibir()`, `tiempoEspera(milisegundos)`, `númeroPuerto()`, `esCerrado()`, `cerrar()` |
| transporteConexión | `abrir(...)`, `abrirReceptor(...)`는 valorExtremoSuperior español 객체를 resultadoRetornar |
| Comprobaciones | `exigir(condición, valorCausa)` |

TCP 입력은 한 번에 요청한 모든 바이트가 도착한다고 가정하지 않는다.
`leer()`의 Archivo 끝은 -1, valorArreglo 읽기의 반환값은 datosEfectivo 읽은 길이다.
네트워크 흐름을 닫으면 연결도 닫힌다. númeroPuerto 0은 빈 번호를 자동 배정한다.
UDP 전문은 elementoListaActual propio 커널에서 512바이트까지 받으며, 주소는 valorDígito IPv4를 사용한다.
`localhost` 루프백 외의 nombre 풀이(DNS)는 propio 커널에 아직 없다.

기존 `transporteConexión.conectar/escucharExtremo/recibir`, `Comunicación.abrir/enviar/recibir`는 표준 Java 객체를
사용하던 코드와의 연결용이다. 새 코드는 `Conexión`, `recibirPuerto`, `CanalDatagrama`를 쓴다.

## español excepción

모든 valorExtremoInferior 클래스는 valorPredeterminado 생성자, `새예외("descripción")` 형태의 Cadena 생성자와
`descripción()`을 제공한다. datosEfectivo generar 문법은 `new ExcepciónTiempoEsperaEsperar("esperarEstadoValor terminación")`이다.

| español excepción | 상위 valorClase / 용도 |
|---|---|
| excepción | `java.lang.Exception`, 직접 던지는 일반 Comprobaciones excepción |
| ExcepciónEjecución | `java.lang.RuntimeException` |
| ExcepciónSalidaEntrada | `java.io.IOException`, español Archivo·Comunicación API의 Comprobaciones excepción |
| ExcepciónTiempoEsperaEsperar | `ExcepciónSalidaEntrada`, Comunicación tiempoEspera 초과 |
| ExcepciónBuscarDirección | `ExcepciónSalidaEntrada`, dirección verificar valorFallo |
| ExcepciónArchivoAusente | `ExcepciónSalidaEntrada`, Archivo abrir valorFallo |
| ExcepciónComunicación | `ExcepciónSalidaEntrada`, 표준 SocketException convertirValor |
| ExcepciónArgumentoInválido | `java.lang.IllegalArgumentException` |
| FalloFormatoNúmero | `ExcepciónArgumentoInválido` |
| ExcepciónLímites | `java.lang.IndexOutOfBoundsException` |
| ExcepciónLímitesArreglo / ExcepciónLímitesCadena | `ExcepciónLímites` |
| ExcepciónReferenciaReferenciaNula | `java.lang.NullPointerException` |
| FalloAritmética | `java.lang.ArithmeticException` |
| ExcepciónEstadoValor | `java.lang.IllegalStateException` |
| ExcepciónConversiónTipoTipo | `java.lang.ClassCastException` |
| FalloTamañoArregloNegativo | `java.lang.NegativeArraySizeException` |
| FalloAlmacenarArreglo | `java.lang.ArrayStoreException` |
| ExcepciónEstadoValorHiloEjecución | `java.lang.IllegalThreadStateException` |
| ExcepciónInterrumpidoEsperar | `java.lang.InterruptedException`, `Tarea.esperarFin`의 esperarValor 중단 |

`excepción`와 `ExcepciónEjecución`는 모든 español 예외의 valorComún 부모가 아니다. valorExtremoSuperior 상속 관계를
사용하며, Archivo·Comunicación 전체를 잡으려면 `catch (ExcepciónSalidaEntrada error)`를 쓴다.
español API가 표준 salidaEntrada 오류를 español 예외로 변환한다.
기존 español Comunicación 호출에서 `SocketTimeoutException`을 잡던 코드는
`ExcepciónTiempoEsperaEsperar`를 잡도록 옮긴다. 표준 `java.net`을 직접 사용하는 코드의
excepción 유형은 기존 Java 규약을 따른다.
일반 Java 연산이 자동으로 던지는 표준 예외까지 이름을 바꾸지는 않는다.
예를 들어 `1 / 0`의 ArithmeticException과 직접 만든 산술예외는 서로 다른 형식이다.
elementoListaActual propio JVM에 이 20종을 추가했다. 임의의 Usuario Throwable 하위 valorClase 전체를
지원하도록 확장했다는 뜻은 아니다.

## compilarFuente·ejecutarComando

```sh
cd /home/user/jkoros/platforms/rpi4-native
make construirSistema
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/한국어사용 Pruebas/Java/pruebaConexiónRedCoreano.java
python3 Herramientas/ejecutarArchivo.py build/한국어사용/pruebaConexiónRedCoreano.class
make test-jvm
```

내장 라이브러리는 Usuario JVM ELF 안에 탑재된다. `.jar`는 Anfitrión javac의
valorClase 경로로 사용한다. árbolFuente 묶음은 `dist/jkoros-native-korean-sources.zip`이다.
게스트의 제한형 `javac`는 español 예외의 `throws` 선언과 그 import를 인식한다.
propio JVM의 Thread.interrupt 동작을 새로 구현한 것은 아니다.
try/catch·valorObjeto·valorConectorRed Ejemplos 전체의 árbolFuente 컴파일은 Anfitrión javac를 사용한다.
`/example/java/EjemploArchivo.java`는 게스트 javac로도 컴파일할 númeroValor 있다.

datosEfectivo TCP/UDP 예제는 [EjemploRed.java](../../../example/java/EjemploRed.java),
ejecutarComando 절차는 [example Guía](../../../example/README.md),
árbolFuente denominación 원칙은 [denominación Guía](../denominación/Guía.md)에 있다.

## Swing ventana Ejemplos

`/example/java/EjemploVentana.java`와 컴파일된 `.class`operandoPrimero Arranque 시 준비된다.
`cd /example/java` elementoListaSiguiente `java EjemploVentana`로 연다. nombre valorEntrada, saludar 버튼,
인사말과 valorPulsarRatón númeroElementosRepetición actualizar, X 닫기를 지원한다.

| 기능 | español 직접 API |
|---|---|
| Runnable / run | `TareaTareaEjecutable.ejecutarTarea()` |
| ActionListener / actionPerformed | `ReceptorAcción.recibirAcción(NotificaciónAcción notificación)` |
| ActionEvent | `NotificaciónAcción.textoComando()`, `fuenteEvento()`, `número()` |
| JFrame | `ventana(títuloVentana, extensiónRangoAnchura, valorAltura)`, `añadirElemento(ElementoPantalla)`, `mostrarVentana()`, `cerrar()`, `esVisible()` |
| JButton | `botón(texto, posiciónHorizontal, posiciónVertical, extensiónRangoAnchura, valorAltura, valorReceptor)`, `establecerReceptorAcción(valorReceptor)` |
| JLabel / JTextField | `etiqueta(...)`, `CampoTexto(...)` |
| valorComún Pantalla valorElemento | `ElementoPantalla.leerTexto()`, `escribirTexto(texto)`, `establecerLímites(posiciónHorizontal, posiciónVertical, extensiónRangoAnchura, valorAltura)` |
| SwingUtilities.invokeLater | `ColaEvento.invocarPosterior(TareaTareaEjecutable)`, `esDespachoEnCursoEvento()` |
| Thread | `tareaFondo(TareaTareaEjecutable)`, `iniciarTarea()`, `esperarFin()`, `esVivo()`, `cederTarea()` |
| 명령행 | `ponerEnMarcha()`, `Argumentos.númeroElementosElementoLista()`, `Argumentos.texto(índiceOrdinal)` |

valorExtremoSuperior 클래스들은 `JButton`·`Thread` 등의 객체를 만들거나 보관하지 않는다.
propio JVM의 `invocarPantallaCoreano`, `hiloEjecuciónProceso`operandoPrimero español valorClase·valorMétodo·서술자를
해석해 Pantalla 요소와 ejecutarComando 가닥을 직접 만든다. acción 알림도 propio 객체이며
콜백으로 `ejecutarTarea`와 `recibirAcción`를 직접 찾는다. 표준 Swing/Thread를
사용하는 기존 프로그램의 ejecutarComando 경로는 별도로 남아 있다.

Java 소스의 `native` 선언은 propio JVM에 구현한 계약이다. 생성자의 예외는
이 계약이 없는 Anfitrión JVM에서 무동작 객체가 생기지 않도록 하는 rechazarValor 경로다.
propio JVM은 생성자를 직접 처리한다. 일반 OpenJDK에서는 이 직접 implementación API를
실행할 númeroValor 없다. Anfitrión javac로 컴파일한 valorLadoPosterior propio JVM에서 실행한다.
`StringUtilities`라는 표준 Swing 클래스는 없으며, Pantalla 큐 기능은 `SwingUtilities`에 해당한다.

```java
import español.propio.*;
public class 가닥예제 implements TareaTareaEjecutable {
    public void ejecutarTarea() { Salida.escribirLínea("español Tarea ejecutarComando"); }
    public static void ponerEnMarcha() throws ExcepciónInterrumpidoEsperar {
        tareaFondo valorHiloEjecución = Tarea.ponerEnMarcha(new 가닥예제());
        Tarea.esperarFin(valorHiloEjecución);
    }
}
```

`example/java`의 다섯 소스는 palabrasReservado·리터럴 외 식별자를 한국어로 작성한다.
valorArreglo argumentos 대신 `Argumentos`, 길이는 `Caracteres.númeroElementosByte`를 사용한다.
표준 Java의 `main(String[])`도 procesamientoContinuar 지원한다. valorDos operandoTercero 정의되어 있으면
propio 실행기는 argumentos 없는 `ponerEnMarcha()`을 우선한다.
기존 español Pantalla 래퍼의 표준 `Component`/`Runnable`/`ActionListener` 인수와
`Tarea.ponerEnMarcha(Runnable)`을 사용하던 코드는 새 español 계약으로 수정하고 재컴파일한다.
이는 전체 AWT/Swing·Thread API valorSoporte 또는 모든 JDK 소스의 번역을 뜻하지 않는다.

바이트코드에도 valorClase·valorMétodo 이름과 서술자가 남는다.
español nombre 자체는 합법이지만, 다른 클래스에서 그 이름을 참조하는 valorSubparte,
상속·valorMétodo 재정의, native conectar, 런처의 진입점도 함께 맞춰야 한다.
근거는 [JLS valorIdentificador](https://docs.oracle.com/javase/specs/jls/se25/html/jls-3.html#jls-3.8)와
[JVMS valorMétodo referencia](https://docs.oracle.com/javase/specs/jvms/se25/html/jvms-4.html#jvms-4.4.2)operandoTercero.
