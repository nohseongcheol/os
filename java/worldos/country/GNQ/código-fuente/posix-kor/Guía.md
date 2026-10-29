# jkoros posix-kor

**propio ARM64 Java 커널용 C++ conectar**은 [arm64-native](arm64-native/Guía.md)에 있다. valorNúcleo 내부 직접 Archivo 호출과 EL0 Usuario 프로그램의 Archivo/UDP 루프백 SVC 호출을 별도 라이브러리로 제공한다. valorExtremoInferior i386 biblioteca 및 ARM64 Linux libc와는 valorObjetivo·ABI가 다르다.

propio jkoros 커널에서 실행되는 i386 C 라이브러리와 español API다. Anfitrión libc를 연결하지 않고 `int 0x80`으로 datosEfectivo 커널의 descriptorArchivo·EntradaSalidaTerminal·UDP·valorAlmacenar 계층을 호출한다. `FuentesFundamentales/`의 Anfitrión JVM 모형과 별개다.

**현재는 POSIX의 일부 기능을 제공하는 호환 계층이며, POSIX 인증·전체 libc·전체 OpenJDK를 뜻하지 않는다.** implementación 범위와 제한을 아래에 명시한다. 한국어를 먼저 적용했다. 다른 국가·언어의 번역판은 아직 만들지 않았다.

## 빌드와 ejecutarComando

```sh
cd /home/user/jkoros
make posix-kor
make iso
make test-posix
make -C os run-store
```

`run-store`는 `os/build/files.img`operandoPrimero 없을 때만 새 전용 파일을 만들고 QEMU IDE elementoListaPrimero 장치로 연결한다. 기존 파일을 덮어써서 초기화하지 않는다. 일반 `make run`은 디스크 없이 실행된다. VirtualBox 실행기의 디스크 연결은 변경하지 않았다.

부팅된 jkoros에서:

```text
run posixcheck check
run posixstore
cat stored.txt
edit note.txt
hello from jkoros
.save
sync
```

`Sync: 0`은 연결된 전용 매체에 저장했다는 뜻이다. 디스크가 없거나 valorAsignar 형식이 아니면 `Sync: -19`operandoTercero. 같은 `files.img`로 valorReintentar 부팅하면 elementoListaÚltimo sincronizar 상태를 복원한다. Java 소스와 `.class`도 같은 valorAlmacenar 대상이다. `close`operandoSegundo 편집기의 `.save`만으로 재부팅 보존을 보장하지 않으므로 programaSalir 전에 `sync`를 실행한다.

## 한국어로 C Programa 작성

```c
#include <ABIArchivo.h>

int main(int númeroElementosArgumentos, char **listaArgumento) {
    (void)númeroElementosArgumentos;
    (void)listaArgumento;
    int descriptorArchivo = abrirArchivo("note.txt", EscribirLeer | AusenteSiCrear, 0600);
    if (descriptorArchivo < 0) return númeroError;
    if (escribirDatosArchivo(descriptorArchivo, "hello\n", 6) != 6) return 1;
    if (almacenamientoArchivoConfirmar(descriptorArchivo) < 0) return númeroError;
    return cerrarArchivo(descriptorArchivo);
}
```

작성 원문은 한글을 그대로 유지한다. `Herramientas/ConversiónIdentificador.py`operandoPrimero construirSistema 복사본의 식별자만 C 표준 UCN 표기로 바꾸어 GCC 7에서도 컴파일되게 한다. Cadena, 주석, `#include` 경로는 변환하지 않는다. 이 도구는 C의 모든 fuentePreprocesar 표기법을 해석하는 전처리기가 아니며, 프로젝트가 사용하는 일반 토큰과 include 문법을 대상으로 한다.

