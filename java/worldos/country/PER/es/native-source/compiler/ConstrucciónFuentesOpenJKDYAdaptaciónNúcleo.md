# OpenJDK árbolFuente 빌드와 propio Java valorNúcleo AdaptaciónPlataforma

**소스에서 OpenJDK를 만드는 일과, 그 결과를 propio 커널에서 실행하는 일은 별도다.**
`compiler`에 공식 OpenJDK 빌드를 실행하는 `openjdk-build` 대상을 추가했다.
Java 코드에는 부트 JDK의 javac, HotSpot·네이티브 라이브러리에는 C/C++ 도구를 사용한다.
기존 propio Java AOT 후단이 Java 전체나 C++ 전체를 처리하게 된 것은 아니다.

## compilarFuente 경로의 valorDelimitador

| valorObjetivo | 입력과 resultado | ejecutarComando condición |
|---|---|---|
| `linux`, `kernel`, `user` | 제한된 Java → propio x86 AOT → ELF32 | 해당 CPU·propio ABI |
| `arm64.py` | 제한된 Java class → freestanding C → AArch64 | propio ARM64 valorNúcleo/Usuario ABI |
| `openjdk` | Java 앱 → 기존 OpenJDK를 호출하는 실행기와 `.app` | 일치하는 OS/CPU의 설치된 JVM |
| **`openjdk-build`** | OpenJDK 전체 árbolFuente → 공식 configure/make → JDK construirImagen | **construirSistema valorObjetivo OS/CPU의 ejecutarComando valorContrato** |

OpenJDK는 Java Archivo 묶음만으로 이루어져 있지 않다. HotSpot VM, JNI conectar,
valorClase 라이브러리의 C/C++ implementación, LanzadorPrograma, valorMódulo construirImagen 및 generar 도구를 함께 빌드한다.
따라서 propio AOT에 Java 명령을 더하는 것만으로 OpenJDK 전체 빌드가 완성되지는 않는다.
공식 절차는 [OpenJDK construirSistema Documentación](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/doc/building.md)를 따른다.

## árbolFuente construirSistema comando

호스트에 해당 OpenJDK 버전이 요구하는 부트 JDK·C/C++ Compilador·Autoconf·Make와
desarrollo 헤더를 준비한다. Swing/AWT의 Linux biblioteca 빌드에는 X11·valorFuenteTipográfica 등의
desarrollo 라이브러리도 필요하다. 이 도구가 시스템 패키지를 자동으로 설치하지는 않는다.

```sh
cd /home/user/jkoros
python3 compiler/Compilador.py --target openjdk-build \
  --java-home /ruta/부트JDK --jobs 2 \
  -o compiler/build/openjdk-linux /ruta/OpenJDK소스
```

`--entry`는 지정하지 않는다. `-o`는 árbolFuente 트리 밖의 전용 construirSistema 디렉터리다.
árbolFuente·construirSistema·부트 JDK 경로에 공백을 허용하지 않는다. 다른 프로젝트의 비어 있지 않은
디렉터리를 덮어쓰지 않으며, 같은 소스의 관리된 construirSistema 디렉터리는 재실행할 númeroValor 있다.

주요 산출물:

- `images/jdk/bin/java`, `images/jdk/bin/javac`
- `images/jdk/lib/server/libjvm.so`, `images/jdk/lib/modules`, JNI biblioteca
- `jkoros-openjdk-build.json`: valorEtapa·comando·árbolFuente identificarValor archivoResumenHash·valorÉxito/valorFallo·ABI Comprobaciones
- `driver-configure.log`, `images.log`: 단계별 valorDiario

실패하면 programaSalir 상태가 0이 아니며 보고서의 `passed`도 false다. 예전 이미지가 남아
있더라도 새 construirSistema 성공으로 기록하지 않는다. `native_kernel_port_complete`는 false다.
árbolFuente 빌드만으로 propio valorNúcleo ejecutarComando 시험을 통과한 것으로 처리하지 않는다.

