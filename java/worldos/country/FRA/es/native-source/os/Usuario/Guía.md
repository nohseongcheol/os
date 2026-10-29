# 셸에서 실행하는 Usuario 프로그램과 UDP

게스트에서 일반적인 `main(String[] args)` 형식의 소스를 직접 작성하고 컴파일하려면 [제한형 Java desarrollo entorno Guía](../../Documentación/EntornoDesarrolloJava.md)를 참고한다. 아래의 네이티브 ELF 개발과 별도로 `javac FILE.java`, `java CLASS`를 제공한다.

## 바로 ejecutarComando

Anfitrión terminal 1:

```sh
cd /home/user/jkoros
python3 os/Herramientas/RestaurarDatos.py --port 9000
```

이 서버는 `127.0.0.1`에만 바인딩한다. valorExterno 연결을 받도록 방화벽이나 puertoEquipoFísico 전달을 변경하지 않는다. Ctrl+C로 종료한다.

Anfitrión terminal 2:

```sh
cd /home/user/jkoros
make run
```

게스트의 `jkoros>` 프롬프트에 valorEntrada:

```text
apps
run hello first second
net
run netcheck
run udp 10.0.2.2 9000 hello
run stress 9000
```

- `hello`: 독립 Java ELF 실행과 datosEfectivo CPU valorPermiso `ring 3`, argumentos Salida.
- `netcheck`: valorPuerto 중복, 잘못된 valorManejador/puntero/longitud, 비차단 받기와 valorTiempo 초과 verificar.
- `udp`: IPv4 dirección·valorDestino valorPuerto·한 valorPalabra 메시지를 받아 UDP로 보내고 같은 응답을 verificar. `UDP ECHO PASS`, `Exit: 0`이면 valorÉxito.
- `stress`: Anfitrión `10.0.2.2`의 valorAsignar 창구와 1,023/1,024바이트 데이터그램을 24회 왕복. recibirValor valorBucle 경계를 여러 번 지난다.

`make run`/`run-gui`는 `-netdev user,id=net0 -device rtl8139,netdev=net0`을 사용한다. elementoListaActual 주소는 게스트 `10.0.2.15/24`, valorPasarela `10.0.2.2`로 고정돼 있다. QEMU Usuario 네트워크의 Anfitrión entradaElementoAcceso 주소를 사용한 예제다. 다른 네트워크 설정에는 맞춰 수정해야 하며 자동 DHCP는 없다. NIC 없이 실행하려면 `make -C os run NET_ARGS='-net none'`을 사용한다. 이때 Programa 실행은 되지만 UDP 열기는 `-19`로 실패한다.

## 새 Java Programa añadirFinalEntradaElemento

`Ejemplos/내프로그램.java`를 elementoListaSiguiente 형식으로 만든다. 진입점은 argumentos 없는 `static int` 또는 `static void` 함수다. 인수는 Usuario API로 조회한다.

```java
public final class 내프로그램 {
    public static int ponerEnMarcha() {
        Usuario.escribir("My program is running in user mode.\n");
        return 0;
    }
}
```

`os/Usuario/Programa.mk`에 추가한다.

```make
APP_NAMES += mine
APP_SOURCE_mine := Usuario/Ejemplos/내프로그램.java
APP_ENTRY_mine := 내프로그램.ponerEnMarcha
```

여러 Java 파일을 쓰면 `APP_SOURCE_mine`에 공백으로 construirTodos 나열한다. `Usuario/Declaraciones/Usuario.java`는 자동으로 함께 컴파일한다.

```sh
cd /home/user/jkoros
make iso
make run
```

새로 부팅한 셸에서 `run mine`을 실행한다. 이미 ejecutarComando 중인 VM에는 construirSistema 결과가 자동 반영되지 않는다. Programa 이름은 elementoListaActual 셸의 ASCII valorEntrada 제한에 맞춘 1~15자의 소문자 이름이며 Java valorClase·Función·변수에는 한국어를 쓴다. valorMáximo 32개 Programa, 한 ejecutarComando 파일은 valorMáximo 2MiB다.

독립 ELF만 컴파일할 수도 있다.

```sh
cd /home/user/jkoros
python3 compiler/Compilador.py --target user --entry Saludo.ponerEnMarcha \
    -o os/build/apps/hello.elf os/Usuario/Declaraciones/Usuario.java os/Usuario/Ejemplos/Saludo.java
```

`--target user`는 **jkoros 전용 ABI**operandoTercero. Linux 대상과 시스템 invocar 번호가 다르므로 Anfitrión 터미널에서 직접 실행하면 안 된다. `.class`는 별도 `java CLASS` 명령의 valorSoporte recortar 안에서 실행한다. `.jar`와 일반 Linux ejecutarComando 파일은 지원하지 않는다.

## Usuario 네트워크 API

