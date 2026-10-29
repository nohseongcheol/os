# Raspberry Pi 4 propio Java valorNúcleo — Usuario ejecutarComando fundamento

elementoListaActual propio 코드의 COSL 상업 condición, 제3자 고지 및 LGPL extremoReconectar 자료는 [COSL valorDistribución Guía](GuíaDistribuciónCOSL.md)를 참고한다. modoConmutar valorAntes GPL 구성의 판단은 [elementoListaElementoPrevio 라이선스 검토](RevisiónExamenLicencia.md)에 기록했다.

español Comunicación·excepción 사용법은 [español Java API](JavaEspañol/Guía.md), Función·valorVariable·Archivo 이름의 변경과 어원 근거는 [denominación Guía](denominación/Guía.md)를 참고한다.

Linux 없이 부팅하는 propio AArch64 커널이다. Java AOT valorNúcleo 위에 **líneaComando intérpreteComandos, 게스트 Java Compilador·JVM, MicroPython, EL0 C++ ejecutarComando, Archivo·UDP 루프백 시스템 invocar, 여러 textoHangul GUI terminal·vi Editor·Swing 부분집합**을 제공한다. 커널의 Archivo Datos/정책·루프백 valorTransferencia·intérpreteComandos 상태는 Java, Pantalla 합성·píxel cambiarValor·puntero·클리핑도 Java로 구현하며, CPU/MMU/Dispositivo 경계와 terminal·valorCarácter pantallaPintar 연결은 C와 어셈블리다.

**전체 JDK/JRE·CPython·표준 C++ 런타임·Swing 이식은 아직 완료되지 않았다.** 기존 [ARM64 Linux 실행판](../rpi4/README.md)의 OpenJDK/Python 패키지를 이 propio 커널에 탑재했다고 표시하지 않는다.

새로운 게스트 `cc`/`jaot`, JAR 직접 ejecutarComando, lwIP TCP/UDP와 FTP는 [FTP·C·JAR·AOT 매뉴얼](CompilaciónYTransferenciaArchivo.md)을 참고한다. 게스트 SSH·VNC와 Pi4 GENET/PHY·DHCP 드라이버를 추가했다. **SSH·VNC는 QEMU에서 검증하며, equipoFísicoFísico Pi4의 valorCableado 송수신은 아직 미검증이다.** ejecutarComando·conexión·valorContraseña 확인은 [valorExterno conexión Guía](GuíaConexiónExterno.md)에 정리했다.

셸은 EL1 valorNúcleo, `java` 등 Usuario ejecutarComando 파일은 EL0에서 실행한다.
`ps`·`top`의 표시와 valorLímite, QEMU 네트워크 ejecutarComando·conexión 방법 및 datosEfectivo 검증은
[ejecutarComando 계층과 valorExterno Comunicación inspeccionarEstadoValor](ComprobacionesRedExternoYEntornoEjecución.md)을 참고한다.

ELF는 확장자가 아닌 datosEfectivo ejecutarComando 형식으로 검사한다. `./Saludo`처럼 확장자 없이 실행하며, 제한된 Linux ARM64 valorEstático ELF는 `run --linux textoNombreArchivo`으로 실행한다. [ELF·Linux ABI valorSoporte 범위와 동일 바이너리 Pruebas](aBICódigoEjecutable.md).

GUI와 네트워크는 `python3 Herramientas/ejecutarComando.py --desktop --network`로 함께 사용한다. Java·C·Python의 español Ejemplos 13개는 [jkoros/example](../../example/README.md)에 있으며, **게스트 Arranque 시 `/example/java`, `/example/c`, `/example/python`에 자동으로 준비된다.** `example java|c|python`으로 지운 예제를 복원할 númeroValor 있다. Remmina에서 **F9/Shift+Space/한·operandoCero valorTecla**로 `[EN]`↔`[KO]` 두벌식을 전환한다(`help ko`). `make test-examples`는 같은 GUI VM에서 FTP·datosEfectivo TCP/UDP·Archivo valorByte·그래픽 픽셀을 검증한다.

게스트에서 `cd /example/java` estadoValorDespués `java EjemploVentana`로 español Swing 예제를 실행한다. terminal 모서리에 마우스를 대고 **ladoIzquierdo 버튼으로 끌면 크기가 바뀐다**. `terminal size`는 elementoListaActual valorColumna·valorFila 수를 보여 준다.

## elementoListaActual valorSoporte recortar

