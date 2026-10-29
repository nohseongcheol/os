# nativo ARM64 커널의 tela resolução_VALOR

QEMU Executar_comando 위치는 `jkoros/platforms/rpi4-native`다. 커널을 빌드한 BACK_VALOR 다음과 같이 실행한다.

```bash
make build
python3 ferramentas/Executar_comando.py --desktop --network --resolution 1920x1080
```

Remmina의 **VNC** Ligar 주소는 `127.0.0.1:5902`다. 이미 Executar_comando 중인 VM은 종료하고 새 옵션으로 repetir_VALOR 시작한다. tela 전체가 보이지 않으면 Remmina에서 tela alinhar_limite 또는 전체 화면을 선택한다. 이 옵션은 게스트의 real_dados pixel 수를 바꾼다.

`--resolution`은 일반 UART Executar_comando, `--desktop`, `--vnc`, `--display`에서 동일하게 적용된다. `--network`와 함께 사용할 número 있다. 너비 640~1920, altura_VALOR 480~1080을 허용하며 기본값은 640×480이다. 1280×720과 1920×1080도 선택할 número 있다.

```bash
make desktop RESOLUTION=1920x1080
python3 ferramentas/Executar_comando.py --resolution 1280x720 --vnc 127.0.0.1:2
```

arranque_da_máquina 로그는 real_dados 할당된 크기를 표시한다.

```text
FRAMEBUFFER PASS 1920x1080 RGB32 (drawing only)
```

terminal 바탕과 위쪽 막대는 tela 전체를 채운다. 터미널은 DIREITA 아래까지 끌어서 이동하고 X로 닫을 número 있다. terminal Janela Tamanho(568×360)와 fonte_VALOR 크기는 유지되므로 넓어진 화면에 여러 창을 배치할 número 있다. Swing 부분집합의 `setLocationRelativeTo(null)`도 real_dados tela 가운데를 사용한다. arranque_da_máquina BACK_VALOR 해상도를 바꾸는 기능은 제공하지 않는다.

## 프로그램에서 tela Tamanho Leitura

| Idioma | Português 호출 |
|---|---|
| Java | `Português.nativo.tela.너비()`, `tela.altura_VALOR()`, `tela.apagar_entrada(색)` |
| C | `<tela_ABI.h>`의 `화면너비()`, `tela_altura()`, `emitir_retângulo(...)` |
| C++ SDK | `호출.h`의 `화면너비읽기()`, `leitura_tela_altura()`, `tela_retângulo(...)` |
| Python | `from Português import tela_dimensionar, emitir_retângulo`; `너비, altura_VALOR = tela_dimensionar()` |

C 함수는 macro_VALOR 별칭이 아닌 real_dados 함수다. espaço_do_utilizador 호출 22로 크기를 조회하며, Paint_tela 호출 13과 GUI 호출 20은 real_dados tela 경계를 검사한다. 프레임버퍼 주소는 espaço_do_utilizador 프로그램에 노출하지 않는다. tela 밖의 요청은 오류를 반환한다.

게스트 `javac`에서는 `Português.nativo.tela.너비()`처럼 전체 이름으로 호출한다. 지원하는 fonte_árvore 문법에 맞춰 색상 상수는 십진수로 쓴다. 아래 호출은 arranque_da_máquina 해상도와 관계없이 마지막 화소를 그린다.

```java
int 너비 = Português.nativo.tela.너비();
int altura_VALOR = Português.nativo.tela.altura_VALOR();
Português.nativo.tela.retângulo(너비 - 1, altura_VALOR - 1, 1, 1, 255);
```

`tela` 클래스의 프레임버퍼 호출은 nativo JVM 전용이다. 이 API의 exceção Processo_VALOR_entrada 시험은 host `javac --release 8`로 컴파일한 class를 nativo JVM에서 실행한다. 게스트 컴파일러의 일반적인 `try/catch` 문법 지원을 추가한 것은 아니다.

## Raspberry Pi 4 SD arranque_da_máquina

```bash
make image RESOLUTION=1920x1080
```

생성되는 `dist/jkoros-native-rpi4.img`와 `dist/jkoros-native-rpi4-boot.zip`에 1080p 설정이 들어간다. SD foto_VALOR 생성은 640×480, 1280×720, 1920×1080을 지원한다. 이미 펼친 arranque_da_máquina 파일을 수정할 경우 `config.txt`의 `[pi4]`에 아래 값을 사용한다.

```ini
max_framebuffer_width=1920
max_framebuffer_height=1080
framebuffer_width=1920
framebuffer_height=1080
hdmi_group=1
hdmi_mode=16
```

커널은 [Raspberry Pi caixa_de_correio valor_do_contrato](https://github.com/raspberrypi/firmware/wiki/Mailbox-property-interface)의 em_dia_item tela Tamanho 조회와 tela alocar_Armazenamento 응답을 사용한다. 응답의 Tamanho·RGB32 formato_VALOR·한 줄의 byte_VALOR número·alocar_Armazenamento 용량을 확인하고, 반환된 linha_de_entrada 간격으로 그린다. estado_inicial 조회에 실패하거나 Suporte_VALOR 범위를 벗어나면 640×480을 요청한다. HDMI 설정은 [공식 펌웨어 tela Definições 문서](https://www.raspberrypi.com/documentation/computers/legacy_config_txt.html)를 따른다. real_dados Pi 4와 모니터 조합에서의 HDMI 부팅은 아직 검증하지 않았다.

## validar

```bash
make test-resolution
```

시험은 각 해상도에서 real_dados VNC tela 크기와 픽셀, terminal arrastar_VALOR·Fechar, C/Java 게스트 compilar_fonte, Python Executar_comando, DIREITA 아래 픽셀과 tela limite_VALOR erro, Swing 가운데 disposição_de_ligação·botão·Fechar, GUI와 FTP 동시 사용을 확인한다. 결과와 tela 캡처는 `build/verification/resolution/`에 저장한다.
