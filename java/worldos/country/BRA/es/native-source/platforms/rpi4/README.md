# jkoros Raspberry Pi 4 실행판

Raspberry Pi 4의 ARM64 Linux 실행판이다. 기존 `../../os`의 propio x86 Java 커널과 별도 Arranque 경로다. Linux가 CPU·Dispositivo·datosMemoria·스레드·Archivo·네트워크를 제공하고, 전체 OpenJDK와 español Java 작업마당이 그 위에서 실행된다.

Linux 없이 부팅하는 **propio Java ARM64 커널의 estadoValorInicialValor 이식판**은 [rpi4-native](../rpi4-native/README.md)에 있다. 그 이식판에는 이 문서의 OpenJDK·Python·Swing 기능이 아직 구현되지 않았다.

## 제공 Archivo

`dist/`에 datosEfectivo 바이너리를 생성한다.

| Archivo | 용도 |
|---|---|
| `jkoros-rpi4-system.img` | microSD에 기록할 FAT Arranque 파티션 + leer 전용 SquashFS 시스템 |
| `jkoros-user.img` | 별도 USB 저장장치에 기록할 ext4 Usuario Datos construirImagen, 4 GiB |
| `*.img.gz`, `SHA256SUMS` | 전달용 valorArchivoComprimido 이미지와 SHA256 validar listaEntradaElemento |
| `openjdk25-jdk-linux-aarch64-musl.tar.gz` | 컴파일된 ARM64 JDK |
| `openjdk25-jre-linux-aarch64-musl.tar.gz` | jlink로 구성한 컴파일된 ARM64 JRE |
| `JavaEspañol.jar` | español 이름으로 Archivo·Caracteres·Comunicación·Tarea·화면을 사용하는 Java biblioteca |
| `manifest.json`, `java-runtimes.json` | construirImagen/런타임 SHA256, 아키텍처와 구성 |
| `packages.lock.json`, `sources.lock.json` | datosEfectivo 설치된 패키지 버전·valorOrigen·라이선스 informaciónSistema |

JDK/JRE는 이 실행판과 같은 **Linux ARM64 + musl** 환경용이다. 다른 libc/CPU/운영체제에서 단독 실행을 보장하지 않는다. 네이티브 의존 라이브러리는 SistemaOperativo 이미지에 함께 들어 있다. JRE는 Java SE와 문자셋·다국어·valorContraseña·ZIP SistemaArchivo 등 valorSelección 모듈을 포함하고, 전체 desarrollo 도구는 JDK에 있다.

## 설치와 ejecutarComando

1. Raspberry Pi Imager의 Usuario valorAsignar construirImagen 기능으로 `jkoros-rpi4-system.img`를 microSD에 기록한다.
2. **별도 USB dispositivoAlmacenamiento**에 `jkoros-user.img`를 기록한다. 이미지가 4 GiB이므로 그보다 큰 장치가 필요하다. 장치의 기존 데이터는 construirImagen registroEntradaDiario 시 지워진다.
3. microSD와 USB Datos Dispositivo, HDMI Pantalla, USB 키보드·마우스를 Raspberry Pi 4에 연결하고 부팅한다.
4. Usuario 이름은 `user`, 홈은 `/home/user`, UID는 1000이다. 로컬 콘솔은 자동 로그인하며, `sudo`로 desarrollo Herramientas·시스템 패키지를 설치할 númeroValor 있다. SSH 서버는 valorPredeterminado 제공하지 않는다.

valorArchivoComprimido 파일을 받은 경우 먼저 `gzip -dk nombreEntradaElementoArchivo.img.gz`로 풀어 기록할 númeroValor 있다. valorDistribución 파일이 construirTodos 같은 폴더에 있으면 `sha256sum -c SHA256SUMS`로 무결성을 확인한다.

Arranque 프로그램은 Datos 장치의 ext4 라벨 `JKDATA`를 찾는다. Datos 장치가 없으면 오류와 recuperarEstadoValor 셸을 표시하며 **자동 포맷하지 않는다**. elementoListaInicialValor 부팅하면 `/home/user/workspace/Saludo.java`operandoPrimero 준비된다. `Ctrl+Space`로 textoHangul 입력을 전환한다. 작업마당의 compilarFuente·ejecutarComando 단추나 명령창에서 `javac`, `java`, `python3`, `gcc`, `jclassc`를 사용한다.

valorCableado 네트워크는 DHCP로 구성한다. Wi-Fi는 `/home/user/.config/jkoros/wifi.conf`에 `wpa_supplicant` 설정을 넣고 Archivo 권한을 600으로 설정한 valorLadoPosterior 재부팅한다. 국가 코드와 SSID·인증 방식은 사용하는 무선망에 맞춰 지정한다. elementoListaActual valorObjetivo 인터페이스는 `wlan0`이다.

