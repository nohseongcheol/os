# interne 커널의 GUI 터미널과 interpréteurCommandes

이 터미널은 interne Java 커널의 셸을 프레임버퍼 창과 UART에서 사용한다. commande entréeÉlémentValeurProcessus·RAM Fichier·파이프는 Java valeurNoyau, 화면의 valeurCaractère 그리기는 freestanding C에서 수행한다. Linux·X11·Bash 없이 동작하며, interne JVM의 Swing valeurPriseEnCharge 부분집합도 같은 fenêtre 시스템을 이용한다. 자세한 vi·다중 fenêtre·코딩 사용법은 [développement 매뉴얼](GuideDéveloppement.md)을 참고한다.

## élémentListeActuel 컴퓨터에서 exécuterCommande

```sh
cd /home/user/jkoros/platforms/rpi4-native
make desktop
```

Remmina에서 **VNC**, adresse **127.0.0.1:5902**로 연결한다. terminal 창은 자동으로 열린다. 연결한 VNC 창에 키를 입력하면 interne 커널의 셸로 전달된다. 종료하려면 `make desktop`을 실행한 Hôte 터미널에서 Ctrl+C를 누른다. 포트를 바꾸려면 construireSystème étatValeurAprès `python3 Outils/exécuterCommande.py --desktop --port 5903`을 사용한다. 서버는 localhost에만 바인드하며 동시에 한 클라이언트가 제어한다.

일반 UART 셸은 `make run`으로 시작한다. QEMU 종료는 Ctrl+A élémentListeSuivant X이다. 같은 VM의 UART에서 `terminal` 또는 F12로 GUI 터미널을 valeurColonne nombre 있다. `gui` exécuterCommande 화면에서는 다섯 번째 **OPEN TERMINAL** 버튼, valeurChiffre 5 또는 T로 연다. `--vnc 127.0.0.1:2`만 사용한 기존 exécuterCommande 방식은 Écran 보기용이며, VNC 키보드를 연결하려면 `--desktop`을 사용한다.

FTP와 valeurExtérieur 네트워크도 함께 쓰려면 `python3 Outils/exécuterCommande.py --desktop --network`로
실행한다. Remmina VNC는 `127.0.0.1:5902`, 게스트에서 `ftpd start` étatValeurAprès FTP는
`127.0.0.1:2121`이다. `--port`, `--ftp-port`, `--forward`를 함께 지정할 nombre 있다.
한 VM의 valeurAuxiliaire UART로 SLIP를 전송하고 주 UART로 GUI 입력을 전달한다.

QEMU exécuterCommande 도구가 VNC 키보드/마우스를 UART 입력으로 변환한다. donnéesEffectif Pi4의 USB 키보드·마우스 드라이버를 구현한 것은 아니다. donnéesEffectif 보드에서는 élémentListeActuel UART 입력이 필요하며 matérielPhysique 부팅은 아직 미검증이다.

## 창과 valeurEntrée

- 640×480~1920×1080 화면에서 valeurMaximal 네 개 terminal fenêtre, valeurDéfaut 568×360(68열 × 19행)과 valeurRécent 160행 préserverValeur, valeurDéfaut ANSI couleurPixel·valeurCurseur·effacerEntréeÉlément entréeÉlémentValeurProcessus.
- 상단 **+ New terminal** 또는 Ctrl+Shift+T로 새 창을 연다. 제목줄을 끌어 이동하고 fenêtre/상단 버튼을 클릭하거나 F6으로 전환한다. 각 창의 Tâche chemin·valeurVariable·commande enregistrementJournal·valeurEntrée 중인 줄은 독립적이다.
- UTF-8 texteHangul·CJK·라틴 문자와 일부 이모지 비트맵 valeurPolice. 복잡한 Caractères 조판·valeursCombiner Caractères·양방향 DispositionLiens·모든 Unicode 글리프를 보장하지 않는다.
- 좌우 방향키/Home/End/Delete/Backspace로 명령을 편집하고 위아래 방향키로 valeurRécent 16개 명령을 찾는다. 긴 명령은 valeurEntrée 줄을 가로로 이동해 보여 주며 `<`, `>`opérandePremier 숨겨진 부분을 나타낸다.
- Tab은 commande nom 또는 élémentListeActuel 디렉터리의 파일명에서 후보가 하나일 때 완성한다. 디렉터리를 포함한 chemin 접두사·guillemet 안의 완성은 아직 없다.
- Ctrl+A/E: élémentListeInitialValeur/terminaison, Ctrl+U/K: valeurCurseur valeurAvantCôté/valeurRetourArrièreCôté 삭제, Ctrl+C: valeurEntrée opérationAnnuler. exécuterCommande 중인 임의 프로그램에 SIGINT를 보내는 기능은 없다. vi와 Swing의 valeurEntrée 대기는 exécuterCommande 기한을 갱신하지만 일반 계산의 약 2초 제한은 유지한다.
- PgUp/PgDn 또는 마우스 휠: élémentListePrécédentÉlément Sortie. 새 출력이 오면 valeurDernierRécent 위치로 돌아온다.
- F12/barreTitre droit 버튼/`exit`: fenêtre fermer. 빈 입력에서 Ctrl+D도 창을 닫는다. VM을 종료하는 명령은 아니다.

