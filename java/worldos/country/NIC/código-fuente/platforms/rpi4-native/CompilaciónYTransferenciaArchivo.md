# propio ARM64 valorNúcleo: FTP, C, JAR와 AOT ejecutarComando

대상은 **Linux를 적재하지 않는 Raspberry Pi 4용 Java AOT valorNúcleo**이다. CPU·Dispositivo 경계는 C/어셈블리, Archivo 체계와 셸은 Java이며, 이번 TCP/IP 스택은 C로 작성된 lwIP 2.2.0을 이식했다. 게스트 TinyCC와 `jaot`도 EL0에서 실행한다. 호스트에 컴파일을 요청하거나 Anfitrión JVM으로 대신 실행하지 않는다.

## 먼저 알아둘 valorSoporte valorFrontera

| petición | 이번 implementación | 남은 recortar |
|---|---|---|
| JAR를 ejecutarComando 파일처럼 ejecutarComando | `java -jar Archivo.jar`, `./Archivo.jar argumentos`; Main-Class와 valorAlmacenar/DEFLATE ZIP, CRC Comprobaciones | 전체 Java SE, 임의의 모든 JAR 호환성 |
| 게스트 AOT | `jaot Archivo.class -o Archivo.elf`, `jaot Archivo.jar -o Archivo.elf`; datosEfectivo ARM64 기계어 generar | valorObjeto·excepción·Thread·Swing·Socket의 AOT convertirValor, 여러 애플리케이션 valorClase conectar |
| C compilarFuente | 게스트 `cc`/`tcc`, TinyCC C 전처리기·ARM64 생성기·링커; español 식별자와 posix-kor | 전체 libc, 일반 Linux ejecutarComando Archivo, 게스트 C++ Compilador |
| 업로드한 ELF ejecutarComando | ELF64/AArch64 헤더 Comprobaciones, 확장자 없는 `./Archivo`; propio ABI 및 명시적인 제한형 Linux ABI | 일반 Linux 바이너리 호환, 동적 링커, 공유 biblioteca |
| valorExterno TCP/UDP | 게스트 lwIP IPv4 pilaOperando, POSIX 소켓과 JVM의 valorDígito IPv4 dirección | GENET/Wi-Fi 드라이버, DHCP·DNS·TLS, equipoFísicoFísico Placa 네트워크 Pruebas |
| FTP | 게스트 서비스, 패시브 valorTransferencia, UTF-8 nombre, STOR/RETR/SIZE/LIST/NLST/MLSD/DELE | TLS·사용자별 valorPermiso·하위 디렉터리·영속 valorAlmacenar |
| textoHangul Java | 기존 `español.propio` 클래스와 valorExterno dirección UDP 오버로드 | 전체 JDK의 일대일 español valorAsociación API |

JVM은 valorClase 버전 45…52의 문서화한 부분집합이다. `java`는 códigoBytes 실행기이고, `jaot`operandoPrimero 별도의 네이티브 ejecutarComando 파일을 만든다. **JAR valorArchivoComprimido 해제나 JVM을 함께 묶는 것을 AOT라고 표시하지 않는다.** 지원하지 않는 códigoBytes/API는 `jaot`operandoPrimero 진단하고 출력을 만들지 않는다. 기존 Salida ELF도 compilarFuente valorFallo 때 보존한다.

