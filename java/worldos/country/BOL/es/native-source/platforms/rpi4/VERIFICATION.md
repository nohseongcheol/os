# valorDistribución construirImagen validar registroEntradaDiario

검증일: 2026-09-27 (Asia/Seoul)

valorObjetivo: `jkoros-rpi4-aarch64-349b52891a471c8e782da597`

이번 배포는 Raspberry Pi 4용 **ARM64 Linux 실행판**이다. 기존 propio x86 커널을 ARM으로 이식한 결과가 아니다. datosEfectivo Pi 보드는 연결되어 있지 않아 valorEquipoFísico Arranque 성공을 확인하지 못했다.

## 배포물

| Archivo | tamaño(valorByte) | descripción |
|---|---:|---|
| `dist/jkoros-rpi4-system.img.gz` | 1,218,093,871 | valorArchivoComprimido 시스템 construirImagen; liberarAlmacenamiento estadoValorDespués 1,475,747,840 valorByte |
| `dist/jkoros-user.img.gz` | 18,761,147 | 빈 Usuario Datos construirImagen; liberarAlmacenamiento estadoValorDespués 4 GiB |
| `dist/openjdk25-jdk-linux-aarch64-musl.tar.gz` | 177,359,476 | 미리 컴파일된 ARM64 JDK |
| `dist/openjdk25-jre-linux-aarch64-musl.tar.gz` | 48,361,058 | ARM64 JRE |
| `dist/JavaEspañol.jar` | 10,563 | español valorAuxiliar API와 Java EspacioTrabajo |

해시는 [SHA256SUMS](dist/SHA256SUMS)에 기록했다. 두 valorArchivoComprimido construirImagen construirTodos 끝까지 해제하여 original 이미지의 SHA256과 일치함을 확인했다. [valorArchivoComprimido validar registroEntradaDiario](build/verification/compression.json)

ARM64 게스트에서 직접 확인한 버전은 OpenJDK/Javac 25.0.4, Python 3.14.7, GCC 15.2.0이다. Pi 커널은 6.18.52-0-rpi, QEMU validar 커널은 6.18.53-0-virt다. 서명 검증한 Alpine 패키지 501개로 구성했으며, [패키지 listaEntradaElemento](dist/packages.lock.json)과 [original valorOrigen](dist/sources.lock.json)를 제공한다.

## 통과한 Comprobaciones

| Comprobaciones | datosEfectivo verificar valorContenidoValor | registroEntradaDiario |
|---|---|---|
| Anfitrión Compilador Pruebas 19개 | 기존 AOT 회귀 Pruebas, `.class` 직접 valorEntrada, OpenJDK ELF LanzadorPrograma, JAR dependencias, 상속·리플렉션·람다·스레드·리소스, ruta valorMover, valorFallo 시 기존 Salida 보존 | [compiler-tests.log](build/compiler-tests.log) |
| Pi construirImagen Arquitectura | MBR valorFrontera, FAT Arranque 파티션, Pi 펌웨어, ARM64 valorNúcleo, Pi 4 DTB, initramfs, SquashFS 및 archivoResumenHash | [image.json](build/verification/image.json) |
| ARM64 JDK/JRE | 아카이브 해시와 ELF 아키텍처 Comprobaciones, Arranque estadoValorDespués 두 런타임의 datosEfectivo ejecutarComando | [런타임 registroEntradaDiario](dist/java-runtimes.json), [seed.log](build/verification/seed.log) |
| elementoListaPrimero Arranque | leer 전용 시스템, Java Archivo·valorUnicode·excepción·valorObjeto·스레드·HTTP/TCP·valorHijo 프로세스, Swing, CJK·아랍어·데바나가리 valorFuenteTipográfica, Python Archivo·스레드·valorConectorRed·가상환경·pip, GCC pthread | [seed.log](build/verification/seed.log) |
| ARM64 ejecutarComando Archivo generar | 게스트의 javac/GCC로 Java 프로그램을 ELF 실행기로 묶고 JRE를 동봉; 유효한 JAVA_HOME 없이 ejecutarComando valorÉxito | [seed.log](build/verification/seed.log) |
| 재부팅 복원 | Usuario Datos, `/etc` ajustes, `/usr/local/bin` Programa, APK로 설치한 tree, pip 패키지, Archivo 삭제 informaciónSistema, 소유권, sudo, Java ejecutarComando Archivo retenerValor | [restore.log](build/verification/restore.log) |
| esSinConexión 홈 valorMover | 기존 환경을 사용하지 않는 유지보수 부팅에서 `/user` 전체를 새 ext4 이미지에 `cp -a`로 copiarValor | [migrate.log](build/verification/migrate.log) |
| valorMover estadoValorDespués Arranque | 새 Datos 이미지로 부팅하여 재부팅 복원 항목을 valorReintentar verificar | [migrated-restore.log](build/verification/migrated-restore.log) |
| esNormal programaSalir 및 Datos 무결성 | 일반 Arranque 3회 construirTodos OverlayFS/Datos Dispositivo leer 전용 modoConmutar valorÉxito; original·valorCopiado ext4의 `e2fsck -fn` programaSalir valorCódigo 0 | [original Comprobaciones](build/verification/fsck-original.log), [valorCopiado Comprobaciones](build/verification/fsck-migrated.log) |