`--desktop`의 VNC valeurEntrée 연결에 **두벌식 texteHangul Combinaison**을 제공한다. 접속한 PC의
입력기를 영어로 두고 **F9**, **Shift+Space**, **한/opérandeZéro valeurTouche** 중 하나를 누르면
fenêtre 제목이 `[EN]`에서 `[KO]`로 바뀐다. `gksrmf` → `texteHangul`,
`dkssudgktpdy` → `안녕하세요`. 같은 키로 영어로 돌아간다.
겹받침·복합 모음과 Combinaison 단계별 Backspace를 지원한다. valeurCurseur valeurDéplacer·마우스 valeurCliquer·
단축키·valeurColler·Enter 때 조합을 확정한다. PC가 Shift+Space나 한/opérandeZéro 키를
interne 처리하면 **F9**를 사용한다. Alt 단독은 modeCommuter 키가 아니다.

이 조합기는 QEMU의 VNC→UART valeurEntrée 연결에서 실행된다. 일반 valeurSériel 접속과
matérielPhysique Pi의 USB 키보드 입력기에 추가된 기능은 아니다. 이미 완성된 Unicode
texteHangul 키도 그대로 전달한다. 클립보드 공유가 활성화되어 표준 VNC ClientCutText가
도착하면 Ctrl+Shift+V로 붙여 넣는다. 클립보드 동기화만으로 명령을 실행하지 않는다.
줄바꿈을 포함해 명시적으로 붙여 넣으면 해당 줄이 실행된다.

게스트에서 `help` 또는 `help ko`를 입력하면 texteHangul valeurEntrée 안내를 볼 nombre 있다.
`help`와 `help ko`에는 한/opérandeZéro valeurTouche·Shift+Space·F9 및 `[EN]`/`[KO]` 안내를 표시한다.
긴 도움말은 PgUp/PgDn으로 스크롤한다.

터미널에서 Java·Python·C++ exécuterCommande 결과를 바로 볼 nombre 있다. 프로그램이 직접 프레임버퍼에 그림을 그린 경우 programmeQuitter étatValeurAprès terminal 창을 복원한다. vi/Swing attendreValeur 중 다른 창으로 전환하면 해당 EL0 프로그램의 donnéesMémoire·레지스터를 보관하고 돌아올 때 재개한다. valeurSélection copierValeur·PTY·전체 VT100/xterm 호환과 임의 프로그램의 동시 병렬 실행은 제공하지 않는다. X로 닫으면 해당 창의 프로그램도 종료되므로 vi에서 저장하지 않은 내용은 사라진다.

## commande

