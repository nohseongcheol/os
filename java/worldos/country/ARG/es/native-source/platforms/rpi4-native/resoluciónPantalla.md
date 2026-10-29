# propio ARM64 커널의 Pantalla valorResolución

QEMU ejecutarComando 위치는 `jkoros/platforms/rpi4-native`operandoTercero. 커널을 빌드한 valorLadoPosterior 다음과 같이 실행한다.

```bash
make build
python3 Herramientas/ejecutarComando.py --desktop --network --resolution 1920x1080
```

Remmina의 **VNC** conectar 주소는 `127.0.0.1:5902`operandoTercero. 이미 ejecutarComando 중인 VM은 종료하고 새 옵션으로 valorReintentar 시작한다. Pantalla 전체가 보이지 않으면 Remmina에서 Pantalla fronteraAlinear 또는 전체 화면을 선택한다. 이 옵션은 게스트의 datosEfectivo píxel 수를 바꾼다.

`--resolution`은 일반 UART ejecutarComando, `--desktop`, `--vnc`, `--display`에서 동일하게 적용된다. `--network`와 함께 사용할 númeroValor 있다. valorAnchura 640~1920, valorAltura 480~1080을 허용하며 기본값은 640×480이다. 1280×720과 1920×1080도 선택할 númeroValor 있다.

```bash
make desktop RESOLUTION=1920x1080
python3 Herramientas/ejecutarComando.py --resolution 1280x720 --vnc 127.0.0.1:2
```

Arranque 로그는 datosEfectivo 할당된 크기를 표시한다.

```text
FRAMEBUFFER PASS 1920x1080 RGB32 (drawing only)
```

terminal 바탕과 ladoSuperior 막대는 Pantalla 전체를 채운다. 터미널은 derecho 아래까지 끌어서 이동하고 X로 닫을 númeroValor 있다. terminal ventana tamaño(568×360)와 valorFuenteTipográfica 크기는 유지되므로 넓어진 화면에 여러 창을 배치할 númeroValor 있다. Swing 부분집합의 `setLocationRelativeTo(null)`도 datosEfectivo Pantalla 가운데를 사용한다. Arranque valorLadoPosterior 해상도를 바꾸는 기능은 제공하지 않는다.

## 프로그램에서 Pantalla tamaño leer

| Lengua | español invocar |
|---|---|
| Java | `español.propio.Pantalla.valorAnchura()`, `Pantalla.valorAltura()`, `Pantalla.borrarEntradaElemento(valorColor)` |
| C | `<ABIPantalla.h>`의 `anchuraPantalla()`, `alturaPantalla()`, `dibujarRectángulo(...)` |
| C++ SDK | `invocar.h`의 `leerAnchuraPantalla()`, `leerAlturaPantalla()`, `rectánguloPantalla(...)` |
| Python | `from español import tamañoPantalla, dibujarRectángulo`; `valorAnchura, valorAltura = tamañoPantalla()` |

C 함수는 valorMacro 별칭이 아닌 datosEfectivo 함수다. Usuario invocar 22로 크기를 조회하며, pantallaPintar invocar 13과 GUI invocar 20은 datosEfectivo Pantalla 경계를 검사한다. 프레임버퍼 주소는 Usuario 프로그램에 노출하지 않는다. Pantalla 밖의 요청은 오류를 반환한다.

게스트 `javac`에서는 `español.propio.Pantalla.valorAnchura()`처럼 전체 이름으로 호출한다. 지원하는 árbolFuente 문법에 맞춰 colorPíxel 상수는 십진수로 쓴다. valorExtremoInferior 호출은 Arranque 해상도와 관계없이 elementoListaÚltimo 화소를 그린다.

```java
int valorAnchura = español.propio.Pantalla.valorAnchura();
int valorAltura = español.propio.Pantalla.valorAltura();
español.propio.Pantalla.rectángulo(valorAnchura - 1, valorAltura - 1, 1, 1, 255);
```

`Pantalla` 클래스의 프레임버퍼 호출은 propio JVM 전용이다. 이 API의 excepción entradaElementoValorProceso 시험은 Anfitrión `javac --release 8`로 컴파일한 class를 propio JVM에서 실행한다. 게스트 컴파일러의 일반적인 `try/catch` 문법 지원을 추가한 것은 아니다.

## Raspberry Pi 4 SD Arranque

```bash
make image RESOLUTION=1920x1080
```

생성되는 `dist/jkoros-native-rpi4.img`와 `dist/jkoros-native-rpi4-boot.zip`에 1080p 설정이 들어간다. SD valorImagen 생성은 640×480, 1280×720, 1920×1080을 지원한다. 이미 펼친 Arranque 파일을 수정할 경우 `config.txt`의 `[pi4]`에 valorExtremoInferior 값을 사용한다.

```ini
max_framebuffer_width=1920
max_framebuffer_height=1080
framebuffer_width=1920
framebuffer_height=1080
hdmi_group=1
hdmi_mode=16
```

커널은 [Raspberry Pi buzón valorContrato](https://github.com/raspberrypi/firmware/wiki/Mailbox-property-interface)의 elementoListaActual Pantalla tamaño 조회와 Pantalla asignarMemoriaAlmacenamiento 응답을 사용한다. 응답의 tamaño·RGB32 valorFormato·한 줄의 valorByte númeroValor·asignarMemoriaAlmacenamiento 용량을 확인하고, 반환된 línea 간격으로 그린다. estadoValorInicialValor 조회에 실패하거나 valorSoporte 범위를 벗어나면 640×480을 요청한다. HDMI 설정은 [공식 펌웨어 Pantalla ajustes Documentación](https://www.raspberrypi.com/documentation/computers/legacy_config_txt.html)를 따른다. datosEfectivo Pi 4와 모니터 조합에서의 HDMI 부팅은 아직 검증하지 않았다.

## validar

```bash
make test-resolution
```

시험은 각 해상도에서 datosEfectivo VNC Pantalla 크기와 픽셀, terminal valorArrastrar·cerrar, C/Java 게스트 compilarFuente, Python ejecutarComando, derecho valorExtremoInferior 픽셀과 Pantalla valorFrontera error, Swing medio DisposiciónEnlace·botón·cerrar, GUI와 FTP 동시 사용을 확인한다. 결과와 Pantalla 캡처는 `build/verification/resolution/`에 저장한다.