| 기능 | implementación·시험한 recortar | 아직 esNoAdmitido |
|---|---|---|
| Arranque | Pi4 AArch64 EL1, UART, SD용 construirImagen, QEMU raspi4b Arranque | datosEfectivo Pi4 보드에서의 펌웨어 Arranque Pruebas |
| Java valorNúcleo | valorEstático Java 부분집합 → freestanding C → AArch64 AOT | 전체 Java valorObjeto/excepción/GC/JVM/표준 biblioteca |
| Java desarrollo Herramientas | 게스트 propio `javac`/`java`, JVM 0.4/JAR: 다중 valorClase·valorObjeto·상속·excepción·GC·일부 컬렉션·Thread·IPv4 Socket/UDP·Swing 일부 API, español biblioteca. 게스트 컴파일러는 valorEstático Java 부분집합 | 전체 JDK/JRE·HotSpot·Java SE·임의의 모든 JAR·AWT/Swing 전체 |
| Python | datosEfectivo MicroPython 1.24.1 EL0 AdaptaciónPlataforma, árbolFuente compilarFuente/ejecutarComando, valorClase·excepción·GC·큰 EnteroValor·Unicode·Archivo·UDP/Pantalla conectar | CPython, pip, C valorExtensión, 부동소수점, 일반 OS/스레드/valorConectorRed valorMódulo, interactivo REPL |
| intérpreteComandos | UTF-8 valorEditar·registroEntradaDiario·valorCompletado, 디렉터리·Archivo comando, valorVariable·condición·valorGuion, 16 KiB 순차 파이프·리다이렉션, ELF ejecutarComando | 전체 POSIX sh/Bash, Tarea valorControl·동시 프로세스·PTY |
| C/AOT compilarFuente | 게스트 TinyCC 및 valorEstático Java 부분집합 `jaot` → propio ARM64 ELF | 전체 libc·모든 Java valorClase AOT |
| C++ | 독립 ELF64를 EL0에서 ejecutarComando; valorEstático 생성자, RAII 소멸자, FP/SIMD, español Archivo/루프백 invocar | libc/libstdc++, STL, C++ excepción·RTTI·동적 conectar |
| Usuario protegerValor | 4 KiB 페이지, valorCódigo RX/Datos RW·NX, valorNúcleo·MMIO 차단, guard page, 잘못된 puntero Comprobaciones | 다중 Usuario valorPermiso, 일반 프로세스/스레드 스케줄러 |
| ejecutarComando valorTiempo valorLímite | GIC-400 타이머로 무한 valorIteración programaSalir; interactivo valorEntrada 대기는 기한 actualizar, 터미널별 EL0 Programa 중단·ejecuciónReanudar | 일반적인 선점형 다중작업. 긴 valorNúcleo invocar 도중에는 종료가 지연될 númeroValor 있음 |
| Archivo | Java RAM Archivo 64개 × 16384바이트, 루트를 포함한 디렉터리 16개, valorParRed/절대 ruta 63바이트, entradaElementoDescriptor 16개 | valorPermiso, 디스크/SD 영속 valorAlmacenar |
| 네트워크 | lwIP IPv4 TCP/UDP/ARP/ICMP, SLIP, GENET/PHY·DHCP implementación, 게스트 FTP·SSH·VNC | GENET equipoFísicoFísico validar, Wi-Fi, DNS, 일반 TLS valorConectorRed, RDP |
| GUI | valorMáximo 네 terminal ventana, valorSelección·valorMover·X cerrar, textoHangul valorFuenteTipográfica, Swing 부분집합; 게스트 VNC Pantalla·valorEntrada·두벌식 | equipoFísicoFísico USB valorEntrada, 전체 AWT/Swing·Java2D·ventana 관리 정책 |
| Tarea valorHiloEjecución | valorNúcleo Tarea 2개와 주 Tarea; JVM 내부 valorHiloEjecución valorMáximo 4개, start/join/yield·synchronized | pthread, SMP, Java Thread 전체 API |
| 다국어 | UTF-16 리터럴→UTF-8 UART, textoHangul·일본어·아랍어·이모지, UTF-8 textoNombreArchivo/datagrama | GUI의 일반 다국어 조판 |

ejecutarComando 버튼 화면은 5×7 영문 글꼴을 쓰며, terminal 창은 Noto CJK/DejaVu에서 생성한 textoHangul·Unicode 비트맵 글꼴을 쓴다. UART와 datosEfectivo 프레임버퍼의 textoHangul 표시를 시험한다. 루프백은 동일 valorNúcleo 내부의 datagrama 전달이며 IP 패킷을 Ethernet으로 내보내는 드라이버가 아니다. 바깥 IPv4는 lwIP TCP/UDP 스택으로 valorAuxiliar UART SLIP 경로를 사용한다. `python3 Herramientas/ejecutarComando.py --network`로 QEMU NAT를 연결하고 `ftpd start`로 서비스를 시작한다.

