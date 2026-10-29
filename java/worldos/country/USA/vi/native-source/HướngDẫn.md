# JUsaOS

phầnMụcHiệnTại tựThân ARM64 배포판은 [LICENSE](LICENSE)의 COSL 상업 조건을 유지한다. 제3자 라이선스의 권리는 별도로 보장하며, giáTrịBảnPhânPhối 시 câyNguồn·điểmCuốiKếtNốiLại 자료를 포함하는 절차는 [COSL giáTrịBảnPhânPhối HướngDẫn](platforms/rpi4-native/HướngDẫnBảnPhânPhốiCOSL.md)에 있다.

tựThân ARM64 판의 `ipconfig`/`ip`, `ping`, `ps`/`top`, `free`/`df`, `poweroff`와 tiếngViệt 명령은 [네트워크·giáTrịHệThốngĐiềuHành lệnh HướngDẫn](platforms/rpi4-native/CácLệnhHệThốngVàMạng.md)를 참고한다. 새 커널을 부팅한 giáTrịLùi `help system`으로 볼 trịSố 있다.

Raspberry Pi 4 **tựThân Java ARM64 giáTrịNhân**은 [tựThân Pi4 HướngDẫn](platforms/rpi4-native/HướngDẫn.md)에 있다. Linux 없이 부팅하며 GUI thiếtBịCuối·vi, tựThân JVM의 Swing 일부 API, TCP/UDP·FTP, 게스트 TinyCC·MicroPython, C/C++의 posix-kor 호출을 제공한다. [tiếngViệt Java TruyềnThông·ngoạiLệ API](platforms/rpi4-native/JavaTiếngViệt/HướngDẫn.md)와 [tiếngViệt câyNguồn cáchĐặtTên](platforms/rpi4-native/cáchĐặtTên/HướngDẫn.md)을 지원한다. [tựThân SSH·VNC 및 GENET 드라이버](platforms/rpi4-native/HướngDẫnKếtNốiBênNgoài.md)를 포함하며, 네트워크는 QEMU의 UART SLIP 경로로 검증했다. dữLiệuThựcTế Pi 4 GENET 동작은 미검증이고, USB giáTrịVào·영속 저장과 전체 OpenJDK·Swing은 아직 giáTrịHỗTrợ cắtXén 밖이다.

Raspberry Pi 4용 Linux·OpenJDK 실행판과 NgườiDùng môiTrường giáTrịDiChuyển 기능은 [라즈베리파이 실행판](platforms/rpi4/README.md)에 있다. dữLiệuThựcTế ARM64 JDK/JRE와 시스템·NgườiDùng xâyDựngẢnh xâyDựngHệThống 경로를 제공한다. 기존 tựThân x86 커널과는 별도 thựcThiLệnh 기반이다. 일반 Java `.class`/JAR의 thựcThiLệnh Tệp 생성은 [OpenJDK thựcThiLệnh Tệp](compiler/OpenJDK-tệpTệpThựcThi.md), tiếngViệt API는 [tiếngViệt Java thưViện](JavaTiếngViệt/HướngDẫn.md)를 참고한다.

`jkoros`는 `engos`의 기능을 Java 관리 커널로 옮기는 프로젝트다. 프로젝트가 소유하는 Java Hàm, giáTrịBiến, giáTrịĐịnhDạng 및 Java Tệp 이름은 한국어로 작성한다. 표준 Java 실행기의 `main`, Java 표준 thưViện giáTrịĐịnhDạng, x86 부트 ABI 등 giáTrịBênNgoài 계약은 보존한다. tựThân ARM64 실행기는 tiếngViệt `chạy()`도 진입점으로 지원하며, tiếngViệt GUI·TácVụ 가닥을 JVM에 직접 구현했다. tựThân ARM64 C 연결부·Python 도구와 공용 x86·ARM64 AOT 번역기의 tựThân 이름도 한국어로 작성한다. phầnMụcTrướcĐó 경로의 호환 điểmMục, OpenJDK giáTrịPhụTrợ 도구와 Linux giáTrịPhiênBản 도구에는 영어 이름이 남아 있고 [cáchĐặtTên 원칙·말의 근거·전체 mãNguồn 검토 cắtXén](platforms/rpi4-native/cáchĐặtTên/HướngDẫn.md)를 별도로 기록한다.

