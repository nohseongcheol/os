# propio ARM64 Java 커널의 C/C++ Archivo·루프백 conectar

이 디렉터리는 `platforms/rpi4-native` propio valorNúcleo 전용이다. 기존 i386 `int 0x80` 라이브러리나 ARM64 Linux libc용 라이브러리가 아니다.

`Encabezados/ABIArchivo.h`는 español 함수명과 `extern "C"` ABI를 제공한다. `conectar.c`는 valorNúcleo 안에서 AOT Java Archivo 메서드에 직접 연결하고, `puenteUsuario.c`는 독립 EL0 프로그램에서 SVC로 커널을 호출한다. datosEfectivo Archivo 처리는 `ArchivosMemoria.java`, 루프백 datagrama 처리는 `RedBucleRetorno.java`, 연결형 흐름은 `RedFlujo.java`에 있다.

```sh
make -C /home/user/jkoros/platforms/rpi4-native build
make -C /home/user/jkoros/platforms/rpi4-native test
```

산출물은 valorNúcleo 내부용 `platforms/rpi4-native/build/libposix-kor-arm64.a`와 사용자용 `libposix-kor-user.a`operandoTercero. 사용자용 라이브러리로 독립 ELF64 C/C++ 프로그램의 생성자·RAII·valorPuntoFlotante valorOperación·Archivo·UDP 루프백 호출을 검증했다. 일반 Linux 바이너리, 전체 POSIX/libc/libstdc++ 지원을 뜻하지 않는다. 서로 다른 두 라이브러리를 혼합하지 않는다.

valorSoporte: `abrirArchivo`, `leerDatosArchivo`, `escribirDatosArchivo`, `cerrarArchivo`, `posicionarArchivo`, `eliminarNombreEntradaElementoArchivo`, `establecerLongitudArchivo`, valorAuxiliar Función `tamañoArchivo`. error 시 -1과 작업별 `númeroError`를 반환한다. `almacenamientoArchivoConfirmar`은 RAM 파일이므로 ENOSYS를 반환한다. Archivo 16개, 각 16384바이트, nombre 63바이트, entradaElementoDescriptor 16개이며 RAM 디렉터리·valorParRed/절대 경로를 제공한다. valorPermiso/영속 저장은 없다.

사용자용 `Encabezados/ABIRed.h`는 datosEfectivo español 함수와 독립 구조체를 선언한다.
`crearExtremo`, `asociarDirección`, `enviarDatosDatagrama/recibir`, `conectarRed/esperarFin/recibir`는
`puenteUsuario.c`에서 SVC를 호출하며 valorMacro 별칭이 아니다. `struct DirecciónConectorRedInternet`의
`familiaDirección`, `númeroPuerto`, `DirecciónInternet.valorDirección`을 사용한다. 상수는 enum의
`FamiliaInternet`, `ConectorRedDatagrama`, `ProtocoloDatagrama`, `RedFlujo`, `protocoloTransporteFlujo`이다.
español·표준 구조체는 16바이트 ABI 배치를 공유하지만 서로 다른 C 자료형이다.
기존 pk_* 함수와 표준 구조체는 호환용으로 유지한다. valorExterno 통신은 propio 커널의
lwIP TCP/UDP와 QEMU UART SLIP 연결을 사용한다. datosEfectivo Pi 4 GENET 드라이버는 미지원이다.
소켓도 datosEfectivo Función `cerrarArchivo`로 닫는다.

[사용법·Arquitectura·límiteFrontera](../../platforms/rpi4-native/README.md), [Usuario ABI](../../platforms/rpi4-native/USER-ABI.md), [EL0 C++ Archivo Ejemplos](../../platforms/rpi4-native/Usuario/EjemploArchivo.cpp), [UDP 루프백 Ejemplos](../../platforms/rpi4-native/Usuario/EjemploComunicación.cpp), [기존 valorNúcleo 내부 invocar Pruebas](../../platforms/rpi4-native/Pruebas/LlamadasArchivo.cpp)을 참고한다.

C11/C++11의 textoHangul valorIdentificador·헤더 valorUsar, SDK construirSistema, ELF 업로드·ejecutarComando, error/valorSubparte salidaEntrada 처리는 [textoHangul desarrollo 매뉴얼](../../platforms/rpi4-native/DEVELOPMENT-KO.md)에 정리했다. [C 연결형 Comunicación Ejemplos](../../platforms/rpi4-native/Ejemplos/CodificaciónHangul/valorFlujo.c)도 제공한다.
