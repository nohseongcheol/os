# 자체 ARM64 Java 커널의 C/C++ Comhad·루프백 Nasc

이 디렉터리는 `platforms/rpi4-native` 자체 eithne_VALUE 전용이다. 기존 i386 `int 0x80` 라이브러리나 ARM64 Linux libc용 라이브러리가 아니다.

`포함/파일규약.h`는 Gaeilge 함수명과 `extern "C"` ABI를 제공한다. `Nasc.c`는 eithne_VALUE 안에서 AOT Java Comhad 메서드에 직접 연결하고, `úsáideoir_traschóiritheoir.c`는 독립 EL0 프로그램에서 SVC로 커널을 호출한다. iarbhír_sonraí Comhad 처리는 `Cuimhne_Comhaid.java`, 루프백 전문 처리는 `되돌림망.java`, 연결형 흐름은 `sruth_Líonra.java`에 있다.

```sh
make -C /home/user/jkoros/platforms/rpi4-native build
make -C /home/user/jkoros/platforms/rpi4-native test
```

산출물은 eithne_VALUE 내부용 `platforms/rpi4-native/build/libposix-kor-arm64.a`와 사용자용 `libposix-kor-user.a`다. 사용자용 라이브러리로 독립 ELF64 C/C++ 프로그램의 생성자·RAII·실수 oibríocht_VALUE·Comhad·UDP 루프백 호출을 검증했다. 일반 Linux 바이너리, 전체 POSIX/libc/libstdc++ 지원을 뜻하지 않는다. 서로 다른 두 라이브러리를 혼합하지 않는다.

Tacaíocht_VALUE: `oscail_comhad`, `파일자료읽기`, `scríobh_comhad_sonraí`, `dún_comhad`, `lorg_comhad`, `bain_comhad_iontráil_ainm`, `tacar_comhad_fad`, 보조 feidhm_VALUE `comhad_socraigh_méid`. ERREÁID 시 -1과 작업별 `오류번호`를 반환한다. `파일저장확정`은 RAM 파일이므로 ENOSYS를 반환한다. Comhad 16개, 각 16384바이트, Ainm 63바이트, 서술자 16개이며 RAM 디렉터리·piara_VALUE/절대 경로를 제공한다. cead_VALUE/영속 저장은 없다.

사용자용 `포함/통신규약.h`는 iarbhír_sonraí Gaeilge 함수와 독립 구조체를 선언한다.
`통신종단점만들기`, `BIND_ADDRESS`, `자료전문보내기/받기`, `nasc_Líonra/기다리기/받기`는
`úsáideoir_traschóiritheoir.c`에서 SVC를 호출하며 macra_VALUE 별칭이 아니다. `struct 인터넷통신주소`의
`ADDRESS_Teaghlach`, `uimhir_phoirt`, `seoladh_Idirlín.ADDRESS_VALUE`을 사용한다. 상수는 enum의
`néal_Teaghlach`, `전문통신`, `전문전송규약`, `sruth_Líonra`, `흐름전송규약`이다.
Gaeilge·표준 구조체는 16바이트 ABI 배치를 공유하지만 서로 다른 C 자료형이다.
기존 pk_* 함수와 표준 구조체는 호환용으로 유지한다. 외부 통신은 자체 커널의
lwIP TCP/UDP와 QEMU UART SLIP 연결을 사용한다. iarbhír_sonraí Pi 4 GENET 드라이버는 미지원이다.
소켓도 iarbhír_sonraí feidhm_VALUE `dún_comhad`로 닫는다.

[사용법·구조·한계](../../platforms/rpi4-native/README.md), [úsáideoir ABI](../../platforms/rpi4-native/USER-ABI.md), [EL0 C++ Comhad 예제](../../platforms/rpi4-native/úsáideoir/파일예제.cpp), [UDP 루프백 예제](../../platforms/rpi4-native/úsáideoir/통신예제.cpp), [기존 eithne_VALUE 내부 호출 시험](../../platforms/rpi4-native/시험/comhad_Glaonna.cpp)을 참고한다.

C11/C++11의 한글 aitheantóir_VALUE·헤더 사용, SDK tóg_córas, ELF 업로드·Rith_ordú, ERREÁID/부분 I_O 처리는 [한글 개발 매뉴얼](../../platforms/rpi4-native/DEVELOPMENT-KO.md)에 정리했다. [C 연결형 통신 예제](../../platforms/rpi4-native/예제/한글코딩/sruth_VALUE.c)도 제공한다.
