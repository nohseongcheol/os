# propio 커널에서 vi·여러 terminal·textoHangul 프로그래밍 사용하기

español Comunicación·excepción 사용법은 [español Java API](JavaEspañol/Guía.md), Función·valorVariable·Archivo 이름의 변경과 어원 근거는 [denominación Guía](denominación/Guía.md)를 참고한다.

대상은 `platforms/rpi4-native`의 propio AArch64 Java 커널이다. vi와 Java/Python/C/C++ 프로그램은 EL0에서 실행한다. Linux 실행판과 별도이며 valorExtremoInferior valorSoporte 목록은 전체 OpenJDK·Vim·POSIX 구현을 뜻하지 않는다.

게스트 `cc`/`jaot`, JAR 직접 ejecutarComando, valorExterno TCP/UDP와 FTP는 [새 ejecutarComando 매뉴얼](CompilaciónYTransferenciaArchivo.md)을 참고한다.

## GUI와 여러 terminal

```sh
cd /home/user/jkoros/platforms/rpi4-native
make desktop
```

Remmina에서 **VNC**, dirección **127.0.0.1:5902**로 연결한다. Pantalla valorExtremoSuperior **+ New terminal**, **Ctrl+Shift+T**로 터미널을 추가한다. valorMáximo 네 개다. ladoSuperior terminal 버튼 또는 창을 클릭해 선택하고 **F6**으로 순환한다. 제목줄을 끌어서 옮기고 **derecho valorExtremoSuperior X**를 클릭하면 닫힌다. elementoListaÚltimo 창을 닫아도 ladoSuperior ejecutarComando 버튼으로 valorReintentar valorColumna númeroValor 있다. 기존 `terminal`, `exit`, F12도 사용할 númeroValor 있다.

창마다 elementoListaActual 디렉터리, intérpreteComandos valorVariable, comando registroEntradaDiario, valorEntrada 중인 명령과 Programa ejecutarComando 상태를 보관한다. Archivo 저장소는 공유한다. vi와 Swing의 이벤트 esperarValor 중에 다른 터미널로 전환하면 Usuario datosMemoria·레지스터·Archivo/valorConectorRed 연결을 보존했다가 돌아올 때 재개한다. **elementoListaActual 네 프로그램이 동시에 CPU에서 실행되는 선점형 스케줄러는 아니다.** resultadoCálculo 중인 프로그램은 elementoListaSiguiente valorEntrada esperarValor 또는 기존 ejecutarComando 기한까지 전환이 지연될 númeroValor 있다.

X로 터미널을 닫으면 그 터미널의 ejecutarComando 중인 프로그램도 종료하며 entradaElementoDescriptor·소켓을 회수한다. 저장하지 않은 valorEditar 내용은 사라진다. 종료한 슬롯은 새 창에서 재사용한다. elementoListaActual 모든 파일은 RAM에 있으며 VM 재시작 후에는 남지 않는다.

화면과 ventana 판단은 게스트 커널이 처리한다. QEMU ejecutarComando 도구는 VNC 키와 마우스 좌표를 UART 패킷으로 전달한다. datosEfectivo Pi4 USB 입력기와 equipoFísicoFísico 부팅은 아직 검증하지 않았다. 일반 UART 셸은 `make run`, GUI Herramientas 종료는 Anfitrión 터미널의 Ctrl+C다.

## vi valorUsar

```text
mkdir Tarea
cd Tarea
vi Saludo.py
```

`vi`는 새로 구현한 **vi comando 부분집합** 편집기다. 내장 `build/user/vi.elf`를 보호된 Usuario 영역에 적재한다. Archivo 크기는 UTF-8 valorByte raízProyecto 16 KiB, 경로는 63바이트까지다. 디스크에 설치한 Vim/Neovim 바이너리를 실행하는 것이 아니다.

