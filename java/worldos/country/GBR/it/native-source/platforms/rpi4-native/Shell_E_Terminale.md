# nativo 커널의 GUI 터미널과 Shell

이 터미널은 nativo Java 커널의 셸을 프레임버퍼 창과 UART에서 사용한다. comando Processi_VALORE_voce·RAM file·파이프는 Java kernel_VALORE, 화면의 carattere_VALORE 그리기는 freestanding C에서 수행한다. Linux·X11·Bash 없이 동작하며, nativo JVM의 Swing Supporto_VALORE 부분집합도 같은 Finestra 시스템을 이용한다. 자세한 vi·다중 Finestra·코딩 사용법은 [sviluppo 매뉴얼](sviluppo_guida.md)을 참고한다.

## Regolari_articolo 컴퓨터에서 Esegui_comando

```sh
cd /home/user/jkoros/platforms/rpi4-native
make desktop
```

Remmina에서 **VNC**, e_mail **127.0.0.1:5902**로 연결한다. terminale 창은 자동으로 열린다. 연결한 VNC 창에 키를 입력하면 nativo 커널의 셸로 전달된다. 종료하려면 `make desktop`을 실행한 host 터미널에서 Ctrl+C를 누른다. 포트를 바꾸려면 costruire 후 `python3 strumenti/Esegui_comando.py --desktop --port 5903`을 사용한다. 서버는 localhost에만 바인드하며 동시에 한 클라이언트가 제어한다.

일반 UART 셸은 `make run`으로 시작한다. QEMU 종료는 Ctrl+A Avanti_articolo X이다. 같은 VM의 UART에서 `terminal` 또는 F12로 GUI 터미널을 colonna_VALORE numero 있다. `gui` Esegui_comando 화면에서는 다섯 번째 **OPEN TERMINAL** 버튼, cifra_VALORE 5 또는 T로 연다. `--vnc 127.0.0.1:2`만 사용한 기존 Esegui_comando 방식은 schermata 보기용이며, VNC 키보드를 연결하려면 `--desktop`을 사용한다.

FTP와 esterno_VALORE 네트워크도 함께 쓰려면 `python3 strumenti/Esegui_comando.py --desktop --network`로
실행한다. Remmina VNC는 `127.0.0.1:5902`, 게스트에서 `ftpd start` 후 FTP는
`127.0.0.1:2121`이다. `--port`, `--ftp-port`, `--forward`를 함께 지정할 numero 있다.
한 VM의 보조 UART로 SLIP를 전송하고 주 UART로 GUI 입력을 전달한다.

QEMU Esegui_comando 도구가 VNC 키보드/마우스를 UART 입력으로 변환한다. effettivo_dati Pi4의 USB 키보드·마우스 드라이버를 구현한 것은 아니다. effettivo_dati 보드에서는 Regolari_articolo UART 입력이 필요하며 fisico_hardware 부팅은 아직 미검증이다.

## 창과 input_VALORE

- 640×480~1920×1080 화면에서 최대 네 개 terminale Finestra, valore_predefinito 568×360(68열 × 19행)과 recenti_VALORE 160행 보관, valore_predefinito ANSI 색상·cursore_VALORE·cancellare_voce Processi_VALORE_voce.
- 상단 **+ New terminal** 또는 Ctrl+Shift+T로 새 창을 연다. 제목줄을 끌어 이동하고 Finestra/상단 버튼을 클릭하거나 F6으로 전환한다. 각 창의 작업 percorso·variabile_VALORE·comando LOG_riga·input_VALORE 중인 줄은 독립적이다.
- UTF-8 한글·CJK·라틴 문자와 일부 이모지 비트맵 tipo_di_carattere_VALORE. 복잡한 문자 조판·결합 문자·양방향 disposizione_di_collegamento·모든 Unicode 글리프를 보장하지 않는다.
- 좌우 방향키/Home/End/Delete/Backspace로 명령을 편집하고 위아래 방향키로 recenti_VALORE 16개 명령을 찾는다. 긴 명령은 input_VALORE 줄을 가로로 이동해 보여 주며 `<`, `>`가 숨겨진 부분을 나타낸다.
- Tab은 comando Nome 또는 Regolari_articolo 디렉터리의 파일명에서 후보가 하나일 때 완성한다. 디렉터리를 포함한 percorso 접두사·offerta 안의 완성은 아직 없다.
- Ctrl+A/E: 처음/끝, Ctrl+U/K: cursore_VALORE frontale_VALORE/BACK_VALORE 삭제, Ctrl+C: input_VALORE Chiudi_operazione. Esegui_comando 중인 임의 프로그램에 SIGINT를 보내는 기능은 없다. vi와 Swing의 input_VALORE 대기는 Esegui_comando 기한을 갱신하지만 일반 계산의 약 2초 제한은 유지한다.
- PgUp/PgDn 또는 마우스 휠: Indietro_articolo uscitaTesto. 새 출력이 오면 최신 위치로 돌아온다.
- F12/barra_del_titolo DESTRA 버튼/`exit`: Finestra Chiudi. 빈 입력에서 Ctrl+D도 창을 닫는다. VM을 종료하는 명령은 아니다.

