# tựThân 커널의 네트워크와 giáTrịHệThốngĐiềuHành lệnh

게스트 SSH·VNC, LAN 공개 thựcThiLệnh, Pi4 GENET·DHCP 추가분은 [giáTrịBênNgoài kếtNối HướngDẫn](HướngDẫnKếtNốiBênNgoài.md)를 먼저 참고한다. QEMU는 `sl0`, phầnCứngVậtLý GENET은 `en0`를 사용한다. phầnCứngVậtLý 드라이버는 아직 보드에서 검증하지 않았다.

이 문서는 `platforms/rpi4-native`의 tựThân ARM64 Java 커널용이다. Linux/OpenJDK 실행환경의 명령어와 구분한다. 새 커널을 빌드하고 giáTrịThửLại 부팅해야 적용된다.

셸과 Java의 dữLiệuThựcTế CPU giáTrịQuyền, `ps`/`top`에 표시되는 giáTrịĐơnVị, Chủ·giáTrịBênNgoài PC nốiKết 방법은
[thựcThiLệnh 계층과 giáTrịBênNgoài TruyềnThông xemXétTrạngThái](CácPhépKiểmTraMạngBênNgoàiVàMôiTrườngChạy.md)에 정리했다.

```sh
cd /home/user/jkoros/platforms/rpi4-native
make desktop ARGS=--network RESOLUTION=1920x1080
# giáTrịNốiTiếp 셸만 사용할 때
make run ARGS=--network
```

게스트에서 `help`, `help system` 또는 `hiệnTrợGiúp system`을 입력한다. giáTrịĐáy 두 이름은 같은 동작을 하며 현지어 이름도 Tab으로 완성할 trịSố 있다.

| 표준 lệnh | tiếngViệt lệnh | 기능 |
|---|---|---|
| ipconfig, ifconfig | 아이피설정 | dữLiệuThựcTế IPv4 địaChỉ·넷마스크·giáTrịCổngNối·송수신 통계 |
| ip | địaChỉIP | địaChỉ giáTrịTruyVấn·cácThiếtLập, nốiKết cácTệpTảiLên·내리기, đườngDẫn giáTrịTruyVấn |
| ping | thửPhảnHồi | dữLiệuThựcTế ICMPv4 lờiĐáp·손실률·왕복 giáTrịThờiGian |
| route | 경로표 | 직접 연결망과 giáTrịMặcĐịnh giáTrịCổngNối |
| netstat, ss | 통신현황 | dữLiệuThựcTế TCP/UDP 끝점의 địaChỉ·cổngPhầnCứng·giáTrịTrạngThái·nhậnGiáTrị 대기량 |
| ps | 작업목록 | giáTrịNhân 작업과 NgườiDùng ChươngTrình PID·giáTrịTrạngThái·매핑량·giáTrịThờiGian |
| top | 작업현황 | 1초마다 TácVụ·dữLiệuBộNhớ giáTrịTruyVấn; q 또는 Ctrl+C로 chươngTrìnhThoátHẳn |
| free | 기억현황 | 펌웨어 RAM, giáTrịNhân giáTrịMiền, AOT giáTrịVùngNhớĐộng, MànHình, NgườiDùng giáTrịĐãÁnhXạ |
| df | 저장현황 | RAM 파일시스템의 dữLiệuThựcTế giáTrịSứcChứa·예약량·자료량·Tệp mụcÔ |
| uptime | 가동시간 | KhởiĐộng trạngTháiSau 경과 giáTrịThờiGian |
| poweroff | tắtNguồnĐiện | 서비스와 NgườiDùng 작업을 정리하고 게스트 chươngTrìnhRa |
| help | hiệnTrợGiúp | 표준·현지어 명령과 môTả |

## IP 설정과 TruyềnThông xácMinh

```sh
ipconfig
ip addr show
ipconfig set 10.0.2.20 255.255.255.0 10.0.2.2
아이피설정 set 10.0.2.20 255.255.255.0 10.0.2.2
ping -c 4 -W 1 10.0.2.2
thửPhảnHồi -c 4 10.0.2.2
ip route show
ip link set dev sl0 down
ip link set dev sl0 up
netstat
```

초깃값은 `sl0`, `10.0.2.15/24`, giáTrịCổngNối `10.0.2.2`toánHạngThứBa. địaChỉ 설정은 재부팅 전까지 유지된다. TCP/UDP 끝점이 열려 있으면 `error -16`으로 변경을 거부한다. 먼저 `ftpd stop` 등으로 서비스를 닫고 프로그램의 소켓을 닫는다. 잘못된 địaChỉ·비연속 넷마스크·다른 망의 관문은 적용하지 않는다.

`ip`는 giáTrịĐỉnh 구문의 부분집합이며 Linux iproute2 전체 문법을 구현하지 않는다. `ping`은 IPv4 giáTrịChữSố địaChỉ, `-c 1..100`, `-W 1..10`초를 지원한다. tên phânTíchCúPhápGiáTrị·IPv6는 미지원이며 GENET의 DHCP는 giáTrịBênNgoài kếtNối 구현에 추가했다. 응답이 없으면 mãRa 1, 잘못된 인수는 2, NgườiDùng 취소는 130이다. `ping ...; echo $?`로 확인한다.

