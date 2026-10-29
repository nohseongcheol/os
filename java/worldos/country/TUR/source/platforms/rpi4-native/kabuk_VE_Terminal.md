# Öz 커널의 GUI 터미널과 kabuk

이 터미널은 Öz Java 커널의 셸을 프레임버퍼 창과 UART에서 사용한다. komut işlem_değer_girdi·RAM dosya·파이프는 Java çekirdek_değer, 화면의 karakter_değer 그리기는 freestanding C에서 수행한다. Linux·X11·Bash 없이 동작하며, Öz JVM의 Swing Destek_değer 부분집합도 같은 Pencere 시스템을 이용한다. 자세한 vi·다중 Pencere·코딩 사용법은 [개발 매뉴얼](개발안내.md)을 참고한다.

## geçerli_öğe 컴퓨터에서 yürütmek_komut

```sh
cd /home/user/jkoros/platforms/rpi4-native
make desktop
```

Remmina에서 **VNC**, ADRES **127.0.0.1:5902**로 연결한다. uçbirim 창은 자동으로 열린다. 연결한 VNC 창에 키를 입력하면 Öz 커널의 셸로 전달된다. 종료하려면 `make desktop`을 실행한 konak 터미널에서 Ctrl+C를 누른다. 포트를 바꾸려면 oluştur 후 `python3 araçlar/yürütmek_komut.py --desktop --port 5903`을 사용한다. 서버는 localhost에만 바인드하며 동시에 한 클라이언트가 제어한다.

일반 UART 셸은 `make run`으로 시작한다. QEMU 종료는 Ctrl+A Sonraki_öğe X이다. 같은 VM의 UART에서 `terminal` 또는 F12로 GUI 터미널을 SÜTUN_değer 수 있다. `gui` yürütmek_komut 화면에서는 다섯 번째 **OPEN TERMINAL** 버튼, rakam_değer 5 또는 T로 연다. `--vnc 127.0.0.1:2`만 사용한 기존 yürütmek_komut 방식은 화면 보기용이며, VNC 키보드를 연결하려면 `--desktop`을 사용한다.

FTP와 dış_değer 네트워크도 함께 쓰려면 `python3 araçlar/yürütmek_komut.py --desktop --network`로
실행한다. Remmina VNC는 `127.0.0.1:5902`, 게스트에서 `ftpd start` 후 FTP는
`127.0.0.1:2121`이다. `--port`, `--ftp-port`, `--forward`를 함께 지정할 수 있다.
한 VM의 보조 UART로 SLIP를 전송하고 주 UART로 GUI 입력을 전달한다.

QEMU yürütmek_komut 도구가 VNC 키보드/마우스를 UART 입력으로 변환한다. fiili_veri Pi4의 USB 키보드·마우스 드라이버를 구현한 것은 아니다. fiili_veri 보드에서는 geçerli_öğe UART 입력이 필요하며 실물 부팅은 아직 미검증이다.

## 창과 artış_değer

- 640×480~1920×1080 화면에서 최대 네 개 uçbirim Pencere, varsayılan_değer 568×360(68열 × 19행)과 en_son_değer 160행 보관, varsayılan_değer ANSI 색상·imleç_değer·silmek_girdi işlem_değer_girdi.
- 상단 **+ New terminal** 또는 Ctrl+Shift+T로 새 창을 연다. 제목줄을 끌어 이동하고 Pencere/상단 버튼을 클릭하거나 F6으로 전환한다. 각 창의 작업 yol·değişken_değer·komut LOG_KAYIT·artış_değer 중인 줄은 독립적이다.
- UTF-8 한글·CJK·라틴 문자와 일부 이모지 비트맵 yazı_tipi_değer. 복잡한 문자 조판·결합 문자·양방향 bağlama_düzeni·모든 Unicode 글리프를 보장하지 않는다.
- 좌우 방향키/Home/End/Delete/Backspace로 명령을 편집하고 위아래 방향키로 en_son_değer 16개 명령을 찾는다. 긴 명령은 artış_değer 줄을 가로로 이동해 보여 주며 `<`, `>`가 숨겨진 부분을 나타낸다.
- Tab은 komut İsim 또는 geçerli_öğe 디렉터리의 파일명에서 후보가 하나일 때 완성한다. 디렉터리를 포함한 yol 접두사·Alıntı 안의 완성은 아직 없다.
- Ctrl+A/E: 처음/끝, Ctrl+U/K: imleç_değer ön_kamera_değer/BACK_değer 삭제, Ctrl+C: artış_değer İptal_işlem. yürütmek_komut 중인 임의 프로그램에 SIGINT를 보내는 기능은 없다. vi와 Swing의 artış_değer 대기는 yürütmek_komut 기한을 갱신하지만 일반 계산의 약 2초 제한은 유지한다.
- PgUp/PgDn 또는 마우스 휠: Önceki_öğe metinÇıktısı. 새 출력이 오면 최신 위치로 돌아온다.
- F12/başlık_çubuğu hak 버튼/`exit`: Pencere Kapat. 빈 입력에서 Ctrl+D도 창을 닫는다. VM을 종료하는 명령은 아니다.