| commande | rogner |
|---|---|
| `help`, `info` | 사용법과 réalisation valeurÉtatValeur |
| `pwd`, `cd [DIR]`, `ls [-l] [PATH]` | élémentListeActuel chemin·디렉터리/Fichier listeEntréeÉlément; arguments 없는 cd는 `/` |
| `mkdir DIR`, `rmdir DIR` | 디렉터리 한 개 créerEntréeÉlément/빈 디렉터리 삭제; `-p` méthodeManquant |
| `touch FILE`, `rm FILE...` | Fichier créerEntréeÉlément/삭제; valeurHorodatage informationSystème méthodeManquant |
| `cp SOURCE DEST`, `mv SOURCE DEST` | Fichier copierValeur/nom changerValeur; 대상은 정확한 Fichier chemin, 재귀/디렉터리 valeurDéplacer méthodeManquant |
| `cat [FILE...]` | Fichier 또는 표준 입력을 valeurOctet 그대로 Sortie |
| `echo [-n] [ARGS...]` | arguments Sortie; `-e` 이스케이프 valeurExtension méthodeManquant |
| `wc [-c\|-l\|-w] [FILE]` | valeurOctet/ligne/valeurMot nombre; valeurMot 구분은 ASCII 공백 |
| `grep TEXT [FILE]` | 정규식 없이 문자열이 포함된 ligne Sortie; estÉgal 없으면 valeurÉtatValeur 1 |
| `head [-n N] [FILE]`, `tail [-n N] [FILE]` | valeurAvantCôté/valeurRetourArrièreCôté N줄, valeurDéfaut 10줄 |
| `tee [-a] FILE` | 표준 입력을 파일과 표준 출력에 enregistrementJournal |
| `export NAME=VALUE`, `unset NAME`, `env` | interpréteurCommandes valeurVariable réglages·삭제·listeEntréeÉlément; HOME/PWD는 lire 전용 |
| `sh FILE`, `source FILE` | commande 파일을 같은 interpréteurCommandes 환경에서 줄별 exécuterCommande; valeurMaximal valeurImbrication 3 |
| `true`, `false`, `exit [N]` | valeurÉtatValeur 0/1; valeurScript 안의 exit는 élémentListeActuel valeurScript programmeQuitter |
| `history`, `clear` | commande enregistrementJournal·Écran effacerEntréeÉlément |
| `vi FILE` | EL0 vi modeMéthode Éditeur: valeurEntrée/commande valeurMode, UTF-8 valeurDéplacer, 검색, 삭제·copierValeur·texteColler·되돌리기, `:w`/`:q`/`:wq` |
| `edit FILE`, `load FILE`, `hex FILE` | 전체 valeurContenuValeur 교체 valeurÉditer, 16진수 업로드/valeurInterroger; 단독 `.` 줄로 valeurStocker |
| `javac`, `java`, `python`, `run` | 기존 interne Java Outils·MicroPython·EL0 C++/ELF exécuterCommande |

`net test`, `tasks`, `selftest`, `samples`도 유지한다. Programme exécuterCommande 범위는 [README](Guide.md)와 [Java exécuterCommande environnement](EnvironnementEnvironnementExécutionJava.md)을 참고한다.

```sh
mkdir Tâche
cd Tâche
echo "안녕하세요" > Salutation.txt
echo "반갑습니다" >> Salutation.txt
cat < Salutation.txt | grep 안녕 | tee 추림.txt | wc -l
cp Salutation.txt copierValeur.txt
mv copierValeur.txt nomNouveau.txt
export nom=누리
echo "$이름: ${PWD}"
false && echo 건너뜀 || echo récupérerÉtatValeur
python -c 'print(123)' > résultat.txt
echo valeurEntrée | python -c 'import jkoros; print(jkoros.stdin(64))'
echo 'echo "$이름"' > exécuterCommande.sh
sh exécuterCommande.sh
echo $?
```

## 문법과 valeurLimite

작은따옴표·큰따옴표·백슬래시, `$NAME`/`${NAME}`/`$?`, valeurMot valeurAvantCôté `~`, ligne 주석 `#`, 순차 exécuterCommande `;`, condition exécuterCommande `&&`/`||`, 파이프 `|`, valeurEntrée `<`, 새 Sortie `>`, ajouterFinEntréeÉlément Sortie `>>`를 제공한다. valeurVariable 확장은 arguments 안에서 수행하며 valeurExtension 결과를 공백으로 valeurRéessayer 나누지 않는다. `export`의 값은 interpréteurCommandes 안에서만 공유하며 Utilisateur ELF의 envp/getenv 환경은 아직 없다.

파이프는 각 단계를 순서대로 실행하고 valeurMaximal **16384바이트**를 élémentListeSuivant 단계로 넘긴다. 여러 프로세스가 동시에 읽고 쓰는 POSIX 파이프가 아니다. valeurCapacité 초과는 erreur 28과 valeurÉchec 상태를 반환하고 해당 실행을 중단한다. `<`는 EOF를 제공하며 `>`/`>>`는 stdout만 바꾼다. EL0 fd 2는 Écran/UART로 출력된다. `2>` 등 번호를 붙인 리다이렉션은 거부한다. 일부 내장 명령의 진단은 stdout을 사용한다. 연결한 프로그램의 `exit N` 진단은 데이터에 섞이지 않도록 생략한다.

`vi`, `edit`, `load`, `gui`, `terminal`, `sh`, `source`에는 파이프와 리다이렉션을 적용할 nombre 없다. 리다이렉션 파일을 열지 못하거나 파이프 용량을 초과하면 élémentListeActuel 명령줄을 중단하며, 그 줄의 뒤쪽 `||` 명령도 실행하지 않는다. valeurScript 파일을 입력할 때 멀티라인 guillemet·valeurContinuation 쓰기는 제공하지 않는다. `if`/`for`/`while`, Fonction, commande 치환, glob, nomAlternatif, 백그라운드 `&`, jobs/fg/bg, 일반 프로세스·신호·PTY는 아직 없다. Bash/POSIX sh 전체 호환으로 표시하지 않는다.

