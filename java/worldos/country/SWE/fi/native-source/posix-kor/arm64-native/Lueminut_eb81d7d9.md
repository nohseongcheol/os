# oma ARM64 Java 커널의 C/C++ tiedoston_nimi·루프백 Yhdistä

이 디렉터리는 `platforms/rpi4-native` oma ydin_ARVO 전용이다. 기존 i386 `int 0x80` 라이브러리나 ARM64 Linux libc용 라이브러리가 아니다.

`esittelyt/파일규약.h`는 suomi 함수명과 `extern "C"` ABI를 제공한다. `Yhdistä.c`는 ydin_ARVO 안에서 AOT Java tiedoston_nimi 메서드에 직접 연결하고, `käyttäjä_silta.c`는 독립 EL0 프로그램에서 SVC로 커널을 호출한다. todellinen_data tiedoston_nimi 처리는 `Muisti_Files.java`, 루프백 datagrammi 처리는 `silmukka_verkko.java`, 연결형 흐름은 `virta_verkko.java`에 있다.

```sh
make -C /home/user/jkoros/platforms/rpi4-native build
make -C /home/user/jkoros/platforms/rpi4-native test
```

산출물은 ydin_ARVO 내부용 `platforms/rpi4-native/build/libposix-kor-arm64.a`와 사용자용 `libposix-kor-user.a`다. 사용자용 라이브러리로 독립 ELF64 C/C++ 프로그램의 생성자·RAII·liukuluku_ARVO leikkaus_ARVO·tiedoston_nimi·UDP 루프백 호출을 검증했다. 일반 Linux 바이너리, 전체 POSIX/libc/libstdc++ 지원을 뜻하지 않는다. 서로 다른 두 라이브러리를 혼합하지 않는다.

Tuki_ARVO: `avata_Tiedosto`, `lukea_Tiedosto_data`, `kirjoitus_Tiedosto_data`, `Sulje_Tiedosto`, `hae_Tiedosto`, `poistaa_Tiedosto_merkintä_nimi`, `ryhmä_Tiedosto_kesto`, 보조 funktio_ARVO `tiedostokoko`. VIRHE 시 -1과 작업별 `virhenumero`를 반환한다. `vahvistaa_muutokset_Files`은 RAM 파일이므로 ENOSYS를 반환한다. tiedoston_nimi 16개, 각 16384바이트, Nimi 63바이트, 서술자 16개이며 RAM 디렉터리·vertaissolmu_ARVO/절대 경로를 제공한다. lupa_ARVO/영속 저장은 없다.

사용자용 `esittelyt/통신규약.h`는 todellinen_data suomi 함수와 독립 구조체를 선언한다.
`Luo_päätepiste`, `BIND_OSOITE`, `lähettää_datagrammi_data/saada`, `YHDISTÄ_verkko/기다리기/saada`는
`käyttäjä_silta.c`에서 SVC를 호출하며 makro_ARVO 별칭이 아니다. `struct pilvi_vastake_OSOITE`의
`OSOITE_Perhe`, `portin_numero`, `Internet_osoite.OSOITE_ARVO`을 사용한다. 상수는 enum의
`pilvi_Perhe`, `datagrammivastake`, `datagrammi_protokolla`, `virta_verkko`, `virta_kuljetusprotokolla`이다.
suomi·표준 구조체는 16바이트 ABI 배치를 공유하지만 서로 다른 C 자료형이다.
기존 pk_* 함수와 표준 구조체는 호환용으로 유지한다. ulkoinen_ARVO 통신은 oma 커널의
lwIP TCP/UDP와 QEMU UART SLIP 연결을 사용한다. todellinen_data Pi 4 GENET 드라이버는 미지원이다.
소켓도 todellinen_data funktio_ARVO `Sulje_Tiedosto`로 닫는다.

[사용법·구조·한계](../../platforms/rpi4-native/README.md), [käyttäjätila ABI](../../platforms/rpi4-native/USER-ABI.md), [EL0 C++ tiedoston_nimi 예제](../../platforms/rpi4-native/käyttäjätila/Tiedostoesimerkki.cpp), [UDP 루프백 예제](../../platforms/rpi4-native/käyttäjätila/통신예제.cpp), [기존 ydin_ARVO 내부 호출 testit](../../platforms/rpi4-native/testit/Tiedosto_Puhelut.cpp)을 참고한다.

C11/C++11의 한글 tunniste_ARVO·헤더 käyttö_ARVO, SDK kääntää_Järjestelmä, ELF 업로드·Suorita_komento, VIRHE/부분 I_O 처리는 [한글 kehitystuote 매뉴얼](../../platforms/rpi4-native/DEVELOPMENT-KO.md)에 정리했다. [C 연결형 통신 예제](../../platforms/rpi4-native/예제/한글코딩/virta_ARVO.c)도 제공한다.