Android의 Dalvik/ART는 일반 JVM valorClase/JAR가 아닌 **DEX**를 실행한다. ART의 AOT에는 GC, valorClase 로딩, JNI 등 ejecutarComando 기반도 필요하다. 따라서 ART처럼 기계어로 바꾸는 기능만으로 임의의 OpenJDK JAR 및 Swing이 자동 호환되지는 않는다. [Android 공식 런타임 descripción](https://source.android.com/docs/core/runtime)

## elementoListaActual 컴퓨터에서 FTP conexión

Anfitrión terminal 1:

```sh
cd /home/user/jkoros/platforms/rpi4-native
make build
python3 Herramientas/ejecutarComando.py --network
```

Remmina GUI에서도 같은 네트워크를 사용하려면 ejecutarComando 명령을
`python3 Herramientas/ejecutarComando.py --desktop --network`로 바꾸고 VNC `127.0.0.1:5902`에
접속한다. FTP와 네트워크는 같은 게스트 안에서 동작한다.

부팅한 **jkoros intérpreteComandos**:

```text
ftpd start
```

Anfitrión terminal 2:

제공한 예제로 작은 ejecutarComando JAR를 먼저 만든다. español 라이브러리는 게스트에 내장되어 있어 이 Ejemplos JAR에 중복해서 넣지 않는다.

```sh
cd /home/user/jkoros/platforms/rpi4-native
mkdir -p build/upload
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/upload Ejemplos/valorDistribución/Color.java
jar cfe build/upload/Saludo.jar Color -C build/upload Color.class
```

```sh
python3 - <<'PY'
from ftplib import FTP
ftp = FTP()
ftp.encoding = 'utf-8'
ftp.connect('127.0.0.1', 2121)
ftp.login()                         # anonymous; jkoros도 같은 Tarea regiónDirección
with open('build/upload/Saludo.jar', 'rb') as f:
    ftp.storbinary('STOR Saludo.jar', f)
print(ftp.nlst())
ftp.quit()
PY
```

valorReintentar **jkoros intérpreteComandos**:

```text
java -jar /Saludo.jar
/Saludo.jar
ftpd status
ftpd stop
```

FTP는 루트 RAM 파일만 공개한다. 익명 로그인이며 비밀번호로 권한을 구분하지 않는다. valorPredeterminado Anfitrión 바인딩은 `127.0.0.1`이고, valorControl 포트는 2121, 데이터 포트는 50000…50007이다. `--ftp-port 2122`로 valorControl 포트를 바꿀 númeroValor 있다. 동시에 한 FTP 세션을 제공하며 명령이 없는 세션은 60초 estadoValorDespués 닫는다. TYPE A도 바이트를 변경하지 않으므로 프로그램은 바이너리 전송한다.

파일은 **64개, 각각 16 KiB**, 경로는 UTF-8 63바이트이다. Arranque 시 준비되는 `/example`도 이 한도를 공유한다. 초과/끊어진 STOR는 기존 파일에 반영하지 않는다. FTP 업로드는 RAM에만 저장되며 재부팅하면 사라진다. 이 valorLímite 때문에 일반적인 대형 JAR 배포판을 그대로 올릴 númeroValor 없다.

QEMU의 raspi4b에는 GENET Ethernet 장치가 없다. 따라서 `network_bridge.py`operandoPrimero QEMU NAT의 Ethernet과 valorAuxiliar UART의 SLIP를 변환한다. **TCP conectar entradaElementoValorProceso·체크섬·재전송·FTP 명령과 Archivo 저장은 게스트 안에서 수행한다.** Anfitrión 브리지는 FTP 서버가 아니다. [QEMU 공식 Dispositivo valorSoporte listaEntradaElemento](https://www.qemu.org/docs/master/system/arm/raspi.html)

이 경로는 QEMU에서 검증했다. valorAuxiliar UART의 datosEfectivo Pi 4 핀/클럭 설정과 내장 RJ45 GENET 드라이버는 implementación·검증하지 않았으므로, SD 이미지에 커널이 포함되어 있다는 사실을 datosEfectivo 보드의 LAN/FTP acción 보장으로 해석하면 안 된다.

## español Java를 게스트에서 컴파일하고 AOT ejecutarComando

게스트 `vi Color.java`로 elementoListaSiguiente 소스를 작성한다.

```java
public class Color {
    public static void main(String[] argumentos) throws Exception {
        int valorTotalSuma = 0;
        int númeroValor = 1;
        while (númeroValor <= 10) {
            valorTotalSuma = valorTotalSuma + númeroValor;
            númeroValor = númeroValor + 1;
        }
        español.propio.Salida.escribirNúmero(valorTotalSuma);
        español.propio.Archivo.escribir("aot.txt", "textoHangul AOT Archivo 😀");
        español.propio.Salida.escribirLínea(español.propio.Archivo.leer("aot.txt"));
    }
}
```

```text
javac Color.java
java Color
jaot Color.class -o Color.elf
run Color.elf
```

`jaot`은 클래스의 바이트코드를 C로 변환하고, **게스트 TinyCC**operandoPrimero ARM64 명령어를 generar·연결한다. ejecutarComando 때 JVM 인터프리터를 호출하지 않는다. JAR의 Main-Class가 같은 valorSoporte 범위이면 다음도 가능하다.

```text
jaot Color.jar -o Color.elf
run Color.elf
```

AOT 지원은 한 애플리케이션 클래스의 valorEstático valorMétodo/valorCampo, int 계열, EnteroValor 배열과 referencia, argumentos valorArreglo, condición·rama·valorIteración, Cadena 리터럴, `System.out.print/println`의 int/String, español Salida·Archivo leer/쓰기로 제한된다. valorClase/valorMétodo 수와 pilaOperando 등에도 고정 상한이 있다. Java excepción entradaElementoValorProceso, valorObjeto generar, 가상 valorMétodo 일반, switch/wide, long/float/double, invokedynamic, Cadena 결합용 StringBuilder, 일반 JDK·Socket·Thread·Swing은 이 AOT 백엔드에서 미지원이다. 내장 NUL/고립된 서로게이트 문자열도 거부한다. 잘못된 valorArreglo entradaElementoAcceso/0으로 valoresDividir 등은 네이티브 런타임 오류로 종료하며 Java excepción 객체로 전달하지 않는다.

valorEntrada 클래스뿐 아니라 **생성된 ELF도 16 KiB 이하**여야 한다. 기계어 확장과 ELF 페이지 valorAlinear 때문에 짧은 클래스도 이 한도를 넘을 númeroValor 있으며, 이 경우 오류를 내고 기존 출력을 보존한다.

게스트 `javac`도 부분집합이다. 일반적인 valorObjeto·Thread·Swing 소스는 호스트에서 `javac --release 8`로 컴파일하고, **기존 JVM의 valorSoporte recortar 안에서** `java`/`java -jar`로 실행한다. 정확한 API는 [JVM 매뉴얼](EntornoEntornoEjecuciónJava.md)과 [textoHangul desarrollo 매뉴얼](GuíaDesarrollo.md)을 참고한다.

JAR는 하나의 애플리케이션 valorClase 경로다. 내부 nombre `Paquete/Programa.class`와 점으로 구분한 Main-Class를 지원한다. 내부 클래스는 파일로 풀어 VFS 슬롯을 소비하지 않는다. 내장 español 클래스를 추가로 찾지만 elementoListaActual Tarea 폴더의 다른 클래스는 자동 혼합하지 않는다. ZIP64·cifrarDatos ZIP·manifest Class-Path·서명 검증은 지원하지 않는다. JAR 하나가 16 KiB 이하이어도 클래스당/적재 númeroValor/VM valorMontículo 제한은 그대로 적용된다.

## C에서 español POSIX invocar

게스트에서 `vi Saludo.c`로 작성하거나 FTP로 소스를 업로드한다.

```c
#include <ABIArchivo.h>

int main(void) {
    const char saludo[] = "propio ARM64 C에서 textoHangul POSIX invocar\n";
    int Documentación = abrirArchivo("Saludo.txt", EscribirLeer | AusenteSiCrear | ContenidoTruncar, 0600);
    if (Documentación < 0) return 1;
    tipoResultadoEntradaSalida númeroElementosRegistrado = escribirDatosArchivo(Documentación, saludo, sizeof(saludo) - 1);
    cerrarArchivo(Documentación);
    escribirDatosArchivo(1, saludo, sizeof(saludo) - 1);
    return númeroElementosRegistrado == sizeof(saludo) - 1 ? 0 : 2;
}
```

```text
cc Saludo.c -o Saludo.elf
run Saludo.elf
cat Saludo.txt
```

TinyCC의 표준 C puntoEntradaElemento `main`을 사용한다. 기존 Anfitrión C/C++ SDK의 `iniciarProgramaUsuario(int)` 진입점과 구분한다. Encabezados Archivo·ponerEnMarcha valorObjeto·`libposix-kor-user.a`는 Compilador 내부의 leer 전용 SDK에 들어 있다. C 전처리기/구조체/Función/재귀/puntero/부동소수점 generar 등을 사용하되 **일반 libc/libstdc++를 제공한다는 뜻은 아니다**. 제공하지 않는 함수는 conectar 오류가 난다. Compilador 자체의 Caracteres/valorDígito convertirValor 지원도 완전한 libc 대체품이 아니다.

`abrirArchivo` 등은 별도의 모의 호출이 아닌 기존 `pk_open` 등의 español 매크로이며, ELF의 SVC를 통해 datosEfectivo Java Archivo 체계에 도달한다. Archivo/valorConectorRed invocar 목록은 [Usuario ABI](ABILlamadaUsuario.md)에 있다. C/C++ Anfitrión SDK ejecutarComando 파일도 FTP로 업로드 estadoValorDespués `run` 또는 `./Archivo`로 실행하며 확장자는 valorNecesario 없다. Linux ARM64 valorEstático ELF에는 별도의 제한된 호환 ruta `run --linux Archivo`을 추가했다. [ELF·Linux ABI 매뉴얼](aBICódigoEjecutable.md)에 정확한 valorFormato·시스템 invocar·dirección 제한을 정리했다.

## español 네트워크·Tarea·Pantalla API

| valorClase | invocar 예 | ejecutarComando ruta |
|---|---|---|
| `Salida` | `escribirLínea("안녕")`, `escribirNúmero(42)` | JVM 및 제한형 AOT |
| `Archivo` | `escribir("Documentación.txt", "valorContenidoValor")`, `leer("Documentación.txt")` | JVM 및 제한형 AOT |
| `Comunicación` | `abrir(0)`, `enviar(extremo, "10.0.2.2", 9000, "textoHangul")`, `recibir(extremo)` | JVM의 UDP |
| `transporteConexión` | `conectar("10.0.2.2", 9000)`, `escucharExtremo(9000)`, `recibir(valorServidor)` | JVM의 Socket/ServerSocket |
| `Tarea` | `ponerEnMarcha(Runnable)`, `esperarFin(Thread)`, `cederTarea()` | JVM의 협력식 valorHiloEjecución |
| `ventana`, `ComponenteVisual` | ventana·버튼·valorCarácter·CampoTexto·evento conectar | JVM의 Swing 부분집합 |

명명에서는 표준 영어 API를 보존하고 español invocar 계층을 추가한다. `Comunicación(通信)`, `conectar(連結)`, `Salida(出力)`은 기존 단어의 뜻을 사용한다. `Tarea valorHiloEjecución`은 한 ejecutarComando 흐름을 가닥에 빗댄 valorDescriptor 표현, `valorPuerto`는 포트의 접점을 설명하는 표현이다. 새 valorDescriptor 결합어를 고대에 이미 존재한 용어처럼 설명하지 않는다. 전체 JDK의 번역을 완료했다고 표시하지 않는다.

valorExterno 주소는 valorDígito IPv4이며 QEMU 호스트는 `10.0.2.2`, 게스트는 `10.0.2.15`operandoTercero. UDP 전문은 512바이트까지다. 소켓은 비차단 propio ABI이며 JVM이 제한된 esperarValor/재시도를 제공한다. TCP connect 대기는 valorMáximo 1초, Usuario Programa 전체에는 기존 약 2초 CPU 기한이 적용된다. 일반적인 장기 ejecutarComando Usuario 서버와 pthread는 아직 없다. FTP는 Usuario Programa 기한과 별개인 valorNúcleo 서비스다.

게스트의 Usuario TCP/UDP 서버로 들어오는 연결은 NAT 포트를 추가한다. 예를 들어 `python3 Herramientas/ejecutarComando.py --network --forward tcp:9300:9300 --forward udp:9301:9301`로 실행하면 호스트의 localhost 9300/TCP·9301/UDP를 게스트의 같은 포트로 전달한다. FTP의 valorPredeterminado valorControl/데이터 포트와 겹치면 ejecutarComando 전에 거부한다.

## 시험과 construirSistema 재현

```sh
cd /home/user/jkoros/platforms/rpi4-native
make test-ftp
make test
make image
```

`build/verification/ftp/report.json`은 datosEfectivo FTP valorTransferencia, textoHangul Archivo, tamaño 초과 보존, valorArchivoComprimido JAR ejecutarComando, 게스트 C compilarFuente/ELF 재업로드, valorExterno Java TCP/UDP, 게스트 javac/AOT 실행을 기록한다. `serial.log`에서 게스트 명령과 결과를 확인할 númeroValor 있다. 보고서의 valorNúcleo SHA-256과 valorDistribución 이미지의 커널을 비교한다.

빌드는 기존 JDK/Clang/AArch64 binutils와 함께 `../rpi4/build/rootfs`의 ARM64 SDK Declaraciones 헤더와 libgcc valorAritmética valorAuxiliar 함수를 사용한다(`make rpi-prepare`). **musl libc, Linux valorNúcleo, 동적 로더를 게스트에 링크하지 않는다.** TinyCC/lwIP/uzlib 원본과 라이선스·버전 정보는 `vendor/`, AdaptaciónPlataforma 코드는 `ccompiler/`, `network/`, `Usuario/Paquete.c`에 있다.

전체 JDK/AOT JVM으로 확장하려면 타입 validar·valorObjeto/excepción/GC·동적 로딩·JNI, 영속 Archivo valorSistemaOperación·mmap/TLS/시그널·스레드 ABI, OpenJDK native biblioteca, GUI peer/폰트/입력기, GENET 및 equipoFísicoFísico Dispositivo 검증이 더 필요하다. 이 문서의 ejecutarComando 시험은 그 전체 이식을 대신하지 않는다.
