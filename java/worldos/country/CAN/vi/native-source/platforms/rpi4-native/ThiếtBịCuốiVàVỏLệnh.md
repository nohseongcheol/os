# tựThân 커널의 GUI 터미널과 vỏLệnh

이 터미널은 tựThân Java 커널의 셸을 프레임버퍼 창과 UART에서 사용한다. lệnh mụcGiáTrịTiếnTrình·RAM Tệp·파이프는 Java giáTrịNhân, 화면의 giáTrịKýTự 그리기는 freestanding C에서 수행한다. Linux·X11·Bash 없이 동작하며, tựThân JVM의 Swing giáTrịHỗTrợ 부분집합도 같은 cửaSổ 시스템을 이용한다. 자세한 vi·다중 cửaSổ·코딩 사용법은 [phátTriển 매뉴얼](HướngDẫnPhátTriển.md)을 참고한다.

## phầnMụcHiệnTại 컴퓨터에서 thựcThiLệnh

```sh
cd /home/user/jkoros/platforms/rpi4-native
make desktop
```

Remmina에서 **VNC**, địaChỉ **127.0.0.1:5902**로 연결한다. thiếtBịCuối 창은 자동으로 열린다. 연결한 VNC 창에 키를 입력하면 tựThân 커널의 셸로 전달된다. 종료하려면 `make desktop`을 실행한 Chủ 터미널에서 Ctrl+C를 누른다. 포트를 바꾸려면 xâyDựngHệThống trạngTháiSau `python3 CôngCụ/thựcThiLệnh.py --desktop --port 5903`을 사용한다. 서버는 localhost에만 바인드하며 동시에 한 클라이언트가 제어한다.

일반 UART 셸은 `make run`으로 시작한다. QEMU 종료는 Ctrl+A phầnMụcKếTiếp X이다. 같은 VM의 UART에서 `terminal` 또는 F12로 GUI 터미널을 giáTrịCột trịSố 있다. `gui` thựcThiLệnh 화면에서는 다섯 번째 **OPEN TERMINAL** 버튼, giáTrịChữSố 5 또는 T로 연다. `--vnc 127.0.0.1:2`만 사용한 기존 thựcThiLệnh 방식은 MànHình 보기용이며, VNC 키보드를 연결하려면 `--desktop`을 사용한다.

FTP와 giáTrịBênNgoài 네트워크도 함께 쓰려면 `python3 CôngCụ/thựcThiLệnh.py --desktop --network`로
실행한다. Remmina VNC는 `127.0.0.1:5902`, 게스트에서 `ftpd start` trạngTháiSau FTP는
`127.0.0.1:2121`이다. `--port`, `--ftp-port`, `--forward`를 함께 지정할 trịSố 있다.
한 VM의 giáTrịPhụTrợ UART로 SLIP를 전송하고 주 UART로 GUI 입력을 전달한다.

QEMU thựcThiLệnh 도구가 VNC 키보드/마우스를 UART 입력으로 변환한다. dữLiệuThựcTế Pi4의 USB 키보드·마우스 드라이버를 구현한 것은 아니다. dữLiệuThựcTế 보드에서는 phầnMụcHiệnTại UART 입력이 필요하며 phầnCứngVậtLý 부팅은 아직 미검증이다.

## 창과 giáTrịVào