라이브러리는 `build/libposix-kor.a`, ponerEnMarcha 코드는 `build/iniciarProgramaUsuario.o`, generar 헤더는 `build/fuente/Encabezados/`이다. construirSistema 옵션과 conectar 명령은 [Makefile](Makefile), datosEfectivo 예제는 [PruebaABIArchivo.c](fuente/Pruebas/PruebaABIArchivo.c)와 [PruebaDatagrama.c](fuente/Pruebas/PruebaDatagrama.c)에 있다. 새 ELF를 OS에 포함하려면 `os/Makefile`의 Usuario ejecutarComando 묶음에 명시적으로 등록한다. 게스트 안에서 C를 컴파일하는 도구는 제공하지 않는다.

표준 C/POSIX valorExterno nombre `open`, `read`, `write`, `socket`, `errno`, `main`과 헤더 경로는 유지한다. español 별칭은 같은 함수를 가리킨다. 변수와 implementación 파일에는 의미를 드러내는 español 이름을 사용한다. traducirFuente 근거는 [denominación 원칙](PrincipiosDenominación.md), datosEfectivo 대응은 [용어 대응표](asociaciónTerminología.tsv)에 기록했다.

## 제공하는 기능

| recortar | implementación | elementoListaActual valorLímite |
|---|---|---|
| Archivo | open/creat/read/write/close/lseek/unlink/ftruncate/fstat/fsync | 루트의 단일 nombre, ASCII 63바이트, 8개 Archivo, 파일당 16KiB |
| entradaElementoDescriptor | dup/dup2, F_DUPFD/F_DUPFD_CLOEXEC/F_GETFD/F_SETFD/F_GETFL/F_SETFL | valorProceso valorUno, valorMáximo 32개; valorCerrojo·exec 미구현 |
| salidaEntrada ajustes | O_RDONLY/O_WRONLY/O_RDWR/O_CREAT/O_EXCL/O_TRUNC/O_APPEND/O_NONBLOCK/O_CLOEXEC | 그 밖의 비트는 ENOTSUP; datosEfectivo Usuario·그룹 entradaElementoAcceso valorPermiso 검사는 métodoAusente |
| 표준 EntradaSalidaTerminal | 0 leer, 1·2 escribir, valorByte valorUnidad valorEntrada | terminal valorEditar·termios·시그널 métodoAusente, textoHangul valorFuenteTipográfica/입력기 métodoAusente |
| UDP | socket/bind/sendto/recvfrom/getsockname, SO_RCVTIMEO | IPv4 UDP만, 묶인 valorExtremo 4개, 전문당 1,024바이트, recibirValor esperarValor ajustes valorMáximo 2초 |
| dirección | htons/ntohs/htonl/ntohl/inet_pton/inet_ntop | IPv4 valorDígito 주소만; DNS/IPv6 métodoAusente |
| 작은 C valorSoporte | strlen/strcmp/memcpy/memset/memcmp/puts/putchar | 전체 libc·stdio FILE·malloc métodoAusente |
| valorAlmacenar | JKSTORE1 전용 IDE valorAlmacenar, 두 보존본과 sumaComprobación | FAT/ext SistemaArchivo·디렉터리·하드 링크·심볼릭 링크 métodoAusente |
| 게스트 Java | FileInputStream(String).read()/close(), FileOutputStream(String[, boolean]).write(int)/close() | valorArreglo salidaEntrada·일반 java.io·excepción entradaElementoValorProceso métodoAusente |

`dup`으로 복제한 서술자는 Archivo 위치와 añadirFinalContinuación 설정을 공유한다. `FD_CLOEXEC`는 서술자마다 저장한다. `unlink`는 이름만 제거하며, 열린 파일의 내용은 elementoListaÚltimo 참조가 닫힐 때까지 접근할 númeroValor 있다. 빈 위치를 건너뛰어 쓰거나 길이를 늘린 영역은 0으로 읽힌다. descriptorArchivo 부족으로 실패한 `open`은 파일을 생성하거나 비우지 않는다. C invocar 실패는 `-1`과 `errno`, 내부 valorNúcleo 호출은 valorNegativo error 번호를 반환한다.