`--desktop`의 VNC input_VALORE 연결에 **두벌식 한글 composizione_VALORE**을 제공한다. 접속한 PC의
입력기를 영어로 두고 **F9**, **Shift+Space**, **한/zero_operando tasto_VALORE** 중 하나를 누르면
Finestra 제목이 `[EN]`에서 `[KO]`로 바뀐다. `gksrmf` → `한글`,
`dkssudgktpdy` → `안녕하세요`. 같은 키로 영어로 돌아간다.
겹받침·복합 모음과 composizione_VALORE 단계별 Backspace를 지원한다. cursore_VALORE spostare_VALORE·마우스 clic_VALORE·
단축키·incollare_VALORE·Enter 때 조합을 확정한다. PC가 Shift+Space나 한/zero_operando 키를
nativo 처리하면 **F9**를 사용한다. Alt 단독은 SWITCH_MODA 키가 아니다.

이 조합기는 QEMU의 VNC→UART input_VALORE 연결에서 실행된다. 일반 seriale_VALORE 접속과
fisico_hardware Pi의 USB 키보드 입력기에 추가된 기능은 아니다. 이미 완성된 Unicode
한글 키도 그대로 전달한다. 클립보드 공유가 활성화되어 표준 VNC ClientCutText가
도착하면 Ctrl+Shift+V로 붙여 넣는다. 클립보드 동기화만으로 명령을 실행하지 않는다.
줄바꿈을 포함해 명시적으로 붙여 넣으면 해당 줄이 실행된다.

게스트에서 `help` 또는 `help ko`를 입력하면 한글 input_VALORE 안내를 볼 numero 있다.
`help`와 `help ko`에는 한/zero_operando tasto_VALORE·Shift+Space·F9 및 `[EN]`/`[KO]` 안내를 표시한다.
긴 도움말은 PgUp/PgDn으로 스크롤한다.

터미널에서 Java·Python·C++ Esegui_comando 결과를 바로 볼 numero 있다. 프로그램이 직접 프레임버퍼에 그림을 그린 경우 Esci_app 후 terminale 창을 복원한다. vi/Swing aspetta_VALORE 중 다른 창으로 전환하면 해당 EL0 프로그램의 Memoria_dati·레지스터를 보관하고 돌아올 때 재개한다. selezione_VALORE copiare_VALORE·PTY·전체 VT100/xterm 호환과 임의 프로그램의 동시 병렬 실행은 제공하지 않는다. X로 닫으면 해당 창의 프로그램도 종료되므로 vi에서 저장하지 않은 내용은 사라진다.

## comando

