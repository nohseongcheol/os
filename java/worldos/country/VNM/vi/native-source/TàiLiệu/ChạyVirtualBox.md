# VirtualBox thựcThiLệnh

```sh
cd ~/jkoros
make vbox
```

별도로 VM을 만들거나 ISO를 연결할 필요가 없다. phầnMụcBanĐầu 실행하면 `os/build/kernel.iso`를 빌드하고 `jkoros operating system`이라는 전용 VM을 만들어 VirtualBox 창으로 부팅한다. `jkoros/os` 안에서도 `make vbox`를 사용할 trịSố 있다.

게스트의 `jkoros>` 프롬프트에서 phầnMụcKếTiếp 명령을 입력한다.

```text
help
apps
run hello vbox
```

phầnMụcCuối 명령은 별도 Java ELF를 실행한다. `USER MODE ring 3`, `arg: vbox`, `Exit: 0` ĐầuRa trạngTháiSau 셸로 돌아오면 정상이다. VGA 화면은 phầnMụcHiệnTại ASCII 글꼴만 지원하므로 한글은 `?`로 보이며, vănBảnHangul 원문은 giáTrịNốiTiếp 기록에서 확인할 trịSố 있다.

## giáTrịTrạngThái 확인과 giáTrịThửLại thựcThiLệnh

```sh
make vbox-status
```

이 명령은 VM giáTrịTrạngThái, ISO와 giáTrịNốiTiếp 기록의 절대 경로를 JSON으로 출력한다.

| phầnMụcHiệnTại giáTrịTrạngThái | `make vbox` hànhĐộng |
| --- | --- |
| 아직 생성하지 않음 | ISO xâyDựngHệThống → 전용 VM sinh → KhởiĐộng |
| cóĐãRa (`poweroff`, `aborted`) | ISO xâyDựngHệThống → 광학 giáTrịPhươngTiện làmMới → 새로 KhởiĐộng |
| thựcThiLệnh 중 (`running`) | 재빌드·재부팅 없이 phầnMụcHiệnTại VM giữLạiGiáTrị |
| 일시정지 (`paused`) | 기존 VM việcThựcThiTiếpDiễn |
| 저장됨 (`saved`) | phầnMụcTrướcĐó giáTrịNốiTiếp 기록을 복사해 보관하고 giáTrịCất giáTrịTrạngThái việcThựcThiTiếpDiễn |
| giáTrịCất·chạy 등 chếĐộChuyển 중 | 변경하지 않고 TácVụ làĐầyĐủ trạngTháiSau 재실행하도록 HướngDẫn |

câyNguồn 변경을 반영하려면 VM을 종료한 phầnMụcKếTiếp giáTrịThửLại `make vbox`를 실행한다. **giáTrịCất 상태를 재개하면 phầnMụcTrướcĐó 커널이 việcXửLýTiếpTục 실행되므로 새 빌드를 반영하지 않는다.** 실행기는 강제 종료하거나 giáTrịCất 상태를 폐기하지 않는다. VirtualBox 창을 닫을 때 사용자가 전원 끄기를 선택하면 dữLiệuBộNhớ 상태가 사라지므로 보존할 작업이 없는지 먼저 확인한다. 게스트의 `halt`는 CPU만 멈추며 VirtualBox의 전원을 끄는 명령은 아니다.

cửaSổ 없는 실행이 필요하면 VM이 꺼져 있을 때 사용한다.

```sh
make vbox VBOX_TYPE=headless
```

thựcThiLệnh 중인 VM에 giáTrịThửLại 명령을 내려도 GUI/headless 방식은 바뀌지 않는다. giáTrịMặcĐịnh tên 대신 다른 이름이 필요하면 **최초 sinh 시에만** `VBOX_NAME="원하는 tên"`을 지정하고 이후에도 같은 값을 사용한다.

## 설정과 DữLiệu 보존

- giáTrịMặcĐịnh 설정은 BIOS, dữLiệuBộNhớ 64MiB, CPU 1개, VGA dữLiệuBộNhớ 16MiB, IDE 광학 부팅이다. 가상 하드디스크를 만들지 않는다.
- VM 설정은 `.vbox/machines/`, giáTrịNộiDung 검사합별 ISO 사본은 `.vbox/media/`, giáTrịNốiTiếp 기록은 `.vbox/logs/`에 보관한다. `.vbox/state.json`은 전용 VM의 UUID와 giáTrịChủSởHữu 표식을 저장한다.
- 꺼진 VM을 부팅할 때 새 giáTrịNốiTiếp 기록을 만든다. giáTrịCất giáTrịTrạngThái việcThựcThiTiếpDiễn 전의 기록은 `before-resume-*.log`로 복사한다. giáTrịCất giáTrịTrạngThái 자체는 삭제하지 않고 VirtualBox가 그대로 재개한다.
- 같은 이름의 다른 VM을 인수하지 않는다. UUID·cácThiếtLập đườngDẫn·giáTrịChủSởHữu 표식을 검사하며, 사용자가 별도로 연결한 디스크나 광학 매체를 자동 교체하지 않는다.
- 기존 ISO 사본과 기록은 자동 삭제하지 않는다. `.vbox`는 Git giáTrịLoạiTrừ 대상이다. 용량을 정리할 때도 thựcThiLệnh·giáTrịCất 상태의 VM이 참조하는 파일과 관리 정보를 임의로 삭제하지 않는다.
- VirtualBox 또는 Chủ 드라이버가 없으면 오류를 안내한다. 자동 càiĐặtGiáTrị, giáTrịBộQuảnLý giáTrịQuyền thựcThiLệnh, ThiếtBị giáTrịQuyền 변경은 하지 않는다.

## 네트워크 giáTrịGiớiHạn

phầnMụcHiệnTại 커널의 RTL8139 드라이버는 QEMU에서 사용한다. VirtualBox의 PCnet/E1000 드라이버는 아직 구현하지 않아 이 실행기는 네트워크 장치를 비활성화한다. 셸과 NgườiDùng 프로그램은 실행되지만 UDP 열기는 `-19`로 실패한다. UDP 왕복은 `make run`과 [NgườiDùng thựcThiLệnh·네트워크 HướngDẫn](../os/NgườiDùng/HướngDẫn.md)의 절차로 시험한다.

## thẩmĐịnh

`make test-vbox`는 가짜 VirtualBox 응답을 사용하여 새 VM sinh, thựcThiLệnh·giáTrịCất·일시정지·chếĐộChuyển giáTrịTrạngThái, tên 충돌, 소유권 불일치, NgườiDùng giáTrịPhươngTiện bảoVệGiáTrị, xâyDựngHệThống giáTrịSựThấtBại, 중단된 sinh khôiPhụcTrạngThái, ISO đổiGiáTrị 감지, đườngDẫn bảoVệGiáTrị 등을 검사한다. dữLiệuThựcTế VM을 만들거나 변경하지 않는다.

2026-09-13에 TrìnhKhởiChạyChươngTrình giáTrịĐơnVị KiểmThử 16개가 통과했다. 별도로 dữLiệuThựcTế VirtualBox 5.2.42에서 `make vbox`의 VM sinh·GUI KhởiĐộng, `JAVA SELFTEST PASS`, 셸의 `run hello vbox` 실행과 `Exit: 0`, thựcThiLệnh 중 재호출 시 재부팅하지 않는 hànhĐộng 및 `make vbox-status`를 확인했다. giáTrịCất·일시정지 분기는 giáTrịĐơnVị 시험으로 검증했다.