- 640×480~1920×1080 화면에서 giáTrịTốiĐa 네 개 thiếtBịCuối cửaSổ, giáTrịMặcĐịnh 568×360(68열 × 19행)과 giáTrịGầnĐây 160행 giữNguyênGiáTrị, giáTrịMặcĐịnh ANSI màuĐiểmẢnh·giáTrịConTrỏVănBản·xóaMục mụcGiáTrịTiếnTrình.
- 상단 **+ New terminal** 또는 Ctrl+Shift+T로 새 창을 연다. 제목줄을 끌어 이동하고 cửaSổ/상단 버튼을 클릭하거나 F6으로 전환한다. 각 창의 TácVụ đườngDẫn·giáTrịBiến·lệnh bảnGhiNhậtKý·giáTrịVào 중인 줄은 독립적이다.
- UTF-8 vănBảnHangul·CJK·라틴 문자와 일부 이모지 비트맵 giáTrịPhôngChữ. 복잡한 KýTự 조판·cácGiáTrịKếtHợp KýTự·양방향 BốTríLiênKết·모든 Unicode 글리프를 보장하지 않는다.
- 좌우 방향키/Home/End/Delete/Backspace로 명령을 편집하고 위아래 방향키로 giáTrịGầnĐây 16개 명령을 찾는다. 긴 명령은 giáTrịVào 줄을 가로로 이동해 보여 주며 `<`, `>`toánHạngĐầuTiên 숨겨진 부분을 나타낸다.
- Tab은 lệnh tên 또는 phầnMụcHiệnTại 디렉터리의 파일명에서 후보가 하나일 때 완성한다. 디렉터리를 포함한 đườngDẫn 접두사·dấuTrích 안의 완성은 아직 없다.
- Ctrl+A/E: phầnMụcBanĐầu/phầnKết, Ctrl+U/K: giáTrịConTrỏVănBản giáTrịPhíaTrước/giáTrịLùi 삭제, Ctrl+C: giáTrịVào thaoTácHủy. thựcThiLệnh 중인 임의 프로그램에 SIGINT를 보내는 기능은 없다. vi와 Swing의 giáTrịVào 대기는 thựcThiLệnh 기한을 갱신하지만 일반 계산의 약 2초 제한은 유지한다.
- PgUp/PgDn 또는 마우스 휠: phầnMụcTrướcĐó ĐầuRa. 새 출력이 오면 giáTrịMớiNhất 위치로 돌아온다.
- F12/thanhTiêuĐề phải 버튼/`exit`: cửaSổ đóng. 빈 입력에서 Ctrl+D도 창을 닫는다. VM을 종료하는 명령은 아니다.

`--desktop`의 VNC giáTrịVào 연결에 **두벌식 vănBảnHangul PhốiHợp**을 제공한다. 접속한 PC의
입력기를 영어로 두고 **F9**, **Shift+Space**, **한/toánHạngKhôngSố giáTrịPhím** 중 하나를 누르면
cửaSổ 제목이 `[EN]`에서 `[KO]`로 바뀐다. `gksrmf` → `vănBảnHangul`,
`dkssudgktpdy` → `안녕하세요`. 같은 키로 영어로 돌아간다.
겹받침·복합 모음과 PhốiHợp 단계별 Backspace를 지원한다. giáTrịConTrỏVănBản giáTrịDiChuyển·마우스 giáTrịNhấnChuột·
단축키·giáTrịDán·Enter 때 조합을 확정한다. PC가 Shift+Space나 한/toánHạngKhôngSố 키를
tựThân 처리하면 **F9**를 사용한다. Alt 단독은 chếĐộChuyển 키가 아니다.

이 조합기는 QEMU의 VNC→UART giáTrịVào 연결에서 실행된다. 일반 giáTrịNốiTiếp 접속과
phầnCứngVậtLý Pi의 USB 키보드 입력기에 추가된 기능은 아니다. 이미 완성된 Unicode
vănBảnHangul 키도 그대로 전달한다. 클립보드 공유가 활성화되어 표준 VNC ClientCutText가
도착하면 Ctrl+Shift+V로 붙여 넣는다. 클립보드 동기화만으로 명령을 실행하지 않는다.
줄바꿈을 포함해 명시적으로 붙여 넣으면 해당 줄이 실행된다.

게스트에서 `help` 또는 `help ko`를 입력하면 vănBảnHangul giáTrịVào 안내를 볼 trịSố 있다.
`help`와 `help ko`에는 한/toánHạngKhôngSố giáTrịPhím·Shift+Space·F9 및 `[EN]`/`[KO]` 안내를 표시한다.
긴 도움말은 PgUp/PgDn으로 스크롤한다.