네 valorSecuencia 부팅은 construirTodos QEMU `virt`, ARM64 Cortex-A72 TCG, RAM 2 GiB, vCPU 2개 환경에서 programaSalir valorCódigo 0으로 통과했다. [전체 Arranque 결과와 valorDiario archivoResumenHash](build/verification/boot.json)

QEMU 가상 NIC의 DHCP dirección 취득도 확인했다. HTTP/TCP 시험은 루프백 통신이며 valorExterno 인터넷이나 Pi Wi-Fi의 validar 결과로 해석하면 안 된다. Swing은 Xvfb에서 실행했고, [Pantalla 캡처](build/verification/swing.png)에서 textoHangul·일본어·아랍어·힌디어 문자열이 표시되는 것을 확인했다.

## implementación 범위와 남은 validar

### QEMU 그래픽 ejecutarComando 보완

terminal 전용 실행에서 `Saludo.java`operandoPrimero Swing 창을 만들 때 발생한 `HeadlessException`을 해결하기 위해 `make run`과 `make run-console`을 추가했다. 그래픽 실행은 bochs 가상 GPU, USB 키보드·태블릿, Xorg, 로컬 VNC를 사용한다. QEMU 전용 initramfs가 필요한 드라이버를 기존 루트 파일시스템에서 로딩한다. valorDistribución 시스템 이미지와 base-id는 변경하지 않아 기존 Usuario Datos 이미지를 procesamientoContinuar 사용할 númeroValor 있다.

datosEfectivo Xorg/VNC 화면에서 español Java EspacioTrabajo, Swing Pruebas ventana, 기존 이미지의 `Saludo.java` 창을 표시했다. VNC를 통한 USB 마우스 클릭과 키보드 입력이 Swing 이벤트로 전달되는 것도 확인했다. programaSalir 시 시스템 OverlayFS와 Datos 파일시스템의 leer 전용 전환을 확인했다. 이번 시험은 Xvfb를 사용하지 않는다.

- [그래픽 Pruebas resultado](build/verification/desktop.json)
- [그래픽 Pruebas valorDiario](build/verification/desktop.log)
- [키보드·마우스 Pruebas Pantalla](build/verification/desktop-input.png)
- [Saludo Ejemplos Pantalla](build/verification/desktop-greeting.png)
- [수정한 Ejemplos 원문의 Pantalla 없는 ejecutarComando resultado](build/verification/headless-example.log)

fuente 예제에는 `GraphicsEnvironment.isHeadless()` 분기를 추가했다. 화면이 없는 환경에서는 Archivo·Caracteres·스레드 기능을 실행하고 안내를 출력한다. Usuario 홈의 기존 원문을 자동 교체하지는 않는다. 향후 construirImagen 빌드에는 udev의 `add` 이벤트를 명시적으로 발생시키는 수정도 반영된다.