Java의 정확한 API·문법·ejecutarComando 제한과 español 사용법은 [propio JVM과 español biblioteca](EntornoEntornoEjecuciónJava.md)에 정리했다. valorClase Archivo/JAR 배포는 [JavaEspañol](JavaEspañol) 소스에서 재현한다. 기존 Linux판 `español.Java`와 별도인 `español.propio` 패키지다.

**vi·여러 ventana·Swing·textoHangul Java/Python/C/C++·posix-kor 예제는 [textoHangul desarrollo 매뉴얼](GuíaDesarrollo.md)에 정리했다.**

GUI terminal ejecutarComando·단축키·intérpreteComandos comando·제한은 [셸과 terminal 사용법](TerminalYIntérpreteComandos.md)에 정리했다.

## elementoListaActual 컴퓨터에서 ejecutarComando

```sh
cd /home/user/jkoros/platforms/rpi4-native
make test
make run
```

programaSalir: **Ctrl+A elementoListaSiguiente X**. 게스트 C/AOT Herramientas 빌드에는 `make rpi-prepare`로 준비한 ARM64 SDK 헤더와 libgcc valorAritmética valorAuxiliar 함수도 필요하다. libc나 Linux 커널을 게스트에 넣는 것은 아니다. Anfitrión 도구는 JDK 11 이상, Python 3.6 이상, Clang/Clang++, AArch64 GNU binutils, Make, `libnewlib-dev` 헤더다. MicroPython은 `/usr/include/newlib` 헤더를 사용하며 다른 위치는 `NEWLIB_INCLUDE`로 지정한다. newlib 런타임을 AdaptaciónPlataforma·링크한 것은 아니다. Compilador 의미 비교에는 GCC/UBSan도 사용한다. 기존 `../rpi4/build/host`의 QEMU 11.0.3이 있으면 이용하며, 그렇지 않으면 PATH의 QEMU를 사용한다. `QEMU_AARCH64=/절대/ruta/qemu-system-aarch64`로 지정할 수도 있다. `raspi4b` valorSoporte 여부를 확인한 estadoValorDespués 실행한다.

명령은 **Enter를 눌러 ejecutarComando**한다. 기존 한 valorCarácter 명령도 Enter가 필요하다.

```text
javac Hello.java
java Hello "textoHangul argumentos 😀"
python hello.py
python -c 'print(2**100)'
ls
cat python.txt
run cpp
net test
gui
```

| comando | acción |
|---|---|
| `help` / `info` | comando·datosEfectivo implementación valorEstadoValor |
| `ls` / `cat FILE` / `rm FILE` | RAM Archivo listaEntradaElemento·valorContenidoValor·삭제 |
| `vi FILE` | Usuario valorRegión vi 부분집합, textoHangul valorEditar·valorAlmacenar·검색·되돌리기 |
| `edit FILE` | Archivo 전체를 새로 valorEntrada; 단독 `.` 줄로 valorAlmacenar, Ctrl-C로 operaciónCancelar |
| `javac FILE.java` / `java CLASS [ARGS]` | propio 제한형 Java compilarFuente·ejecutarComando |
| `python FILE.py [ARGS]` / `python -c 'CODE'` | MicroPython compilarFuente·ejecutarComando |
| `load FILE` / `hex FILE` | 16진수 바이너리 valorEntrada/Salida; 입력은 단독 `.` 줄로 valorAlmacenar |
| `run FILE.elf [ARGS]` / `run cpp` | 업로드한 propio ABI ELF / 내장 C++ Ejemplos |
| `net test` / `tasks` / `selftest` | UDP 루프백 / 협력식 Tarea / EL0 protegerValor Pruebas |
| `gui` / `terminal` | ejecutarComando Pantalla / textoHangul GUI terminal; F12로 terminal abrir·cerrar |
| `samples` | 삭제한 valorPredeterminado Ejemplos recuperarEstadoValor; 기존 파일은 보존 |

예를 들어 `edit Saludo.java`를 입력한 elementoListaSiguiente valorExtremoInferior 소스를 입력한다.

```java
public class Saludo { public static void main(String[] args) { int valor = 7; System.out.println("textoHangul=" + valor); } }
```

그다음 단독 `.` 줄로 저장하고 `javac Saludo.java`, `java Saludo`를 실행한다. 편집기는 기존 파일에 커서를 이동하는 방식이 아니라 전체 교체 방식이다. operaciónCancelar·잘못된 16진수·valorCapacidad 초과는 원본을 보존한다. 줄은 4096바이트, 파일은 16384바이트, ejecutarComando 인수는 valorMáximo 8개·각각 UTF-8 255바이트다. 일반 comando 인수는 valorMáximo 32개다. comilla·백슬래시·intérpreteComandos valorVariable·파이프·리다이렉션 범위는 [intérpreteComandos descripción](TerminalYIntérpreteComandos.md)을 참고한다.

