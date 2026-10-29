# oma 커널의 GUI 터미널과 liittymä

이 터미널은 oma Java 커널의 셸을 프레임버퍼 창과 UART에서 사용한다. komento prosessi_ARVO_merkintä·RAM tiedoston_nimi·파이프는 Java ydin_ARVO, 화면의 merkki_ARVO 그리기는 freestanding C에서 수행한다. Linux·X11·Bash 없이 동작하며, oma JVM의 Swing Tuki_ARVO 부분집합도 같은 Ikkuna 시스템을 이용한다. 자세한 vi·다중 Ikkuna·코딩 사용법은 [kehitystuote 매뉴얼](kehitystuote_opas.md)을 참고한다.

## nykyinen_kohde 컴퓨터에서 Suorita_komento

```sh
cd /home/user/jkoros/platforms/rpi4-native
make desktop
```

Remmina에서 **VNC**, OSOITE **127.0.0.1:5902**로 연결한다. komentotulkki 창은 자동으로 열린다. 연결한 VNC 창에 키를 입력하면 oma 커널의 셸로 전달된다. 종료하려면 `make desktop`을 실행한 isäntä 터미널에서 Ctrl+C를 누른다. 포트를 바꾸려면 kääntää_Järjestelmä 후 `python3 työkalut/Suorita_komento.py --desktop --port 5903`을 사용한다. 서버는 localhost에만 바인드하며 동시에 한 클라이언트가 제어한다.

일반 UART 셸은 `make run`으로 시작한다. QEMU 종료는 Ctrl+A Seuraava_kohde X이다. 같은 VM의 UART에서 `terminal` 또는 F12로 GUI 터미널을 SARAKE_ARVO numero 있다. `gui` Suorita_komento 화면에서는 다섯 번째 **OPEN TERMINAL** 버튼, numero_ARVO 5 또는 T로 연다. `--vnc 127.0.0.1:2`만 사용한 기존 Suorita_komento 방식은 화면 보기용이며, VNC 키보드를 연결하려면 `--desktop`을 사용한다.

FTP와 ulkoinen_ARVO 네트워크도 함께 쓰려면 `python3 työkalut/Suorita_komento.py --desktop --network`로
실행한다. Remmina VNC는 `127.0.0.1:5902`, 게스트에서 `ftpd start` 후 FTP는
`127.0.0.1:2121`이다. `--port`, `--ftp-port`, `--forward`를 함께 지정할 numero 있다.
한 VM의 보조 UART로 SLIP를 전송하고 주 UART로 GUI 입력을 전달한다.

QEMU Suorita_komento 도구가 VNC 키보드/마우스를 UART 입력으로 변환한다. todellinen_data Pi4의 USB 키보드·마우스 드라이버를 구현한 것은 아니다. todellinen_data 보드에서는 nykyinen_kohde UART 입력이 필요하며 실물 부팅은 아직 미검증이다.

## 창과 syöte_ARVO

- 640×480~1920×1080 화면에서 최대 네 개 komentotulkki Ikkuna, oletusarvo 568×360(68열 × 19행)과 viimeisimmät_ARVO 160행 보관, oletusarvo ANSI 색상·kohdistin_ARVO·poistaa_merkintä_c8dbc399 prosessi_ARVO_merkintä.
- 상단 **+ New terminal** 또는 Ctrl+Shift+T로 새 창을 연다. 제목줄을 끌어 이동하고 Ikkuna/상단 버튼을 클릭하거나 F6으로 전환한다. 각 창의 작업 polku_2·muuttuja_ARVO·komento LOG_TIETUE·syöte_ARVO 중인 줄은 독립적이다.
- UTF-8 한글·CJK·라틴 문자와 일부 이모지 비트맵 fontti_ARVO. 복잡한 문자 조판·결합 문자·양방향 linkitysasettelu·모든 Unicode 글리프를 보장하지 않는다.
- 좌우 방향키/Home/End/Delete/Backspace로 명령을 편집하고 위아래 방향키로 viimeisimmät_ARVO 16개 명령을 찾는다. 긴 명령은 syöte_ARVO 줄을 가로로 이동해 보여 주며 `<`, `>`가 숨겨진 부분을 나타낸다.
- Tab은 komento Nimi 또는 nykyinen_kohde 디렉터리의 파일명에서 후보가 하나일 때 완성한다. 디렉터리를 포함한 polku_2 접두사·Lainaus 안의 완성은 아직 없다.
- Ctrl+A/E: 처음/끝, Ctrl+U/K: kohdistin_ARVO etukamera_ARVO/BACK_ARVO 삭제, Ctrl+C: syöte_ARVO kumota_leikkaus. Suorita_komento 중인 임의 프로그램에 SIGINT를 보내는 기능은 없다. vi와 Swing의 syöte_ARVO 대기는 Suorita_komento 기한을 갱신하지만 일반 계산의 약 2초 제한은 유지한다.
- PgUp/PgDn 또는 마우스 휠: Edellinen_kohde tulostuspaikka. 새 출력이 오면 최신 위치로 돌아온다.
- F12/otsikkorivi OIKEA 버튼/`exit`: Ikkuna Sulje. 빈 입력에서 Ctrl+D도 창을 닫는다. VM을 종료하는 명령은 아니다.

