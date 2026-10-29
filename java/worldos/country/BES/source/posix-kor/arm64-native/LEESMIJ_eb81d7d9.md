# Eigen ARM64 Java 커널의 C/C++ bestand·루프백 Verbinden

이 디렉터리는 `platforms/rpi4-native` Eigen kernel_WAARDE 전용이다. 기존 i386 `int 0x80` 라이브러리나 ARM64 Linux libc용 라이브러리가 아니다.

`declaraties/파일규약.h`는 Nederlands 함수명과 `extern "C"` ABI를 제공한다. `Verbinden.c`는 kernel_WAARDE 안에서 AOT Java bestand 메서드에 직접 연결하고, `gebruiker_brug.c`는 독립 EL0 프로그램에서 SVC로 커널을 호출한다. werkelijk_gegevens bestand 처리는 `GeheugenBestanden.java`, 루프백 datagram 처리는 `loopback_net.java`, 연결형 흐름은 `Stream_net.java`에 있다.

```sh
make -C /home/user/jkoros/platforms/rpi4-native build
make -C /home/user/jkoros/platforms/rpi4-native test
```

산출물은 kernel_WAARDE 내부용 `platforms/rpi4-native/build/libposix-kor-arm64.a`와 사용자용 `libposix-kor-user.a`다. 사용자용 라이브러리로 독립 ELF64 C/C++ 프로그램의 생성자·RAII·drijvende_komma_WAARDE operatie_WAARDE·bestand·UDP 루프백 호출을 검증했다. 일반 Linux 바이너리, 전체 POSIX/libc/libstdc++ 지원을 뜻하지 않는다. 서로 다른 두 라이브러리를 혼합하지 않는다.

steun_WAARDE: `open_Bestand`, `파일자료읽기`, `schrijven_Bestand_gegevens`, `Sluiten_Bestand`, `zoeken_Bestand`, `verwijderen_Bestand_invoer_naam`, `set_Bestand_tijdsduur`, 보조 FUNCTIE_WAARDE `bestandsgrootte`. fout 시 -1과 작업별 `foutnummer`를 반환한다. `doorvoeren_Files`은 RAM 파일이므로 ENOSYS를 반환한다. bestand 16개, 각 16384바이트, Naam 63바이트, 서술자 16개이며 RAM 디렉터리·peer_WAARDE/절대 경로를 제공한다. machtiging_WAARDE/영속 저장은 없다.

사용자용 `declaraties/통신규약.h`는 werkelijk_gegevens Nederlands 함수와 독립 구조체를 선언한다.
`maken_eindpunt`, `BIND_ADRES`, `e_mailen_datagram_gegevens/ontvangen`, `VERBINDEN_net/기다리기/ontvangen`는
`gebruiker_brug.c`에서 SVC를 호출하며 macro_WAARDE 별칭이 아니다. `struct mesh_socket_ADRES`의
`ADRES_Gezin`, `poortnummer`, `internetadres.ADRES_WAARDE`을 사용한다. 상수는 enum의
`mesh_Gezin`, `datagramsocket`, `datagram_protocol`, `Stream_net`, `Stream_transportprotocol`이다.
Nederlands·표준 구조체는 16바이트 ABI 배치를 공유하지만 서로 다른 C 자료형이다.
기존 pk_* 함수와 표준 구조체는 호환용으로 유지한다. extern_WAARDE 통신은 Eigen 커널의
lwIP TCP/UDP와 QEMU UART SLIP 연결을 사용한다. werkelijk_gegevens Pi 4 GENET 드라이버는 미지원이다.
소켓도 werkelijk_gegevens FUNCTIE_WAARDE `Sluiten_Bestand`로 닫는다.

[사용법·architectuur·한계](../../platforms/rpi4-native/README.md), [gebruikersruimte ABI](../../platforms/rpi4-native/USER-ABI.md), [EL0 C++ bestand 예제](../../platforms/rpi4-native/gebruikersruimte/Bestandsvoorbeeld.cpp), [UDP 루프백 예제](../../platforms/rpi4-native/gebruikersruimte/통신예제.cpp), [기존 kernel_WAARDE 내부 호출 tests](../../platforms/rpi4-native/tests/Bestand_Oproepen.cpp)을 참고한다.

C11/C++11의 한글 id_WAARDE·헤더 gebruik_WAARDE, SDK bouwen, ELF 업로드·Uitvoeren_opdracht, fout/부분 I_O 처리는 [한글 ontwikkeling 매뉴얼](../../platforms/rpi4-native/DEVELOPMENT-KO.md)에 정리했다. [C 연결형 communicatie 예제](../../platforms/rpi4-native/예제/한글코딩/Stream_WAARDE.c)도 제공한다.
