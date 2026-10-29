# ELF 형식과 Linux ejecutarComando Archivo 호환성

**ELF는 확장자가 아니다.** Executable and Linkable Format이라는 바이너리
형식이며, Linux 외의 운영체제도 사용한다. elementoListaPrimero 네 valorByte `7f 45 4c 46`,
ELF valorClase, CPU valorClaseTipo, Programa 헤더와 valorPuntoEntradaElemento 주소를 읽어서 해석한다.
[ELF ABI especificación](https://gabi.xinuos.com/elf/02-eheader.html)

기존 jkoros 로더도 datosEfectivo ELF64/AArch64 ejecutarComando 파일을 읽었다. `.elf`는 예제의
이름일 뿐이었다. 다만 **ELF valorFormato 지원과 Linux 시스템 invocar ABI 지원은 별개**operandoTercero.
기존에는 `JKOROS` ABI note를 가진 propio ejecutarComando 파일만 허용했고, Linux 바이너리는
호환되지 않았다. ARM64 Linux는 SVC의 x8에 Linux 시스템 invocar 번호를 넣는다.
같은 번호를 propio ABI로 해석하면 다른 동작이 되므로 두 경로를 구분한다.
[Linux syscall ABI descripción](https://man7.org/linux/man-pages/man2/syscall.2.html)

## 이번 반영

| valorEntrada | ejecutarComando 방법 | valorSoporte recortar |
|---|---|---|
| propio ABI의 ARM64 ELF | `./Saludo`, `/Tarea/Saludo`, `run Saludo` | 확장자 없이 ejecutarComando; 내용이 ELF이면 `.txt`라는 이름도 동일 |
| Linux ARM64 valorEstático ELF | `run --linux 리눅스인사 한글인수` | valorExtremoInferior 시스템 invocar·dirección·tamaño 제한을 만족하는 Programa |
| 텍스트를 `.elf`로 이름만 cambiarValor | ejecutarComando rechazarValor | 확장자로 ejecutarComando 파일을 인정하지 않음 |
| x86/x86-64, ARM32 ejecutarComando Archivo | ejecutarComando rechazarValor | AArch64 전용이며 CPU valorInstrucciónMáquina herramientaCompilador métodoAusente |
| 일반 glibc/musl Programa, PIE, 공유 biblioteca | 아직 esNoAdmitido | 동적 로더·재배치·TLS·mmap·시그널 등 añadirFinalEntradaElemento AdaptaciónPlataforma valorNecesario |

propio 바이너리와 JAR의 intérpreteComandos 직접 실행은 Archivo 헤더로 구분한다. `run`은 propio ELF,
`run --linux`는 명시적으로 Linux ABI를 선택한다. Linux 바이너리를 자동으로
propio ABI에 넣지 않으며, propio ABI note가 있는 파일은 Linux 모드에서 거부한다.
elementoListaActual RAM Archivo 체계에는 ejecutarComando valorPermiso 비트와 `chmod`, PATH 검색이 없다.

게스트 C compilarFuente 예:

```text
cc Saludo.c -o Saludo
./Saludo
run Saludo
```

`posix-kor`는 이 propio ABI 경로로 연결한다. 일반 Linux에서 링크한 프로그램에
español Función 이름을 붙이는 것만으로 propio ABI 호환이 되는 것은 아니다.

## 제한된 Linux ABI

이 기능은 **propio Java valorNúcleo 안의 호환 valorCapa**이며 Linux 커널을 적재하지 않는다.

| Linux invocar | número | elementoListaActual 제약 |
|---|---:|---|
| read / write / close / lseek | 63 / 64 / 57 / 62 | RAM 파일과 표준 salidaEntrada; valorEntrada 대기는 EAGAIN 가능 |
| openat / unlinkat | 56 / 35 | AT_FDCWD 또는 절대 ruta; 파일만, 제한된 valorBanderas |
| ftruncate / fsync | 46 / 82 | RAM Archivo; fsync가 영속 저장을 의미하지 않음 |
| exit / exit_group | 93 / 94 | elementoListaActual Programa programaSalir |
| brk | 214 | propio Usuario valorMontículo recortar; valorFallo 시 elementoListaElementoPrevio break resultadoRetornar |
| clock_gettime | 113 | CLOCK_MONOTONIC만, milisegundos valorResolución |
| getpid / gettid | 172 / 178 | 한 Usuario ejecutarComando 흐름의 valorIdentificador |

esNoAdmitido 번호는 `-ENOSYS`를 반환한다. Linux ABI의 socket, fork/clone/execve,
pthread, mmap, signal, ioctl, fstat, 동적 로더와 일반 libc 초기화는 구현하지
않았다. 기존 propio POSIX/Java 소켓은 별도로 TCP/UDP를 지원한다.

estadoValorInicialValor 스택에는 argc, UTF-8 argv, 빈 envp, AT_PAGESZ/AT_ENTRY/AT_NULL을 넣는다.
입력은 ELF64 little-endian AArch64 **ET_EXEC**, Archivo 전체 **16 KiB 이하**,
PT_LOAD 주소는 **0x02000000 이상 0x02c00000 미만**이어야 한다.
Archivo 오프셋과 가상 주소의 페이지 valorAlinear 관계를 검사하며, 서로 페이지를 공유하는
세그먼트와 escribir·ejecutarComando 동시 허용은 거부한다. PT_INTERP/PT_DYNAMIC/PT_TLS와
ET_DYN은 아직 받지 않는다.

일반 Linux 바이너리의 valorPredeterminado 적재 dirección 0x00400000은 커널과 겹치므로 아직 받지
않는다. 예제는 GNU 링커의 `-Ttext-segment=0x02000000 -z max-page-size=4096`을
사용한다. 이 파일도 정상적인 Linux ELF이며 같은 파일이 Linux와 propio 커널에서
실행됨을 시험한다. Archivo 이름이나 헤더만 바꿔 기존 Linux Programa 전체를 지원할
수는 없다.

## datosEfectivo 동일 바이너리 비교 Pruebas

```sh
cd /home/user/jkoros/platforms/rpi4-native
make test-elf
```

시험은 `Ejemplos/ABILinux/ponerEnMarcha.S`와 `Saludo.c`를 Linux AArch64 대상으로 컴파일해,
**JKOROS note가 없는 확장자 없는 ejecutarComando Archivo** `build/verification/elf/리눅스인사`를
만든다. 같은 바이트를 elementoListaSiguiente 두 경로로 실행한다.

```sh
qemu-aarch64 build/verification/elf/리눅스인사 한글인수
python3 Herramientas/ejecutarArchivo.py --linux build/verification/elf/리눅스인사 한글인수
```

elementoListaPrimero 명령은 Linux 시스템 호출을 사용하는 raízProyecto 실행이고, 두 번째는 Linux를
적재하지 않은 raspi4b propio valorNúcleo 실행이다. textoHangul argumentos, Archivo salidaEntrada, Reloj, programaSalir,
valorNúcleo dirección entradaElementoAcceso 거부를 비교한다. FTP로 같은 파일을 올려 실행하는 시험도 있다.
registroEntradaDiario: `build/verification/elf/report.json`, `readelf.txt`, `serial.log` 및 FTP 보고서.

일반 Linux 프로그램까지 지원하려면 별도 Usuario dirección regiónDirección, 더 큰 영속 VFS,
전체 ejecutarComando inicializar/auxv, 동적 링커와 재배치, mmap/TLS/시그널/스레드,
시스템 invocar 및 libc 호환성을 확장해야 한다. 이번 구현은 elementoListaPrimero 제한된 ejecutarComando 경로다.