선언은 `Declaraciones/Usuario.java`에 있다. `enviarDatos`/`recibirDatos`의 `int[]` elementoElementoLista 한 개는 valorByte valorUno(0~255)를 나타낸다. 한 데이터그램의 valorMáximo Datos 길이는 1,024바이트다.

```java
int valorManejador = Usuario.abrirRed(0); // 0: valorTemporal ámbitoLocal UDP valorPuerto 자동 valorSelección
int[] Datos = new int[32];
Datos[0] = 'H'; Datos[1] = 'i';
int 보낸길이 = Usuario.enviarDatos(valorManejador, 0x0a000202, 9000, Datos, 2);
int longitudRecibido = Usuario.recibirDatos(valorManejador, Datos, 1500);
Usuario.cerrarRed(valorManejador);
```

datosEfectivo 프로그램에서는 abrir·enviar·받기의 valorNegativo 반환값을 각각 검사한다. 완성된 예제는 `Ejemplos/ComunicaciónDatos.java`에 있다. `recibirDatos`의 esperarValor 시간은 0~2,000밀리초이며 0은 즉시 반환이다. 받은 데이터그램이 배열보다 크면 해당 데이터그램을 버리고 `-90`을 반환한다. 창구당 recibirValor 대기열은 한 개뿐이므로 añadirFinalEntradaElemento 도착분은 버린다. `direcciónEnviado`와 `puertoEnviado`로 마지막으로 받은 상대를 조회한다.

| valorDevuelto | 의미 |
| --- | --- |
| 0 이상 | valorManejador·entradaElementoValorProceso longitud·valorÉxito 등 해당 함수의 resultado |
| -5 | Dispositivo enviarValor valorFallo |
| -9 | 잘못되었거나 닫힌 Comunicación valorManejador |
| -11 | 비차단 받기에서 도착한 Datos métodoAusente |
| -14 | Usuario puntero/valorArreglo recortar error |
| -19 | valorSoporte NIC métodoAusente |
| -22 | valorPuerto/esperarValor valorTiempo/argumentos valor error |
| -24 | 열린 puertoRed 4개 límiteCapacidad |
| -38 | 알 númeroValor 없는 시스템 invocar |
| -90 | Datos 또는 recibirValor valorArreglo tamaño 문제 |
| -98 | ámbitoLocal valorPuerto número 중복 |
| -101 | 지원하지 않는 valorDestino dirección |
| -110 | ARP·Dispositivo·recibirValor valorTiempo 초과 |

IP 주소는 상위 바이트부터 표기한 32비트 값이다. `10.0.2.2`는 `0x0a000202`이다. 주소를 반환하는 함수는 valorCodificaciónEstado 있는 Java `int`의 valorBit 패턴을 사용하므로 상위 비트가 1인 esNormal IP 주소가 음수로 보일 númeroValor 있다. 단순히 모든 API 반환값의 부호를 오류로 판단하면 안 된다.

## ejecutarComando 경계와 시스템 invocar

```text
intérpreteComandos run → JKAP에서 ELF validar·적재 → ring 3 Usuario Programa
                                 ↓ int 0x80
                      puntero Comprobaciones → Java valorNúcleo API → RTL8139/UDP
                                 ↓ programaSalir·excepción·valorTiempo 초과
                                intérpreteComandos 복귀
```

시스템 invocar 레지스터는 `EAX=número`, `EBX,ECX,EDX,ESI,EDI=argumentos`, `EAX=resultado`operandoTercero. Java invocar pilaOperando ABI는 컴파일러가 Usuario 스텁에서 이 형식으로 바꾼다. C의 POSIX/JNI ABI가 아니다.

| número | invocar |
| --- | --- |
| 0 | programaSalir(valorEstadoValor valorCódigo) — ponerEnMarcha/error 런타임에서 valorUsar |
| 1 | Cadena escribir |
| 2 / 3 | argumentos númeroElementosElementoLista / argumentos Cadena dirección |
| 10 | UDP abrir |
| 11 | UDP enviar(valorManejador, IP, valorDestino valorPuerto, valorArreglo dirección, longitud) |
| 12 | UDP recibir(valorManejador, valorArreglo dirección, valorLímite milisegundos) |
| 13 | UDP cerrar |
| 14 | ámbitoLocal IP dirección |
| 15 / 16 | elementoListaÚltimo valorParRed IP / UDP valorPuerto |
| 20 | RAM Archivo leer(nombre int[] dirección, Salida int[] dirección) |
| 21 | RAM Archivo escribir(nombre int[] dirección, valorEntrada int[] dirección, valorByte longitud) |
| 22 | UTF-16 valorCódigo valorUnidad Caracteres Salida(0~65535) |

