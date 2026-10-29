# tựThân ARM64 Java 커널의 C/C++ Tệp·루프백 nốiKết

이 디렉터리는 `platforms/rpi4-native` tựThân giáTrịNhân 전용이다. 기존 i386 `int 0x80` 라이브러리나 ARM64 Linux libc용 라이브러리가 아니다.

`TệpĐầuMục/ABITệp.h`는 tiếngViệt 함수명과 `extern "C"` ABI를 제공한다. `nốiKết.c`는 giáTrịNhân 안에서 AOT Java Tệp 메서드에 직접 연결하고, `cầuNốiNgườiDùng.c`는 독립 EL0 프로그램에서 SVC로 커널을 호출한다. dữLiệuThựcTế Tệp 처리는 `CácTệpBộNhớ.java`, 루프백 điệnDữLiệu 처리는 `MạngVòngVề.java`, 연결형 흐름은 `MạngLuồng.java`에 있다.

```sh
make -C /home/user/jkoros/platforms/rpi4-native build
make -C /home/user/jkoros/platforms/rpi4-native test
```

산출물은 giáTrịNhân 내부용 `platforms/rpi4-native/build/libposix-kor-arm64.a`와 사용자용 `libposix-kor-user.a`toánHạngThứBa. 사용자용 라이브러리로 독립 ELF64 C/C++ 프로그램의 생성자·RAII·giáTrịĐiểmDấuPhẩyĐộng giáTrịThaoTác·Tệp·UDP 루프백 호출을 검증했다. 일반 Linux 바이너리, 전체 POSIX/libc/libstdc++ 지원을 뜻하지 않는다. 서로 다른 두 라이브러리를 혼합하지 않는다.

giáTrịHỗTrợ: `mởTệp`, `đọcDữLiệuTệp`, `ghiDữLiệuTệp`, `đóngTệp`, `dịchVịTệp`, `gỡTênMụcTệp`, `đặtGiáTrịĐộDàiTệp`, giáTrịPhụTrợ Hàm `cỡTệp`. lỗi 시 -1과 작업별 `sốLỗi`를 반환한다. `lưuTrữTệpChốt`은 RAM 파일이므로 ENOSYS를 반환한다. Tệp 16개, 각 16384바이트, tên 63바이트, mụcBộMôTả 16개이며 RAM 디렉터리·giáTrịĐốiTác/절대 경로를 제공한다. giáTrịQuyền/영속 저장은 없다.

사용자용 `TệpĐầuMục/ABIMạng.h`는 dữLiệuThựcTế tiếngViệt 함수와 독립 구조체를 선언한다.
`tạoĐiểmCuối`, `ràngBuộcĐịaChỉ`, `gửiDữLiệuĐiệnDữLiệu/nhận`, `kếtNốiMạng/đợi/nhận`는
`cầuNốiNgườiDùng.c`에서 SVC를 호출하며 giáTrịVĩLệnh 별칭이 아니다. `struct ĐịaChỉỔCắmMạngLiênMạng`의
`họĐịaChỉ`, `sốCổng`, `ĐịaChỉLiênMạng.giáTrịĐịaChỉ`을 사용한다. 상수는 enum의
`HọLiênMạng`, `ỔCắmMạngĐiệnDữLiệu`, `GiaoThứcĐiệnDữLiệu`, `MạngLuồng`, `giaoThứcVậnChuyểnLuồng`이다.
tiếngViệt·표준 구조체는 16바이트 ABI 배치를 공유하지만 서로 다른 C 자료형이다.
기존 pk_* 함수와 표준 구조체는 호환용으로 유지한다. giáTrịBênNgoài 통신은 tựThân 커널의
lwIP TCP/UDP와 QEMU UART SLIP 연결을 사용한다. dữLiệuThựcTế Pi 4 GENET 드라이버는 미지원이다.
소켓도 dữLiệuThựcTế Hàm `đóngTệp`로 닫는다.

[사용법·KiếnTrúc·giớiHạnRanhGiới](../../platforms/rpi4-native/README.md), [NgườiDùng ABI](../../platforms/rpi4-native/USER-ABI.md), [EL0 C++ Tệp VíDụ](../../platforms/rpi4-native/NgườiDùng/VíDụTệp.cpp), [UDP 루프백 VíDụ](../../platforms/rpi4-native/NgườiDùng/VíDụTruyềnThông.cpp), [기존 giáTrịNhân 내부 gọiThựcHiện KiểmThử](../../platforms/rpi4-native/KiểmThử/CácLờiGọiTệp.cpp)을 참고한다.

C11/C++11의 vănBảnHangul giáTrịĐịnhDanh·헤더 giáTrịDùng, SDK xâyDựngHệThống, ELF 업로드·thựcThiLệnh, lỗi/giáTrịPhầnCon đầuRaĐầuVào 처리는 [vănBảnHangul phátTriển 매뉴얼](../../platforms/rpi4-native/DEVELOPMENT-KO.md)에 정리했다. [C 연결형 TruyềnThông VíDụ](../../platforms/rpi4-native/VíDụ/LậpTrìnhHangul/giáTrịLuồng.c)도 제공한다.