## phầnMụcHiệnTại phầnCàiĐặt

giáTrịĐáy 목록은 기존 `NguồnNềnTảng/`의 JVM 관리 커널에 대한 것이다. dữLiệuThựcTế 네이티브 커널의 범위는 `os/HướngDẫn.md`에서 별도로 설명한다.

- giáTrịCănChỉnh 할당과 해제를 지원하는 VùngNhớ giáTrịBộQuảnLý
- địaChỉ miềnĐịaChỉ, giáTrịTrang nốiKết, ghi 시 saoChépGiáTrị(COW)
- giáTrịTiếnTrình giáTrịĐịnhDanh, chuẩnBị 대기열, fork/wait giáTrịTrạngThái
- 과정별 Tệp mụcBộMôTả, open/read/seek/dup/close
- ELF32 nhậnDạngGiáTrị 및 giáTrịMụcĐoạn CácPhépKiểmTra
- 키보드·마우스 giáTrịVào sựKiện 대기열
- giáTrịNốiTiếp 단말과 네이티브 giáTrịPhầnCứng giáTrịRanhGiới
- 관리 giáTrịNhân 전체 자동 KiểmThử

세부 giáTrịPhépÁnhXạ 범위와 아직 필요한 네이티브 연결은 [기능 대응표](TàiLiệu/ĐốiChiếuChứcNăng.md)에 기록한다.

## 빌드와 KiểmThử

새 네이티브 구현은 `compiler/`와 `os/`에 있다. 기존 `NguồnNềnTảng/`의 JVM 관리 커널은 그대로 보존하며, 두 구현의 시험과 기능 범위는 서로 다르다.

```sh
cd /home/user/jkoros
make                 # 네이티브 phépTính VíDụ + Java giáTrịNhân ELF
make iso             # os/build/kernel.iso
make run             # QEMU giáTrịNốiTiếp VàoRaThiếtBịCuối; help giáTrịVào (종료는 Ctrl+A, X)
make run-gui         # ISO를 QEMU MànHình/PS2 키보드로 thựcThiLệnh
make vbox            # 전용 VirtualBox VM 자동 sinh·thựcThiLệnh (GUI)
make vbox-status     # VirtualBox giáTrịTrạngThái·ISO·giáTrịNốiTiếp bảnGhiNhậtKý đườngDẫn xácMinh
make test-vbox       # VirtualBox TrìnhKhởiChạyChươngTrình giáTrịTrạngThái mụcGiáTrịTiếnTrình KiểmThử (dữLiệuThựcTế VM đổiGiáTrị phươngThứcThiếu)
make test            # TrìnhBiênDịch KiểmThử + ELF/ISO KhởiĐộng 및 lệnh giáTrịVào KiểmThử
make apps            # 독립 NgườiDùng ELF ChươngTrình xâyDựngHệThống
make test-network    # NgườiDùng giáTrịChếĐộ·UDP 왕복·dữLiệuBộNhớ bảoVệGiáTrị KiểmThử
make test-java       # 게스트 javac/JVM + OpenJDK 양방향 교차 thựcThiLệnh KiểmThử
make posix-kor       # tiếngViệt C 헤더와 dữLiệuThựcTế giáTrịNhân gọiThựcHiện thưViện
make test-posix      # Tệp/UDP/giáTrịCất/Java Tệp đầuRaĐầuVào KiểmThử
make -C os run-store # 전용 giáTrịCất 매체로 QEMU KhởiĐộng
make legacy-test     # giáTrịĐáy 기존 JVM 관리 커널의 47개 KiểmThử
```

`compiler/`는 호스트의 `javac`를 문법·giáTrịKiểu CácPhépKiểmTra 전단으로 사용하고 tựThân mãByte→x86 변환기로 ELF32 기계어를 만든다. 빌드할 때는 JDK가 필요하지만 생성된 커널과 ELF는 giáTrịBênNgoài JVM 없이 실행된다. 전체 Java, giáTrịĐốiTượng 모델, 표준 라이브러리와 기존 관리 giáTrịNhân 전체의 AOT 변환은 아직 지원하지 않는다. 자세한 giáTrịHỗTrợ 문법과 명령은 [TrìnhBiênDịch HướngDẫn](compiler/HướngDẫn.md), dữLiệuThựcTế KhởiĐộng 기능과 한계는 [네이티브 HệĐiềuHành HướngDẫn](os/HướngDẫn.md)를 참고한다.