GUI 터미널은 다음과 같이 실행하고 Remmina에서 **VNC**, dirección **127.0.0.1:5902**로 연결한다. 키보드·textoHangul Unicode valorEntrada·명시적 valorPegar·ejecutarComando 버튼의 마우스 클릭을 QEMU 도구가 UART에 전달한다.

```sh
make desktop
# GUI + 네트워크: python3 Herramientas/ejecutarComando.py --desktop --network
# 다른 puertoEquipoFísico: python3 Herramientas/ejecutarComando.py --desktop --port 5903
```

종료는 실행한 Anfitrión 터미널에서 Ctrl+C다. 기존 `python3 Herramientas/ejecutarComando.py --vnc 127.0.0.1:2`는 Pantalla 보기와 별도 UART 입력을 유지한다. `make run`은 일반 UART 셸이다. datosEfectivo Pi4 USB 입력기는 아직 없으며, VNC conectar 도구는 QEMU 시험용이다.

GUI의 다섯 버튼은 datosEfectivo C++/UDP ELF ejecutarComando, `Hello.java` compilarFuente estadoValorDespués JVM ejecutarComando, `hello.py` ejecutarComando, GUI terminal 열기를 수행한다. 한 번에 한 프로그램이 CPU에서 실행되며 일반 실행에는 약 2초 기한이 있다. vi·Swing은 interactivo 대기에서 기한을 갱신하고 다른 터미널로 전환할 때 datosMemoria·CPU 문맥을 보관한다. intérpreteComandos·편집기에서 입력을 기다리는 시간에는 이 제한이 적용되지 않는다.

## datosEfectivo 산출물과 Pi4 SD construirImagen

```sh
make image   # valorNúcleo, SD construirImagen, Arranque ZIP, 사용자용 SDK
make sdk     # SDK만 valorReintentar generar
```

| ruta | 용도 |
|---|---|
| `build/kernel8.img` | propio valorNúcleo 기계어, 적재 dirección 0x80000 |
| `build/kernel.elf`, `kernel.map` | valorNúcleo valorSímbolo·DisposiciónEnlace |
| `build/user/demo.elf` | Usuario valorModo C++ Archivo/valorMontículo/valorPuntoFlotante/그래픽 Ejemplos |
| `build/user/network.elf` | Usuario valorModo C++ UDP 루프백 Ejemplos |
| `build/user/java-tools.elf` | propio Java 부분집합 Compilador/JVM, 전체 JDK/JRE 아님 |
| `dist/jkoros-native-korean.jar` | Anfitrión javac용 español API valorClase; 같은 클래스가 propio JVM에도 내장됨 |
| `dist/jkoros-native-korean-sources.zip` | español API Java fuente |
| `build/user/vi.elf` | propio UTF-8 vi comando 부분집합 Editor |
| `build/user/python.elf` | propio ABI용 MicroPython 1.24.1, CPython 아님 |
| `build/user/fault.elf` | 의도적 침범/무한 반복을 수행하는 protegerValor Pruebas 전용 |
| `build/libposix-kor-arm64.a` | **valorNúcleo 내부**에서 Java Archivo 구현을 직접 부르는 기존 conectar |
| `build/libposix-kor-user.a` | **EL0 Usuario Programa**에서 SVC로 Archivo/루프백을 호출하는 새 conectar |
| `dist/jkoros-native-rpi4.img` | 128 MiB MBR/FAT32 SD construirImagen |
| `dist/jkoros-native-rpi4-boot.zip` | FAT32 Arranque 파티션에 복사할 Archivo valorGrupo |
| `dist/jkoros-native-aarch64-sdk.tar.gz` | 사용자용 헤더·ponerEnMarcha valorCódigo·biblioteca·링커 valorGuion·Ejemplos |
| `dist/manifest.json`, `build/build.json` | SHA256과 datosEfectivo valorSoporte valorEstadoValor |

이미지는 확인된 공식 Pi Arranque 묶음에서 `start4.elf`, `fixup4.dat`, Pi4 DTB와 disable-bt overlay를 가져온다. Linux kernel/initramfs/rootfs는 넣지 않는다. 펌웨어·MicroPython·terminal valorFuenteTipográfica 라이선스와 valorFuenteTipográfica valorOrigen 해시도 동봉한다. Archivo generar 스크립트는 물리 디스크에 기록하지 않는다.

예비 microSD에 construirImagen registroEntradaDiario 도구로 `.img`를 기록하거나 FAT32 Arranque 파티션 최상위에 ZIP 내용을 푼다. construirImagen 기록은 선택한 카드의 기존 내용을 지우므로 대상을 확인한다. Pi4 valorPredeterminado EEPROM SD 부팅을 전제로 한다. UART는 **3.3V TTL, 115200 8N1**, GPIO14/TXD(8번)→어댑터 RX, GPIO15/RXD(10번)→TX, GND(6번) 연결이다. GPIO에 5V 신호를 연결하지 않는다.