| valorTecla/comando | acción |
|---|---|
| `i`, `a`, `I`, `A` | elementoListaActual/elementoListaSiguiente posición 또는 línea elementoListaInicialValor/끝에서 valorEntrada |
| `o`, `O` | valorExtremoInferior/위에 새 줄을 만들고 valorEntrada |
| Esc | 일반 valorModo |
| `h j k l`, 방향키 | UTF-8 Caracteres/línea valorMover |
| `0`, `$`, Home, End | línea elementoListaInicialValor/terminación |
| `gg`, `G`, `:número` | Archivo elementoListaInicialValor/elementoListaÚltimo línea/valorAsignar línea |
| PgUp, PgDn | Pantalla valorUnidad valorMover |
| `x`, Delete | elementoListaActual Caracteres 삭제 |
| `dd`, `yy`, `p` | línea 삭제/copiarValor/textoPegar |
| `u` | elementoListaÚltimo 편집을 puenteRetornar; 한 valorEtapa 토글 |
| `/Cadena`, `n` | 단순 Cadena 검색/elementoListaSiguiente esIgual; 정규식 métodoAusente |
| `:w`, `:w 다른이름` | RAM Archivo valorAlmacenar/다른 경로로 valorAlmacenar |
| `:q` | 변경이 없을 때 programaSalir |
| `:q!` | 변경을 버리고 programaSalir |
| `:wq`, `ZZ` | 저장하고 programaSalir |

붙여 넣은 한글을 Caracteres 경계에 맞춰 valorMover·삭제한다. 일반 vi의 수량 접두사, valorMacro, ajustes Archivo, 플러그인, 정규식, 여러 버퍼/분할 ventana, 문법 강조 등은 아직 없다. `--desktop`에서는 F9·Shift+Space·한/operandoCero 키로 두벌식 조합을 전환한다. PC 입력기를 영어로 두고 ventana títuloVentana `[KO]`에서 입력하며, `help ko`에 단축키를 표시한다. 완성된 Unicode 문자와 VNC의 명시적 붙여넣기도 전달한다.

vi와 Swing 프로그램은 **단독 comando**으로 실행한다. 파이프·리다이렉션·valorGuion·`;`/`&&`/`||`로 연결한 실행에서 interactivo 대기를 시작하면 거부한다. valorEntrada 대기는 약 2초 CPU 기한을 갱신하지만 valorEntrada esperarValor 없이 무한 반복하는 프로그램은 기존처럼 종료한다.

## textoHangul Java

vi에서 다음을 `Saludo.java`에 입력하고 Esc → `:wq`로 저장한다.

```java
public class Saludo {
    static int añadirValores(int ordinalPrimero, int ordinalSegundo) { return ordinalPrimero + ordinalSegundo; }
    public static void main(String[] argumentos) {
        int valorTotal = añadirValores(20, 22);
        System.out.println("안녕하세요 · valorTotal=" + valorTotal);
    }
}
```

게스트 셸에서 실행한다.

```text
javac Saludo.java
java Saludo
```

textoHangul textoNombreArchivo·nombreClase·textoNombreMétodo·변수명·문자열을 사용할 númeroValor 있다. **게스트 javac는 valorEstático Java 부분집합**이다. valorObjeto·리스너·Swing·소켓을 사용하는 소스는 elementoListaActual Anfitrión JDK에서 `javac --release 8 -encoding UTF-8`로 컴파일하고 propio JVM에 class를 올린다. propio JVM에서 지원하는 códigoBytes/API 범위는 [EntornoEntornoEjecuciónJava.md](EntornoEntornoEjecuciónJava.md)를 따른다.

```sh
# Anfitrión
mkdir -p build/my-java
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/my-java Pruebas/Java/PruebaSwing.java
python3 Herramientas/archivosSubir.py build/my-java/PruebaSwing.class
```

`upload.py`는 게스트 `load`에 붙여 넣을 16진수 명령을 생성한다. Salida 전체를 GUI 터미널에 보내면 업로드한다. 업로드 estadoValorDespués **별도로** `java PruebaSwing`을 실행한다. 종속 class가 있으면 각각 업로드한다. 패키지 class의 파일명은 `패키지.valorClase.class` 형식이다. 내장 español 라이브러리는 별도 업로드가 valorNecesario 없다. español ventana API의 예제는 [pruebaVentanaHangul.java](Pruebas/Java/pruebaVentanaHangul.java)이며 같은 방법으로 compilarFuente·업로드해 `java pruebaVentanaHangul`으로 실행한다.

