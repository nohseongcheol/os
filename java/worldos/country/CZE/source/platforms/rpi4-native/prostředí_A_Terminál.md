# vlastní 커널의 GUI 터미널과 prostředí

이 터미널은 vlastní Java 커널의 셸을 프레임버퍼 창과 UART에서 사용한다. příkaz Proces_HODNOTA_položka·RAM název_souboru·파이프는 Java jádro_HODNOTA, 화면의 znak_HODNOTA 그리기는 freestanding C에서 수행한다. Linux·X11·Bash 없이 동작하며, vlastní JVM의 Swing vzpěra_HODNOTA 부분집합도 같은 Okno 시스템을 이용한다. 자세한 vi·다중 Okno·코딩 사용법은 [개발 매뉴얼](개발안내.md)을 참고한다.

## dobrá_zboží 컴퓨터에서 Provést_příkaz

```sh
cd /home/user/jkoros/platforms/rpi4-native
make desktop
```

Remmina에서 **VNC**, Adresa **127.0.0.1:5902**로 연결한다. interpret_příkazů 창은 자동으로 열린다. 연결한 VNC 창에 키를 입력하면 vlastní 커널의 셸로 전달된다. 종료하려면 `make desktop`을 실행한 hostit 터미널에서 Ctrl+C를 누른다. 포트를 바꾸려면 BLD_Systém 후 `python3 nástroje/Provést_příkaz.py --desktop --port 5903`을 사용한다. 서버는 localhost에만 바인드하며 동시에 한 클라이언트가 제어한다.

일반 UART 셸은 `make run`으로 시작한다. QEMU 종료는 Ctrl+A Další_zboží X이다. 같은 VM의 UART에서 `terminal` 또는 F12로 GUI 터미널을 SLOUPEC_HODNOTA číslo 있다. `gui` Provést_příkaz 화면에서는 다섯 번째 **OPEN TERMINAL** 버튼, číslice_HODNOTA 5 또는 T로 연다. `--vnc 127.0.0.1:2`만 사용한 기존 Provést_příkaz 방식은 화면 보기용이며, VNC 키보드를 연결하려면 `--desktop`을 사용한다.

FTP와 externí_HODNOTA 네트워크도 함께 쓰려면 `python3 nástroje/Provést_příkaz.py --desktop --network`로
실행한다. Remmina VNC는 `127.0.0.1:5902`, 게스트에서 `ftpd start` 후 FTP는
`127.0.0.1:2121`이다. `--port`, `--ftp-port`, `--forward`를 함께 지정할 číslo 있다.
한 VM의 보조 UART로 SLIP를 전송하고 주 UART로 GUI 입력을 전달한다.

QEMU Provést_příkaz 도구가 VNC 키보드/마우스를 UART 입력으로 변환한다. skutečný_data Pi4의 USB 키보드·마우스 드라이버를 구현한 것은 아니다. skutečný_data 보드에서는 dobrá_zboží UART 입력이 필요하며 실물 부팅은 아직 미검증이다.

## 창과 vstup_HODNOTA