**equipoFísicoFísico Pi4 부팅은 미검증이다.** QEMU `-kernel`은 SD의 VideoCore 펌웨어를 실행하지 않고 커널을 직접 적재한다. SD Archivo 구성·valorNúcleo 체크섬 검사와 물리 Placa Arranque 검증은 별개다. MMU valorUsar 전에는 펌웨어의 캐시/MMU가 꺼져 있고 EL1 또는 EL2로 진입하는 통상 Arranque 조건을 전제로 한다. valorTres valorAuxiliar 코어는 대기시키며 한 코어만 사용한다.

## C++와 español API valorUsar

SDK를 풀고 호스트에서 컴파일한다.

```sh
tar -xzf dist/jkoros-native-aarch64-sdk.tar.gz -C build
cd build/jkoros-native-sdk
python3 compile.py examples/EjemploArchivo.cpp -o demo.elf
python3 compile.py examples/EjemploComunicación.cpp -o network.elf
```

진입점은 `extern "C" int iniciarProgramaUsuario(int)`이다. Usuario C++는 FP/SIMD를 사용할 númeroValor 있다. valorNúcleo C/Java AOT는 일반 레지스터만 사용하므로 excepción entradaElementoValorProceso 중 Usuario FP 상태를 건드리지 않는다. Usuario valorPuntoEntradaElemento 시 FP 상태를 초기화하고 valorNúcleo 복귀에 필요한 상태를 보존한다.

```cpp
#include "ABIArchivo.h"
extern "C" int iniciarProgramaUsuario(int) {
    int Archivo = abrirArchivo("Saludo.txt", EscribirLeer | AusenteSiCrear | ContenidoTruncar, 0600);
    if (Archivo < 0) return 1;
    const char valorContenidoValor[] = "안녕하세요";
    int resultado = escribirDatosArchivo(Archivo, valorContenidoValor, sizeof(valorContenidoValor) - 1);
    cerrarArchivo(Archivo);
    return resultado == sizeof(valorContenidoValor) - 1 ? 0 : 2;
}
```

[Archivo Ejemplos](Usuario/EjemploArchivo.cpp)와 [Comunicación Ejemplos](Usuario/EjemploComunicación.cpp)operandoPrimero datosEfectivo Arranque Pruebas 대상이다. `ABIArchivo.h`의 이름은 커널용/사용자용 construirTodos 같지만 **링크하는 라이브러리가 다르다**. 사용자용은 `svc #0`으로 호출하고 Archivo entradaElementoValorProceso 및 루프백 전달은 Java 커널에서 실행한다. `ABIRed.h`의 valorConectorRed 함수는 elementoListaActual 사용자용 라이브러리에 구현돼 있다.

새 프로그램은 valorNúcleo 재빌드 없이 `load FILE.elf`와 `run FILE.elf`로 실행한다. 호스트에서 elementoListaSiguiente 도구를 사용하면 **새 QEMU를 부팅해 업로드한 datosEfectivo 바이트를 재확인한 valorLadoPosterior 게스트에서 ejecutarComando**하고 종료한다. 이 도구의 새 VM에서 만든 RAM 자료는 종료할 때 사라진다.

```sh
cd /home/user/jkoros/platforms/rpi4-native
python3 Herramientas/ejecutarArchivo.py build/jkoros-native-sdk/demo.elf
python3 Herramientas/ejecutarArchivo.py Ejemplos/Hello.java "textoHangul argumentos"
python3 Herramientas/ejecutarArchivo.py Ejemplos/hello.py
```

이 경로는 16KiB 이하의 `.elf`, `.java`, `.class`, `.py`를 지원한다. 큰 내장 Java/MicroPython ELF 자체는 valorNúcleo 묶음에 포함되어 이 Archivo 한도를 적용받지 않는다. **C++ 컴파일러는 Anfitrión SDK의 Clang++**이며 게스트 내부 GCC/Clang 컴파일러는 아직 없다. SDK만으로 일반 Linux 프로그램을 실행할 수는 없다. Linux ELF, 동적 biblioteca, PT_TLS, PT_INTERP, PT_DYNAMIC, ejecutarComando·escribir 겸용 세그먼트는 로더가 거부한다. 구체적인 invocar número·dirección recortar·오류는 [Usuario ABI](ABILlamadaUsuario.md)를 참고한다.