GUI가 valorNecesario 없는 단일 árbolFuente/클래스는 호스트의 `python3 Herramientas/ejecutarArchivo.py ruta/Saludo.java`로 별도 QEMU에 업로드·ejecutarComando·종료할 númeroValor 있다. interactivo Swing에는 ejecutarComando estadoValorDespués Usuario 입력을 유지하는 `make desktop`을 사용한다.

## propio JVM의 Swing recortar

실제로 제공하는 것은 **표준 패키지 이름으로 호출하는 propio Swing API 부분집합**이다. OpenJDK `java.desktop` 모듈이나 AWT 전체를 이식한 것은 아니다.

| API | acción |
|---|---|
| `JFrame` | títuloVentana, tamaño·posición, mostrarVentana, cerrar 정책, dispose |
| `JPanel` | valorHijo 요소를 담는 패널 |
| `JLabel` | 한글을 포함한 Cadena mostrarValor·cambiarValor |
| `JButton` | 버튼과 ActionListener valorPulsarRatón entradaElementoValorProceso |
| `JTextField` | 한 línea UTF-8 valorEntrada, 삭제, getText/setText, Enter 이벤트 |
| valorComún | setBounds, setSize, add, getContentPane, repaint, validate |
| `SwingUtilities` | invokeLater, isEventDispatchThread |
| `ActionEvent` | getSource, getActionCommand, getID |

`setLayout(null)`과 `setBounds`로 배치한다. FlowLayout/BorderLayout/GridLayout, pack, 폰트·스타일 전체, 메뉴·테이블·트리·스크롤 패널, Java2D, 네이티브 AWT peer/JNI, 복잡한 Caracteres 조판은 아직 없다. 이벤트 콜백은 propio JVM의 단일 이벤트 ejecutarComando 흐름에서 처리하며 OpenJDK EDT 구현과 동일하지 않다. ventana·요소는 ejecutarComando 하나당 valorTotal 32개, valorElemento 글자는 valorMáximo 127 코드포인트다. valorPredeterminado 서체와 색은 커널이 제공한다.

[PruebaSwing.java](Pruebas/Java/PruebaSwing.java)는 ventana·textoHangul valorEtiquetaMarcador·CampoTexto·버튼·이벤트 처리의 ejecutarComando 가능한 예제다. [propio Swing Pantalla](build/verification/swing/native-swing.png)을 참고한다.

español 라이브러리에는 다음을 추가했다. Anfitrión compilarFuente 시 `dist/jkoros-native-korean.jar`를 classpath에 넣는다.

- `español.propio.ventana`: `añadirElemento`, `mostrarVentana`, `cerrar`.
- `español.propio.ComponenteVisual`: `valorEtiquetaMarcador`, `botón`, `CampoTexto` generar.
- `español.propio.transporteConexión`: `conectar`, `escucharExtremo`, `recibir`.
- 기존 `Salida`, `Caracteres`, `Archivo`, `Tarea`, `listaEntradaElemento`, `Diccionario`, `Comunicación`, `Pantalla`, `valorNúcleo`도 유지한다.

## Java 네트워크

기존 `DatagramSocket`/`DatagramPacket`의 UDP 루프백에 `Socket`/`ServerSocket`의 **valorNúcleo 내부 연결형 valorByte valorFlujo**을 추가했다. Archivo/소켓과 마찬가지로 SVC를 통해 Java 커널이 전송한다. 물리 NIC의 TCP/IP 패킷 스택은 아니다.

