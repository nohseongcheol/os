# eigen 커널의 GUI 터미널과 befehlshülle

이 터미널은 eigen Java 커널의 셸을 프레임버퍼 창과 UART에서 사용한다. befehl prozessWertEintrag·RAM Datei·파이프는 Java betriebskernWert, 화면의 zeichenWert 그리기는 freestanding C에서 수행한다. Linux·X11·Bash 없이 동작하며, eigen JVM의 Swing unterstützungWert 부분집합도 같은 fenster 시스템을 이용한다. 자세한 vi·다중 fenster·코딩 사용법은 [entwicklung 매뉴얼](EntwicklungLeitfaden.md)을 참고한다.

## aktuellElementeintrag 컴퓨터에서 befehlAusführen

```sh
cd /home/user/jkoros/platforms/rpi4-native
make desktop
```

Remmina에서 **VNC**, adresse **127.0.0.1:5902**로 연결한다. terminal 창은 자동으로 열린다. 연결한 VNC 창에 키를 입력하면 eigen 커널의 셸로 전달된다. 종료하려면 `make desktop`을 실행한 Wirtssystem 터미널에서 Ctrl+C를 누른다. 포트를 바꾸려면 systemErzeugenAbbild danachStatuswert `python3 Werkzeuge/befehlAusführen.py --desktop --port 5903`을 사용한다. 서버는 localhost에만 바인드하며 동시에 한 클라이언트가 제어한다.

일반 UART 셸은 `make run`으로 시작한다. QEMU 종료는 Ctrl+A nächsterElementeintrag X이다. 같은 VM의 UART에서 `terminal` 또는 F12로 GUI 터미널을 spalteWert Zahl 있다. `gui` befehlAusführen 화면에서는 다섯 번째 **OPEN TERMINAL** 버튼, zifferWert 5 또는 T로 연다. `--vnc 127.0.0.1:2`만 사용한 기존 befehlAusführen 방식은 Bildschirm 보기용이며, VNC 키보드를 연결하려면 `--desktop`을 사용한다.

FTP와 externWert 네트워크도 함께 쓰려면 `python3 Werkzeuge/befehlAusführen.py --desktop --network`로
실행한다. Remmina VNC는 `127.0.0.1:5902`, 게스트에서 `ftpd start` danachStatuswert FTP는
`127.0.0.1:2121`이다. `--port`, `--ftp-port`, `--forward`를 함께 지정할 Zahl 있다.
한 VM의 hilfsWert UART로 SLIP를 전송하고 주 UART로 GUI 입력을 전달한다.

QEMU befehlAusführen 도구가 VNC 키보드/마우스를 UART 입력으로 변환한다. tatsächlichDaten Pi4의 USB 키보드·마우스 드라이버를 구현한 것은 아니다. tatsächlichDaten 보드에서는 aktuellElementeintrag UART 입력이 필요하며 physischHardware 부팅은 아직 미검증이다.

## 창과 Eingabewert

- 640×480~1920×1080 화면에서 höchstwertWert 네 개 terminal fenster, standardwertWert 568×360(68열 × 19행)과 kürzlichWert 160행 wertBewahren, standardwertWert ANSI bildpunktFarbe·mauszeigerWert·eintragTilgen prozessWertEintrag.
- 상단 **+ New terminal** 또는 Ctrl+Shift+T로 새 창을 연다. 제목줄을 끌어 이동하고 fenster/상단 버튼을 클릭하거나 F6으로 전환한다. 각 창의 Aufgabe pfad·variableWert·befehl protokolldateiAufzeichnung·Eingabewert 중인 줄은 독립적이다.
- UTF-8 HangulText·CJK·라틴 문자와 일부 이모지 비트맵 schriftartWert. 복잡한 Zeichen 조판·zusammenfügenWerte Zeichen·양방향 Bindungsanordnung·모든 Unicode 글리프를 보장하지 않는다.
- 좌우 방향키/Home/End/Delete/Backspace로 명령을 편집하고 위아래 방향키로 kürzlichWert 16개 명령을 찾는다. 긴 명령은 Eingabewert 줄을 가로로 이동해 보여 주며 `<`, `>`ersterOperand 숨겨진 부분을 나타낸다.
- Tab은 befehl Name 또는 aktuellElementeintrag 디렉터리의 파일명에서 후보가 하나일 때 완성한다. 디렉터리를 포함한 pfad 접두사·anführungszeichen 안의 완성은 아직 없다.
- Ctrl+A/E: anfänglichElementeintrag/endung, Ctrl+U/K: mauszeigerWert vorderseiteWert/rückseiteWert 삭제, Ctrl+C: Eingabewert abbrechenVorgangVorgang. befehlAusführen 중인 임의 프로그램에 SIGINT를 보내는 기능은 없다. vi와 Swing의 Eingabewert 대기는 befehlAusführen 기한을 갱신하지만 일반 계산의 약 2초 제한은 유지한다.
- PgUp/PgDn 또는 마우스 휠: vorherigElementeintrag Ausgabe. 새 출력이 오면 neuesterWert 위치로 돌아온다.
- F12/titelLeiste rechts 버튼/`exit`: fenster schließen. 빈 입력에서 Ctrl+D도 창을 닫는다. VM을 종료하는 명령은 아니다.