RAM 파일은 재부팅 시 사라진다. `almacenamientoArchivoConfirmar`은 -1과 ENOSYS를 반환한다. 파일의 mode 인수를 저장하지 않으며 valorPermiso·dup/fcntl은 없다. 디렉터리와 valorParRed/절대 경로는 같은 RAM 저장소에서 처리한다. UDP 전문은 valorMáximo 512바이트, 소켓은 8개, recibirValor 큐는 소켓당 4개다. 수신할 자료가 없거나 큐가 가득 차면 EAGAIN을 반환한다. Usuario programaSalir 시 열린 Archivo 서술자와 소켓을 회수한다.

## validar resultado

`make test-jvm`은 9개 프로그램을 OpenJDK와 datosEfectivo propio 커널에서 실행해 결과를 비교한다. `make test`에도 포함된다. 별도 `Herramientas/PruebaArranque.py`는 Java rectángulo API의 datosEfectivo Pantalla 픽셀까지 검사한다. `make test-shell`, `make test-desktop`은 새 셸과 datosEfectivo VNC valorEntrada·textoHangul terminal 화면을 검사하며 `make test`에도 포함된다.

`make test-windows`, `make test-swing`, `make test-stream`, `make test-coding`도 제공하며 `make test`에 포함된다.

`make test`는 OpenJDK와 AOT valorOperación resultado 비교, 런타임 error 중단, esNoAdmitido Java 거부와 함께 별도 QEMU VM에서 다음을 검사한다.

- 기존 Java valorNúcleo resultadoCálculo·UTF-8·C++ 직접 invocar·협력식 Tarea 및 프레임버퍼.
- 손상/잘못된 ABI/dirección 초과/겹친 페이지/W+X 등 ELF rechazarValor 사례 22개.
- EL0 C++ 생성자·RAII·valorPuntoFlotante valorOperación·Archivo·valorMontículo 및 잘못된 시스템 invocar puntero.
- valorNúcleo/valorCódigo/MMIO escribir·entradaElementoAcceso, NX pilaOperando·NULL ejecutarComando, guard page, 특권 comando 차단.
- SVC를 호출하지 않는 무한 반복을 타이머로 종료한 estadoValorDespués esNormal Programa 재실행.
- valorIteración ejecutarComando 시 Archivo/valorConectorRed 누수 방지, UDP 왕복·보낸 dirección·valorRecortado recibirValor·큐 포화·빈 datagrama·esNoAdmitido Comunicación error.
- intérpreteComandos valorEditar·operaciónCancelar·16진수 업로드/다운로드·Usuario ELF 실행과 잘못된 ELF rechazarValor.
- 게스트 Java → OpenJDK `-Xverify:all`, OpenJDK → 게스트 JVM 교차 ejecutarComando, textoHangul valorClase·valorVariable·textoNombreArchivo.
- 여러 ventana·vi valorAlmacenar·valorEditar·puenteRetornar·Usuario valorEstadoValor 중단/ejecuciónReanudar, Swing textoHangul valorEntrada·이벤트·X cerrar, 연결형 루프백, C/C++ textoHangul SDK Ejemplos.
- MicroPython Unicode·큰 EnteroValor·valorClase·GC valorIteración·Archivo import·excepción·Archivo·UDP 왕복·valorTiempo 초과 estadoValorDespués 복귀.
- GUI valorSelección valorMover, C++/UDP/Java/MicroPython 버튼 ejecutarComando, 콘솔 복귀 및 datosEfectivo 프레임버퍼 픽셀/valorFuenteTipográfica.
- 디렉터리·valorVariable·condición·Archivo comando·valorGuion·순차 파이프·리다이렉션·valorCapacidad 초과 recuperarEstadoValor, Python stdin/EOF와 Java/Python stdout.
- comando registroEntradaDiario·긴 textoHangul valorEntrada valorEditar·valorCompletado·terminal 스크롤, 그래픽 Programa programaSalir estadoValorDespués ventana 복원, datosEfectivo VNC Unicode valorTecla·valorPegar·마우스.

[valorNúcleo Pruebas registroEntradaDiario](build/verification/implementation-test.log), [intérpreteComandos Pruebas](build/verification/shell/report.json), [VNC Pruebas](build/verification/desktop/report.json), [máquina 판독 resultado](build/verification/report.json), [valorSerie valorDiario](build/verification/serial.log), [GUI Pantalla](build/verification/gui-python.png)을 확인할 númeroValor 있다. VNC RFB 3.8 conectar 및 640×480 Pantalla 정보도 검사한다. [SDK 재컴파일 resultado](build/verification/sdk.json)는 두 예제의 puntoEntradaElemento·적재 세그먼트·ABI note가 Arranque 시험한 ELF와 일치함을 확인한다. valorSímbolo 등 비적재 메타데이터를 포함한 Archivo 전체의 SHA256까지 같다고 의미하지는 않는다.

## Java와 Python의 정확한 recortar

