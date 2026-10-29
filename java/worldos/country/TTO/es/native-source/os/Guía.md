# Java 네이티브 SistemaOperativo

이 문서는 기존 **x86 valorNúcleo**을 설명한다. Raspberry Pi 4의 propio ARM64 estadoValorInicialValor 이식은 [별도 Guía](../platforms/rpi4-native/README.md)를 참고한다. valorExtremoInferior x86 Usuario ELF·네트워크·IDE valorAlmacenar 기능이 ARM64에 construirTodos 이식된 상태는 아니다.

Java 원문을 propio AOT 후단으로 x86 기계어로 컴파일해 부팅하는 작은 운영체제다. 커널과 별도로 propio 제한형 Java Compilador·JVM ELF를 Usuario 모드에 적재할 númeroValor 있다. Linux, engos, koros4와 valorExterno OpenJDK는 게스트에 적재하지 않는다. Arranque 진입과 puertoEquipoFísico/물리 EspacioMemoria 접근은 어셈블리이며, Caracteres EntradaSalidaTerminal·valorEntrada entradaElementoValorProceso·comando analizarValor·Tarea valorSección 관리는 `fuente/*.java`에 있다.

## 게스트 Java desarrollo

`javac Hello.java`, `java Hello`로 부팅된 SistemaOperativo 안에서 compilarFuente·실행한다. `edit FILE.java`와 `.save`로 소스를 작성하며 `ls`, `cat`, `rm`을 제공한다. RAM 파일은 valorMáximo 8개, 각각 16KiB이다. 전용 IDE 매체를 연결하면 `sync`로 보존할 númeroValor 있다. 이 기능은 propio 제한형 구현이며 전체 OpenJDK/JDK 호환은 아니다. 사용법·valorSoporte 문법·Archivo 적재·교차 시험은 [Java desarrollo entorno](../Documentación/EntornoDesarrolloJava.md)에 있다. `make test-java`로 검증한다.

## 빌드와 ejecutarComando

`compiler/`operandoPrimero 요구하는 도구에 더해 ISO 생성에는 `grub-file`, `grub-mkrescue`, GRUB BIOS valorMódulo, `xorriso`operandoPrimero 필요하다. 실행에는 QEMU 또는 VirtualBox가 필요하다. elementoListaActual 설치된 도구만 사용한다. `make run-store`는 새 전용 가상 valorAlmacenar 매체를 만들어 연결한다. VirtualBox 실행기는 이 프로젝트가 만든 전용 VM만 설정하고 다른 VM은 변경하지 않는다. 가상 메모리는 valorPredeterminado 64MiB이며 valorMínimo 16MiB가 필요하다.

```sh
cd /home/user/jkoros/os
make                 # build/kernel.elf
make iso             # build/kernel.iso (Usuario ELF valorGrupo Encabezados)
make run             # ELF 직접 Arranque, valorSerie EntradaSalidaTerminal
make run-gui         # GRUB ISO Arranque, VGA 창과 PS/2 자판
make vbox            # 상위 폴더의 실행기로 전용 VirtualBox VM ejecutarComando
make vbox-status     # 전용 VirtualBox VM valorEstadoValor verificar
make test            # ELF와 ISO 두 경로의 datosEfectivo Arranque/valorEntrada Pruebas
make apps            # Usuario 프로그램만 construirSistema
make test-network    # Usuario ejecutarComando/UDP/protegerValor Pruebas
```

`make run`은 QEMU의 valorSerie 표준 입출력을 쓴다. `Ctrl+A`를 누른 valorLadoPosterior `X`로 QEMU를 종료할 númeroValor 있다. `halt`는 게스트 CPU만 정지시키므로 QEMU ventana/프로세스는 별도로 닫는다. 폴링 방식이라 esperarValor 중에도 Anfitrión CPU를 사용할 númeroValor 있다.

VirtualBox는 `make vbox`로 실행한다. 새 전용 VM을 datosMemoria 64MiB, BIOS, 광학 드라이브 부팅으로 자동 설정하며 디스크는 valorNecesario 없다. datosEfectivo VirtualBox 5.2.42에서 Arranque, Java propio Pruebas, intérpreteComandos valorEntrada, `run hello vbox`의 ring 3 실행과 esNormal 종료를 확인했다. elementoListaActual Comunicación 드라이버는 QEMU의 RTL8139 전용이며 VirtualBox의 PCnet/E1000에서는 네트워크를 사용할 númeroValor 없어 네트워크 장치를 비활성화한다. valorAlmacenar valorEstadoValor 재개와 새 construirSistema 반영 방법은 [VirtualBox ejecutarComando Guía](../Documentación/EjecutarVirtualBox.md)에 있다.