인터넷 conectar estadoValorDespués NTP로 시간을 맞춘다. Pi 4에 별도 RTC가 없을 때는 elementoListaElementoPrevio programaSalir valorMarcaTiempo 또는 construirImagen construirSistema 시각에서 시작하므로, HTTPS 이용 valorAntes datosEfectivo 시각이 맞는지 확인한다. valorEditar 창을 닫아도 ventana 관리자는 procesamientoContinuar 실행된다.

esNormal 종료는 `sudo poweroff`operandoTercero. Arranque 파티션의 `cmdline.txt`에 `jkoros.desktop=off`를 추가하면 그래픽 환경을 시작하지 않는다. valorSerie 콘솔은 GPIO UART이며 Bluetooth 대신 PL011을 사용하도록 설정했다.

## elementoListaActual PC의 QEMU에서 그래픽 ejecutarComando

이미 ejecutarComando 중인 QEMU가 있다면 게스트에서 `sudo poweroff`로 종료한다. 같은 Datos 이미지를 두 QEMU에서 동시에 열지 않는다. Anfitrión 터미널에서 다음을 실행한다.

```sh
cd /home/user/jkoros/platforms/rpi4
make run
```

다른 **Anfitrión terminal**에서 화면에 연결한다. elementoListaActual PC에 Remmina가 설치되어 있다.

```sh
remmina -c /home/user/jkoros/platforms/rpi4/build/qemu-5901.remmina
```

처음에는 화면이 검을 númeroValor 있다. x86 PC에서 ARM64를 소프트웨어로 에뮬레이션하므로 Java와 다국어 valorFuenteTipográfica 초기화에 몇 분이 걸릴 númeroValor 있다. 부팅과 Java EspacioTrabajo 초기화가 끝나면 데스크톱과 터미널이 표시된다. **VNC Pantalla 안의 terminal**에서 실행한다.

```sh
cd ~/workspace
javac Saludo.java
java Saludo
```

`make run`은 기존 `build/manual-user.img`를 사용하고, 없을 때만 새 2 GiB Datos 이미지를 만든다. 다른 Datos 이미지는 `python3 tools/run_qemu.py --data /ruta/Datos.img`로 지정한다. VNC는 호스트의 `127.0.0.1:5901`에서만 수신한다. 포트가 valorUsar 중이면 `--vnc-port 5902`로 변경하고 생성된 `build/qemu-5902.remmina`에 연결한다. esNormal 종료는 게스트에서 `sudo poweroff`operandoTercero. Remmina 창을 닫아도 QEMU는 procesamientoContinuar 실행된다.

기존 `-display none`과 `jkoros.desktop=off` 조합은 그래픽 장치와 X 서버가 없는 terminal 전용 실행이다. 이 상태에서 `JFrame`을 만들면 `HeadlessException`이 발생한다. `DISPLAY=:0`만 지정하거나 `-Djava.awt.headless=false`만 추가해도 X 서버가 생기지는 않는다.

새 실행기는 가상 그래픽 카드·USB 키보드·마우스를 연결하고 QEMU 전용 initramfs에서 드라이버를 미리 로딩한다. 기존 시스템 이미지와 `base-id`를 그대로 사용하므로 **이번 modificarValor 적용에 `make image`operandoSegundo Datos construirImagen 재생성은 필요하지 않다**. valorPredeterminado valorSerie 터미널로만 사용하려면 `make run-console`을 사용한다.

그래픽으로 부팅한 valorLadoPosterior **valorSerie 콘솔에서** Swing 창을 VNC 화면으로 열고 싶다면 다음처럼 conexión 정보도 지정한다.

```sh
export DISPLAY=:0
export XAUTHORITY=/run/user/1000/Xauthority
cd ~/workspace
java Saludo
```

이 설정은 `make run`으로 X 서버가 실행된 상태에서만 유효하다. fuente Ejemplos `JavaEspañol/Ejemplos/Saludo.java`에는 화면이 없으면 terminal 결과만 출력하는 분기도 추가했다. 이미 Usuario 폴더에 저장된 예제는 자동으로 덮어쓰지 않는다.

`make test-desktop`은 별도 Datos 이미지에서 datosEfectivo Xorg/VNC 화면과 USB 키보드·마우스 입력을 Swing으로 검사한다. Anfitrión Python의 Pillow가 필요하며 결과와 Pantalla 캡처는 `build/verification/desktop*`에 저장된다. 기존 `make test`의 Swing 시험은 Xvfb를 사용하는 별도 자동 시험이다.