- 640×480~1920×1080 화면에서 최대 네 개 interpret_příkazů Okno, výchozí_hodnota 568×360(68열 × 19행)과 nedávné_HODNOTA 160행 보관, výchozí_hodnota ANSI 색상·kurzor_HODNOTA·vymazat_položka Proces_HODNOTA_položka.
- 상단 **+ New terminal** 또는 Ctrl+Shift+T로 새 창을 연다. 제목줄을 끌어 이동하고 Okno/상단 버튼을 클릭하거나 F6으로 전환한다. 각 창의 작업 cesta_2·proměnná_HODNOTA·příkaz LOGZ_ZÁZNAM·vstup_HODNOTA 중인 줄은 독립적이다.
- UTF-8 한글·CJK·라틴 문자와 일부 이모지 비트맵 písmo_HODNOTA. 복잡한 문자 조판·결합 문자·양방향 rozvržení_spojování·모든 Unicode 글리프를 보장하지 않는다.
- 좌우 방향키/Home/End/Delete/Backspace로 명령을 편집하고 위아래 방향키로 nedávné_HODNOTA 16개 명령을 찾는다. 긴 명령은 vstup_HODNOTA 줄을 가로로 이동해 보여 주며 `<`, `>`가 숨겨진 부분을 나타낸다.
- Tab은 příkaz Název 또는 dobrá_zboží 디렉터리의 파일명에서 후보가 하나일 때 완성한다. 디렉터리를 포함한 cesta_2 접두사·Citát 안의 완성은 아직 없다.
- Ctrl+A/E: 처음/끝, Ctrl+U/K: kurzor_HODNOTA přední_fotoaparát_HODNOTA/BACK_HODNOTA 삭제, Ctrl+C: vstup_HODNOTA Zrušit_operace. Provést_příkaz 중인 임의 프로그램에 SIGINT를 보내는 기능은 없다. vi와 Swing의 vstup_HODNOTA 대기는 Provést_příkaz 기한을 갱신하지만 일반 계산의 약 2초 제한은 유지한다.
- PgUp/PgDn 또는 마우스 휠: Předchozí_zboží výstupní_pozice. 새 출력이 오면 최신 위치로 돌아온다.
- F12/záhlaví právo 버튼/`exit`: Okno Zavřené. 빈 입력에서 Ctrl+D도 창을 닫는다. VM을 종료하는 명령은 아니다.

`--desktop`의 VNC vstup_HODNOTA 연결에 **두벌식 한글 složení_HODNOTA**을 제공한다. 접속한 PC의
입력기를 영어로 두고 **F9**, **Shift+Space**, **한/nula_operand Klíč_HODNOTA** 중 하나를 누르면
Okno 제목이 `[EN]`에서 `[KO]`로 바뀐다. `gksrmf` → `한글`,
`dkssudgktpdy` → `안녕하세요`. 같은 키로 영어로 돌아간다.
겹받침·복합 모음과 složení_HODNOTA 단계별 Backspace를 지원한다. kurzor_HODNOTA přesunout_HODNOTA·마우스 klepnout_HODNOTA·
단축키·vložit_HODNOTA·Enter 때 조합을 확정한다. PC가 Shift+Space나 한/nula_operand 키를
vlastní 처리하면 **F9**를 사용한다. Alt 단독은 SWITCH_MODE 키가 아니다.

이 조합기는 QEMU의 VNC→UART vstup_HODNOTA 연결에서 실행된다. 일반 직렬 접속과
실물 Pi의 USB 키보드 입력기에 추가된 기능은 아니다. 이미 완성된 Unicode
한글 키도 그대로 전달한다. 클립보드 공유가 활성화되어 표준 VNC ClientCutText가
도착하면 Ctrl+Shift+V로 붙여 넣는다. 클립보드 동기화만으로 명령을 실행하지 않는다.
줄바꿈을 포함해 명시적으로 붙여 넣으면 해당 줄이 실행된다.

게스트에서 `help` 또는 `help ko`를 입력하면 한글 vstup_HODNOTA 안내를 볼 číslo 있다.
`help`와 `help ko`에는 한/nula_operand Klíč_HODNOTA·Shift+Space·F9 및 `[EN]`/`[KO]` 안내를 표시한다.
긴 도움말은 PgUp/PgDn으로 스크롤한다.

터미널에서 Java·Python·C++ Provést_příkaz 결과를 바로 볼 číslo 있다. 프로그램이 직접 프레임버퍼에 그림을 그린 경우 Konec_program 후 interpret_příkazů 창을 복원한다. vi/Swing počkej_HODNOTA 중 다른 창으로 전환하면 해당 EL0 프로그램의 Paměť_data·레지스터를 보관하고 돌아올 때 재개한다. výběr_HODNOTA instance_HODNOTA·PTY·전체 VT100/xterm 호환과 임의 프로그램의 동시 병렬 실행은 제공하지 않는다. X로 닫으면 해당 창의 프로그램도 종료되므로 vi에서 저장하지 않은 내용은 사라진다.