QEMU giáTrịBênNgoài 통신은 UART SLIP→NAT 연결을 사용한다. `--network` 없이도 tựThân địaChỉ giáTrịTruyVấn·설정은 가능하지만 giáTrịBênNgoài 응답은 오지 않는다. giáTrịMặcĐịnh NAT는 `10.0.2.0/24`toánHạngThứBa. phầnCứngVậtLý Pi의 GENET 드라이버는 별도로 추가했으며 BoMạch 검증이 필요하다. Wi-Fi는 미지원이다.

주소를 `.20`으로 바꾼 giáTrịLùi FTP 등 **외부에서 들어오는 nốiKết**đếnKhi 사용할 때는 thựcThiLệnh 시 giáTrịTiến 대상도 지정한다.

```sh
make desktop ARGS="--network --guest-ip 10.0.2.20"
# 부팅한 게스트 안에서
ipconfig set 10.0.2.20 255.255.255.0 10.0.2.2
ftpd start
```

`--guest-ip`는 NAT giáTrịTiến 대상이며 게스트의 주소를 자동 설정하지 않는다. FTP giáTrịĐiềuKhiển 포트는 Chủ `127.0.0.1:2121`, 수동 데이터 포트는 50000~50007이다. 여러 VM을 함께 띄울 때는 `--network-host 127.0.0.2 --port 5903`처럼 Chủ 루프백 주소와 VNC 포트를 구분한다. FTP와 Java/C 소켓은 변경된 dữLiệuThựcTế 게스트 IP를 사용한다.

## giáTrịTrạngThái 조회의 의미

`ps`는 giáTrịNhân/vỏLệnh, 살아 있는 협력 TácVụ, giáTrịTốiĐa 4개의 EL0 NgườiDùng 세션을 표시한다. 다른 터미널에 열린 `vi` 등을 `SUSPENDED` 상태로 볼 trịSố 있다. `MAPPED_KiB`는 dữLiệuThựcTế 페이지 giáTrịĐãÁnhXạ, `RUN_ms`는 해당 세션이 선택된 동안의 경과 giáTrịThờiGian(시스템 gọiThựcHiện TệpĐầuMục)이며 정밀 CPU 사용률이 아니다. `top -n 1`은 한 번, `top -n 2`는 두 번 표시한다. 리다이렉션된 `top`의 기본값은 한 번이다.

`free`의 AOT giáTrịVùngNhớĐộng 사용량은 할당기에서 읽는다. 힙은 giáTrịNhân BSS에 포함되므로 각 줄을 xâyDựngTấtCả 더하면 중복된다. 고정 예약 영역과 NgườiDùng 페이지 매핑을 표시하며 Linux의 가용 RAM 계산이나 Chủ dữLiệuBộNhớ 통계를 꾸며서 표시하지 않는다.

`df`는 RAM 파일시스템의 Tệp 64칸 × 16 KiB를 표시한다. Tệp 하나는 논리 크기와 별도로 16 KiB 칸을 예약한다. `Data`는 dữLiệuThựcTế DữLiệu độDài giáTrịTổngCộng, `Reserved`는 giáTrịDùng 중인 mụcÔ 용량이다. 삭제 후에도 열린 파일은 phầnMụcCuối 참조를 닫을 때까지 계산한다. SD/영구 디스크 사용량은 아직 지원하지 않는다.

## 종료와 thẩmĐịnh

게스트에서 `poweroff` 또는 `tắtNguồnĐiện`를 입력한다. FTP·giáTrịỔCắmMạng·NgườiDùng 세션을 닫은 giáTrịLùi BCM PM chươngTrìnhRa 절차를 실행한다. RAM 파일은 재부팅 trạngTháiSau 보존되지 않는다. QEMU에서는 게스트의 `SHUTDOWN / guest-shutdown` 이벤트와 làBìnhThường 종료를 검증한다. phầnCứngVậtLý Pi 4 전원 회로 동작은 아직 시험하지 않았다.

phầnCàiĐặt 근거: [Linux BCM watchdog의 power-off 절차](https://github.com/torvalds/linux/blob/master/drivers/watchdog/bcm2835_wdt.c), [QEMU BCM PM ThiếtBị](https://github.com/qemu/qemu/blob/master/hw/misc/bcm2835_powermgt.c).

```sh
make test-system
# kếtQuả: build/verification/system-tools/report.json 및 serial.log
```

이 시험은 잘못된 IP từChốiGiáTrị, dữLiệuThựcTế ICMP giáTrịThànhCông·시간초과, nốiKết up/down, IP đổiGiáTrị trạngTháiSau FTP 송수신, df sinh·삭제, giáTrịVùngNhớĐộng phépTính, 다른 터미널의 vi PID·dữLiệuBộNhớ, top làmMới·chươngTrìnhRa, vănBảnHangul lệnh·Tab, 게스트 poweroff를 검사한다.

`java/worldos/giáTrịQuốcGia/국가코드` 판에는 같은 기능과 국가별 lệnh 대응표 `native-commands.json`이 들어간다. 표준 명령은 모든 판에서 유지한다. 새 현지어 이름은 기능 중심 제안이며 현지 화자·어원 검토를 완료한 표준 용어는 아니다. 미번역 항목은 대응표의 `pending`에 명시한다.