```java
java.net.ServerSocket valorServidor = new java.net.ServerSocket(9250);
java.net.Socket valorInvitado = new java.net.Socket("localhost", 9250);
java.net.Socket conectar = valorServidor.accept();
valorInvitado.getOutputStream().write("안녕하세요".getBytes("UTF-8"));
byte[] elementoListaRecibido = new byte[64];
int longitud = conectar.getInputStream().read(elementoListaRecibido);
conectar.close(); valorInvitado.close(); valorServidor.close();
```

generar·conectar·accept·양방향 valorByte/valorArreglo salidaEntrada·close·EOF·setSoTimeout을 지원한다. `String.getBytes()`와 UTF-8 이름을 지정한 getBytes도 제공한다. 루프백 주소는 `localhost`/`127.0.0.1`이다. 연결형 puntoFin 16개, recibirValor 버퍼당 1024바이트, esperarValor conectar valorMáximo 4개이며 Java의 대기는 내부 가닥에 실행을 양보한다. valorPredeterminado valorTiempo valorLímite 0은 별도 valorConectorRed 기한을 설정하지 않지만 JVM comando númeroValor/valorNúcleo ejecutarComando 기한은 여전히 적용된다.

valorExterno valorDígito IPv4 TCP/UDP는 lwIP/SLIP로 지원한다. datosEfectivo Ethernet/Wi-Fi 드라이버, DNS·TLS·HTTP biblioteca 전체는 미지원이다. `java.net`의 모든 메서드와 옵션, `SocketChannel`/select, SSL, shutdownInput/Output는 아직 없다. [pruebaFlujo.java](Pruebas/Java/pruebaFlujo.java)는 datosEfectivo 송수신·EOF·기한·conectar 회수의 Pruebas 예제다.

## textoHangul Python

게스트 vi에서 textoHangul 이름을 사용해 작성한다.

```python
valor = 21

def 두배(valorDígito):
    return valorDígito * 2

print("resultado:", 두배(valor))
```

valorAlmacenar estadoValorDespués `python Saludo.py`로 실행한다. 실행기는 MicroPython 1.24.1이다. Python 문법 키워드는 그대로 사용하며 Función·valorVariable·Archivo 이름과 문자열을 한글로 쓴다.

[español.py](Ejemplos/CodificaciónHangul/español.py)를 같은 디렉터리에 두면 elementoListaSiguiente 별칭을 사용할 númeroValor 있다.

```python
import español
español.escribirArchivo("Saludo.txt", "안녕하세요")
español.Salida(español.leerArchivo("Saludo.txt").decode())
```

Salida·Archivo leer/escribir/삭제·표준 valorEntrada·rectángulo·valorTiempo·UDP를 연결한다. 기존 `udp_send`는 루프백, 새 `udp_sendto(fd, "10.0.2.2", port, data)`는 valorDígito IPv4 dirección 전송이다. `wait_key()`는 화면을 확인할 때 interactivo 입력을 기다린다. Python 함수는 `jkoros` 내장 모듈을 통해 SVC를 사용한다. C ABI인 posix-kor valorEstático 라이브러리를 Python이 직접 링크하는 구성은 아니다. CPython과 일반 valorExtensión 모듈은 아직 없다. 제한형 `pip`의 árbolFuente 설치는 [Python Paquete Guía](PaquetePython.md)를 따른다. [valorTres 언어의 datosEfectivo Ejemplos](../../example/README.md).

## C·C++에서 posix-kor invocar

두 Lengua construirTodos español 헤더와 Función 이름을 직접 사용한다. [Saludo.c](Ejemplos/CodificaciónHangul/Saludo.c), [Saludo.cpp](Ejemplos/CodificaciónHangul/Saludo.cpp)operandoPrimero datosEfectivo EL0 ejecutarComando Pruebas 대상이다.

```c
#include "ABIArchivo.h"
#ifdef __cplusplus
extern "C"
#endif
int iniciarProgramaUsuario(int argumentos) {
    (void)argumentos;
    const char saludo[] = "안녕하세요\n";
    int Documentación = abrirArchivo("Saludo.txt", EscribirLeer | AusenteSiCrear | ContenidoTruncar, 0600);
    if (Documentación < 0) return 1;
    tipoResultadoEntradaSalida númeroElementosRegistrado = escribirDatosArchivo(Documentación, saludo, sizeof(saludo) - 1);
    cerrarArchivo(Documentación);
    escribirDatosArchivo(1, saludo, sizeof(saludo) - 1); /* elementoListaActual terminal stdout */
    return númeroElementosRegistrado == sizeof(saludo) - 1 ? 0 : 2;
}
```

