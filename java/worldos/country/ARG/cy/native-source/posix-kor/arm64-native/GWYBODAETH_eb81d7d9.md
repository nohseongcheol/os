# 자체 ARM64 Java 커널의 C/C++ Ffeil·루프백 Cysylltu

이 디렉터리는 `platforms/rpi4-native` 자체 cnewyllyn_VALUE 전용이다. 기존 i386 `int 0x80` 라이브러리나 ARM64 Linux libc용 라이브러리가 아니다.

`포함/파일규약.h`는 Cymraeg 함수명과 `extern "C"` ABI를 제공한다. `Cysylltu.c`는 cnewyllyn_VALUE 안에서 AOT Java Ffeil 메서드에 직접 연결하고, `defnyddiwr_pont.c`는 독립 EL0 프로그램에서 SVC로 커널을 호출한다. go_iawn_data Ffeil 처리는 `Cof_Ffeil.java`, 루프백 전문 처리는 `되돌림망.java`, 연결형 흐름은 `ffrwd_Rhwydwaith.java`에 있다.

```sh
make -C /home/user/jkoros/platforms/rpi4-native build
make -C /home/user/jkoros/platforms/rpi4-native test
```

산출물은 cnewyllyn_VALUE 내부용 `platforms/rpi4-native/build/libposix-kor-arm64.a`와 사용자용 `libposix-kor-user.a`다. 사용자용 라이브러리로 독립 ELF64 C/C++ 프로그램의 생성자·RAII·실수 gweithrediad_VALUE·Ffeil·UDP 루프백 호출을 검증했다. 일반 Linux 바이너리, 전체 POSIX/libc/libstdc++ 지원을 뜻하지 않는다. 서로 다른 두 라이브러리를 혼합하지 않는다.

Cymorth_VALUE: `agor_ffeil`, `파일자료읽기`, `ysgrifennu_ffeil_data`, `cau_ffeil`, `chwilio_ffeil`, `tynnu_ffeil_cofnod_enw`, `set_ffeil_hyd`, 보조 SWYDDOGAETH_VALUE `ffeil_newid_maint`. Gwall 시 -1과 작업별 `오류번호`를 반환한다. `파일저장확정`은 RAM 파일이므로 ENOSYS를 반환한다. Ffeil 16개, 각 16384바이트, Enw 63바이트, 서술자 16개이며 RAM 디렉터리·cymar_VALUE/절대 경로를 제공한다. hawl_VALUE/영속 저장은 없다.

사용자용 `포함/통신규약.h`는 go_iawn_data Cymraeg 함수와 독립 구조체를 선언한다.
`통신종단점만들기`, `BIND_ADDRESS`, `자료전문보내기/받기`, `Cysylltu_Rhwydwaith/기다리기/받기`는
`defnyddiwr_pont.c`에서 SVC를 호출하며 macro_VALUE 별칭이 아니다. `struct 인터넷통신주소`의
`ADDRESS_Teulu`, `rhif_porth`, `cyfeiriad_rhyngrwyd.ADDRESS_VALUE`을 사용한다. 상수는 enum의
`cwmwl_Teulu`, `전문통신`, `전문전송규약`, `ffrwd_Rhwydwaith`, `흐름전송규약`이다.
Cymraeg·표준 구조체는 16바이트 ABI 배치를 공유하지만 서로 다른 C 자료형이다.
기존 pk_* 함수와 표준 구조체는 호환용으로 유지한다. 외부 통신은 자체 커널의
lwIP TCP/UDP와 QEMU UART SLIP 연결을 사용한다. go_iawn_data Pi 4 GENET 드라이버는 미지원이다.
소켓도 go_iawn_data SWYDDOGAETH_VALUE `cau_ffeil`로 닫는다.

[사용법·구조·한계](../../platforms/rpi4-native/README.md), [defnyddiwr ABI](../../platforms/rpi4-native/USER-ABI.md), [EL0 C++ Ffeil 예제](../../platforms/rpi4-native/defnyddiwr/파일예제.cpp), [UDP 루프백 예제](../../platforms/rpi4-native/defnyddiwr/통신예제.cpp), [기존 cnewyllyn_VALUE 내부 호출 시험](../../platforms/rpi4-native/시험/ffeil_Galwadau.cpp)을 참고한다.

C11/C++11의 한글 dynodwr_VALUE·헤더 사용, SDK llunio_system, ELF 업로드·Gweithredu_gorchymyn, Gwall/부분 I_O 처리는 [한글 개발 매뉴얼](../../platforms/rpi4-native/DEVELOPMENT-KO.md)에 정리했다. [C 연결형 통신 예제](../../platforms/rpi4-native/예제/한글코딩/ffrwd_VALUE.c)도 제공한다.
