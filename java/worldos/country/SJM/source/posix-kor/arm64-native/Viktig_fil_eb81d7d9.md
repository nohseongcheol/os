# eget ARM64 Java 커널의 C/C++ Fil·루프백 Koble_til

이 디렉터리는 `platforms/rpi4-native` eget kjerne_VERDI 전용이다. 기존 i386 `int 0x80` 라이브러리나 ARM64 Linux libc용 라이브러리가 아니다.

`포함/파일규약.h`는 norsk 함수명과 `extern "C"` ABI를 제공한다. `Koble_til.c`는 kjerne_VERDI 안에서 AOT Java Fil 메서드에 직접 연결하고, `bruker_bro.c`는 독립 EL0 프로그램에서 SVC로 커널을 호출한다. faktisk_data Fil 처리는 `Minne_Filer.java`, 루프백 datagram 처리는 `tilbakekobling_nettverk.java`, 연결형 흐름은 `strøm_nettverk.java`에 있다.

```sh
make -C /home/user/jkoros/platforms/rpi4-native build
make -C /home/user/jkoros/platforms/rpi4-native test
```

산출물은 kjerne_VERDI 내부용 `platforms/rpi4-native/build/libposix-kor-arm64.a`와 사용자용 `libposix-kor-user.a`다. 사용자용 라이브러리로 독립 ELF64 C/C++ 프로그램의 생성자·RAII·flyttall_VERDI operasjon_VERDI·Fil·UDP 루프백 호출을 검증했다. 일반 Linux 바이너리, 전체 POSIX/libc/libstdc++ 지원을 뜻하지 않는다. 서로 다른 두 라이브러리를 혼합하지 않는다.

støtte_VERDI: `åpen_Fil`, `파일자료읽기`, `skrive_Fil_data`, `Lukk_Fil`, `søk_Fil`, `fjerne_Fil_oppføring_navn`, `sett_Fil_lengde`, 보조 FUNKSJON_VERDI `filstørrelse`. feil 시 -1과 작업별 `feilnummer`를 반환한다. `파일저장확정`은 RAM 파일이므로 ENOSYS를 반환한다. Fil 16개, 각 16384바이트, Navn 63바이트, 서술자 16개이며 RAM 디렉터리·node_VERDI_6a3b6fa7/절대 경로를 제공한다. tillatelse_VERDI/영속 저장은 없다.

사용자용 `포함/통신규약.h`는 faktisk_data norsk 함수와 독립 구조체를 선언한다.
`åpne_deltaker`, `BIND_e_post`, `sende_datagram_data/motta`, `KOBLE_TIL_nettverk/기다리기/motta`는
`bruker_bro.c`에서 SVC를 호출하며 makro_VERDI 별칭이 아니다. `struct sky_socket_e_post`의
`e_post_serie`, `portnummer`, `Internett_adresse.e_post_VERDI`을 사용한다. 상수는 enum의
`sky_serie`, `datagramsocket`, `datagram_protokoll`, `strøm_nettverk`, `strøm_transportprotokoll`이다.
norsk·표준 구조체는 16바이트 ABI 배치를 공유하지만 서로 다른 C 자료형이다.
기존 pk_* 함수와 표준 구조체는 호환용으로 유지한다. ekstern_VERDI 통신은 eget 커널의
lwIP TCP/UDP와 QEMU UART SLIP 연결을 사용한다. faktisk_data Pi 4 GENET 드라이버는 미지원이다.
소켓도 faktisk_data FUNKSJON_VERDI `Lukk_Fil`로 닫는다.

[사용법·구조·한계](../../platforms/rpi4-native/README.md), [bruker ABI](../../platforms/rpi4-native/USER-ABI.md), [EL0 C++ Fil 예제](../../platforms/rpi4-native/bruker/Fileksempel.cpp), [UDP 루프백 예제](../../platforms/rpi4-native/bruker/통신예제.cpp), [기존 kjerne_VERDI 내부 호출 시험](../../platforms/rpi4-native/시험/Fil_Anrop.cpp)을 참고한다.

C11/C++11의 한글 identifikator_VERDI·헤더 bruk_VERDI, SDK bygg_System, ELF 업로드·Utfør_kommando, feil/부분 I_U 처리는 [한글 utviklet_materiale 매뉴얼](../../platforms/rpi4-native/DEVELOPMENT-KO.md)에 정리했다. [C 연결형 통신 예제](../../platforms/rpi4-native/예제/한글코딩/strøm_VERDI.c)도 제공한다.
