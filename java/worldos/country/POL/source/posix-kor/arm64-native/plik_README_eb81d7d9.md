# własny ARM64 Java 커널의 C/C++ nazwa_pliku·루프백 Połącz

이 디렉터리는 `platforms/rpi4-native` własny jądro_WARTOŚĆ 전용이다. 기존 i386 `int 0x80` 라이브러리나 ARM64 Linux libc용 라이브러리가 아니다.

`deklaracje/Plik_ABI.h`는 polski 함수명과 `extern "C"` ABI를 제공한다. `Połącz.c`는 jądro_WARTOŚĆ 안에서 AOT Java nazwa_pliku 메서드에 직접 연결하고, `użytkownik_mostek.c`는 독립 EL0 프로그램에서 SVC로 커널을 호출한다. rzeczywisty_dane nazwa_pliku 처리는 `Pamięć_Files.java`, 루프백 datagram 처리는 `sprzężenie_zwrotne_sieć.java`, 연결형 흐름은 `Stream_sieć.java`에 있다.

```sh
make -C /home/user/jkoros/platforms/rpi4-native build
make -C /home/user/jkoros/platforms/rpi4-native test
```

산출물은 jądro_WARTOŚĆ 내부용 `platforms/rpi4-native/build/libposix-kor-arm64.a`와 사용자용 `libposix-kor-user.a`다. 사용자용 라이브러리로 독립 ELF64 C/C++ 프로그램의 생성자·RAII·liczba_zmiennoprzecinkowa_WARTOŚĆ zabieg_WARTOŚĆ·nazwa_pliku·UDP 루프백 호출을 검증했다. 일반 Linux 바이너리, 전체 POSIX/libc/libstdc++ 지원을 뜻하지 않는다. 서로 다른 두 라이브러리를 혼합하지 않는다.

wsparcie_WARTOŚĆ: `otwarty_Plik`, `파일자료읽기`, `zapis_Plik_dane`, `Zamknij_Plik`, `szukać_Plik`, `usuń_Plik_wpis_nazwa`, `set_Plik_długość`, 보조 FUNKCJA_WARTOŚĆ `rozmiar_pliku`. błąd 시 -1과 작업별 `numer_błędu`를 반환한다. `przekazywać_Files`은 RAM 파일이므로 ENOSYS를 반환한다. nazwa_pliku 16개, 각 16384바이트, Nazwa 63바이트, deskryptor_wpis 16개이며 RAM 디렉터리·węzeł_równorzędny_WARTOŚĆ/절대 경로를 제공한다. pozwolenie_WARTOŚĆ/영속 저장은 없다.

사용자용 `deklaracje/sieć_ABI.h`는 rzeczywisty_dane polski 함수와 독립 구조체를 선언한다.
`Twórca_uczestnik`, `BIND_ADRES`, `wysłać_datagram_dane/odbierać`, `POŁĄCZ_sieć/기다리기/odbierać`는
`użytkownik_mostek.c`에서 SVC를 호출하며 makro_WARTOŚĆ 별칭이 아니다. `struct chmura_gniazdo_ADRES`의
`ADRES_Rodzina`, `numer_portu`, `adres_internetowy.ADRES_WARTOŚĆ`을 사용한다. 상수는 enum의
`chmura_Rodzina`, `gniazdo_do_przesyłania_datagramów`, `datagram_protokół`, `Stream_sieć`, `Stream_protokół_transportu`이다.
polski·표준 구조체는 16바이트 ABI 배치를 공유하지만 서로 다른 C 자료형이다.
기존 pk_* 함수와 표준 구조체는 호환용으로 유지한다. zewnętrzny_WARTOŚĆ 통신은 własny 커널의
lwIP TCP/UDP와 QEMU UART SLIP 연결을 사용한다. rzeczywisty_dane Pi 4 GENET 드라이버는 미지원이다.
소켓도 rzeczywisty_dane FUNKCJA_WARTOŚĆ `Zamknij_Plik`로 닫는다.

[사용법·architektura·한계](../../platforms/rpi4-native/README.md), [przestrzeń_użytkownika ABI](../../platforms/rpi4-native/USER-ABI.md), [EL0 C++ nazwa_pliku 예제](../../platforms/rpi4-native/przestrzeń_użytkownika/PrzykładPliku.cpp), [UDP 루프백 예제](../../platforms/rpi4-native/przestrzeń_użytkownika/통신예제.cpp), [기존 jądro_WARTOŚĆ 내부 호출 testy](../../platforms/rpi4-native/testy/Plik_Połączenia.cpp)을 참고한다.

C11/C++11의 한글 identyfikator_WARTOŚĆ·헤더 używać_WARTOŚĆ, SDK BLD_System, ELF 업로드·Wykonaj_polecenie, błąd/부분 We_Wy 처리는 [한글 materiał_pochodny 매뉴얼](../../platforms/rpi4-native/DEVELOPMENT-KO.md)에 정리했다. [C 연결형 komunikacja 예제](../../platforms/rpi4-native/예제/한글코딩/Stream_WARTOŚĆ.c)도 제공한다.