파일은 게스트 vi로 작성할 númeroValor 있다. C는 게스트 `cc` 또는 Anfitrión SDK, C++는 Anfitrión SDK의 Clang++로 컴파일한다. valorExtremoInferior 예제는 기존 Anfitrión SDK 경로다. 게스트 내부 GCC/Clang·libc/libstdc++ 전체를 탑재한 것은 아니다. SDK가 `.c`에는 C11, `.cpp`에는 C++11을 선택한다.

```sh
# 호스트에서 SDK generar·extraer
make sdk
mkdir -p build/sdk-work
tar -xzf dist/jkoros-native-aarch64-sdk.tar.gz -C build/sdk-work
cd build/sdk-work/jkoros-native-sdk
python3 compile.py examples/Saludo.c -o Saludo-c.elf
python3 compile.py examples/Saludo.cpp -o Saludo-cpp.elf

# 프로젝트로 돌아와 별도 QEMU에서 datosEfectivo ejecutarComando
cd /home/user/jkoros/platforms/rpi4-native
python3 Herramientas/ejecutarArchivo.py build/sdk-work/jkoros-native-sdk/Saludo-c.elf
python3 Herramientas/ejecutarArchivo.py build/sdk-work/jkoros-native-sdk/Saludo-cpp.elf
```

elementoListaActual GUI VM에서 실행하려면 `python3 Herramientas/archivosSubir.py ruta/Saludo-c.elf`의 출력을 게스트에 보내고 `run Saludo-c.elf`를 입력한다. 게스트에서 작성한 소스의 전송은 `hex textoNombreArchivo`으로 내용을 얻어 호스트에서 `bytes.fromhex(...)`로 복원할 númeroValor 있다. 호스트와 게스트의 Archivo 시스템은 별개다.

| español nombre | C símbolo | recortar |
|---|---|---|
| abrirArchivo/cerrarArchivo | pk_open/pk_close | RAM Archivo, valorParRed/절대 ruta |
| leerDatosArchivo/escribirDatosArchivo | pk_read/pk_write | Archivo, fd 0/1/2 표준 salidaEntrada, 연결형 valorConectorRed |
| posicionarArchivo | pk_lseek | PrincipioDesde/raízActual/origenFin |
| tamañoArchivo/establecerLongitudArchivo | pk_size/pk_ftruncate | longitud valorConsultar/cambiarValor |
| eliminarNombreEntradaElementoArchivo | pk_unlink | Archivo nombre 삭제 |
| almacenamientoArchivoConfirmar | pk_fsync | RAM이므로 -1, númeroError=ENOSYS |
| crearExtremo/asociarDirección | pk_socket/pk_bind | AF_INET, SOCK_DGRAM 또는 SOCK_STREAM |
| enviarDatosDatagrama/recibirDatosDatagrama | pk_sendto/pk_recvfrom | UDP 루프백 |
| conectarRed | pk_connect | 연결형 루프백 |
| esperarConexiónRedPara | pk_listen | esperarValor conectar valorMáximo 4개 |
| aceptarConexiónRed | pk_accept | elementoListaActual dirección 인수는 NULL/NULL만 valorSoporte |
| leerDirecciónConectorRed | pk_getsockname | 로컬 dirección/valorPuerto |

`ABIRed.h`의 propio `pk_sockaddr_in`을 사용하며 valorPuerto·주소는 `cortoRed`/`enteroValorRed`로 변환한다. C valorConectorRed 호출은 비차단이며 Datos/연결이 없으면 -1과 `númeroError=11`(EAGAIN)을 반환한다. 양수 salidaEntrada 결과가 요청보다 작을 númeroValor 있으므로 valorIteración 처리한다. valorFallo 후에만 오류번호를 확인한다.