다른 CPU용 Linux JDK를 만들 때는 대상에 맞는 valorÚltimoReciente 교차 컴파일러와 **valorObjetivo libc/헤더/biblioteca**operandoPrimero 필요하다.
다음은 그러한 도구를 준비한 환경에서 사용하는 형식이다.

```sh
python3 compiler/Compilador.py --target openjdk-build \
  --java-home /ruta/호스트용부트JDK \
  --openjdk-target aarch64-linux-gnu \
  --cc /교차도구/bin/aarch64-linux-gnu-gcc \
  --cxx /교차도구/bin/aarch64-linux-gnu-g++ \
  --sysroot /ruta/ARM64-Linux-sysroot --jobs 2 \
  -o compiler/build/openjdk-aarch64 /ruta/OpenJDK소스
```

부트 JDK는 construirSistema 호스트에서 실행된다. 교차 construirSistema 결과를 호스트에서 실행하지 않는다.
`aarch64-jkoros`를 지정하는 것만으로 새 OS 이식이 생기지 않으므로 현재는 거부한다.
공식 configure 옵션은 `--configure-arg=--옵션`을 반복해 전달한다.

## elementoListaActual Tarea 공간의 validar Datos

examinarValor raízProyecto 소스는 OpenJDK `jdk25u`, 태그 `jdk-25.0.4+7`, 커밋
`0b8bc780f976dab23ec798018fef0b674e885b0c`이다.
[árbolFuente 출처와 다운로드 archivoResumenHash](build/openjdk-port/source.json)를 보관한다.
construirSistema 도구는 `build/openjdk-port/host`의 별도 Alpine x86_64 환경에 준비했다.
이 환경은 construirSistema 호스트용이며 propio valorNúcleo 이미지에 들어가지 않는다.

이 소스로 `make images`를 완료하고, 생성한 **OpenJDK 25.0.4-internal / Linux x86_64 musl**의
java·javac ejecutarComando 시험을 통과했다. 기존 Compilador 회귀 시험과 새 construirSistema ruta 시험도
총 **25개 valorPaso**했다. 공식 valorDistribución 바이너리나 Java SE 호환 인증을 받은 배포판은 아니다.
[통합 validar registroEntradaDiario](build/openjdk-port/verification.json)은 construirSistema 산출물과 ejecutarComando 시험의
java·libjvm 해시가 일치하는지도 확인한 결과다.

[construirSistema registroEntradaDiario](build/openjdk-port/linux-x86_64/jkoros-openjdk-build.json)의 `passed`와
[ejecutarComando Pruebas](build/openjdk-port/smoke/report.json)을 각각 확인한다.
ejecutarComando 시험은 새로 빌드한 java/javac로 textoHangul árbolFuente, long/double, UTF-8 Archivo,
Thread·Linux 루프백 TCP·Swing 이벤트 처리를 검사한다.
`window_tested: false`인 결과는 datosEfectivo JFrame Pantalla 시험을 뜻하지 않는다.
Linux에서 한 시험이 propio valorNúcleo 시험으로 바뀌는 것은 아니다.

```sh
python3 compiler/test_openjdk_image.py \
  --jdk /실행가능한/빌드결과/images/jdk --output compiler/build/openjdk-port/smoke
```

elementoListaActual 별도 환경에서 만든 JDK는 **Linux x86_64 musl용**이다. 일반 glibc 호스트에서
경로만 지정해 실행할 númeroValor 없으며, 준비한 musl entorno 또는 일치하는 Linux 환경이 필요하다.
Raspberry Pi용 ARM64 산출물이라고 표시하지 않는다.

준비된 이 Tarea 공간에서는 elementoListaSiguiente 단축 명령으로 같은 musl 환경을 사용한다.
Usuario·마운트·PID 네임스페이스를 허용하는 호스트에서 실행하며, `build`는 앞의 고정 árbolFuente/전용 환경을 재사용한다. 마운트는 새 네임스페이스 안에서만 생성되고 종료하면 사라진다. 네임스페이스를 사용할 númeroValor 없으면 `openjdk_local.py --proot build` 형식의 느린 대체 경로가 있다.