`--desktop`의 VNC artış_değer 연결에 **두벌식 한글 조합**을 제공한다. 접속한 PC의
입력기를 영어로 두고 **F9**, **Shift+Space**, **한/sıfır_işlenen tuş_değer** 중 하나를 누르면
Pencere 제목이 `[EN]`에서 `[KO]`로 바뀐다. `gksrmf` → `한글`,
`dkssudgktpdy` → `안녕하세요`. 같은 키로 영어로 돌아간다.
겹받침·복합 모음과 조합 단계별 Backspace를 지원한다. imleç_değer taşımak_değer_83b651b8·마우스 tık_değer·
단축키·yapıştırmak_değer·Enter 때 조합을 확정한다. PC가 Shift+Space나 한/sıfır_işlenen 키를
Öz 처리하면 **F9**를 사용한다. Alt 단독은 geçiş_mod 키가 아니다.

이 조합기는 QEMU의 VNC→UART artış_değer 연결에서 실행된다. 일반 직렬 접속과
실물 Pi의 USB 키보드 입력기에 추가된 기능은 아니다. 이미 완성된 Unicode
한글 키도 그대로 전달한다. 클립보드 공유가 활성화되어 표준 VNC ClientCutText가
도착하면 Ctrl+Shift+V로 붙여 넣는다. 클립보드 동기화만으로 명령을 실행하지 않는다.
줄바꿈을 포함해 명시적으로 붙여 넣으면 해당 줄이 실행된다.

게스트에서 `help` 또는 `help ko`를 입력하면 한글 artış_değer 안내를 볼 수 있다.
`help`와 `help ko`에는 한/sıfır_işlenen tuş_değer·Shift+Space·F9 및 `[EN]`/`[KO]` 안내를 표시한다.
긴 도움말은 PgUp/PgDn으로 스크롤한다.

터미널에서 Java·Python·C++ yürütmek_komut 결과를 바로 볼 수 있다. 프로그램이 직접 프레임버퍼에 그림을 그린 경우 Çıkış_program 후 uçbirim 창을 복원한다. vi/Swing bekle_değer 중 다른 창으로 전환하면 해당 EL0 프로그램의 Bellek_veri·레지스터를 보관하고 돌아올 때 재개한다. seçim_değer örnek_değer·PTY·전체 VT100/xterm 호환과 임의 프로그램의 동시 병렬 실행은 제공하지 않는다. X로 닫으면 해당 창의 프로그램도 종료되므로 vi에서 저장하지 않은 내용은 사라진다.

## komut