`--desktop`의 VNC Eingabewert 연결에 **두벌식 HangulText Zusammenstellung**을 제공한다. 접속한 PC의
입력기를 영어로 두고 **F9**, **Shift+Space**, **한/nullwertOperand tasteWert** 중 하나를 누르면
fenster 제목이 `[EN]`에서 `[KO]`로 바뀐다. `gksrmf` → `HangulText`,
`dkssudgktpdy` → `안녕하세요`. 같은 키로 영어로 돌아간다.
겹받침·복합 모음과 Zusammenstellung 단계별 Backspace를 지원한다. mauszeigerWert bewegenWert·마우스 klickenWert·
단축키·einsetzenWert·Enter 때 조합을 확정한다. PC가 Shift+Space나 한/nullwertOperand 키를
eigen 처리하면 **F9**를 사용한다. Alt 단독은 umschaltenBetriebsart 키가 아니다.

이 조합기는 QEMU의 VNC→UART Eingabewert 연결에서 실행된다. 일반 seriellWert 접속과
physischHardware Pi의 USB 키보드 입력기에 추가된 기능은 아니다. 이미 완성된 Unicode
HangulText 키도 그대로 전달한다. 클립보드 공유가 활성화되어 표준 VNC ClientCutText가
도착하면 Ctrl+Shift+V로 붙여 넣는다. 클립보드 동기화만으로 명령을 실행하지 않는다.
줄바꿈을 포함해 명시적으로 붙여 넣으면 해당 줄이 실행된다.

게스트에서 `help` 또는 `help ko`를 입력하면 HangulText Eingabewert 안내를 볼 Zahl 있다.
`help`와 `help ko`에는 한/nullwertOperand tasteWert·Shift+Space·F9 및 `[EN]`/`[KO]` 안내를 표시한다.
긴 도움말은 PgUp/PgDn으로 스크롤한다.

터미널에서 Java·Python·C++ befehlAusführen 결과를 바로 볼 Zahl 있다. 프로그램이 직접 프레임버퍼에 그림을 그린 경우 verlassenProzessProgramm danachStatuswert terminal 창을 복원한다. vi/Swing wertWarten 중 다른 창으로 전환하면 해당 EL0 프로그램의 speicherDaten·레지스터를 보관하고 돌아올 때 재개한다. auswahlWert wertKopieren·PTY·전체 VT100/xterm 호환과 임의 프로그램의 동시 병렬 실행은 제공하지 않는다. X로 닫으면 해당 창의 프로그램도 종료되므로 vi에서 저장하지 않은 내용은 사라진다.

## befehl