터미널에서 Java·Python·C++ thựcThiLệnh 결과를 바로 볼 trịSố 있다. 프로그램이 직접 프레임버퍼에 그림을 그린 경우 chươngTrìnhRa trạngTháiSau thiếtBịCuối 창을 복원한다. vi/Swing chờGiáTrị 중 다른 창으로 전환하면 해당 EL0 프로그램의 dữLiệuBộNhớ·레지스터를 보관하고 돌아올 때 재개한다. giáTrịViệcChọn saoChépGiáTrị·PTY·전체 VT100/xterm 호환과 임의 프로그램의 동시 병렬 실행은 제공하지 않는다. X로 닫으면 해당 창의 프로그램도 종료되므로 vi에서 저장하지 않은 내용은 사라진다.

## lệnh

| lệnh | cắtXén |
|---|---|
| `help`, `info` | 사용법과 phầnCàiĐặt giáTrịTrạngThái |
| `pwd`, `cd [DIR]`, `ls [-l] [PATH]` | phầnMụcHiệnTại đườngDẫn·디렉터리/Tệp danhSáchMục; cácĐốiSố 없는 cd는 `/` |
| `mkdir DIR`, `rmdir DIR` | 디렉터리 한 개 tạoMục/빈 디렉터리 삭제; `-p` phươngThứcThiếu |
| `touch FILE`, `rm FILE...` | Tệp tạoMục/삭제; giáTrịDấuThờiGian thôngTinHệThống phươngThứcThiếu |
| `cp SOURCE DEST`, `mv SOURCE DEST` | Tệp saoChépGiáTrị/tên đổiGiáTrị; 대상은 정확한 Tệp đườngDẫn, 재귀/디렉터리 giáTrịDiChuyển phươngThứcThiếu |
| `cat [FILE...]` | Tệp 또는 표준 입력을 giáTrịByte 그대로 ĐầuRa |
| `echo [-n] [ARGS...]` | cácĐốiSố ĐầuRa; `-e` 이스케이프 giáTrịPhầnMởRộng phươngThứcThiếu |
| `wc [-c\|-l\|-w] [FILE]` | giáTrịByte/dòng/giáTrịTừ trịSố; giáTrịTừ 구분은 ASCII 공백 |
| `grep TEXT [FILE]` | 정규식 없이 문자열이 포함된 dòng ĐầuRa; làBằng 없으면 giáTrịTrạngThái 1 |
| `head [-n N] [FILE]`, `tail [-n N] [FILE]` | giáTrịPhíaTrước/giáTrịLùi N줄, giáTrịMặcĐịnh 10줄 |
| `tee [-a] FILE` | 표준 입력을 파일과 표준 출력에 bảnGhiNhậtKý |
| `export NAME=VALUE`, `unset NAME`, `env` | vỏLệnh giáTrịBiến cácThiếtLập·삭제·danhSáchMục; HOME/PWD는 đọc 전용 |
| `sh FILE`, `source FILE` | lệnh 파일을 같은 vỏLệnh 환경에서 줄별 thựcThiLệnh; giáTrịTốiĐa giáTrịLồngNhau 3 |
| `true`, `false`, `exit [N]` | giáTrịTrạngThái 0/1; giáTrịKịchBản 안의 exit는 phầnMụcHiệnTại giáTrịKịchBản chươngTrìnhRa |
| `history`, `clear` | lệnh bảnGhiNhậtKý·MànHình xóaMục |
| `vi FILE` | EL0 vi chếĐộPhươngThức TrìnhSoạnThảo: giáTrịVào/lệnh giáTrịChếĐộ, UTF-8 giáTrịDiChuyển, 검색, 삭제·saoChépGiáTrị·vănBảnDán·되돌리기, `:w`/`:q`/`:wq` |
| `edit FILE`, `load FILE`, `hex FILE` | 전체 giáTrịNộiDung 교체 giáTrịSửa, 16진수 업로드/giáTrịTruyVấn; 단독 `.` 줄로 giáTrịCất |
| `javac`, `java`, `python`, `run` | 기존 tựThân Java CôngCụ·MicroPython·EL0 C++/ELF thựcThiLệnh |

`net test`, `tasks`, `selftest`, `samples`도 유지한다. ChươngTrình thựcThiLệnh 범위는 [README](HướngDẫn.md)와 [Java thựcThiLệnh môiTrường](MôiTrườngMôiTrườngChạyJava.md)을 참고한다.