[valorFlujo.c](Ejemplos/CodificaciónHangul/valorFlujo.c)는 C에서 español 이름으로 conectar·accept·valorSubparte leer/escribir·큐 포화·EOF를 처리하는 ejecutarComando 예제다. SDK의 `examples/valorFlujo.c`를 같은 `compile.py`로 컴파일한다.

SDK는 **libposix-kor-user.a**를 링크한다. invocar 흐름은 C/C++ → datosEfectivo español C Función 또는 호환용 `pk_*` → `svc #0` → 커널의 소유권·puntero Comprobaciones → Java RAM Archivo/루프백 또는 valorExterno lwIP TCP/UDP 구현이다. `libposix-kor-arm64.a`는 valorNúcleo 내부용이므로 EL0 프로그램에 링크하지 않는다. Linux 헤더나 Linux ELF와 혼합하지 않는다. 동적 conectar, 표준 C printf, libstdc++/STL, excepción·RTTI는 제공하지 않으며 C++의 valorEstático 생성자·ámbitoLocal valorObjeto 소멸자는 지원한다. 상세 número·datosMemoria 범위는 [ABILlamadaUsuario.md](ABILlamadaUsuario.md)를 참고한다.

## validar

`make test-windows`, `make test-swing`, `make test-stream`, `make test-coding`으로 새 기능을 각각 시험한다. `make test`는 기존 intérpreteComandos·VNC·JVM·AOT·valorNúcleo protegerValor 시험까지 포함한다. datosEfectivo Placa 대신 QEMU raspi4b에서 수행한다. 결과는 [elementoListaElementoPrevio GUI valorExtensión validar registroEntradaDiario](build/verification/release.json)과 [elementoListaActual EntornoEjecución validar registroEntradaDiario](build/verification/native-runtime-summary.json), [여러 terminal Pantalla](build/verification/windows/four-terminals.png), [Swing Pantalla](build/verification/swing/native-swing.png)을 참고한다.

implementación 시 참고한 표준 API: [Socket](https://docs.oracle.com/javase/8/docs/api/java/net/Socket.html), [JFrame](https://docs.oracle.com/javase/8/docs/api/javax/swing/JFrame.html), [JButton](https://docs.oracle.com/javase/8/docs/api/javax/swing/JButton.html). 이 문서의 implementación 범위가 valorExtremoSuperior 표준 전체를 지원한다는 뜻은 아니다.

## español 이름으로 직접 작성하는 창과 valorHiloEjecución

`example/java/EjemploVentana.java`는 `TareaTareaEjecutable.ejecutarTarea`,
`ReceptorAcción.recibirAcción(NotificaciónAcción)`, `botón`, `ColaEvento.invocarPosterior`, `ponerEnMarcha()`을 쓴다.
propio JVM에 이 이름들의 valorObjeto·valorMétodo·콜백을 직접 구현했으며 영어 Swing 객체를
보관하는 래퍼가 아니다. `tareaFondo`도 propio 스케줄러와 직접 연결된다.
세부 메서드와 기존 español API에서의 변경은 [español API Documentación](JavaEspañol/Guía.md)를 본다.

Anfitrión javac는 valorDistribución JAR를 valorClase 경로로 사용한다.

```sh
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/한국어사용 ../../example/java/EjemploVentana.java
python3 Herramientas/ejecutarComando.py --desktop --network --resolution 1920x1080
```

게스트에는 빌드한 예제가 `/example/java`에 설치된다.

```text
cd /example/java
java EjemploVentana
```

직접 Pantalla/valorHiloEjecución API와 `ponerEnMarcha()` 진입점은 propio JVM 전용이다.
전체 OpenJDK·Swing 재구현이나 일반 OpenJDK에서 같은 API의 실행을 보장하지 않는다.
기존 표준 `main(String[])` 프로그램은 procesamientoContinuar 실행할 númeroValor 있다.