| befehl | beschneiden |
|---|---|
| `help`, `info` | 사용법과 umsetzung statuswertWert |
| `pwd`, `cd [DIR]`, `ls [-l] [PATH]` | aktuellElementeintrag pfad·디렉터리/Datei eintragListe; argumente 없는 cd는 `/` |
| `mkdir DIR`, `rmdir DIR` | 디렉터리 한 개 eintragErstellen/빈 디렉터리 삭제; `-p` fehlendMethode |
| `touch FILE`, `rm FILE...` | Datei eintragErstellen/삭제; zeitstempelWert systemInformation fehlendMethode |
| `cp SOURCE DEST`, `mv SOURCE DEST` | Datei wertKopieren/Name wertÄndern; 대상은 정확한 Datei pfad, 재귀/디렉터리 bewegenWert fehlendMethode |
| `cat [FILE...]` | Datei 또는 표준 입력을 byteWert 그대로 Ausgabe |
| `echo [-n] [ARGS...]` | argumente Ausgabe; `-e` 이스케이프 erweiterungWert fehlendMethode |
| `wc [-c\|-l\|-w] [FILE]` | byteWert/zeile/maschinenwortWert Zahl; maschinenwortWert 구분은 ASCII 공백 |
| `grep TEXT [FILE]` | 정규식 없이 문자열이 포함된 zeile Ausgabe; istGleich 없으면 statuswertWert 1 |
| `head [-n N] [FILE]`, `tail [-n N] [FILE]` | vorderseiteWert/rückseiteWert N줄, standardwertWert 10줄 |
| `tee [-a] FILE` | 표준 입력을 파일과 표준 출력에 protokolldateiAufzeichnung |
| `export NAME=VALUE`, `unset NAME`, `env` | befehlshülle variableWert einstellungen·삭제·eintragListe; HOME/PWD는 lesen 전용 |
| `sh FILE`, `source FILE` | befehl 파일을 같은 befehlshülle 환경에서 줄별 befehlAusführen; höchstwertWert verschachtelungWert 3 |
| `true`, `false`, `exit [N]` | statuswertWert 0/1; skriptWert 안의 exit는 aktuellElementeintrag skriptWert verlassenProzessProgramm |
| `history`, `clear` | befehl protokolldateiAufzeichnung·Bildschirm eintragTilgen |
| `vi FILE` | EL0 vi methodeBetriebsart Editor: Eingabewert/befehl betriebsartWert, UTF-8 bewegenWert, 검색, 삭제·wertKopieren·einsetzenText·되돌리기, `:w`/`:q`/`:wq` |
| `edit FILE`, `load FILE`, `hex FILE` | 전체 inhaltswertWert 교체 bearbeitenWert, 16진수 업로드/abfragenWert; 단독 `.` 줄로 ablegenDatenWert |
| `javac`, `java`, `python`, `run` | 기존 eigen Java Werkzeuge·MicroPython·EL0 C++/ELF befehlAusführen |

`net test`, `tasks`, `selftest`, `samples`도 유지한다. Programm befehlAusführen 범위는 [README](Anleitung.md)와 [Java befehlAusführen umgebung](JavaLaufzeitUmgebung.md)을 참고한다.

```sh
mkdir Aufgabe
cd Aufgabe
echo "안녕하세요" > Gruß.txt
echo "반갑습니다" >> Gruß.txt
cat < Gruß.txt | grep 안녕 | tee 추림.txt | wc -l
cp Gruß.txt wertKopieren.txt
mv wertKopieren.txt neuName.txt
export Name=누리
echo "$이름: ${PWD}"
false && echo 건너뜀 || echo statuswertWiederherstellen
python -c 'print(123)' > ergebnis.txt
echo Eingabewert | python -c 'import jkoros; print(jkoros.stdin(64))'
echo 'echo "$이름"' > befehlAusführen.sh
sh befehlAusführen.sh
echo $?
```

## 문법과 grenzwertWert

작은따옴표·큰따옴표·백슬래시, `$NAME`/`${NAME}`/`$?`, maschinenwortWert vorderseiteWert `~`, zeile 주석 `#`, 순차 befehlAusführen `;`, bedingung befehlAusführen `&&`/`||`, 파이프 `|`, Eingabewert `<`, 새 Ausgabe `>`, eintragAnhängen Ausgabe `>>`를 제공한다. variableWert 확장은 argumente 안에서 수행하며 erweiterungWert 결과를 공백으로 erneutVersuchenWert 나누지 않는다. `export`의 값은 befehlshülle 안에서만 공유하며 Benutzer ELF의 envp/getenv 환경은 아직 없다.

파이프는 각 단계를 순서대로 실행하고 höchstwertWert **16384바이트**를 nächsterElementeintrag 단계로 넘긴다. 여러 프로세스가 동시에 읽고 쓰는 POSIX 파이프가 아니다. kapazitätWert 초과는 fehler 28과 fehlschlagWert 상태를 반환하고 해당 실행을 중단한다. `<`는 EOF를 제공하며 `>`/`>>`는 stdout만 바꾼다. EL0 fd 2는 Bildschirm/UART로 출력된다. `2>` 등 번호를 붙인 리다이렉션은 거부한다. 일부 내장 명령의 진단은 stdout을 사용한다. 연결한 프로그램의 `exit N` 진단은 데이터에 섞이지 않도록 생략한다.

`vi`, `edit`, `load`, `gui`, `terminal`, `sh`, `source`에는 파이프와 리다이렉션을 적용할 Zahl 없다. 리다이렉션 파일을 열지 못하거나 파이프 용량을 초과하면 aktuellElementeintrag 명령줄을 중단하며, 그 줄의 뒤쪽 `||` 명령도 실행하지 않는다. skriptWert 파일을 입력할 때 멀티라인 anführungszeichen·fortsetzungWert 쓰기는 제공하지 않는다. `if`/`for`/`while`, Funktion, befehl 치환, glob, alternativName, 백그라운드 `&`, jobs/fg/bg, 일반 프로세스·신호·PTY는 아직 없다. Bash/POSIX sh 전체 호환으로 표시하지 않는다.