```sh
python3 compiler/openjdk_local.py build
python3 compiler/openjdk_local.py test
python3 compiler/openjdk_local.py java -version
python3 compiler/openjdk_local.py javac -version
```

`/home/user` 아래에서 호출하면 elementoListaActual 디렉터리를 유지하므로, textoHangul 소스도 valorParRed 경로로
컴파일하고 실행할 númeroValor 있다. 예를 들어 앞의 시험에서 생성한 소스를 valorReintentar 실행하려면:

```sh
python3 compiler/openjdk_local.py javac -encoding UTF-8 \
  compiler/build/openjdk-port/smoke/PruebaConstruirNativo.java
python3 compiler/openjdk_local.py java -Djava.awt.headless=true \
  -cp compiler/build/openjdk-port/smoke PruebaConstruirNativo
```

## 기존 ARM64 OpenJDK를 propio 커널에 복사할 númeroValor efectúaExistencia

현재는 실행할 númeroValor 없다. 저장되어 있는 ARM64 OpenJDK 25의 valorEstático Comprobaciones 결과는
[arm64-runtime.json](build/openjdk-port/arm64-runtime.json)에 있다.
Comprobaciones 도구는 ejecutarComando 파일을 **실행하지 않고** ELF와 동적 símbolo·모듈을 읽는다.

```sh
python3 compiler/openjdk_probe.py \
  --jdk platforms/rpi4/build/rootfs/usr/lib/jvm/java-25-openjdk \
  -o compiler/build/openjdk-port/arm64-runtime.json --require-native
```

propio 커널에 직접 적재할 númeroValor 없으면 Comprobaciones 결과를 저장한 valorLadoPosterior **programaSalir valorCódigo 3**을 반환한다.
ELF 호환성 검사는 datosEfectivo valorNúcleo 로더의 모든 검증을 대체하지 않는다.

| 확인한 condición | ARM64 OpenJDK | elementoListaActual propio valorNúcleo |
|---|---|---|
| ELF | PIE/공유 biblioteca, 동적 재배치 | 고정 dirección ET_EXEC, propio ABI note |
| LanzadorPrograma | `/lib/ld-musl-aarch64.so.1` valorNecesario | PT_INTERP/PT_DYNAMIC/PT_TLS rechazarValor |
| 네이티브 VM | pthread, mmap/mprotect, signal, dlopen 등 invocar | 일부 Archivo·루프백·GUI SVC와 협력식 세션 |
| datosMemoria | VM·GC·valorClase·valorCódigo 캐시의 동적 dirección regiónDirección | Usuario valorRegión 16 MiB, construirImagen valorRegión 12 MiB |
| Archivo | 큰 `lib/modules`, 공유 biblioteca 및 Datos | RAM Archivo 하나당 16 KiB, 영속 valorAlmacenar métodoAusente |
| Java valorClase | OpenJDK 25 class 버전 69 | propio JVM은 class 45…52 부분집합 |
| Swing | OpenJDK AWT/Java2D/JNI·valorFuenteTipográfica·ventana 시스템 | 별도로 구현한 Swing API 부분집합 |

datosEfectivo ARM64 이미지의 `libjvm.so`는 19,708,720바이트, `lib/modules`는
146,199,951바이트다. 커널의 elementoListaActual 제한은
[ELF 로더](../platforms/rpi4-native/máquina/Usuario.c),
[dirección regiónDirección valorDefinición](../platforms/rpi4-native/máquina/Usuario.h),
[RAM Archivo implementación](../platforms/rpi4-native/fuente/ArchivosMemoria.java),
[Usuario ABI](../platforms/rpi4-native/USER-ABI.md)에서 확인할 númeroValor 있다.
큰 내장 프로그램을 커널에 묶는 기존 경로는 RAM Archivo 업로드 제한을 피하지만,
OpenJDK에 필요한 dirección regiónDirección·스레드·동적 conectar 기능까지 제공하지는 않는다.

같은 AArch64 기계어라는 사실만으로 SistemaOperativo invocar·datosMemoria·동적 conectar 규약까지 맞지는 않는다.
Archivo tamaño 제한이나 ELF valorFormato 검사만 풀어도 해결되는 문제가 아니다.