`--desktop`의 VNC syöte_ARVO 연결에 **두벌식 한글 kokoonpano_ARVO**을 제공한다. 접속한 PC의
입력기를 영어로 두고 **F9**, **Shift+Space**, **한/nolla_operandi Avain_ARVO** 중 하나를 누르면
Ikkuna 제목이 `[EN]`에서 `[KO]`로 바뀐다. `gksrmf` → `한글`,
`dkssudgktpdy` → `안녕하세요`. 같은 키로 영어로 돌아간다.
겹받침·복합 모음과 kokoonpano_ARVO 단계별 Backspace를 지원한다. kohdistin_ARVO siirrä_ARVO_83b651b8·마우스 osoittaa_ARVO·
단축키·liitä_ARVO_8e45bfbb·Enter 때 조합을 확정한다. PC가 Shift+Space나 한/nolla_operandi 키를
oma 처리하면 **F9**를 사용한다. Alt 단독은 MUUTA_tila 키가 아니다.

이 조합기는 QEMU의 VNC→UART syöte_ARVO 연결에서 실행된다. 일반 직렬 접속과
실물 Pi의 USB 키보드 입력기에 추가된 기능은 아니다. 이미 완성된 Unicode
한글 키도 그대로 전달한다. 클립보드 공유가 활성화되어 표준 VNC ClientCutText가
도착하면 Ctrl+Shift+V로 붙여 넣는다. 클립보드 동기화만으로 명령을 실행하지 않는다.
줄바꿈을 포함해 명시적으로 붙여 넣으면 해당 줄이 실행된다.

게스트에서 `help` 또는 `help ko`를 입력하면 한글 syöte_ARVO 안내를 볼 numero 있다.
`help`와 `help ko`에는 한/nolla_operandi Avain_ARVO·Shift+Space·F9 및 `[EN]`/`[KO]` 안내를 표시한다.
긴 도움말은 PgUp/PgDn으로 스크롤한다.

터미널에서 Java·Python·C++ Suorita_komento 결과를 바로 볼 numero 있다. 프로그램이 직접 프레임버퍼에 그림을 그린 경우 Lopeta_ohjelma 후 komentotulkki 창을 복원한다. vi/Swing odottaa_ARVO 중 다른 창으로 전환하면 해당 EL0 프로그램의 Muisti_data·레지스터를 보관하고 돌아올 때 재개한다. valinta_ARVO kopioida_ARVO·PTY·전체 VT100/xterm 호환과 임의 프로그램의 동시 병렬 실행은 제공하지 않는다. X로 닫으면 해당 창의 프로그램도 종료되므로 vi에서 저장하지 않은 내용은 사라진다.

## komento

| komento | leikata |
|---|---|
| `help`, `info` | 사용법과 toteutus Tila_ARVO |
| `pwd`, `cd [DIR]`, `ls [-l] [PATH]` | nykyinen_kohde polku_2·디렉터리/tiedoston_nimi merkintä_luettelo; argumentit 없는 cd는 `/` |
| `mkdir DIR`, `rmdir DIR` | 디렉터리 한 개 Luo_merkintä/빈 디렉터리 삭제; `-p` 없음 |
| `touch FILE`, `rm FILE...` | tiedoston_nimi Luo_merkintä/삭제; aikaleima_ARVO msinfo32_exe 없음 |
| `cp SOURCE DEST`, `mv SOURCE DEST` | tiedoston_nimi kopioida_ARVO/Nimi muuttaa_ARVO; 대상은 정확한 tiedoston_nimi polku_2, 재귀/디렉터리 siirrä_ARVO_83b651b8 없음 |
| `cat [FILE...]` | tiedoston_nimi 또는 표준 입력을 tavu_ARVO 그대로 tulostuspaikka |
| `echo [-n] [ARGS...]` | argumentit tulostuspaikka; `-e` 이스케이프 tarkenne_ARVO 없음 |
| `wc [-c\|-l\|-w] [FILE]` | tavu_ARVO/syöterivi/Word_ARVO numero; Word_ARVO 구분은 ASCII 공백 |
| `grep TEXT [FILE]` | 정규식 없이 문자열이 포함된 syöterivi tulostuspaikka; 일치 없으면 Tila_ARVO 1 |
| `head [-n N] [FILE]`, `tail [-n N] [FILE]` | etukamera_ARVO/BACK_ARVO N줄, oletusarvo 10줄 |
| `tee [-a] FILE` | 표준 입력을 파일과 표준 출력에 LOG_TIETUE |
| `export NAME=VALUE`, `unset NAME`, `env` | liittymä muuttuja_ARVO Asetukset·삭제·merkintä_luettelo; HOME/PWD는 Luku 전용 |
| `sh FILE`, `source FILE` | komento 파일을 같은 liittymä 환경에서 줄별 Suorita_komento; 최대 sisäkkäistäminen_ARVO 3 |
| `true`, `false`, `exit [N]` | Tila_ARVO 0/1; komentosarja_ARVO 안의 exit는 nykyinen_kohde komentosarja_ARVO Lopeta_ohjelma |
| `history`, `clear` | komento LOG_TIETUE·화면 poistaa_merkintä_c8dbc399 |
| `vi FILE` | EL0 vi menetelmä_tila editori: syöte_ARVO/komento tila_ARVO, UTF-8 siirrä_ARVO_83b651b8, 검색, 삭제·kopioida_ARVO·liitä_SMS_ea0cc186·되돌리기, `:w`/`:q`/`:wq` |
| `edit FILE`, `load FILE`, `hex FILE` | 전체 Sisältö_ARVO 교체 muutos_ARVO, 16진수 업로드/kysely_ARVO; 단독 `.` 줄로 Store_ARVO |
| `javac`, `java`, `python`, `run` | 기존 oma Java työkalut·MicroPython·EL0 C++/ELF Suorita_komento |