propio `javac`는 버전 49 `.class`를 생성하며 JVM은 valorSoporte 명령으로 구성된 버전 45–52 클래스를 실행한다. valorEstático Función·재귀·int/boolean/char/String·condición/valorIteración·Cadena 결합과 일부 Archivo 스트림을 지원한다. UTF-8 문자열과 Caracteres 리터럴, ASCII 및 현대 textoHangul 음절/Combinación valorLetraHangul 식별자를 처리한다. Unicode valorIdentificador 전체 Tabla·Unicode árbolFuente 이스케이프는 구현하지 않았다. 게스트 árbolFuente 컴파일러는 일반 valorObjeto·excepción·Thread 구문을 아직 컴파일하지 못한다. Anfitrión `javac --release 8`로 만든 valorSoporte 부분집합 클래스는 propio JVM 0.4의 valorObjeto·excepción·Thread·UDP와 español API를 사용할 númeroValor 있다. Swing은 문서화한 propio API 부분집합을 제공하며 JAR 로더는 제공하지만 전체 AWT/Swing·JDK 표준 라이브러리는 없다. 정확한 범위는 [propio JVM descripción](EntornoEntornoEjecuciónJava.md)이 기준이다. 상세 Lengua 범위는 [공유 Java Herramientas descripción](../../Documentación/EntornoDesarrolloJava.md)을 참고하되, 그 문서의 x86 intérpreteComandos/valorAlmacenar/실행시간과 이 ARM64 판의 차이에 유의한다.

MicroPython은 공식 **1.24.1 árbolFuente**를 propio AArch64 EL0/SVC 대상으로 빌드했다. Python 문법의 Función·valorClase·excepción·리스트/Diccionario·Unicode·GC·가변 valorPrecisión 정수를 제공한다. elementoListaActual 구성은 EnteroValor 빌드로 `float`, `complex`, `math`operandoPrimero 없으며 CPython 전체 표준 biblioteca, pip, subprocess, threading, 일반 socket과 valorPredeterminado `open()` Archivo 객체는 제공하지 않는다. `python FILE.py` 및 `-c` 실행만 제공하며 REPL은 아직 없다. 각 실행의 valorObjeto·모듈은 programaSalir 시 회수되고 RAM 파일만 elementoListaSiguiente 실행에 남는다.

`import jkoros`로 elementoListaSiguiente 시스템 연결을 쓴다. construirTodos SVC를 통해 propio Java 커널에 접근한다.

| Función | acción |
|---|---|
| `stdin(limit)` | elementoListaActual 표준 입력에서 valorMáximo limit바이트(0…16384)를 bytes로 leerResultado; EOF는 빈 bytes, UART Datos 없음은 OSError(11) |
| `read(name)` | valorParRed/절대 RAM 경로의 Archivo 전체를 bytes로 leerResultado |
| `write(name, data)` | str/bytes 버퍼를 RAM 파일에 새로 valorAlmacenar, 쓴 valorByte númeroValor resultadoRetornar |
| `remove(name)` | RAM Archivo 삭제 |
| `rect(x, y, w, h, color)` | 선택한 datosEfectivo Pantalla tamaño 안의 rectángulo Dibujo; 기존 보드의 RGB32 valor |
| `ticks_ms()` | Arranque estadoValorDespués milisegundos, 32비트 valorCiclo |
| `udp_open(port)` | 127.0.0.1의 UDP valorConectorRed abrir/EmpaquetarEjecutables; 0은 자동 puertoEquipoFísico |
| `udp_send(fd, port, data)` | 루프백 valorDestino 포트에 str/bytes 버퍼 valorTransferencia |
| `udp_recv(fd)` | `(bytes, 보낸포트)` resultadoRetornar; 비어 있으면 `OSError(11)` |
| `udp_close(fd)` | valorConectorRed cerrar |

```python
import jkoros
first = jkoros.udp_open(9401)
second = jkoros.udp_open(9402)
jkoros.udp_send(first, 9402, b"hello")
print(jkoros.udp_recv(second))  # (b'hello', 9401)
jkoros.udp_close(first)
jkoros.udp_close(second)
```