```sh
mkdir TácVụ
cd TácVụ
echo "안녕하세요" > LờiChào.txt
echo "반갑습니다" >> LờiChào.txt
cat < LờiChào.txt | grep 안녕 | tee 추림.txt | wc -l
cp LờiChào.txt saoChépGiáTrị.txt
mv saoChépGiáTrị.txt tênMới.txt
export tên=누리
echo "$이름: ${PWD}"
false && echo 건너뜀 || echo khôiPhụcTrạngThái
python -c 'print(123)' > kếtQuả.txt
echo giáTrịVào | python -c 'import jkoros; print(jkoros.stdin(64))'
echo 'echo "$이름"' > thựcThiLệnh.sh
sh thựcThiLệnh.sh
echo $?
```

## 문법과 giáTrịGiớiHạn

작은따옴표·큰따옴표·백슬래시, `$NAME`/`${NAME}`/`$?`, giáTrịTừ giáTrịPhíaTrước `~`, dòng 주석 `#`, 순차 thựcThiLệnh `;`, điềuKiện thựcThiLệnh `&&`/`||`, 파이프 `|`, giáTrịVào `<`, 새 ĐầuRa `>`, thêmCuốiMục ĐầuRa `>>`를 제공한다. giáTrịBiến 확장은 cácĐốiSố 안에서 수행하며 giáTrịPhầnMởRộng 결과를 공백으로 giáTrịThửLại 나누지 않는다. `export`의 값은 vỏLệnh 안에서만 공유하며 NgườiDùng ELF의 envp/getenv 환경은 아직 없다.

파이프는 각 단계를 순서대로 실행하고 giáTrịTốiĐa **16384바이트**를 phầnMụcKếTiếp 단계로 넘긴다. 여러 프로세스가 동시에 읽고 쓰는 POSIX 파이프가 아니다. giáTrịSứcChứa 초과는 lỗi 28과 giáTrịSựThấtBại 상태를 반환하고 해당 실행을 중단한다. `<`는 EOF를 제공하며 `>`/`>>`는 stdout만 바꾼다. EL0 fd 2는 MànHình/UART로 출력된다. `2>` 등 번호를 붙인 리다이렉션은 거부한다. 일부 내장 명령의 진단은 stdout을 사용한다. 연결한 프로그램의 `exit N` 진단은 데이터에 섞이지 않도록 생략한다.

`vi`, `edit`, `load`, `gui`, `terminal`, `sh`, `source`에는 파이프와 리다이렉션을 적용할 trịSố 없다. 리다이렉션 파일을 열지 못하거나 파이프 용량을 초과하면 phầnMụcHiệnTại 명령줄을 중단하며, 그 줄의 뒤쪽 `||` 명령도 실행하지 않는다. giáTrịKịchBản 파일을 입력할 때 멀티라인 dấuTrích·giáTrịSựTiếpDiễn 쓰기는 제공하지 않는다. `if`/`for`/`while`, Hàm, lệnh 치환, glob, tênThayThế, 백그라운드 `&`, jobs/fg/bg, 일반 프로세스·신호·PTY는 아직 없다. Bash/POSIX sh 전체 호환으로 표시하지 않는다.

Tệp 64개 × 각 16384바이트, 루트 외 디렉터리 15개, Tệp mụcBộMôTả 16개, đườngDẫn giáTrịTốiĐa UTF-8 63바이트다. giáTrịĐốiTác/절대 경로와 `.`/`..`를 정규화하지만 giáTrịQuyền·심볼릭 링크·마운트·디스크 영속 저장은 없다. **Tệp·디렉터리·giáTrịBiến·기록의 chỉnhSửaGiáTrị 내용은 재부팅하면 사라진다.** NgườiDùng 실행도 phầnMụcHiệnTại vỏLệnh 경로를 사용한다. Java/Python/C++의 Tệp API는 같은 RAM 저장소를 본다. `/example`의 giáTrịBa NgônNgữ 예제와 설명서는 부팅할 때 원본으로 준비된다.