### textoHangul 입력과 valorFuenteTipográfica

ejecutarComando 중인 게스트에서 `sudo poweroff`한 elementoListaSiguiente, 호스트에서 valorReintentar `make run`하고 valorExtremoSuperior Remmina 파일로 연결하면 입력기·valorFuenteTipográfica 수정이 적용된다. 기존 `build/manual-user.img`와 시스템 이미지를 그대로 사용한다. `make image`operandoSegundo Datos construirImagen 초기화는 필요하지 않다.

VNC Pantalla 안의 터미널이나 Java 편집기를 클릭하고 **Ctrl+Space**로 한·영을 전환한다. **한/operandoCero valorTecla**도 등록되어 있다. valorPredeterminado textoHangul 배열은 두벌식이다. `gksrmf` 키를 누르면 `textoHangul`이 입력된다. Anfitrión 입력기는 영문 상태로 두고 게스트의 입력기로 조합한다. 호스트가 Ctrl+Space를 먼저 처리한다면 VNC 클라이언트의 키보드 잡기 기능을 사용한다.

Caracteres 로케일은 `ko_KR.UTF-8`, 입력기는 Fcitx5의 Hangul/XIM이다. 입력기 응답을 확인한 estadoValorDespués 터미널과 Java를 실행한다. 터미널은 영문에 DejaVu Sans Mono, 한글에 Noto Sans Mono CJK KR을 사용하며, Java 작업마당은 16 크기의 textoCuerpo 글꼴과 안티앨리어싱을 사용한다. 새 X 터미널은 `jkoros-terminal`로 valorColumna númeroValor 있다. terminal valorFuenteTipográfica 크기는 `jkoros-terminal -fs 14`처럼 지정할 númeroValor 있다. colorPíxel 등 개인 X 리소스 설정은 `~/.Xresources`에서 읽는다.

QEMU 실행기가 전달하는 modificarValor 파일은 Usuario 자료의 시스템 변경분에 저장된다. 교체 valorAntes 시스템 파일은 `~/.jkoros/desktop-updates/`, 기존 Fcitx 설정과 Java valorFuenteTipográfica 캐시는 `~/.local/state/jkoros/desktop-settings/`에 보관한다. Tarea 중인 문서와 설치한 프로그램은 유지한다. 같은 modificarValor 버전은 재부팅 때 valorIteración 적용하지 않아 이후의 개인 설정을 보존한다. 향후 `make image`로 새 이미지를 빌드할 때도 같은 valorPredeterminado 설정이 포함된다.

`make test-korean`은 별도 Pruebas Datos 이미지에서 datosEfectivo VNC valorTecla 입력으로 Swing과 xterm에 `textoHangul valorEntrada`을 조합하고, UTF-8 Archivo valorAlmacenar 결과를 확인한다. 결과와 Pantalla 캡처는 `build/verification/korean*`에 저장한다.