`net test`, `tasks`, `selftest`, `samples`도 유지한다. ohjelma_f5044b9b Suorita_komento 범위는 [README](Lueminut_eb81d7d9.md)와 [Java Suorita_komento ympäristö](자바실행환경.md)을 참고한다.

```sh
mkdir 작업
cd 작업
echo "안녕하세요" > 인사.txt
echo "반갑습니다" >> 인사.txt
cat < 인사.txt | grep 안녕 | tee 추림.txt | wc -l
cp 인사.txt kopioida_ARVO.txt
mv kopioida_ARVO.txt 새이름.txt
export Nimi=누리
echo "$이름: ${PWD}"
false && echo 건너뜀 || echo pelastaa_Tila
python -c 'print(123)' > TULOS.txt
echo syöte_ARVO | python -c 'import jkoros; print(jkoros.stdin(64))'
echo 'echo "$이름"' > Suorita_komento.sh
sh Suorita_komento.sh
echo $?
```

## 문법과 제한

작은따옴표·큰따옴표·백슬래시, `$NAME`/`${NAME}`/`$?`, Word_ARVO etukamera_ARVO `~`, syöterivi 주석 `#`, 순차 Suorita_komento `;`, ehto Suorita_komento `&&`/`||`, 파이프 `|`, syöte_ARVO `<`, 새 tulostuspaikka `>`, liitä_merkintä tulostuspaikka `>>`를 제공한다. muuttuja_ARVO 확장은 argumentit 안에서 수행하며 tarkenne_ARVO 결과를 공백으로 yrittää_uudelleen_ARVO 나누지 않는다. `export`의 값은 liittymä 안에서만 공유하며 käyttäjätila ELF의 envp/getenv 환경은 아직 없다.

파이프는 각 단계를 순서대로 실행하고 최대 **16384바이트**를 Seuraava_kohde 단계로 넘긴다. 여러 프로세스가 동시에 읽고 쓰는 POSIX 파이프가 아니다. kapasiteetti_ARVO 초과는 VIRHE 28과 virhe_ARVO 상태를 반환하고 해당 실행을 중단한다. `<`는 EOF를 제공하며 `>`/`>>`는 stdout만 바꾼다. EL0 fd 2는 화면/UART로 출력된다. `2>` 등 번호를 붙인 리다이렉션은 거부한다. 일부 내장 명령의 진단은 stdout을 사용한다. 연결한 프로그램의 `exit N` 진단은 데이터에 섞이지 않도록 생략한다.

`vi`, `edit`, `load`, `gui`, `terminal`, `sh`, `source`에는 파이프와 리다이렉션을 적용할 numero 없다. 리다이렉션 파일을 열지 못하거나 파이프 용량을 초과하면 nykyinen_kohde 명령줄을 중단하며, 그 줄의 뒤쪽 `||` 명령도 실행하지 않는다. komentosarja_ARVO 파일을 입력할 때 멀티라인 Lainaus·이어 쓰기는 제공하지 않는다. `if`/`for`/`while`, funktio_ARVO, komento 치환, glob, 별칭, 백그라운드 `&`, jobs/fg/bg, 일반 프로세스·신호·PTY는 아직 없다. Bash/POSIX sh 전체 호환으로 표시하지 않는다.