한 명령줄은 4096바이트, 구문 giáTrịTừTố 128개, thựcThiLệnh cácĐốiSố 32개, 변수는 16개(tên 31바이트·giáTrị 255바이트)까지다. NgườiDùng 프로그램에 전달하는 인수는 기존 ABI대로 giáTrịTốiĐa 8개·각 255바이트다. lệnh 기록은 1024바이트 이하 줄을 giáTrịGầnĐây 16개까지 저장한다.

## 재현 가능한 KiểmThử

```sh
make test-shell
make test-desktop
make test-windows
make test-swing
make test
```

vỏLệnh 시험은 dữLiệuThựcTế raspi4b QEMU에서 đườngDẫn·Tệp·giáTrịBiến·điềuKiện·파이프·리다이렉션·lỗi khôiPhụcTrạngThái·giáTrịKịchBản·편집을 검사하고, Java/Python 출력과 Python stdin의 EOF를 확인한다. VNC 시험은 dữLiệuThựcTế RFB 클라이언트로 vănBảnHangul giáTrịPhím·Ctrl PhốiHợp·명시적 giáTrịDán·마우스와 게스트 프레임버퍼를 검사한다. Remmina 앱 자체의 자동화 시험과 phầnCứngVậtLý USB giáTrịVào 시험은 별개다.

결과와 MànHình: [vỏLệnh kếtQuả](build/verification/shell/report.json), [VNC kếtQuả](build/verification/desktop/report.json), [thiếtBịCuối MànHình](build/verification/desktop/vnc-terminal.png). giáTrịPhôngChữ giáTrịGốc·tệpMãBăm·라이선스는 [vendor](vendor/README.md)에 있다.

## 마우스로 cỡ đổiGiáTrị

네 모서리의 안쪽 8픽셀에 마우스를 대면 방향에 맞는 대각선 양방향 포인터가
나타난다. **bênTrái 버튼을 누른 채 끌고 놓는다.** phải 버튼으로는 크기가 바뀌지 않는다.
tiêuĐềCửaSổ 표시줄의 giáTrịSốDư 부분은 giáTrịDiChuyển, phải giáTrịĐỉnh X는 닫기다.
giáTrịTốiThiểu 크기는 360×216이며 giáTrịTốiĐa 크기는 phầnMụcHiệnTại MànHình 안에 제한된다.
각 창의 giáTrịKýTự 칸은 `(khoảngTrảiRộng-24)/8`giáTrịCột, `(giáTrịCao-56)/16`행이다. `terminal size`로 조회한다.

명령줄의 giáTrịVào·giáTrịConTrỏVănBản·기록과 vi의 미저장 문서를 유지하며 보이는 영역을 갱신한다.
지난 출력은 저장된 dòng 단위를 유지하고, 좁아진 창에서 가려진 열은 giáTrịThửLại 넓히면
볼 trịSố 있다. 과거 ĐầuRa 전체를 새 너비에 맞춰 재배열하는 기능은 아니다.
크기를 바꾼 giáTrịLùi 출력되는 글은 새 giáTrịCột 수로 줄바꿈한다. vi는 giáTrịVào chờGiáTrị 중에도
SVC 16의 hànhĐộng 3으로 phầnMụcHiệnTại cỡ(상위 16비트 giáTrịHàng, 하위 16비트 giáTrịCột)를 조회한다.
tươngTác tty의 giáTrịNhân MànHình ĐầuRa 시간은 NgườiDùng phépTính 기한에서 제외하며, giáTrịVào chờGiáTrị 없이
계산만 반복하는 NgườiDùng 프로그램의 giáTrịThờiGian 제한은 유지한다.
커널이 프레임버퍼에 포인터를 그리며, Remmina 중계는 giáTrịTừXa 포인터를 숨겨 중복을 피한다.
로컬 VNC 중계는 giáTrịMặcĐịnh Raw 인코딩을 사용한다.

thẩmĐịnh: `make test-resize` — 640×480·1920×1080에서 네 giáTrịGóc, bênTrái/phải 버튼,
giáTrịTốiThiểu·giáTrịTốiĐa cỡ, conTrỏ 복원, giáTrịVào 보존, vi giáTrịCất·việcXửLýTiếpTục giáTrịVào, 창별 크기를 확인한다.