네이티브 셸에 tựThân 제한형 `javac`와 `java`를 추가했다. `edit Demo.java`로 소스를 입력하고 `.save`로 저장한 giáTrịLùi `javac Demo.java`, `java Demo`로 **게스트 내부에서 컴파일하고 thựcThiLệnh**할 trịSố 있다. giáTrịMặcĐịnh 예제는 `javac Hello.java`, `java Hello`toánHạngThứBa. 파일은 RAM에서 동작하며, 전용 giáTrịCất 매체를 연결하면 `sync`로 재부팅 후에도 보존할 trịSố 있다. **OpenJDK/JDK 전체 이식은 아니며**, 단일 giáTrịLớp·giáTrịTĩnh Hàm·SốNguyên·ChuỗiKýTự·điềuKiện/반복문과 일부 표준 호출을 지원한다. giáTrịHỗTrợ cắtXén, giáTrịBênNgoài Tệp 적재와 시험은 [Java phátTriển môiTrường HướngDẫn](TàiLiệu/MôiTrườngPhátTriểnJava.md)에 있다.

네이티브 셸에서 `apps`, `run hello first second`, `net`, `run netcheck`를 사용할 trịSố 있다. 독립 ELF를 ring 3에 적재하고 `int 0x80` 호출을 통해 ĐầuRa·cácĐốiSố·UDP 네트워크를 제공한다. 별도 Chủ 터미널에서 `python3 os/CôngCụ/PhụcHồiDữLiệu.py --port 9000`을 실행한 giáTrịLùi 게스트에서 `run udp 10.0.2.2 9000 hello`로 dữLiệuThựcTế 왕복을 확인한다. 새 ChươngTrình thanhGhiMục, API 및 제한은 [NgườiDùng thựcThiLệnh·네트워크 HướngDẫn](os/NgườiDùng/HướngDẫn.md)를 참고한다. phầnMụcHiệnTại QEMU RTL8139·giáTrịTĩnh IPv4·UDP 전용이며 TCP/DNS는 미지원이며, 전용 IDE giáTrịCất 형식과 POSIX Tệp/UDP 일부 기능을 추가했다.

`make vbox`는 `jkoros operating system` 전용 VM을 만들고 디스크 없이 ISO로 부팅한다. thựcThiLệnh 중이면 유지하고, giáTrịCất·일시정지 상태이면 재개하며, 꺼져 있을 때만 새 ISO를 빌드해 연결한다. VirtualBox에서 부팅과 셸의 NgườiDùng ChươngTrình 실행을 확인했다. 다만 phầnMụcHiệnTại VirtualBox용 네트워크 드라이버는 없어 네트워크 장치를 비활성화한다. UDP 시험에는 `make run`을 사용한다. 상태별 동작과 새 xâyDựngHệThống 반영 방법은 [VirtualBox thựcThiLệnh HướngDẫn](TàiLiệu/ChạyVirtualBox.md)에 있다.

기존 관리 커널만 시험하려면:

```sh
cd /home/user/jkoros
make -f tạoMục.mk CácPhépKiểmTra
make -f tạoMục.mk Chủ
```

`Chủ`는 여전히 JVM 관리 계층의 hànhĐộng 시험이다. `make -f tạoMục.mk xâyDựngẢnh`는 새 `os/`의 제한형 네이티브 giáTrịNhân ISO를 만든다. 기존 `NguồnNềnTảng/`의 HệThốngTệp·giáTrịTiếnTrình·NgănXếpMạng phầnCàiĐặt 전체를 이 ISO에 이식했다는 의미는 아니다.

tiếngViệt Hàm·giáTrịBiến·Tệp 이름과 dữLiệuThựcTế C API는 [posix-kor](posix-kor/HướngDẫn.md)에 있다. 게스트 Java에서는 `FileInputStream`·`FileOutputStream`의 단일 giáTrịByte 입출력도 지원한다. 전체 POSIX·OpenJDK·Swing 지원으로 확대된 것은 아니다.

giáTrịBênNgoài 배포용 `pack.sh` / `unpack.sh`와 자동 cácPhụThuộc 복원은 [giáTrịBảnPhânPhối HướngDẫn](distribution/README.md)를 참고하세요.