## příkaz

| příkaz | oříznout |
|---|---|
| `help`, `info` | 사용법과 implementace Stav_HODNOTA |
| `pwd`, `cd [DIR]`, `ls [-l] [PATH]` | dobrá_zboží cesta_2·디렉터리/název_souboru položka_Seznam; argumenty 없는 cd는 `/` |
| `mkdir DIR`, `rmdir DIR` | 디렉터리 한 개 Create_položka/빈 디렉터리 삭제; `-p` 없음 |
| `touch FILE`, `rm FILE...` | název_souboru Create_položka/삭제; timestamp_HODNOTA Informace_o_systému 없음 |
| `cp SOURCE DEST`, `mv SOURCE DEST` | název_souboru instance_HODNOTA/Název změnit_HODNOTA; 대상은 정확한 název_souboru cesta_2, 재귀/디렉터리 přesunout_HODNOTA 없음 |
| `cat [FILE...]` | název_souboru 또는 표준 입력을 bajt_HODNOTA 그대로 výstupní_pozice |
| `echo [-n] [ARGS...]` | argumenty výstupní_pozice; `-e` 이스케이프 přípona_HODNOTA 없음 |
| `wc [-c\|-l\|-w] [FILE]` | bajt_HODNOTA/vstupní_řádek/Word_HODNOTA číslo; Word_HODNOTA 구분은 ASCII 공백 |
| `grep TEXT [FILE]` | 정규식 없이 문자열이 포함된 vstupní_řádek výstupní_pozice; 일치 없으면 Stav_HODNOTA 1 |
| `head [-n N] [FILE]`, `tail [-n N] [FILE]` | přední_fotoaparát_HODNOTA/BACK_HODNOTA N줄, výchozí_hodnota 10줄 |
| `tee [-a] FILE` | 표준 입력을 파일과 표준 출력에 LOGZ_ZÁZNAM |
| `export NAME=VALUE`, `unset NAME`, `env` | prostředí proměnná_HODNOTA Nastavení·삭제·položka_Seznam; HOME/PWD는 Čtení 전용 |
| `sh FILE`, `source FILE` | příkaz 파일을 같은 prostředí 환경에서 줄별 Provést_příkaz; 최대 vnoření_HODNOTA 3 |
| `true`, `false`, `exit [N]` | Stav_HODNOTA 0/1; skript_HODNOTA 안의 exit는 dobrá_zboží skript_HODNOTA Konec_program |
| `history`, `clear` | příkaz LOGZ_ZÁZNAM·화면 vymazat_položka |
| `vi FILE` | EL0 vi metoda_MODE Editor: vstup_HODNOTA/příkaz MODE_HODNOTA, UTF-8 přesunout_HODNOTA, 검색, 삭제·instance_HODNOTA·vložit_SMS·되돌리기, `:w`/`:q`/`:wq` |
| `edit FILE`, `load FILE`, `hex FILE` | 전체 Obsah_HODNOTA 교체 úprava_HODNOTA, 16진수 업로드/dotaz_HODNOTA; 단독 `.` 줄로 Store_HODNOTA |
| `javac`, `java`, `python`, `run` | 기존 vlastní Java nástroje·MicroPython·EL0 C++/ELF Provést_příkaz |

`net test`, `tasks`, `selftest`, `samples`도 유지한다. program_f5044b9b Provést_příkaz 범위는 [README](안내.md)와 [Java Provést_příkaz prostředí_5d36e09c](자바실행환경.md)을 참고한다.