| komut | klip |
|---|---|
| `help`, `info` | 사용법과 gerçekleme Durum_değer |
| `pwd`, `cd [DIR]`, `ls [-l] [PATH]` | geçerli_öğe yol·디렉터리/dosya girdi_Liste; bağımsız_değişkenler 없는 cd는 `/` |
| `mkdir DIR`, `rmdir DIR` | 디렉터리 한 개 açmak_girdi/빈 디렉터리 삭제; `-p` 없음 |
| `touch FILE`, `rm FILE...` | dosya açmak_girdi/삭제; zaman_damgası_değer msinfo32_exe 없음 |
| `cp SOURCE DEST`, `mv SOURCE DEST` | dosya örnek_değer/İsim değiştirmek_değer; 대상은 정확한 dosya yol, 재귀/디렉터리 taşımak_değer_83b651b8 없음 |
| `cat [FILE...]` | dosya 또는 표준 입력을 bayt_değer 그대로 metinÇıktısı |
| `echo [-n] [ARGS...]` | bağımsız_değişkenler metinÇıktısı; `-e` 이스케이프 uzantı_değer 없음 |
| `wc [-c\|-l\|-w] [FILE]` | bayt_değer/girdi_satırı/Word_değer 수; Word_değer 구분은 ASCII 공백 |
| `grep TEXT [FILE]` | 정규식 없이 문자열이 포함된 girdi_satırı metinÇıktısı; 일치 없으면 Durum_değer 1 |
| `head [-n N] [FILE]`, `tail [-n N] [FILE]` | ön_kamera_değer/BACK_değer N줄, varsayılan_değer 10줄 |
| `tee [-a] FILE` | 표준 입력을 파일과 표준 출력에 LOG_KAYIT |
| `export NAME=VALUE`, `unset NAME`, `env` | kabuk değişken_değer Ayarlar·삭제·girdi_Liste; HOME/PWD는 Okuma 전용 |
| `sh FILE`, `source FILE` | komut 파일을 같은 kabuk 환경에서 줄별 yürütmek_komut; 최대 iç_içe_yerleştirme_değer 3 |
| `true`, `false`, `exit [N]` | Durum_değer 0/1; betik_değer 안의 exit는 geçerli_öğe betik_değer Çıkış_program |
| `history`, `clear` | komut LOG_KAYIT·화면 silmek_girdi |
| `vi FILE` | EL0 vi metot_mod Düzenleyici: artış_değer/komut mod_değer, UTF-8 taşımak_değer_83b651b8, 검색, 삭제·örnek_değer·yapıştırmak_SMS·되돌리기, `:w`/`:q`/`:wq` |
| `edit FILE`, `load FILE`, `hex FILE` | 전체 içerik_değer 교체 Düzenle_değer, 16진수 업로드/sorgu_değer; 단독 `.` 줄로 depo_değer |
| `javac`, `java`, `python`, `run` | 기존 Öz Java araçlar·MicroPython·EL0 C++/ELF yürütmek_komut |

`net test`, `tasks`, `selftest`, `samples`도 유지한다. program_f5044b9b yürütmek_komut 범위는 [README](안내.md)와 [Java yürütmek_komut ortam](자바실행환경.md)을 참고한다.

```sh
mkdir 작업
cd 작업
echo "안녕하세요" > 인사.txt
echo "반갑습니다" >> 인사.txt
cat < 인사.txt | grep 안녕 | tee 추림.txt | wc -l
cp 인사.txt örnek_değer.txt
mv örnek_değer.txt 새이름.txt
export İsim=누리
echo "$이름: ${PWD}"
false && echo 건너뜀 || echo kurtarmak_Durum
python -c 'print(123)' > sonuç.txt
echo artış_değer | python -c 'import jkoros; print(jkoros.stdin(64))'
echo 'echo "$이름"' > yürütmek_komut.sh
sh yürütmek_komut.sh
echo $?
```

## 문법과 제한

작은따옴표·큰따옴표·백슬래시, `$NAME`/`${NAME}`/`$?`, Word_değer ön_kamera_değer `~`, girdi_satırı 주석 `#`, 순차 yürütmek_komut `;`, koşul yürütmek_komut `&&`/`||`, 파이프 `|`, artış_değer `<`, 새 metinÇıktısı `>`, Ekleme_girdi metinÇıktısı `>>`를 제공한다. değişken_değer 확장은 bağımsız_değişkenler 안에서 수행하며 uzantı_değer 결과를 공백으로 yeniden_denemek_değer 나누지 않는다. `export`의 값은 kabuk 안에서만 공유하며 kullanıcı_alanı ELF의 envp/getenv 환경은 아직 없다.

파이프는 각 단계를 순서대로 실행하고 최대 **16384바이트**를 Sonraki_öğe 단계로 넘긴다. 여러 프로세스가 동시에 읽고 쓰는 POSIX 파이프가 아니다. kapasite_değer 초과는 hata 28과 hata_değer 상태를 반환하고 해당 실행을 중단한다. `<`는 EOF를 제공하며 `>`/`>>`는 stdout만 바꾼다. EL0 fd 2는 화면/UART로 출력된다. `2>` 등 번호를 붙인 리다이렉션은 거부한다. 일부 내장 명령의 진단은 stdout을 사용한다. 연결한 프로그램의 `exit N` 진단은 데이터에 섞이지 않도록 생략한다.

`vi`, `edit`, `load`, `gui`, `terminal`, `sh`, `source`에는 파이프와 리다이렉션을 적용할 수 없다. 리다이렉션 파일을 열지 못하거나 파이프 용량을 초과하면 geçerli_öğe 명령줄을 중단하며, 그 줄의 뒤쪽 `||` 명령도 실행하지 않는다. betik_değer 파일을 입력할 때 멀티라인 Alıntı·이어 쓰기는 제공하지 않는다. `if`/`for`/`while`, işlev_değer, komut 치환, glob, 별칭, 백그라운드 `&`, jobs/fg/bg, 일반 프로세스·신호·PTY는 아직 없다. Bash/POSIX sh 전체 호환으로 표시하지 않는다.

