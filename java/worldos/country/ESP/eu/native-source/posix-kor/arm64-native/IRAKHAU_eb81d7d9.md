# 자체 ARM64 Java 커널의 C/C++ Fitxategia·루프백 Konektatu

이 디렉터리는 `platforms/rpi4-native` 자체 nukleo_balio 전용이다. 기존 i386 `int 0x80` 라이브러리나 ARM64 Linux libc용 라이브러리가 아니다.

`포함/파일규약.h`는 Euskara 함수명과 `extern "C"` ABI를 제공한다. `Konektatu.c`는 nukleo_balio 안에서 AOT Java Fitxategia 메서드에 직접 연결하고, `erabiltzaile_zubi.c`는 독립 EL0 프로그램에서 SVC로 커널을 호출한다. benetako_datuak Fitxategia 처리는 `Memoria_Fitxategiak.java`, 루프백 전문 처리는 `되돌림망.java`, 연결형 흐름은 `Stream_sare.java`에 있다.

```sh
make -C /home/user/jkoros/platforms/rpi4-native build
make -C /home/user/jkoros/platforms/rpi4-native test
```

산출물은 nukleo_balio 내부용 `platforms/rpi4-native/build/libposix-kor-arm64.a`와 사용자용 `libposix-kor-user.a`다. 사용자용 라이브러리로 독립 ELF64 C/C++ 프로그램의 생성자·RAII·mugikor_p_balio kirurgia_balio·Fitxategia·UDP 루프백 호출을 검증했다. 일반 Linux 바이너리, 전체 POSIX/libc/libstdc++ 지원을 뜻하지 않는다. 서로 다른 두 라이브러리를 혼합하지 않는다.

Laguntza_balio: `ireki_fitxategi`, `파일자료읽기`, `idatzi_fitxategi_datuak`, `itxi_fitxategi`, `bilatu_fitxategi`, `kendu_fitxategi_sarrera_izen`, `sorta_fitxategi_luzera`, 보조 FUNTZIOA_balio `파일크기`. errorea 시 -1과 작업별 `errorearen_zenbaki`를 반환한다. `파일저장확정`은 RAM 파일이므로 ENOSYS를 반환한다. Fitxategia 16개, 각 16384바이트, Izena 63바이트, 서술자 16개이며 RAM 디렉터리·pareko_balio/절대 경로를 제공한다. baimen_balio/영속 저장은 없다.

사용자용 `포함/통신규약.h`는 benetako_datuak Euskara 함수와 독립 구조체를 선언한다.
`sortu_amaiera_puntu`, `lotu_helbide`, `자료전문보내기/받기`, `KONEKTATU_sare/기다리기/받기`는
`erabiltzaile_zubi.c`에서 SVC를 호출하며 makro_balio 별칭이 아니다. `struct 인터넷통신주소`의
`helbide_sorta`, `ataka_zenbaki`, `Internet_helbide.helbide_balio`을 사용한다. 상수는 enum의
`hodei_sorta`, `전문통신`, `전문전송규약`, `Stream_sare`, `Stream_garraio_protokolo`이다.
Euskara·표준 구조체는 16바이트 ABI 배치를 공유하지만 서로 다른 C 자료형이다.
기존 pk_* 함수와 표준 구조체는 호환용으로 유지한다. 외부 통신은 자체 커널의
lwIP TCP/UDP와 QEMU UART SLIP 연결을 사용한다. benetako_datuak Pi 4 GENET 드라이버는 미지원이다.
소켓도 benetako_datuak FUNTZIOA_balio `itxi_fitxategi`로 닫는다.

[사용법·구조·한계](../../platforms/rpi4-native/README.md), [erabiltzaile ABI](../../platforms/rpi4-native/USER-ABI.md), [EL0 C++ Fitxategia 예제](../../platforms/rpi4-native/erabiltzaile/파일예제.cpp), [UDP 루프백 예제](../../platforms/rpi4-native/erabiltzaile/통신예제.cpp), [기존 nukleo_balio 내부 호출 시험](../../platforms/rpi4-native/시험/fitxategi_Deiak.cpp)을 참고한다.

C11/C++11의 한글 identifikatzaile_balio·헤더 사용, SDK eraiki_sistema, ELF 업로드·exekutatu_komando, errorea/부분 S_I 처리는 [한글 개발 매뉴얼](../../platforms/rpi4-native/DEVELOPMENT-KO.md)에 정리했다. [C 연결형 통신 예제](../../platforms/rpi4-native/예제/한글코딩/Stream_balio.c)도 제공한다.