```sh
mkdir 작업
cd 작업
echo "안녕하세요" > 인사.txt
echo "반갑습니다" >> 인사.txt
cat < 인사.txt | grep 안녕 | tee 추림.txt | wc -l
cp 인사.txt instance_HODNOTA.txt
mv instance_HODNOTA.txt 새이름.txt
export Název=누리
echo "$이름: ${PWD}"
false && echo 건너뜀 || echo zotavit_Stav
python -c 'print(123)' > VÝSLEDEK.txt
echo vstup_HODNOTA | python -c 'import jkoros; print(jkoros.stdin(64))'
echo 'echo "$이름"' > Provést_příkaz.sh
sh Provést_příkaz.sh
echo $?
```

## 문법과 제한

작은따옴표·큰따옴표·백슬래시, `$NAME`/`${NAME}`/`$?`, Word_HODNOTA přední_fotoaparát_HODNOTA `~`, vstupní_řádek 주석 `#`, 순차 Provést_příkaz `;`, podmínka Provést_příkaz `&&`/`||`, 파이프 `|`, vstup_HODNOTA `<`, 새 výstupní_pozice `>`, Připojit_položka výstupní_pozice `>>`를 제공한다. proměnná_HODNOTA 확장은 argumenty 안에서 수행하며 přípona_HODNOTA 결과를 공백으로 zkusit_znovu_HODNOTA 나누지 않는다. `export`의 값은 prostředí 안에서만 공유하며 uživatelský_prostor ELF의 envp/getenv 환경은 아직 없다.

파이프는 각 단계를 순서대로 실행하고 최대 **16384바이트**를 Další_zboží 단계로 넘긴다. 여러 프로세스가 동시에 읽고 쓰는 POSIX 파이프가 아니다. kapacita_HODNOTA 초과는 chyba 28과 selhání_HODNOTA 상태를 반환하고 해당 실행을 중단한다. `<`는 EOF를 제공하며 `>`/`>>`는 stdout만 바꾼다. EL0 fd 2는 화면/UART로 출력된다. `2>` 등 번호를 붙인 리다이렉션은 거부한다. 일부 내장 명령의 진단은 stdout을 사용한다. 연결한 프로그램의 `exit N` 진단은 데이터에 섞이지 않도록 생략한다.

`vi`, `edit`, `load`, `gui`, `terminal`, `sh`, `source`에는 파이프와 리다이렉션을 적용할 číslo 없다. 리다이렉션 파일을 열지 못하거나 파이프 용량을 초과하면 dobrá_zboží 명령줄을 중단하며, 그 줄의 뒤쪽 `||` 명령도 실행하지 않는다. skript_HODNOTA 파일을 입력할 때 멀티라인 Citát·이어 쓰기는 제공하지 않는다. `if`/`for`/`while`, funkce_HODNOTA, příkaz 치환, glob, 별칭, 백그라운드 `&`, jobs/fg/bg, 일반 프로세스·신호·PTY는 아직 없다. Bash/POSIX sh 전체 호환으로 표시하지 않는다.

název_souboru 64개 × 각 16384바이트, 루트 외 디렉터리 15개, název_souboru popisovač_položka 16개, cesta_2 최대 UTF-8 63바이트다. partner_HODNOTA/절대 경로와 `.`/`..`를 정규화하지만 oprávnění_HODNOTA·심볼릭 링크·마운트·디스크 영속 저장은 없다. **název_souboru·디렉터리·proměnná_HODNOTA·기록의 수정 내용은 재부팅하면 사라진다.** uživatelský_prostor 실행도 dobrá_zboží prostředí 경로를 사용한다. Java/Python/C++의 název_souboru API는 같은 RAM 저장소를 본다. `/example`의 세 Jazyk 예제와 설명서는 부팅할 때 원본으로 준비된다.

한 명령줄은 4096바이트, 구문 token_HODNOTA 128개, Provést_příkaz argumenty 32개, 변수는 16개(Název 31바이트·HODNOTA 255바이트)까지다. uživatelský_prostor 프로그램에 전달하는 인수는 기존 ABI대로 최대 8개·각 255바이트다. příkaz 기록은 1024바이트 이하 줄을 nedávné_HODNOTA 16개까지 저장한다.