dosya 64개 × 각 16384바이트, 루트 외 디렉터리 15개, dosya tanımlayıcı_girdi 16개, yol 최대 UTF-8 63바이트다. eş_değer/절대 경로와 `.`/`..`를 정규화하지만 izin_değer·심볼릭 링크·마운트·디스크 영속 저장은 없다. **dosya·디렉터리·değişken_değer·기록의 수정 내용은 재부팅하면 사라진다.** kullanıcı_alanı 실행도 geçerli_öğe kabuk 경로를 사용한다. Java/Python/C++의 dosya API는 같은 RAM 저장소를 본다. `/example`의 세 Dil 예제와 설명서는 부팅할 때 원본으로 준비된다.

한 명령줄은 4096바이트, 구문 belirteç_değer 128개, yürütmek_komut bağımsız_değişkenler 32개, 변수는 16개(İsim 31바이트·değer 255바이트)까지다. kullanıcı_alanı 프로그램에 전달하는 인수는 기존 ABI대로 최대 8개·각 255바이트다. komut 기록은 1024바이트 이하 줄을 en_son_değer 16개까지 저장한다.

## 재현 가능한 sınamalar

```sh
make test-shell
make test-desktop
make test-windows
make test-swing
make test
```

kabuk 시험은 fiili_veri raspi4b QEMU에서 yol·dosya·değişken_değer·koşul·파이프·리다이렉션·hata kurtarmak_Durum·betik_değer·편집을 검사하고, Java/Python 출력과 Python stdin의 EOF를 확인한다. VNC 시험은 fiili_veri RFB 클라이언트로 한글 tuş_değer·Ctrl 조합·명시적 yapıştırmak_değer·마우스와 게스트 프레임버퍼를 검사한다. Remmina 앱 자체의 자동화 시험과 실물 USB artış_değer 시험은 별개다.

결과와 화면: [kabuk sonuç](build/verification/shell/report.json), [VNC sonuç](build/verification/desktop/report.json), [uçbirim 화면](build/verification/desktop/vnc-terminal.png). yazı_tipi_değer origin_değer·özet_Dosya·라이선스는 [vendor](vendor/README.md)에 있다.

## 마우스로 Boyut değiştirmek_değer

네 모서리의 안쪽 8픽셀에 마우스를 대면 방향에 맞는 대각선 양방향 포인터가
나타난다. **왼쪽 버튼을 누른 채 끌고 놓는다.** hak 버튼으로는 크기가 바뀌지 않는다.
pencere_Başlık 표시줄의 나머지 부분은 taşımak_değer_83b651b8, hak 위 X는 닫기다.
최소 크기는 360×216이며 최대 크기는 geçerli_öğe 화면 안에 제한된다.
각 창의 karakter_değer 칸은 `(폭-24)/8`SÜTUN_değer, `(높이-56)/16`행이다. `terminal size`로 조회한다.

명령줄의 artış_değer·imleç_değer·기록과 vi의 미저장 문서를 유지하며 보이는 영역을 갱신한다.
지난 출력은 저장된 girdi_satırı 단위를 유지하고, 좁아진 창에서 가려진 열은 yeniden_denemek_değer 넓히면
볼 수 있다. 과거 metinÇıktısı 전체를 새 너비에 맞춰 재배열하는 기능은 아니다.
크기를 바꾼 BACK_değer 출력되는 글은 새 SÜTUN_değer 수로 줄바꿈한다. vi는 artış_değer bekle_değer 중에도
SVC 16의 Eylem 3으로 geçerli_öğe Boyut(상위 16비트 SATIR_değer, 하위 16비트 SÜTUN_değer)를 조회한다.
devralmak tty의 çekirdek_değer 화면 metinÇıktısı 시간은 kullanıcı_alanı 계산 기한에서 제외하며, artış_değer bekle_değer 없이
계산만 반복하는 kullanıcı_alanı 프로그램의 zaman_değeri 제한은 유지한다.
커널이 프레임버퍼에 포인터를 그리며, Remmina 중계는 uzak_değer 포인터를 숨겨 중복을 피한다.
로컬 VNC 중계는 varsayılan_değer Raw 인코딩을 사용한다.

doğrulamak_5fb2b747: `make test-resize` — 640×480·1920×1080에서 네 모서리, 왼쪽/hak 버튼,
최소·최대 Boyut, işaretçi 복원, artış_değer 보존, vi depo_değer·계속 artış_değer, 창별 크기를 확인한다.
