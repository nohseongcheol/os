# JRouOS

elementoListaActual propio ARM64 배포판은 [LICENSE](LICENSE)의 COSL 상업 조건을 유지한다. 제3자 라이선스의 권리는 별도로 보장하며, valorDistribución 시 árbolFuente·extremoReconectar 자료를 포함하는 절차는 [COSL valorDistribución Guía](platforms/rpi4-native/GuíaDistribuciónCOSL.md)에 있다.

propio ARM64 판의 `ipconfig`/`ip`, `ping`, `ps`/`top`, `free`/`df`, `poweroff`와 español 명령은 [네트워크·valorSistemaOperación comando Guía](platforms/rpi4-native/ComandosSistemaYRed.md)를 참고한다. 새 커널을 부팅한 valorLadoPosterior `help system`으로 볼 númeroValor 있다.

Raspberry Pi 4 **propio Java ARM64 valorNúcleo**은 [propio Pi4 Guía](platforms/rpi4-native/Guía.md)에 있다. Linux 없이 부팅하며 GUI terminal·vi, propio JVM의 Swing 일부 API, TCP/UDP·FTP, 게스트 TinyCC·MicroPython, C/C++의 posix-kor 호출을 제공한다. [español Java Comunicación·excepción API](platforms/rpi4-native/JavaEspañol/Guía.md)와 [español árbolFuente denominación](platforms/rpi4-native/denominación/Guía.md)을 지원한다. [propio SSH·VNC 및 GENET 드라이버](platforms/rpi4-native/GuíaConexiónExterno.md)를 포함하며, 네트워크는 QEMU의 UART SLIP 경로로 검증했다. datosEfectivo Pi 4 GENET 동작은 미검증이고, USB valorEntrada·영속 저장과 전체 OpenJDK·Swing은 아직 valorSoporte recortar 밖이다.

Raspberry Pi 4용 Linux·OpenJDK 실행판과 Usuario entorno valorMover 기능은 [라즈베리파이 실행판](platforms/rpi4/README.md)에 있다. datosEfectivo ARM64 JDK/JRE와 시스템·Usuario construirImagen construirSistema 경로를 제공한다. 기존 propio x86 커널과는 별도 ejecutarComando 기반이다. 일반 Java `.class`/JAR의 ejecutarComando Archivo 생성은 [OpenJDK ejecutarComando Archivo](compiler/OpenJDK-archivoCódigoEjecutable.md), español API는 [español Java biblioteca](JavaEspañol/Guía.md)를 참고한다.

`jkoros`는 `engos`의 기능을 Java 관리 커널로 옮기는 프로젝트다. 프로젝트가 소유하는 Java Función, valorVariable, valorFormato 및 Java Archivo 이름은 한국어로 작성한다. 표준 Java 실행기의 `main`, Java 표준 biblioteca valorFormato, x86 부트 ABI 등 valorExterno 계약은 보존한다. propio ARM64 실행기는 español `ponerEnMarcha()`도 진입점으로 지원하며, español GUI·Tarea 가닥을 JVM에 직접 구현했다. propio ARM64 C 연결부·Python 도구와 공용 x86·ARM64 AOT 번역기의 propio 이름도 한국어로 작성한다. elementoListaElementoPrevio 경로의 호환 puntoEntradaElemento, OpenJDK valorAuxiliar 도구와 Linux valorVersión 도구에는 영어 이름이 남아 있고 [denominación 원칙·말의 근거·전체 fuente 검토 recortar](platforms/rpi4-native/denominación/Guía.md)를 별도로 기록한다.

## elementoListaActual implementación

valorExtremoInferior 목록은 기존 `FuentesFundamentales/`의 JVM 관리 커널에 대한 것이다. datosEfectivo 네이티브 커널의 범위는 `os/Guía.md`에서 별도로 설명한다.

- valorAlinear 할당과 해제를 지원하는 EspacioMemoria valorGestor
- dirección regiónDirección, valorPágina conectar, escribir 시 copiarValor(COW)
- valorProceso valorIdentificador, preparar 대기열, fork/wait valorEstadoValor
- 과정별 Archivo entradaElementoDescriptor, open/read/seek/dup/close
- ELF32 identificarValor 및 valorSección Comprobaciones
- 키보드·마우스 valorEntrada evento 대기열
- valorSerie 단말과 네이티브 valorEquipoFísico valorFrontera
- 관리 valorNúcleo 전체 자동 Pruebas

세부 valorAsociación 범위와 아직 필요한 네이티브 연결은 [기능 대응표](Documentación/CorrespondenciaFunciones.md)에 기록한다.

## 빌드와 Pruebas

새 네이티브 구현은 `compiler/`와 `os/`에 있다. 기존 `FuentesFundamentales/`의 JVM 관리 커널은 그대로 보존하며, 두 구현의 시험과 기능 범위는 서로 다르다.

