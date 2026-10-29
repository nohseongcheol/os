# interne ARM64 커널의 Écran valeurRésolution

QEMU exécuterCommande 위치는 `jkoros/platforms/rpi4-native`opérandeTroisième. 커널을 빌드한 valeurRetourArrièreCôté 다음과 같이 실행한다.

```bash
make build
python3 Outils/exécuterCommande.py --desktop --network --resolution 1920x1080
```

Remmina의 **VNC** connecter 주소는 `127.0.0.1:5902`opérandeTroisième. 이미 exécuterCommande 중인 VM은 종료하고 새 옵션으로 valeurRéessayer 시작한다. Écran 전체가 보이지 않으면 Remmina에서 Écran frontièreAligner 또는 전체 화면을 선택한다. 이 옵션은 게스트의 donnéesEffectif pixel 수를 바꾼다.

`--resolution`은 일반 UART exécuterCommande, `--desktop`, `--vnc`, `--display`에서 동일하게 적용된다. `--network`와 함께 사용할 nombre 있다. valeurLargeur 640~1920, valeurHauteur 480~1080을 허용하며 기본값은 640×480이다. 1280×720과 1920×1080도 선택할 nombre 있다.

```bash
make desktop RESOLUTION=1920x1080
python3 Outils/exécuterCommande.py --resolution 1280x720 --vnc 127.0.0.1:2
```

Amorçage 로그는 donnéesEffectif 할당된 크기를 표시한다.

```text
FRAMEBUFFER PASS 1920x1080 RGB32 (drawing only)
```

terminal 바탕과 côtéSupérieur 막대는 Écran 전체를 채운다. 터미널은 droit 아래까지 끌어서 이동하고 X로 닫을 nombre 있다. terminal fenêtre taille(568×360)와 valeurPolice 크기는 유지되므로 넓어진 화면에 여러 창을 배치할 nombre 있다. Swing 부분집합의 `setLocationRelativeTo(null)`도 donnéesEffectif Écran 가운데를 사용한다. Amorçage valeurRetourArrièreCôté 해상도를 바꾸는 기능은 제공하지 않는다.

## 프로그램에서 Écran taille lire

| Langue | français invoquer |
|---|---|
| Java | `français.interne.Écran.valeurLargeur()`, `Écran.valeurHauteur()`, `Écran.effacerEntréeÉlément(valeurCouleur)` |
| C | `<ABIÉcran.h>`의 `largeurÉcran()`, `hauteurÉcran()`, `dessinerRectangle(...)` |
| C++ SDK | `invoquer.h`의 `lireLargeurÉcran()`, `lireHauteurÉcran()`, `rectangleÉcran(...)` |
| Python | `from français import tailleÉcran, dessinerRectangle`; `valeurLargeur, valeurHauteur = tailleÉcran()` |

C 함수는 valeurMacro 별칭이 아닌 donnéesEffectif 함수다. Utilisateur invoquer 22로 크기를 조회하며, écranPeindre invoquer 13과 GUI invoquer 20은 donnéesEffectif Écran 경계를 검사한다. 프레임버퍼 주소는 Utilisateur 프로그램에 노출하지 않는다. Écran 밖의 요청은 오류를 반환한다.

게스트 `javac`에서는 `français.interne.Écran.valeurLargeur()`처럼 전체 이름으로 호출한다. 지원하는 arbreSource 문법에 맞춰 couleurPixel 상수는 십진수로 쓴다. valeurBasExtrémité 호출은 Amorçage 해상도와 관계없이 élémentListeDernier 화소를 그린다.

```java
int valeurLargeur = français.interne.Écran.valeurLargeur();
int valeurHauteur = français.interne.Écran.valeurHauteur();
français.interne.Écran.rectangle(valeurLargeur - 1, valeurHauteur - 1, 1, 1, 255);
```

`Écran` 클래스의 프레임버퍼 호출은 interne JVM 전용이다. 이 API의 exception entréeÉlémentValeurProcessus 시험은 Hôte `javac --release 8`로 컴파일한 class를 interne JVM에서 실행한다. 게스트 컴파일러의 일반적인 `try/catch` 문법 지원을 추가한 것은 아니다.

## Raspberry Pi 4 SD Amorçage

```bash
make image RESOLUTION=1920x1080
```

생성되는 `dist/jkoros-native-rpi4.img`와 `dist/jkoros-native-rpi4-boot.zip`에 1080p 설정이 들어간다. SD valeurImage 생성은 640×480, 1280×720, 1920×1080을 지원한다. 이미 펼친 Amorçage 파일을 수정할 경우 `config.txt`의 `[pi4]`에 valeurBasExtrémité 값을 사용한다.

```ini
max_framebuffer_width=1920
max_framebuffer_height=1080
framebuffer_width=1920
framebuffer_height=1080
hdmi_group=1
hdmi_mode=16
```

커널은 [Raspberry Pi boîteMessages valeurContrat](https://github.com/raspberrypi/firmware/wiki/Mailbox-property-interface)의 élémentListeActuel Écran taille 조회와 Écran allouerStockage 응답을 사용한다. 응답의 taille·RGB32 valeurFormat·한 줄의 valeurOctet nombre·allouerStockage 용량을 확인하고, 반환된 ligne 간격으로 그린다. étatValeurInitialValeur 조회에 실패하거나 valeurPriseEnCharge 범위를 벗어나면 640×480을 요청한다. HDMI 설정은 [공식 펌웨어 Écran réglages Documentation](https://www.raspberrypi.com/documentation/computers/legacy_config_txt.html)를 따른다. donnéesEffectif Pi 4와 모니터 조합에서의 HDMI 부팅은 아직 검증하지 않았다.

## valider

```bash
make test-resolution
```

시험은 각 해상도에서 donnéesEffectif VNC Écran 크기와 픽셀, terminal valeurGlisser·fermer, C/Java 게스트 compilerSource, Python exécuterCommande, droit valeurBasExtrémité 픽셀과 Écran valeurFrontière erreur, Swing milieu DispositionLiens·bouton·fermer, GUI와 FTP 동시 사용을 확인한다. 결과와 Écran 캡처는 `build/verification/resolution/`에 저장한다.