Fichier 64개 × 각 16384바이트, 루트 외 디렉터리 15개, Fichier entréeÉlémentDescripteur 16개, chemin valeurMaximal UTF-8 63바이트다. valeurPairRéseau/절대 경로와 `.`/`..`를 정규화하지만 valeurPermission·심볼릭 링크·마운트·디스크 영속 저장은 없다. **Fichier·디렉터리·valeurVariable·기록의 modifierValeur 내용은 재부팅하면 사라진다.** Utilisateur 실행도 élémentListeActuel interpréteurCommandes 경로를 사용한다. Java/Python/C++의 Fichier API는 같은 RAM 저장소를 본다. `/example`의 valeurTrois Langue 예제와 설명서는 부팅할 때 원본으로 준비된다.

한 명령줄은 4096바이트, 구문 valeurJeton 128개, exécuterCommande arguments 32개, 변수는 16개(nom 31바이트·valeur 255바이트)까지다. Utilisateur 프로그램에 전달하는 인수는 기존 ABI대로 valeurMaximal 8개·각 255바이트다. commande 기록은 1024바이트 이하 줄을 valeurRécent 16개까지 저장한다.

## 재현 가능한 Tests

```sh
make test-shell
make test-desktop
make test-windows
make test-swing
make test
```

interpréteurCommandes 시험은 donnéesEffectif raspi4b QEMU에서 chemin·Fichier·valeurVariable·condition·파이프·리다이렉션·erreur récupérerÉtatValeur·valeurScript·편집을 검사하고, Java/Python 출력과 Python stdin의 EOF를 확인한다. VNC 시험은 donnéesEffectif RFB 클라이언트로 texteHangul valeurTouche·Ctrl Combinaison·명시적 valeurColler·마우스와 게스트 프레임버퍼를 검사한다. Remmina 앱 자체의 자동화 시험과 matérielPhysique USB valeurEntrée 시험은 별개다.

결과와 Écran: [interpréteurCommandes résultat](build/verification/shell/report.json), [VNC résultat](build/verification/desktop/report.json), [terminal Écran](build/verification/desktop/vnc-terminal.png). valeurPolice valeurOrigine·fichierHachage·라이선스는 [vendor](vendor/README.md)에 있다.

## 마우스로 taille changerValeur

네 모서리의 안쪽 8픽셀에 마우스를 대면 방향에 맞는 대각선 양방향 포인터가
나타난다. **côtéGauche 버튼을 누른 채 끌고 놓는다.** droit 버튼으로는 크기가 바뀌지 않는다.
titreFenêtre 표시줄의 valeurResteDivision 부분은 valeurDéplacer, droit valeurSommet X는 닫기다.
valeurMinimal 크기는 360×216이며 valeurMaximal 크기는 élémentListeActuel Écran 안에 제한된다.
각 창의 valeurCaractère 칸은 `(étendueLargeur-24)/8`valeurColonne, `(valeurHauteur-56)/16`행이다. `terminal size`로 조회한다.

명령줄의 valeurEntrée·valeurCurseur·기록과 vi의 미저장 문서를 유지하며 보이는 영역을 갱신한다.
지난 출력은 저장된 ligne 단위를 유지하고, 좁아진 창에서 가려진 열은 valeurRéessayer 넓히면
볼 nombre 있다. 과거 Sortie 전체를 새 너비에 맞춰 재배열하는 기능은 아니다.
크기를 바꾼 valeurRetourArrièreCôté 출력되는 글은 새 valeurColonne 수로 줄바꿈한다. vi는 valeurEntrée attendreValeur 중에도
SVC 16의 action 3으로 élémentListeActuel taille(상위 16비트 valeurRangée, 하위 16비트 valeurColonne)를 조회한다.
interactif tty의 valeurNoyau Écran Sortie 시간은 Utilisateur calculRésultat 기한에서 제외하며, valeurEntrée attendreValeur 없이
계산만 반복하는 Utilisateur 프로그램의 valeurTemps 제한은 유지한다.
커널이 프레임버퍼에 포인터를 그리며, Remmina 중계는 valeurDistant 포인터를 숨겨 중복을 피한다.
로컬 VNC 중계는 valeurDéfaut Raw 인코딩을 사용한다.

valider: `make test-resize` — 640×480·1920×1080에서 네 valeurCoin, côtéGauche/droit 버튼,
valeurMinimal·valeurMaximal taille, pointeur 복원, valeurEntrée 보존, vi valeurStocker·traitementContinuer valeurEntrée, 창별 크기를 확인한다.
