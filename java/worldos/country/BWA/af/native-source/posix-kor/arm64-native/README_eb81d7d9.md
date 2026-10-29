# 자체 ARM64 Java 커널의 C/C++ Lêer·루프백 Koppel

이 디렉터리는 `platforms/rpi4-native` 자체 kern_VALUE 전용이다. 기존 i386 `int 0x80` 라이브러리나 ARM64 Linux libc용 라이브러리가 아니다.

`포함/파일규약.h`는 한국어 함수명과 `extern "C"` ABI를 제공한다. `Koppel.c`는 kern_VALUE 안에서 AOT Java Lêer 메서드에 직접 연결하고, `gebruiker_brug.c`는 독립 EL0 프로그램에서 SVC로 커널을 호출한다. werklik_data Lêer 처리는 `Geheue_Lêers.java`, 루프백 전문 처리는 `되돌림망.java`, 연결형 흐름은 `Stream_Netwerk.java`에 있다.

```sh
make -C /home/user/jkoros/platforms/rpi4-native build
make -C /home/user/jkoros/platforms/rpi4-native test
```

산출물은 kern_VALUE 내부용 `platforms/rpi4-native/build/libposix-kor-arm64.a`와 사용자용 `libposix-kor-user.a`다. 사용자용 라이브러리로 독립 ELF64 C/C++ 프로그램의 생성자·RAII·실수 werking_VALUE·Lêer·UDP 루프백 호출을 검증했다. 일반 Linux 바이너리, 전체 POSIX/libc/libstdc++ 지원을 뜻하지 않는다. 서로 다른 두 라이브러리를 혼합하지 않는다.

Bystand_VALUE: `skep_lêer`, `파일자료읽기`, `skryf_lêer_data`, `sluit_lêer`, `soek_lêer`, `verwyder_lêer_inskrywing_naam`, `stel_lêer_lengte`, 보조 funksie_VALUE `lêer_verstel`. Fout 시 -1과 작업별 `오류번호`를 반환한다. `파일저장확정`은 RAM 파일이므로 ENOSYS를 반환한다. Lêer 16개, 각 16384바이트, Naam 63바이트, 서술자 16개이며 RAM 디렉터리·portuur_VALUE/절대 경로를 제공한다. toestemming_VALUE/영속 저장은 없다.

사용자용 `포함/통신규약.h`는 werklik_data 한국어 함수와 독립 구조체를 선언한다.
`통신종단점만들기`, `BIND_adres`, `자료전문보내기/받기`, `KOPPEL_Netwerk/기다리기/받기`는
`gebruiker_brug.c`에서 SVC를 호출하며 makro_VALUE 별칭이 아니다. `struct 인터넷통신주소`의
`adres_Gesin`, `접속번호`, `internetadres.adres_VALUE`을 사용한다. 상수는 enum의
`wolk_Gesin`, `전문통신`, `전문전송규약`, `Stream_Netwerk`, `흐름전송규약`이다.
한국어·표준 구조체는 16바이트 ABI 배치를 공유하지만 서로 다른 C 자료형이다.
기존 pk_* 함수와 표준 구조체는 호환용으로 유지한다. 외부 통신은 자체 커널의
lwIP TCP/UDP와 QEMU UART SLIP 연결을 사용한다. werklik_data Pi 4 GENET 드라이버는 미지원이다.
소켓도 werklik_data funksie_VALUE `sluit_lêer`로 닫는다.

[사용법·구조·한계](../../platforms/rpi4-native/README.md), [gebruiker ABI](../../platforms/rpi4-native/USER-ABI.md), [EL0 C++ Lêer 예제](../../platforms/rpi4-native/gebruiker/파일예제.cpp), [UDP 루프백 예제](../../platforms/rpi4-native/gebruiker/통신예제.cpp), [기존 kern_VALUE 내부 호출 시험](../../platforms/rpi4-native/시험/lêer_Oproepe.cpp)을 참고한다.

C11/C++11의 한글 waarde_VALUE·헤더 사용, SDK bou_stelsel, ELF 업로드·uitvoer_bevel, Fout/부분 I_O 처리는 [한글 개발 매뉴얼](../../platforms/rpi4-native/DEVELOPMENT-KO.md)에 정리했다. [C 연결형 통신 예제](../../platforms/rpi4-native/예제/한글코딩/Stream_VALUE.c)도 제공한다.