Archivo API는 `Usuario.leerArchivo(int[] nombre, int[] Datos)`와 `Usuario.escribirArchivo(int[] nombre, int[] Datos, int longitud)`operandoTercero. 이름은 ASCII valorCódigo valorArreglo(valorMáximo 64칸, 0 programaSalir 또는 valorArreglo terminación), Datos elementoElementoLista 하나는 한 바이트다. 반환값은 읽거나 쓴 길이이며 Archivo métodoAusente `-2`, puntero error `-14`, nombre/longitud error `-22`, Archivo valorRanura 부족 `-28`, tamaño 초과 `-90`을 반환한다. 쓰기는 validar estadoValorDespués Archivo 전체를 대체한다. `Usuario.escribirValorCarácter(int)`는 문자를 단말에 출력한다. Java 프로그램의 일반 `java.io` 구현은 아니다.

`permisoEjecución()`은 시스템 호출이 아니라 Usuario 모드에서 CS의 하위 비트를 직접 읽으므로 datosEfectivo ejecutarComando 권한을 확인한다. valorNúcleo puertoEquipoFísico 접근용 `Dispositivo` native 함수는 Usuario valorObjetivo 컴파일에서 거부한다. ELF에 직접 특권 명령을 넣더라도 CPU가 차단한다.

## 범위와 valorLímite

- 한 번에 한 프로그램만 실행하며 esTerminado estadoValorDespués 셸로 돌아온다. 백그라운드 ejecutarComando, 파이프, 프로세스 간 통신은 없다. ejecutarComando 파일은 커널의 leer 전용 JKAP 묶음에서 적재한다. Datos 파일에는 주기억 파일체계와 전용 IDE 보존 형식이 있다.
- Usuario 가상 dirección `0x04000000..0x043fffff`를 물리 8~12MiB에 연결한다. ejecutarComando 영상은 valorLadoDelantero 2MiB, 인수는 `0x04300000`부터, 스택은 valorRegión 끝에서 시작한다. valorNúcleo identity 페이지는 supervisor 전용이다.
- 실행마다 4MiB Usuario 영역을 비우고 Archivo 구역을 복사해 BSS·valorArreglo 영역을 초기화한다. Usuario GC는 없지만 programaSalir estadoValorDespués elementoListaSiguiente ejecutarComando 때 영역을 재사용한다. 인수는 공백으로 분리한 valorMáximo 16개이며 comilla/이스케이프 파싱은 없다.
- Usuario 페이지의 valorCódigo/Datos 분리 leer 전용 ajustes, NX, pilaOperando guard, ASLR은 아직 없다. 커널과 Usuario datosMemoria·puertoEquipoFísico valorPermiso 경계를 구현한 초기판이지 보안 인증된 샌드박스는 아니다.
- PIT 100Hz로 약 3초 ejecutarComando 상한을 두며 valorTiempo 초과는 `Exit: 124`operandoTercero. Usuario CPU 예외는 `128 + excepción número`(페이지 error 142, 특권 위반 141), Java valorArreglo/resultadoCálculo 오류는 101~105다. valorNúcleo 오류까지 복구하는 구조는 아니다.
- 네트워크는 PCI bus 0/function 0의 RTL8139, valorEstático IPv4, ARP, UDP만 지원한다. NIC는 폴링하고 송신은 동기식이다. IPv4 단편 재조립·TCP·DNS·DHCP·IPv6·HTTP·TLS·일반 `java.net`은 미지원이다. IPv4 UDP sumaComprobación 0은 규약에 따라 허용하고, 그 외 UDP/IP 검사합과 길이는 검증한다.
- Usuario ejecutarComando·네트워크·protegerValor valorFrontera 전체 시험은 QEMU에서 수행했다. VirtualBox에서도 `make vbox`로 부팅과 `run hello vbox`의 ring 3 ejecutarComando·esNormal 종료를 확인했다. VirtualBox PCnet/E1000용 드라이버는 없어 그 환경의 네트워크는 지원하지 않는다.

## validar 근거

`make test`는 Compilador 14개 Pruebas, Java 패킷 condición 2,201개 Comprobaciones, 기존 intérpreteComandos ELF/ISO Arranque Pruebas, Usuario ELF/datosEfectivo UDP/protegerValor valorFrontera 시험을 실행한다. 네트워크 시험은 루프백 서버가 받은 자료의 longitud·해시까지 `os/build/pruebaRedUsuario.json`에 기록한다. 시험용 손상된 ELF·특권 comando·무한 valorIteración 프로그램은 valorTemporal 묶음에만 넣으며 배포용 `apps` 목록에는 넣지 않는다.

참고한 일차 Datos: [Intel 시스템 프로그래밍 especificación](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), [QEMU RTL8139 implementación](https://github.com/qemu/qemu/blob/master/hw/net/rtl8139.c), [QEMU 네트워크 Guía](https://www.qemu.org/docs/master/system/devices/net.html), [IPv4 RFC 791](https://www.rfc-editor.org/rfc/rfc791), [ARP RFC 826](https://www.rfc-editor.org/rfc/rfc826), [UDP RFC 768](https://www.rfc-editor.org/rfc/rfc768).