Datei 64개 × 각 16384바이트, 루트 외 디렉터리 15개, Datei deskriptorEintrag 16개, pfad höchstwertWert UTF-8 63바이트다. gegenstelleWert/절대 경로와 `.`/`..`를 정규화하지만 erlaubnisWert·심볼릭 링크·마운트·디스크 영속 저장은 없다. **Datei·디렉터리·variableWert·기록의 wertVerändern 내용은 재부팅하면 사라진다.** Benutzer 실행도 aktuellElementeintrag befehlshülle 경로를 사용한다. Java/Python/C++의 Datei API는 같은 RAM 저장소를 본다. `/example`의 dreiWert Sprache 예제와 설명서는 부팅할 때 원본으로 준비된다.

한 명령줄은 4096바이트, 구문 wortzeichenWert 128개, befehlAusführen argumente 32개, 변수는 16개(Name 31바이트·Wert 255바이트)까지다. Benutzer 프로그램에 전달하는 인수는 기존 ABI대로 höchstwertWert 8개·각 255바이트다. befehl 기록은 1024바이트 이하 줄을 kürzlichWert 16개까지 저장한다.

## 재현 가능한 Prüfungen

```sh
make test-shell
make test-desktop
make test-windows
make test-swing
make test
```

befehlshülle 시험은 tatsächlichDaten raspi4b QEMU에서 pfad·Datei·variableWert·bedingung·파이프·리다이렉션·fehler statuswertWiederherstellen·skriptWert·편집을 검사하고, Java/Python 출력과 Python stdin의 EOF를 확인한다. VNC 시험은 tatsächlichDaten RFB 클라이언트로 HangulText tasteWert·Ctrl Zusammenstellung·명시적 einsetzenWert·마우스와 게스트 프레임버퍼를 검사한다. Remmina 앱 자체의 자동화 시험과 physischHardware USB Eingabewert 시험은 별개다.

결과와 Bildschirm: [befehlshülle ergebnis](build/verification/shell/report.json), [VNC ergebnis](build/verification/desktop/report.json), [terminal Bildschirm](build/verification/desktop/vnc-terminal.png). schriftartWert ursprungWert·prüfsummeDatei·라이선스는 [vendor](vendor/README.md)에 있다.

## 마우스로 größe wertÄndern

네 모서리의 안쪽 8픽셀에 마우스를 대면 방향에 맞는 대각선 양방향 포인터가
나타난다. **linksSeiteRand 버튼을 누른 채 끌고 놓는다.** rechts 버튼으로는 크기가 바뀌지 않는다.
fensterTitel 표시줄의 restwertWert 부분은 bewegenWert, rechts oberkanteWert X는 닫기다.
mindestwertWert 크기는 360×216이며 höchstwertWert 크기는 aktuellElementeintrag Bildschirm 안에 제한된다.
각 창의 zeichenWert 칸은 `(breiteSpannweite-24)/8`spalteWert, `(höheWert-56)/16`행이다. `terminal size`로 조회한다.

명령줄의 Eingabewert·mauszeigerWert·기록과 vi의 미저장 문서를 유지하며 보이는 영역을 갱신한다.
지난 출력은 저장된 zeile 단위를 유지하고, 좁아진 창에서 가려진 열은 erneutVersuchenWert 넓히면
볼 Zahl 있다. 과거 Ausgabe 전체를 새 너비에 맞춰 재배열하는 기능은 아니다.
크기를 바꾼 rückseiteWert 출력되는 글은 새 spalteWert 수로 줄바꿈한다. vi는 Eingabewert wertWarten 중에도
SVC 16의 aktion 3으로 aktuellElementeintrag größe(상위 16비트 zeilennummerWert, 하위 16비트 spalteWert)를 조회한다.
interaktiv tty의 betriebskernWert Bildschirm Ausgabe 시간은 Benutzer berechnung 기한에서 제외하며, Eingabewert wertWarten 없이
계산만 반복하는 Benutzer 프로그램의 zeitWert 제한은 유지한다.
커널이 프레임버퍼에 포인터를 그리며, Remmina 중계는 entferntWert 포인터를 숨겨 중복을 피한다.
로컬 VNC 중계는 standardwertWert Raw 인코딩을 사용한다.

validieren: `make test-resize` — 640×480·1920×1080에서 네 eckeWert, linksSeiteRand/rechts 버튼,
mindestwertWert·höchstwertWert größe, zeiger 복원, Eingabewert 보존, vi ablegenDatenWert·fortsetzenVerarbeitung Eingabewert, 창별 크기를 확인한다.
