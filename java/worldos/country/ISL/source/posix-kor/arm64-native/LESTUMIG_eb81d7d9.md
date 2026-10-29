# eigin ARM64 Java 커널의 C/C++ Skrá·루프백 Tengjast

이 디렉터리는 `platforms/rpi4-native` eigin kjarni_VALUE 전용이다. 기존 i386 `int 0x80` 라이브러리나 ARM64 Linux libc용 라이브러리가 아니다.

`포함/파일규약.h`는 Íslenska 함수명과 `extern "C"` ABI를 제공한다. `Tengjast.c`는 kjarni_VALUE 안에서 AOT Java Skrá 메서드에 직접 연결하고, `notandi_brú.c`는 독립 EL0 프로그램에서 SVC로 커널을 호출한다. raun_gögn Skrá 처리는 `Minni_Skrár.java`, 루프백 전문 처리는 `되돌림망.java`, 연결형 흐름은 `Stream_Net.java`에 있다.

```sh
make -C /home/user/jkoros/platforms/rpi4-native build
make -C /home/user/jkoros/platforms/rpi4-native test
```

산출물은 kjarni_VALUE 내부용 `platforms/rpi4-native/build/libposix-kor-arm64.a`와 사용자용 `libposix-kor-user.a`다. 사용자용 라이브러리로 독립 ELF64 C/C++ 프로그램의 생성자·RAII·실수 aðgerð_VALUE·Skrá·UDP 루프백 호출을 검증했다. 일반 Linux 바이너리, 전체 POSIX/libc/libstdc++ 지원을 뜻하지 않는다. 서로 다른 두 라이브러리를 혼합하지 않는다.

Aðstoð_VALUE: `opið_skrá`, `파일자료읽기`, `skrifa_skrá_gögn`, `loka_skrá`, `leita_skrá`, `fjarlægja_skrá_færsla_heiti`, `sett_skrá_lengd`, 보조 fall_VALUE `skrá_breyta_stærð`. Villa 시 -1과 작업별 `villa_númer`를 반환한다. `파일저장확정`은 RAM 파일이므로 ENOSYS를 반환한다. Skrá 16개, 각 16384바이트, Heiti 63바이트, 서술자 16개이며 RAM 디렉터리·jafningi_VALUE/절대 경로를 제공한다. leyfi_VALUE/영속 저장은 없다.

사용자용 `포함/통신규약.h`는 raun_gögn Íslenska 함수와 독립 구조체를 선언한다.
`stofna_endastöð`, `BIND_slóð`, `자료전문보내기/받기`, `TENGJA_Net/기다리기/받기`는
`notandi_brú.c`에서 SVC를 호출하며 fjölvi_VALUE 별칭이 아니다. `struct 인터넷통신주소`의
`slóð_Fjölskylda`, `tengisnúmer`, `veffang.slóð_VALUE`을 사용한다. 상수는 enum의
`skýið_Fjölskylda`, `전문통신`, `전문전송규약`, `Stream_Net`, `Stream_flutningur_samskiptaregla`이다.
Íslenska·표준 구조체는 16바이트 ABI 배치를 공유하지만 서로 다른 C 자료형이다.
기존 pk_* 함수와 표준 구조체는 호환용으로 유지한다. 외부 통신은 eigin 커널의
lwIP TCP/UDP와 QEMU UART SLIP 연결을 사용한다. raun_gögn Pi 4 GENET 드라이버는 미지원이다.
소켓도 raun_gögn fall_VALUE `loka_skrá`로 닫는다.

[사용법·구조·한계](../../platforms/rpi4-native/README.md), [notandi ABI](../../platforms/rpi4-native/USER-ABI.md), [EL0 C++ Skrá 예제](../../platforms/rpi4-native/notandi/Skráardæmi.cpp), [UDP 루프백 예제](../../platforms/rpi4-native/notandi/통신예제.cpp), [기존 kjarni_VALUE 내부 호출 시험](../../platforms/rpi4-native/시험/skrá_Símtöl.cpp)을 참고한다.

C11/C++11의 한글 auðkenni_VALUE·헤더 사용, SDK smíð_kerfi, ELF 업로드·keyra_skipun, Villa/부분 I_Ú 처리는 [한글 개발 매뉴얼](../../platforms/rpi4-native/DEVELOPMENT-KO.md)에 정리했다. [C 연결형 통신 예제](../../platforms/rpi4-native/예제/한글코딩/Stream_VALUE.c)도 제공한다.