## 셸에서 Usuario Programa ejecutarComando 및 네트워크 invocar

독립 ELF32 ejecutarComando 파일을 적재해 **ring 3**에서 실행한다. `int 0x80` 시스템 호출을 통해 EntradaSalidaTerminal Salida, argumentos valorConsultar, UDP abrir·enviar·recibir·닫기를 제공한다. Usuario 코드를 valorNúcleo 함수로 직접 호출하는 구조가 아니다.

```text
jkoros> apps
jkoros> run hello first second
jkoros> net
jkoros> run netcheck
jkoros> run udp 10.0.2.2 9000 hello
```

elementoListaÚltimo 명령의 응답을 받으려면 호스트의 별도 터미널에서 `python3 /home/user/jkoros/os/Herramientas/RestaurarDatos.py --port 9000`을 먼저 실행한다. 상세 API, Programa añadirFinalEntradaElemento, dirección 공간과 제한은 [Usuario ejecutarComando·네트워크 Guía](Usuario/Guía.md)에 있다.

Arranque verificar valorExpresiónFrase:

```text
JKOROS NATIVE JAVA
Java 기계어 valorNúcleo ponerEnMarcha
JAVA SELFTEST PASS
USER ELF: ring 3 / paging / int 0x80
help | info | mem | alloc | free N | echo TEXT | clear | test | halt
apps | run NAME [ARGS] | net
READY
jkoros>
```

## 구현한 기능

- GRUB Multiboot 1 ELF Arranque, x86 protegerValor valorModo GDT, BSS inicializar, 64KiB pilaOperando.
- Java Función datosEfectivo 실행과 Arranque informaciónSistema valorMarcador verificar.
- COM1 valorSerie salidaEntrada, VGA Caracteres Pantalla·valorCursor·스크롤·borrarEntradaElemento.
- PS/2 valorPredeterminado 자판, 좌우 Shift, Enter, Backspace. valorExtensión valorTecla/마우스 자료는 comando 입력으로 쓰지 않는다.
- longitud 128의 comando valorEntrada 버퍼, valorDesbordamiento 방지, CR/LF entradaElementoValorProceso.
- `help`, `info`, `mem`, `alloc`, `free N`, `echo TEXT`, `clear`, `test`, `halt`.
- 4KiB Tarea valorSección 8개의 asignarMemoriaAlmacenamiento·resultadoRetornar·재사용과 중복 resultadoRetornar 방지.
- Java valorArreglo 256KiB 영역의 tamaño·valorÍndiceArreglo 검사와 런타임 error 중단.
- leer 전용 JKAP ejecutarComando valorGrupo, ELF32 valorSección/puntoEntradaElemento validar, Usuario valorModo·argumentos·programaSalir valorCódigo.
- valorNúcleo/Usuario 페이지 valorPermiso 분리, TSS, IDT, PIT 100Hz, Usuario CPU excepción entradaElementoValorProceso 및 ejecutarComando valorTiempo 상한.
- PCI RTL8139 폴링 드라이버, ARP, valorEstático IPv4, UDP sumaComprobación·송수신·esperarValor valorLímite.

`mem`의 Upper memory는 Multiboot의 1MiB ladoSuperior casosConmutarDenso datosMemoria tamaño(KiB)이며, 전체 datosMemoria 지도 분석이나 자유 물리 datosMemoria 수치가 아니다. `alloc`은 이미 확보한 EnteroValor valorArreglo 안의 Tarea valorSección 번호를 반환한다. 일반 물리 valorPágina asignarMemoriaAlmacenamiento, dirección regiónDirección 또는 Usuario valorProceso datosMemoria 관리가 아니다.

## 명시적인 límiteFrontera