| comando | ritagliare |
|---|---|
| `help`, `info` | 사용법과 implementazione Stato_VALORE |
| `pwd`, `cd [DIR]`, `ls [-l] [PATH]` | Regolari_articolo percorso·디렉터리/file voce_elenco; argomenti 없는 cd는 `/` |
| `mkdir DIR`, `rmdir DIR` | 디렉터리 한 개 Crea_voce/빈 디렉터리 삭제; `-p` 없음 |
| `touch FILE`, `rm FILE...` | file Crea_voce/삭제; timestamp_VALORE msinfo32_exe 없음 |
| `cp SOURCE DEST`, `mv SOURCE DEST` | file copiare_VALORE/Nome cambiare_VALORE; 대상은 정확한 file percorso, 재귀/디렉터리 spostare_VALORE 없음 |
| `cat [FILE...]` | file 또는 표준 입력을 byte_VALORE 그대로 uscitaTesto |
| `echo [-n] [ARGS...]` | argomenti uscitaTesto; `-e` 이스케이프 estensione_VALORE 없음 |
| `wc [-c\|-l\|-w] [FILE]` | byte_VALORE/riga_di_ingresso/Word_VALORE numero; Word_VALORE 구분은 ASCII 공백 |
| `grep TEXT [FILE]` | 정규식 없이 문자열이 포함된 riga_di_ingresso uscitaTesto; 일치 없으면 Stato_VALORE 1 |
| `head [-n N] [FILE]`, `tail [-n N] [FILE]` | frontale_VALORE/BACK_VALORE N줄, valore_predefinito 10줄 |
| `tee [-a] FILE` | 표준 입력을 파일과 표준 출력에 LOG_riga |
| `export NAME=VALUE`, `unset NAME`, `env` | Shell variabile_VALORE Impostazioni·삭제·voce_elenco; HOME/PWD는 Lettura 전용 |
| `sh FILE`, `source FILE` | comando 파일을 같은 Shell 환경에서 줄별 Esegui_comando; 최대 annidamento_VALORE 3 |
| `true`, `false`, `exit [N]` | Stato_VALORE 0/1; script_VALORE 안의 exit는 Regolari_articolo script_VALORE Esci_app |
| `history`, `clear` | comando LOG_riga·schermata cancellare_voce |
| `vi FILE` | EL0 vi metodo_MODA Editor: input_VALORE/comando MODA_VALORE, UTF-8 spostare_VALORE, 검색, 삭제·copiare_VALORE·incollare_SMS·되돌리기, `:w`/`:q`/`:wq` |
| `edit FILE`, `load FILE`, `hex FILE` | 전체 Contenuto_VALORE 교체 Modifica_VALORE, 16진수 업로드/query_VALORE; 단독 `.` 줄로 Store_VALORE |
| `javac`, `java`, `python`, `run` | 기존 nativo Java strumenti·MicroPython·EL0 C++/ELF Esegui_comando |

`net test`, `tasks`, `selftest`, `samples`도 유지한다. app_f5044b9b Esegui_comando 범위는 [README](README_eb81d7d9.md)와 [Java Esegui_comando ambiente](자바실행환경.md)을 참고한다.

```sh
mkdir 작업
cd 작업
echo "안녕하세요" > messaggio_di_saluto_ae353e94.txt
echo "반갑습니다" >> messaggio_di_saluto_ae353e94.txt
cat < messaggio_di_saluto_ae353e94.txt | grep 안녕 | tee 추림.txt | wc -l
cp messaggio_di_saluto_ae353e94.txt copiare_VALORE.txt
mv copiare_VALORE.txt 새이름.txt
export Nome=누리
echo "$이름: ${PWD}"
false && echo 건너뜀 || echo recuperare_Stato
python -c 'print(123)' > risultato.txt
echo input_VALORE | python -c 'import jkoros; print(jkoros.stdin(64))'
echo 'echo "$이름"' > Esegui_comando.sh
sh Esegui_comando.sh
echo $?
```

## 문법과 제한

작은따옴표·큰따옴표·백슬래시, `$NAME`/`${NAME}`/`$?`, Word_VALORE frontale_VALORE `~`, riga_di_ingresso 주석 `#`, 순차 Esegui_comando `;`, condizione Esegui_comando `&&`/`||`, 파이프 `|`, input_VALORE `<`, 새 uscitaTesto `>`, Aggiunta_voce uscitaTesto `>>`를 제공한다. variabile_VALORE 확장은 argomenti 안에서 수행하며 estensione_VALORE 결과를 공백으로 retry_VALORE 나누지 않는다. `export`의 값은 Shell 안에서만 공유하며 spazio_utente ELF의 envp/getenv 환경은 아직 없다.

파이프는 각 단계를 순서대로 실행하고 최대 **16384바이트**를 Avanti_articolo 단계로 넘긴다. 여러 프로세스가 동시에 읽고 쓰는 POSIX 파이프가 아니다. capacità_VALORE 초과는 errore 28과 errore_VALORE 상태를 반환하고 해당 실행을 중단한다. `<`는 EOF를 제공하며 `>`/`>>`는 stdout만 바꾼다. EL0 fd 2는 schermata/UART로 출력된다. `2>` 등 번호를 붙인 리다이렉션은 거부한다. 일부 내장 명령의 진단은 stdout을 사용한다. 연결한 프로그램의 `exit N` 진단은 데이터에 섞이지 않도록 생략한다.

`vi`, `edit`, `load`, `gui`, `terminal`, `sh`, `source`에는 파이프와 리다이렉션을 적용할 numero 없다. 리다이렉션 파일을 열지 못하거나 파이프 용량을 초과하면 Regolari_articolo 명령줄을 중단하며, 그 줄의 뒤쪽 `||` 명령도 실행하지 않는다. script_VALORE 파일을 입력할 때 멀티라인 offerta·이어 쓰기는 제공하지 않는다. `if`/`for`/`while`, FUNZIONE_VALORE, comando 치환, glob, alternativa_nome, 백그라운드 `&`, jobs/fg/bg, 일반 프로세스·신호·PTY는 아직 없다. Bash/POSIX sh 전체 호환으로 표시하지 않는다.