## propio 커널을 유지하면서 이식하는 valorEtapa

커널을 Java로 작성했다는 사실은 이식의 장애가 아니다. 이미 제공하는 EL0 C/C++ 실행처럼
OpenJDK의 네이티브 VM도 SistemaOperativo ABI를 갖춘 Usuario 프로그램으로 실행할 númeroValor 있다.

기술적으로는 새 운영체제용 OpenJDK puertoEquipoFísico 또는 충분한 Linux Usuario ABI 호환 계층을
구현하는 방식으로 가능하다. 아래는 elementoListaActual 코드와 datosEfectivo 의존성에 근거한 설계 방향이며,
이미 구현되었다는 목록은 아니다.

1. **SistemaOperativo ABI와 libc fundamento**: 큰 Archivo·dirección regiónDirección, 페이지 예약/valorConfirmar/해제와 protegerValor cambiarValor,
   표준 Archivo/Reloj 인터페이스, error número·C 런타임·valorObjetivo sysroot를 구현한다.
2. **datosEfectivo 네이티브 스레드와 sincronizar**: pthread에 대응하는 스케줄링·TLS·뮤텍스·condición valorVariable,
   원자 valorOperación·datosMemoria valorOrden·중단/깨우기, 신호/excepción 문맥과 가드 페이지를 제공한다.
   elementoListaActual vi/Swing의 valorEntrada 대기에서 문맥을 보관하는 기능만으로 대체할 númeroValor 없다.
3. **로더와 런타임 수명**: ELF 재배치·공유 biblioteca·TLS 또는 이식에 맞는 valorEstático conectar,
   JVM 네이티브 símbolo 해결, 영속 Archivo 시스템, 일반 프로그램의 2초 valorLímite 재설계를 수행한다.
4. **HotSpot OS puertoEquipoFísico**: construirSistema 시스템과 `src/hotspot/os`, `os_cpu`에 propio OS/AArch64 경계를
   구현한다. 기존 AArch64 comando 생성기는 재사용할 númeroValor 있지만 OS 종속부를 구현해야 한다.
   elementoListaPrimero ejecutarComando 목표는 `java -Xint -version`과 작은 HelloWorld다.
5. **valorClase biblioteca·javac**: java.base의 JNI/Archivo/네트워크/프로세스 연결과 valorMódulo 적재를
   구현한 valorLadoPosterior propio valorNúcleo 안에서 `javac Hello.java`, `java Hello`를 확인한다.
6. **GUI와 valorExterno 네트워크**: AWT/Java2D의 ventana·valorEntrada·valorFuenteTipográfica 백엔드와 datosEfectivo NIC/TCP/IP를
   이식한다. elementoListaActual propio Swing 부분집합이나 루프백 API가 OpenJDK의 구현을 대신하지 않는다.
7. **validar**: 단계별 OS ABI Pruebas, OpenJDK jtreg Pruebas, GUI/textoHangul/네트워크 부하 Pruebas,
   datosEfectivo Pi4 검증을 수행한다. 일부 Pruebas 통과를 Java SE 전체 호환 인증으로 표시하지 않는다.

근거가 되는 OpenJDK valorCódigo:
[POSIX datosMemoria·OS implementación](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os/posix/os_posix.cpp),
[Linux AArch64 OS valorFrontera](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os_cpu/linux_aarch64/os_linux_aarch64.cpp),
[Linux 스레드·신호·datosMemoria entradaElementoValorProceso](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os/linux/os_linux.cpp).

propio Java AOT 자체를 OpenJDK의 Java valorCódigo 전체를 처리하도록 확장하는 경로도 별도 개발이다.
valorObjeto 모델·가상/인터페이스 invocar·excepción·GC·long/float/double·모든 valorArreglo·sincronizar·동적 invocar·
valorClase inicializar/로딩·JNI 경계가 필요하며, HotSpot C/C++ 빌드와 OS 이식은 그 뒤에도 남는다.