ajustes 근거: [Fcitx의 XIM·로케일 Guía](https://fcitx-im.org/wiki/Input_method_related_environment_variables/en), [xterm의 valorFuenteTipográfica·입력기 옵션](https://invisible-island.net/xterm/manpage/xterm.html).

## 시스템과 Usuario entorno 분리

```text
microSD: firmware + kernel + initramfs + immutable system
USB(ext4, JKDATA): /user  → ejecutarComando 중 /home/user
  ├── workspace, .config, .local, .venvs, Usuario Archivo
  └── .jkoros/system/
        ├── base-id      같은 시스템 이미지인지 verificar
        ├── upper/       /usr, /opt, /etc, 패키지 DB 등 모든 시스템 변경분
        └── work/        OverlayFS Tarea valorRegión
```

시스템 valorPredeterminado 파일은 leer 전용이다. `sudo apk add Programa`으로 설치한 Archivo, 패키지 데이터베이스, `/etc` ajustes, 기존 파일의 삭제 정보도 Usuario 폴더의 OverlayFS 변경분에 들어간다. 따라서 일반 Usuario 파일과 Usuario instalarValor 프로그램을 함께 옮길 númeroValor 있다. `/run`, `/tmp`, `/dev/shm`은 일시 자료다.

**valorMover condición:** 양쪽의 시스템 construirImagen `base-id`, ARM64 아키텍처, Usuario ruta `/home/user`, UID 1000이 같아야 한다. Arranque 시 construirImagen 식별자를 검사하며 다르면 해당 변경분을 임의로 적용하지 않는다. 이 버전은 서로 다른 시스템 버전 사이의 자동 마이그레이션을 제공하지 않는다.

두 운영체제를 esNormal 종료하고 다른 Linux에서 Datos 장치를 마운트한 valorLadoPosterior, 새 Datos 장치에 `user` 폴더가 없는 상태에서 다음처럼 복사한다.

```sh
sudo cp -a /media/OLD/user /media/NEW/
sync
```

ejecutarComando 중에는 이 폴더가 `/home/user`로 보인다. 반드시 valorOculto Archivo, 심볼릭 링크, 소유권, valorPermiso, valorExtensión valorAtributo, OverlayFS 삭제 정보를 보존해야 한다. ext4 사이의 valorMover 또는 Linux의 `sudo cp -a`/적절한 tar 보관을 사용한다. FAT/exFAT에 일반 폴더로 복사하면 이 정보가 보존되지 않는다. `user`를 기존 환경과 병합하지 않는다.

`jkoros-environment info`는 elementoListaActual 환경의 식별자를 보여준다. esSinConexión 보관은 다른 Linux에서 `sudo python3 runtime/environment export --home /media/OLD/user --output /backup/user.tar`로 수행한다. 복원은 빈 대상에서 `sudo tar --xattrs --acls --numeric-owner -xpf /backup/user.tar -C /media/NEW`operandoTercero.

이 구조는 환경의 휴대성을 위한 것이다. 호스트와 격리하는 보안 샌드박스는 아니다. 별도 valorExterno 디스크·valorRemoto 서비스의 Datos, Arranque 펌웨어 변경은 `/home/user` 이동에 포함되지 않는다.

## Programa instalarValor

español Java 라이브러리는 `/opt/jkoros/lib/JavaEspañol.jar`에 있다. Archivo·Caracteres·Comunicación·스레드·Swing valorAyudante 22개 메서드와 Java 작업마당의 사용법은 [español biblioteca GuíaUsuario](../../JavaEspañol/GuíaUsuario.md)를 참고한다. Python의 Java 프로세스 invocar, C++의 JNI 직접 invocar 예제와 añadirFinalEntradaElemento 설치가 필요한 Python conectar 방식도 구분해 설명한다.

```sh
sudo apk update
sudo apk add tree
python3 -m virtualenv ~/.venvs/dev
. ~/.venvs/dev/bin/activate
pip install 패키지이름
```

Python 가상환경, 직접 빌드한 Programa, Usuario 설정도 `/home/user`에 둔다. 시스템에 설치하는 패키지도 변경분이 같은 폴더에 보관된다.

## 빌드와 Pruebas

Linux x86-64 construirSistema 호스트에서 Python 3, curl, JDK 11 이상, GNU C Compilador, make, kmod, squashfs-tools, dosfstools, mtools, e2fsprogs가 필요하다. 일반 construirImagen 빌드는 root 권한이나 datosEfectivo 디스크 접근을 사용하지 않는다.

```sh
make prepare       # 서명된 ARM64 패키지와 Pi 공식 펌웨어 확보
make prepare-host  # 프로젝트 내부에 valorÚltimoReciente QEMU·jlink·proot 확보
make runtimes      # ARM64 JRE 구성 및 JDK/JRE 아카이브 generar
make image         # SistemaOperativo construirImagen generar; 기존 Usuario 이미지는 retenerValor
make test          # ARM64 Arranque/ejecutarComando/재부팅/esSinConexión 홈 valorMover Pruebas
make verify        # Pi construirImagen 구조와 ARM64 JDK/JRE validar
make release       # instalarValor construirImagen valorArchivoComprimido 및 SHA256SUMS generar
```

`proot`는 ptrace가 허용된 construirSistema 환경에서 실행한다. 패키지 검증을 끄는 옵션은 사용하지 않는다. 버전 고정 저장소의 패키지 갱신에 따라 elementoListaSiguiente construirSistema 결과는 달라질 númeroValor 있으며, valorDistribución 이미지의 datosEfectivo 버전과 해시는 valorCerrojo 파일에 기록한다.

Pruebas 결과는 `build/verification/`에 있다. QEMU `virt` 시험은 같은 ARM64 Usuario entorno·estadoValorInicialValor Arranque valorCódigo·valorAlmacenar 구조를 검증하지만, datosEfectivo Pi 4의 HDMI·USB·Wi-Fi·SD 드라이버 동작을 대신 검증하지 않는다. 이 저장소에 datosEfectivo Pi 4 보드를 연결한 Arranque 결과는 아직 없다.

valorDistribución 결과와 validar 범위는 [VERIFICATION.md](VERIFICATION.md)를 참조한다. 컴파일러의 OpenJDK ejecutarComando Archivo 방식과 제약은 [Compilador Guía](../../compiler/OpenJDK-archivoCódigoEjecutable.md)에 설명되어 있다.