## 재현 가능한 zkoušky

```sh
make test-shell
make test-desktop
make test-windows
make test-swing
make test
```

prostředí 시험은 skutečný_data raspi4b QEMU에서 cesta_2·název_souboru·proměnná_HODNOTA·podmínka·파이프·리다이렉션·chyba zotavit_Stav·skript_HODNOTA·편집을 검사하고, Java/Python 출력과 Python stdin의 EOF를 확인한다. VNC 시험은 skutečný_data RFB 클라이언트로 한글 Klíč_HODNOTA·Ctrl složení_HODNOTA·명시적 vložit_HODNOTA·마우스와 게스트 프레임버퍼를 검사한다. Remmina 앱 자체의 자동화 시험과 실물 USB vstup_HODNOTA 시험은 별개다.

결과와 화면: [prostředí VÝSLEDEK](build/verification/shell/report.json), [VNC VÝSLEDEK](build/verification/desktop/report.json), [interpret_příkazů 화면](build/verification/desktop/vnc-terminal.png). písmo_HODNOTA origin_HODNOTA·hodnota_hash_Soubor·라이선스는 [vendor](vendor/README.md)에 있다.

## 마우스로 Velikost změnit_HODNOTA

네 모서리의 안쪽 8픽셀에 마우스를 대면 방향에 맞는 대각선 양방향 포인터가
나타난다. **왼쪽 버튼을 누른 채 끌고 놓는다.** právo 버튼으로는 크기가 바뀌지 않는다.
okno_Název 표시줄의 나머지 부분은 přesunout_HODNOTA, právo 위 X는 닫기다.
최소 크기는 360×216이며 최대 크기는 dobrá_zboží 화면 안에 제한된다.
각 창의 znak_HODNOTA 칸은 `(폭-24)/8`SLOUPEC_HODNOTA, `(výška_HODNOTA-56)/16`행이다. `terminal size`로 조회한다.

명령줄의 vstup_HODNOTA·kurzor_HODNOTA·기록과 vi의 미저장 문서를 유지하며 보이는 영역을 갱신한다.
지난 출력은 저장된 vstupní_řádek 단위를 유지하고, 좁아진 창에서 가려진 열은 zkusit_znovu_HODNOTA 넓히면
볼 číslo 있다. 과거 výstupní_pozice 전체를 새 너비에 맞춰 재배열하는 기능은 아니다.
크기를 바꾼 BACK_HODNOTA 출력되는 글은 새 SLOUPEC_HODNOTA 수로 줄바꿈한다. vi는 vstup_HODNOTA počkej_HODNOTA 중에도
SVC 16의 Akce 3으로 dobrá_zboží Velikost(상위 16비트 ŘÁDEK_HODNOTA, 하위 16비트 SLOUPEC_HODNOTA)를 조회한다.
interaktivní tty의 jádro_HODNOTA 화면 výstupní_pozice 시간은 uživatelský_prostor 계산 기한에서 제외하며, vstup_HODNOTA počkej_HODNOTA 없이
계산만 반복하는 uživatelský_prostor 프로그램의 časová_hodnota 제한은 유지한다.
커널이 프레임버퍼에 포인터를 그리며, Remmina 중계는 vzdálený_HODNOTA 포인터를 숨겨 중복을 피한다.
로컬 VNC 중계는 výchozí_hodnota Raw 인코딩을 사용한다.

ověřit_5fb2b747: `make test-resize` — 640×480·1920×1080에서 네 모서리, 왼쪽/právo 버튼,
최소·최대 Velikost, ukazatel 복원, vstup_HODNOTA 보존, vi Store_HODNOTA·계속 vstup_HODNOTA, 창별 크기를 확인한다.