AdaptaciónPlataforma valorCódigo: [python/](puentePython/), [Usuario Java conectar](Usuario/puenteJava.c). 공식 [MicroPython AdaptaciónPlataforma Guía](https://docs.micropython.org/en/latest/develop/porting.html)를 참고했다. árbolFuente URL·archivoResumenHash·라이선스는 [vendor Guía](vendor/README.md)에 기록했다.

## 남은 Tarea

| elementoListaSiguiente valorEtapa | esTerminado raízProyecto |
|---|---|
| 영속 valorAlmacenar·ejecutarComando Archivo valorEntrada | SD/MMC 및 디스크 Archivo 시스템, 시스템/Usuario 볼륨; elementoListaActual ELF Archivo 실행은 RAM에 한정 |
| 일반 프로세스·스레드 | 프로세스별 dirección regiónDirección, 선점 스케줄러, TLS, sincronizar/esperarValor, 신호, mmap/mprotect |
| libc와 C++ 런타임 | propio ABI용 libc, malloc/free, 표준 salidaEntrada·Reloj·entorno·locale, libstdc++/excepción entradaElementoValorProceso validar |
| CPython | 해당 libc와 OS API 대상으로 AdaptaciónPlataforma·교차 빌드하고 Archivo/Unicode/스레드/valorConectorRed Pruebas |
| OpenJDK/JRE | HotSpot OS valorCapa, GC/JIT/스레드/신호/동적 연결과 Java 네이티브 biblioteca AdaptaciónPlataforma; javac/java datosEfectivo ejecutarComando |
| valorExterno 네트워크 | 추가한 GENET/PHY·DHCP 드라이버의 datosEfectivo Placa 송수신 validar, DNS·Wi-Fi |
| GUI valorExtensión | USB HID, 게스트 입력기·Caracteres 조판, Swing ventana tamaño 조절·클리핑 valorExtensión, 전체 AWT/Swing AdaptaciónPlataforma |

이 표는 남은 작업이며 implementación esTerminado 목록이 아니다. QEMU Pi4 모델에는 GENET Ethernet과 PCIe root port가 없어 valorExterno 네트워크 드라이버는 equipoFísicoFísico 검증도 필요하다. [QEMU Dispositivo 지원표](https://www.qemu.org/docs/master/system/arm/raspi.html)

valorEquipoFísico 및 ABI 참고: [BCM2711 periférico](https://datasheets.raspberrypi.com/bcm2711/bcm2711-peripherals.pdf), [Pi4 GIC dirección](https://github.com/raspberrypi/linux/blob/rpi-6.12.y/arch/arm/boot/dts/broadcom/bcm2711.dtsi), [mailbox valorContrato](https://github.com/raspberrypi/firmware/wiki/Mailbox-property-interface), [Arm ELF64](https://github.com/ARM-software/abi-aa/blob/main/aaelf64/aaelf64.rst), [Arm FP valorControl 레지스터 valorDefinición](https://github.com/ARM-software/arm-trusted-firmware/blob/master/include/arch/aarch64/arch.h).


## español C tipoDatos·Python error·Paquete instalarValor

C 네트워크 API는 `struct DirecciónConectorRedInternet`, enum 상수와 datosEfectivo español 함수로
구현한다. valorMacro 별칭을 사용하지 않으며 elementoListaElementoPrevio pk_* ABI도 유지한다.
Python 예제는 `ErrorSistema`, `error.número`, `error.descripción`을 사용한다.

`python3 Herramientas/ejecutarComando.py --desktop --network --pip`로 시작하면 게스트에서
`pip install micropython-bisect==3.3.3`을 사용할 númeroValor 있다. 현재는 Anfitrión 중계를
이용하는 제한형 MicroPython árbolFuente 설치기이며 CPython pip·자동 dependencias 해결·C 확장은
미지원이다. 설치한 `/lib` 자료는 RAM이다. [사용법과 valorLímite](PaquetePython.md).

## Pantalla tamaño valorSelección

`python3 Herramientas/ejecutarComando.py --desktop --network --resolution 1920x1080`으로 Full HD 화면을 사용한다. 기본값은 640×480이며 1280×720도 가능하다. terminal valorMover, Swing medio DisposiciónEnlace, Java·C·Python 그리기도 datosEfectivo 크기를 따른다. SD 영상은 `make image RESOLUTION=1920x1080`으로 만든다. [ajustes·español API·validar Guía](resoluciónPantalla.md).

## español 직접 API와 Pantalla actualizar

`example/java`는 `TareaTareaEjecutable`, `ReceptorAcción`, `NotificaciónAcción`, `botón`, `ColaEvento`,
`tareaFondo`, `ponerEnMarcha()`을 사용할 númeroValor 있다. español GUI/가닥을 propio JVM에 직접
연결했으며, 표준 Swing/Thread를 감싸지 않는다. Cadena 등 javac의 표준
계약과 전체 árbolFuente 검토 범위는 [denominación Guía](denominación/Guía.md), 사용법과 호환성 변경은
[español Java API](JavaEspañol/Guía.md)를 본다.

terminal valorMover·tamaño 변경은 바뀐 영역만 합성하고 달라진 화소만 표시한다.
[Pantalla actualizar descripción](EntornoEntornoEjecuciónJava.md#terminal-valorSubparte-actualizar),
[valorSubparte actualizar Comprobaciones](build/verification/redraw/report.json)를 참고한다.