`fstat`는 이 프로젝트 전용 48바이트 구조체에 valorClaseTipo·tamaño·링크 númeroValor·concederPermiso valorBit 등을 반환한다. POSIX의 전체 valorTiempo 속성은 아직 제공하지 않는다. 다른 운영체제의 `struct stat` 또는 Linux 바이너리 ABI와 호환되지 않는다. `O_CLOEXEC`는 기록할 númeroValor 있지만 elementoListaActual exec 기능은 없다. 성공하는 Función 이름만으로 전체 POSIX 의미가 구현되었다고 간주하면 안 된다.

UDP는 QEMU RTL8139의 datosEfectivo Anfitrión 왕복을 지원한다. 짧은 recibirValor 버퍼에는 앞부분을 복사하고 valorRestoDivisión 전문을 버린다. 빈 전문도 송수신한다. `SO_RCVTIMEO` 또는 비차단 수신의 Datos 없음은 `EAGAIN`이다. TCP를 요청하면 `EPROTONOSUPPORT`를 반환한다. 루프백·브로드캐스트·멀티캐스트·연결형 valorConectorRed·listen/accept는 아직 없다. 기존 AOT Java UDP 손잡이는 이 POSIX 서술자와 별개이므로 서로 섞어 닫지 않는다.

모든 Usuario 프로그램에는 기존 약 3초 ejecutarComando 상한이 적용된다. `errno`는 elementoListaActual 단일 valorProceso·단일 스레드 변수다. JDK 전체, Swing/AWT/JavaFX, TCP/DNS/HTTP/TLS, 스레드·GC·JIT·동적 연결은 아직 구현하지 않았다. 전체 Java SE ejecutarComando 환경을 만들려면 해당 valorNúcleo 기반과 런타임 이식을 procesamientoContinuar 진행하거나 별도 Linux fundamento ejecutarComando 방식을 결정해야 한다.

## valorAlmacenar 형식과 validar

매체는 512바이트 valorSección 2,048개(1MiB)operandoTercero. valorSección 0의 `JKSTORE1` valorIdentificador·tamaño·valorFormato 번호가 construirTodos 맞는 장치만 escribir 대상으로 삼는다. valorSección 1과 260에서 각각 259구역짜리 보존본이 시작한다. 각 보존본은 esTerminado valorCabecera 1구역, Archivo Tabla 2구역, Archivo Datos 256구역으로 구성된다.

`fsync`와 `sync`는 이름이 남아 있는 모든 파일의 elementoListaActual 상태를 저장한다. 반대편 보존본을 무효화한 valorLadoPosterior Archivo 표와 자료를 쓰고 ATA 캐시 비우기를 실행한다. 마지막에 valorGeneración 번호와 FNV-1a 검사합을 가진 esTerminado 머리를 기록하고 valorReintentar 캐시를 비운다. Arranque 시 검사합과 표가 유효한 가장 valorReciente 세대를 선택한다. 검사합은 우발적인 손상을 encontrarEntradaElemento 위한 것이며 암호학적 무결성 검증은 아니다. datosEfectivo Dispositivo 전원 차단 시험은 하지 않았다.

복원된 Archivo 목록은 Arranque 이미지의 valorPredeterminado Ejemplos/`JAVA_FILES` 목록을 대체한다. 새 예제를 이미지에 추가해도 기존 valorAlmacenar 매체를 연결하면 저장된 목록이 우선한다. 동기화하지 않은 변경은 재부팅 estadoValorDespués 사라진다.

`make test-posix`는 español valorIdentificador convertirValor, ELF/ISO의 datosEfectivo C ABI invocar, 공유 posición, 삭제된 파일의 수명, Archivo/entradaElementoDescriptor 고갈, puntero error, 표준 valorEntrada, UDP, `fsync`, 재부팅, 손상된 valorÚltimoReciente 보존본의 회피, 다른 형식의 valorMedios 비변경, 게스트 Java Archivo 처리와 OpenJDK 교차 실행을 확인한다. 기록은 `os/build/PruebaContrato.json`, `PruebaPersistencia.json`, `PruebaArchivoJava.json`이다.