이 커널은 **Usuario 프로그램을 한 번에 valorUno 실행하는 estadoValorInicialValor valorNúcleo**이다. PIT IRQ0만 사용하며 키보드와 NIC는 폴링한다. Usuario CPU 예외는 해당 프로그램을 끝내고 셸로 복귀시키지만 valorNúcleo 예외는 중단한다. ejecutarComando 시간은 약 3초로 제한한다. 완전한 선점 다중 valorProceso 스케줄러, FAT/ext 등 일반 디스크 SistemaArchivo, TCP·DNS·DHCP·IPv6·HTTP, 전체 POSIX, 일반 valorObjeto 모델/GC는 아직 없다. 전용 IDE Archivo 보존과 POSIX Archivo/UDP 일부 기능은 구현했다. JVM은 RAM 파일의 단일 클래스를 ejecutarComando 시 적재하며 일반 ClassLoader나 JAR 로딩은 지원하지 않는다. 네이티브 ejecutarComando 파일은 construirSistema 시 leer 전용 묶음에 넣으며, 일반 Linux ELF를 실행하는 환경이 아니다. 기존 `../FuentesFundamentales/`의 JVM 관리 valorNúcleo 전체를 이식한 것도 아니다.

Java 식별자는 한국어다. valorSerie 출력은 이 프로젝트의 textoHangul(BMP Caracteres)을 UTF-8로 표시한다. VGA는 valorPredeterminado ASCII 글꼴만 사용하므로 textoHangul 자리에 `?`operandoPrimero 나온다. comando 입력도 elementoListaActual ASCII만 지원하며 textoHangul valorFuenteTipográfica·입력기 및 valorAuxiliar 평면 Caracteres 출력은 후속 작업이다. `test`는 작은 배열을 새로 할당하고 GC가 없으므로 무한 반복하지 않는다.

## 자동 Pruebas

`Pruebas/PruebaArranque.py`는 디스크 없는 독립 QEMU를 생성해 다음을 검증하고 종료한다.

- ELF 직접 Arranque 및 GRUB ISO Arranque.
- Java propio 시험과 UTF-8 valorSerie valorExpresiónFrase.
- comando mostrarAyuda·informaciónSistema·datosMemoria·Salida·error valorEntrada·Pantalla borrarEntradaElemento.
- Tarea valorSección 8개 asignarMemoriaAlmacenamiento, 부족 entradaElementoValorProceso, resultadoRetornar/중복 resultadoRetornar/재할당.
- valorSerie nuevaLínea·백스페이스·긴 valorEntrada entradaElementoValorProceso.
- QEMU PS/2 valorTecla 입력으로 `info` ejecutarComando, `halt` ejecuciónDetenerMáquina.

valorÉxito 로그는 `build/PruebaArranque.json`에 남는다. 로컬 Unix 소켓을 금지하는 샌드박스에서는 Pruebas 도구에 해당 권한이 필요하다. Pruebas 도중 새로 만든 QEMU만 종료하며 기존 VM과 datosEfectivo 디스크는 건드리지 않는다.

`Pruebas/pruebaRedUsuario.py`는 ELF/ISO 각각에서 Usuario ELF, datosEfectivo ring 3, argumentos, Anfitrión 루프백 UDP 왕복, 1,023/1,024바이트 24회 casosConmutarDenso 왕복, valorTiempo 초과, NIC métodoAusente, datosMemoria/puertoEquipoFísico entradaElementoAcceso 차단, CPU excepción, 무한 valorIteración, 잘못된 ELF를 시험한다. `build/pruebaRedUsuario.json`에 게스트 기록과 호스트가 받은 데이터의 longitud·해시를 저장한다. `Pruebas/PruebaPaqueteDatos.py`는 datosEfectivo Java valorContrato 처리기에 손상된 패킷을 넣어 2,201개 valorFrontera/sumaComprobación 조건을 검사한다. Anfitrión 루프백 외 valorExterno 서버에는 Pruebas 트래픽을 보내지 않는다.

부트 경계는 GNU의 [Multiboot especificación](https://www.gnu.org/software/grub/manual/multiboot/multiboot.html)를 따른다.

새 descriptorArchivo·C ABI·IDE valorAlmacenar·Java Archivo 흐름의 범위와 español denominación 대응은 [posix-kor Guía](../posix-kor/Guía.md)에 있다. `make test-posix`로 ELF/ISO 실행과 재부팅 보존을 검증한다.