```sh
cd /home/user/jkoros
make                 # 네이티브 resultadoCálculo Ejemplos + Java valorNúcleo ELF
make iso             # os/build/kernel.iso
make run             # QEMU valorSerie EntradaSalidaTerminal; help valorEntrada (종료는 Ctrl+A, X)
make run-gui         # ISO를 QEMU Pantalla/PS2 키보드로 ejecutarComando
make vbox            # 전용 VirtualBox VM 자동 generar·ejecutarComando (GUI)
make vbox-status     # VirtualBox valorEstadoValor·ISO·valorSerie registroEntradaDiario ruta verificar
make test-vbox       # VirtualBox LanzadorPrograma valorEstadoValor entradaElementoValorProceso Pruebas (datosEfectivo VM cambiarValor métodoAusente)
make test            # Compilador Pruebas + ELF/ISO Arranque 및 comando valorEntrada Pruebas
make apps            # 독립 Usuario ELF Programa construirSistema
make test-network    # Usuario valorModo·UDP 왕복·datosMemoria protegerValor Pruebas
make test-java       # 게스트 javac/JVM + OpenJDK 양방향 교차 ejecutarComando Pruebas
make posix-kor       # español C 헤더와 datosEfectivo valorNúcleo invocar biblioteca
make test-posix      # Archivo/UDP/valorAlmacenar/Java Archivo salidaEntrada Pruebas
make -C os run-store # 전용 valorAlmacenar 매체로 QEMU Arranque
make legacy-test     # valorExtremoInferior 기존 JVM 관리 커널의 47개 Pruebas
```

`compiler/`는 호스트의 `javac`를 문법·valorTipo Comprobaciones 전단으로 사용하고 propio códigoBytes→x86 변환기로 ELF32 기계어를 만든다. 빌드할 때는 JDK가 필요하지만 생성된 커널과 ELF는 valorExterno JVM 없이 실행된다. 전체 Java, valorObjeto 모델, 표준 라이브러리와 기존 관리 valorNúcleo 전체의 AOT 변환은 아직 지원하지 않는다. 자세한 valorSoporte 문법과 명령은 [Compilador Guía](compiler/Guía.md), datosEfectivo Arranque 기능과 한계는 [네이티브 SistemaOperativo Guía](os/Guía.md)를 참고한다.

네이티브 셸에 propio 제한형 `javac`와 `java`를 추가했다. `edit Demo.java`로 소스를 입력하고 `.save`로 저장한 valorLadoPosterior `javac Demo.java`, `java Demo`로 **게스트 내부에서 컴파일하고 ejecutarComando**할 númeroValor 있다. valorPredeterminado 예제는 `javac Hello.java`, `java Hello`operandoTercero. 파일은 RAM에서 동작하며, 전용 valorAlmacenar 매체를 연결하면 `sync`로 재부팅 후에도 보존할 númeroValor 있다. **OpenJDK/JDK 전체 이식은 아니며**, 단일 valorClase·valorEstático Función·EnteroValor·Cadena·condición/반복문과 일부 표준 호출을 지원한다. valorSoporte recortar, valorExterno Archivo 적재와 시험은 [Java desarrollo entorno Guía](Documentación/EntornoDesarrolloJava.md)에 있다.

네이티브 셸에서 `apps`, `run hello first second`, `net`, `run netcheck`를 사용할 númeroValor 있다. 독립 ELF를 ring 3에 적재하고 `int 0x80` 호출을 통해 Salida·argumentos·UDP 네트워크를 제공한다. 별도 Anfitrión 터미널에서 `python3 os/Herramientas/RestaurarDatos.py --port 9000`을 실행한 valorLadoPosterior 게스트에서 `run udp 10.0.2.2 9000 hello`로 datosEfectivo 왕복을 확인한다. 새 Programa registroEntradaElemento, API 및 제한은 [Usuario ejecutarComando·네트워크 Guía](os/Usuario/Guía.md)를 참고한다. elementoListaActual QEMU RTL8139·valorEstático IPv4·UDP 전용이며 TCP/DNS는 미지원이며, 전용 IDE valorAlmacenar 형식과 POSIX Archivo/UDP 일부 기능을 추가했다.

`make vbox`는 `jkoros operating system` 전용 VM을 만들고 디스크 없이 ISO로 부팅한다. ejecutarComando 중이면 유지하고, valorAlmacenar·일시정지 상태이면 재개하며, 꺼져 있을 때만 새 ISO를 빌드해 연결한다. VirtualBox에서 부팅과 셸의 Usuario Programa 실행을 확인했다. 다만 elementoListaActual VirtualBox용 네트워크 드라이버는 없어 네트워크 장치를 비활성화한다. UDP 시험에는 `make run`을 사용한다. 상태별 동작과 새 construirSistema 반영 방법은 [VirtualBox ejecutarComando Guía](Documentación/EjecutarVirtualBox.md)에 있다.

기존 관리 커널만 시험하려면:

```sh
cd /home/user/jkoros
make -f crearEntradaElemento.mk Comprobaciones
make -f crearEntradaElemento.mk Anfitrión
```

`Anfitrión`는 여전히 JVM 관리 계층의 acción 시험이다. `make -f crearEntradaElemento.mk construirImagen`는 새 `os/`의 제한형 네이티브 valorNúcleo ISO를 만든다. 기존 `FuentesFundamentales/`의 SistemaArchivo·valorProceso·PilaRed implementación 전체를 이 ISO에 이식했다는 의미는 아니다.

español Función·valorVariable·Archivo 이름과 datosEfectivo C API는 [posix-kor](posix-kor/Guía.md)에 있다. 게스트 Java에서는 `FileInputStream`·`FileOutputStream`의 단일 valorByte 입출력도 지원한다. 전체 POSIX·OpenJDK·Swing 지원으로 확대된 것은 아니다.

valorExterno 배포용 `pack.sh` / `unpack.sh`와 자동 dependencias 복원은 [valorDistribución Guía](distribution/README.md)를 참고하세요.