file 64개 × 각 16384바이트, 루트 외 디렉터리 15개, file descrittore_voce 16개, percorso 최대 UTF-8 63바이트다. peer_VALORE/절대 경로와 `.`/`..`를 정규화하지만 privilegio_VALORE·심볼릭 링크·마운트·디스크 영속 저장은 없다. **file·디렉터리·variabile_VALORE·기록의 수정 내용은 재부팅하면 사라진다.** spazio_utente 실행도 Regolari_articolo Shell 경로를 사용한다. Java/Python/C++의 file API는 같은 RAM 저장소를 본다. `/example`의 세 Lingua 예제와 설명서는 부팅할 때 원본으로 준비된다.

한 명령줄은 4096바이트, 구문 token_VALORE 128개, Esegui_comando argomenti 32개, 변수는 16개(Nome 31바이트·VALORE 255바이트)까지다. spazio_utente 프로그램에 전달하는 인수는 기존 ABI대로 최대 8개·각 255바이트다. comando 기록은 1024바이트 이하 줄을 recenti_VALORE 16개까지 저장한다.

## 재현 가능한 prove

```sh
make test-shell
make test-desktop
make test-windows
make test-swing
make test
```

Shell 시험은 effettivo_dati raspi4b QEMU에서 percorso·file·variabile_VALORE·condizione·파이프·리다이렉션·errore recuperare_Stato·script_VALORE·편집을 검사하고, Java/Python 출력과 Python stdin의 EOF를 확인한다. VNC 시험은 effettivo_dati RFB 클라이언트로 한글 tasto_VALORE·Ctrl composizione_VALORE·명시적 incollare_VALORE·마우스와 게스트 프레임버퍼를 검사한다. Remmina 앱 자체의 자동화 시험과 fisico_hardware USB input_VALORE 시험은 별개다.

결과와 schermata: [Shell risultato](build/verification/shell/report.json), [VNC risultato](build/verification/desktop/report.json), [terminale schermata](build/verification/desktop/vnc-terminal.png). tipo_di_carattere_VALORE origine_VALORE·hash_File·라이선스는 [vendor](vendor/README.md)에 있다.

## 마우스로 Dimensione cambiare_VALORE

네 모서리의 안쪽 8픽셀에 마우스를 대면 방향에 맞는 대각선 양방향 포인터가
나타난다. **왼쪽 버튼을 누른 채 끌고 놓는다.** DESTRA 버튼으로는 크기가 바뀌지 않는다.
finestra_titolo 표시줄의 나머지 부분은 spostare_VALORE, DESTRA 위 X는 닫기다.
최소 크기는 360×216이며 최대 크기는 Regolari_articolo schermata 안에 제한된다.
각 창의 carattere_VALORE 칸은 `(폭-24)/8`colonna_VALORE, `(altezza_VALORE-56)/16`행이다. `terminal size`로 조회한다.

명령줄의 input_VALORE·cursore_VALORE·기록과 vi의 미저장 문서를 유지하며 보이는 영역을 갱신한다.
지난 출력은 저장된 riga_di_ingresso 단위를 유지하고, 좁아진 창에서 가려진 열은 retry_VALORE 넓히면
볼 numero 있다. 과거 uscitaTesto 전체를 새 너비에 맞춰 재배열하는 기능은 아니다.
크기를 바꾼 BACK_VALORE 출력되는 글은 새 colonna_VALORE 수로 줄바꿈한다. vi는 input_VALORE aspetta_VALORE 중에도
SVC 16의 Azione 3으로 Regolari_articolo Dimensione(상위 16비트 riga_VALORE, 하위 16비트 colonna_VALORE)를 조회한다.
interattivo tty의 kernel_VALORE schermata uscitaTesto 시간은 spazio_utente 계산 기한에서 제외하며, input_VALORE aspetta_VALORE 없이
계산만 반복하는 spazio_utente 프로그램의 valore 제한은 유지한다.
커널이 프레임버퍼에 포인터를 그리며, Remmina 중계는 remoto_VALORE 포인터를 숨겨 중복을 피한다.
로컬 VNC 중계는 valore_predefinito Raw 인코딩을 사용한다.

convalidare: `make test-resize` — 640×480·1920×1080에서 네 모서리, 왼쪽/DESTRA 버튼,
최소·최대 Dimensione, puntatore 복원, input_VALORE 보존, vi Store_VALORE·계속 input_VALORE, 창별 크기를 확인한다.