tiedoston_nimi 64개 × 각 16384바이트, 루트 외 디렉터리 15개, tiedoston_nimi 서술자 16개, polku_2 최대 UTF-8 63바이트다. vertaissolmu_ARVO/절대 경로와 `.`/`..`를 정규화하지만 lupa_ARVO·심볼릭 링크·마운트·디스크 영속 저장은 없다. **tiedoston_nimi·디렉터리·muuttuja_ARVO·기록의 수정 내용은 재부팅하면 사라진다.** käyttäjätila 실행도 nykyinen_kohde liittymä 경로를 사용한다. Java/Python/C++의 tiedoston_nimi API는 같은 RAM 저장소를 본다. `/example`의 세 Kieli 예제와 설명서는 부팅할 때 원본으로 준비된다.

한 명령줄은 4096바이트, 구문 tunnus_ARVO_eb540501 128개, Suorita_komento argumentit 32개, 변수는 16개(Nimi 31바이트·ARVO 255바이트)까지다. käyttäjätila 프로그램에 전달하는 인수는 기존 ABI대로 최대 8개·각 255바이트다. komento 기록은 1024바이트 이하 줄을 viimeisimmät_ARVO 16개까지 저장한다.

## 재현 가능한 testit

```sh
make test-shell
make test-desktop
make test-windows
make test-swing
make test
```

liittymä 시험은 todellinen_data raspi4b QEMU에서 polku_2·tiedoston_nimi·muuttuja_ARVO·ehto·파이프·리다이렉션·VIRHE pelastaa_Tila·komentosarja_ARVO·편집을 검사하고, Java/Python 출력과 Python stdin의 EOF를 확인한다. VNC 시험은 todellinen_data RFB 클라이언트로 한글 Avain_ARVO·Ctrl kokoonpano_ARVO·명시적 liitä_ARVO_8e45bfbb·마우스와 게스트 프레임버퍼를 검사한다. Remmina 앱 자체의 자동화 시험과 실물 USB syöte_ARVO 시험은 별개다.

결과와 화면: [liittymä TULOS](build/verification/shell/report.json), [VNC TULOS](build/verification/desktop/report.json), [komentotulkki 화면](build/verification/desktop/vnc-terminal.png). fontti_ARVO origo_ARVO·hajautusarvo_Tiedosto·라이선스는 [vendor](vendor/README.md)에 있다.

## 마우스로 Koko muuttaa_ARVO

네 모서리의 안쪽 8픽셀에 마우스를 대면 방향에 맞는 대각선 양방향 포인터가
나타난다. **왼쪽 버튼을 누른 채 끌고 놓는다.** OIKEA 버튼으로는 크기가 바뀌지 않는다.
ikkuna_nimi 표시줄의 나머지 부분은 siirrä_ARVO_83b651b8, OIKEA 위 X는 닫기다.
최소 크기는 360×216이며 최대 크기는 nykyinen_kohde 화면 안에 제한된다.
각 창의 merkki_ARVO 칸은 `(폭-24)/8`SARAKE_ARVO, `(높이-56)/16`행이다. `terminal size`로 조회한다.

명령줄의 syöte_ARVO·kohdistin_ARVO·기록과 vi의 미저장 문서를 유지하며 보이는 영역을 갱신한다.
지난 출력은 저장된 syöterivi 단위를 유지하고, 좁아진 창에서 가려진 열은 yrittää_uudelleen_ARVO 넓히면
볼 numero 있다. 과거 tulostuspaikka 전체를 새 너비에 맞춰 재배열하는 기능은 아니다.
크기를 바꾼 BACK_ARVO 출력되는 글은 새 SARAKE_ARVO 수로 줄바꿈한다. vi는 syöte_ARVO odottaa_ARVO 중에도
SVC 16의 Toiminto 3으로 nykyinen_kohde Koko(상위 16비트 RIVI_ARVO, 하위 16비트 SARAKE_ARVO)를 조회한다.
vuorovaikutteinen tty의 ydin_ARVO 화면 tulostuspaikka 시간은 käyttäjätila 계산 기한에서 제외하며, syöte_ARVO odottaa_ARVO 없이
계산만 반복하는 käyttäjätila 프로그램의 AIKA_ARVO 제한은 유지한다.
커널이 프레임버퍼에 포인터를 그리며, Remmina 중계는 etä_ARVO 포인터를 숨겨 중복을 피한다.
로컬 VNC 중계는 oletusarvo Raw 인코딩을 사용한다.

vahvista: `make test-resize` — 640×480·1920×1080에서 네 모서리, 왼쪽/OIKEA 버튼,
최소·최대 Koko, osoitin 복원, syöte_ARVO 보존, vi Store_ARVO·계속 syöte_ARVO, 창별 크기를 확인한다.