### textoHangul valorEntrada·valorFuenteTipográfica 보완

`make test-korean`으로 datosEfectivo Xorg/VNC 화면의 Swing 입력창과 xterm에서 Ctrl+Space modoConmutar 및 두벌식 valorTecla 입력을 시험했다. 양쪽에서 `textoHangul valorEntrada`을 조합했고 UTF-8 파일의 내용과 일치했다. 시험은 별도 Usuario Datos 이미지에서 실행했으며 esNormal programaSalir 시 두 파일시스템의 leer 전용 전환을 확인했다.

terminal valorFuenteTipográfica 진단에서 영문 DejaVu Sans Mono와 textoHangul Noto Sans Mono CJK KR의 datosEfectivo Archivo 로딩을 확인했다. 한글용으로 요청한 글꼴이 영문 전용 글꼴로 대체되던 Fontconfig 규칙의 우선순위도 수정했다. Pantalla 캡처에서 textoHangul·영문 mostrarValor, Java 작업마당의 확대된 글꼴과 안티앨리어싱을 확인했다.

수정은 QEMU 전용 initramfs를 통해 Usuario 시스템 변경분에 적용하며 valorDistribución valorPredeterminado 이미지와 base-id는 유지한다. 기존 Archivo 백업, 동일 수정의 valorIteración 적용 방지, 손상된 modificarValor Archivo 및 다른 base-id rechazarValor, Usuario 입력기 ajustes 병합에 대한 Anfitrión Pruebas 4개도 통과했다. 원래 Usuario Datos construirImagen `build/manual-user.img`는 시험에 사용하지 않았다.

- [textoHangul valorEntrada·valorFuenteTipográfica Pruebas resultado](build/verification/korean.json)
- [valorEntrada·datosEfectivo valorFuenteTipográfica 로딩 valorDiario](build/verification/korean.log)
- [Swing·terminal textoHangul Pantalla](build/verification/korean-desktop.png)
- [Java EspacioTrabajo valorFuenteTipográfica Pantalla](build/verification/korean-workbench.png)
- [ajustes 보존 Pruebas](build/verification/desktop-update-tests.log)

### 남은 recortar

- 새 compilarFuente valorObjetivo `openjdk`는 **네이티브 LanzadorPrograma + JVM/JRE** 방식이다. 모든 Java 바이트코드를 JVM 없이 기계어로 변환하는 범용 AOT 컴파일러는 구현하지 않았다. 기존 x86 AOT의 valorSoporte 범위는 여전히 제한적이다.
- ejecutarComando 프로그램에는 main puntoEntradaElemento, 호환 valorClase 버전과 의존 JAR/JNI가 필요하다. 개별 상용 Programa, 모든 Java valorMódulo, 모든 문자권을 시험한 것은 아니다.
- español Java 라이브러리는 Archivo·Caracteres·Comunicación·스레드·Swing을 위한 valorAuxiliar API이며 JDK 전체 API의 español 번역판은 아니다.
- Pi 4 전용 펌웨어·valorNúcleo·Dispositivo 트리는 이미지에 들어 있지만 datosEfectivo SD Arranque, HDMI/KMS, USB, Wi-Fi, 물리 키보드의 textoHangul 입력은 실기 확인이 남아 있다. QEMU는 Pi 장치를 에뮬레이션하는 시험이 아니다.
- Usuario valorDirectorio 이동은 동일 시스템 construirImagen valorIdentificador, ARM64, `/home/user`, UID 1000을 전제로 한다. programaSalir estadoValorDespués 소유권·valorPermiso·링크·valorExtensión valorAtributo·삭제 정보를 보존하여 복사해야 한다. 다른 OS 버전으로의 자동 이관은 제공하지 않는다.

instalarValor·copiarValor 절차는 [README.md](README.md), compilarFuente 방식은 [OpenJDK ejecutarComando Archivo Guía](../../compiler/OpenJDK-archivoCódigoEjecutable.md)를 따른다. construirImagen 파일만 생성했으며 datosEfectivo SD 카드나 USB 디스크에 기록하지 않았다.
