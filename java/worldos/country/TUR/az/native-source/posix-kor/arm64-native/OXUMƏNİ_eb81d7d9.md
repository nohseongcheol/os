# 자체 ARM64 Java 커널의 C/C++ FAYL·루프백 Bağlan

이 디렉터리는 `platforms/rpi4-native` 자체 nüvə_VALUE 전용이다. 기존 i386 `int 0x80` 라이브러리나 ARM64 Linux libc용 라이브러리가 아니다.

`포함/파일규약.h`는 한국어 함수명과 `extern "C"` ABI를 제공한다. `Bağlan.c`는 nüvə_VALUE 안에서 AOT Java FAYL 메서드에 직접 연결하고, `istifadəçi_körpü.c`는 독립 EL0 프로그램에서 SVC로 커널을 호출한다. faktiki_verilənlər FAYL 처리는 `Yaddaş_Fayllar.java`, 루프백 전문 처리는 `되돌림망.java`, 연결형 흐름은 `axın_Şəbəkə.java`에 있다.

```sh
make -C /home/user/jkoros/platforms/rpi4-native build
make -C /home/user/jkoros/platforms/rpi4-native test
```

산출물은 nüvə_VALUE 내부용 `platforms/rpi4-native/build/libposix-kor-arm64.a`와 사용자용 `libposix-kor-user.a`다. 사용자용 라이브러리로 독립 ELF64 C/C++ 프로그램의 생성자·RAII·실수 əməliyyat_VALUE·FAYL·UDP 루프백 호출을 검증했다. 일반 Linux 바이너리, 전체 POSIX/libc/libstdc++ 지원을 뜻하지 않는다. 서로 다른 두 라이브러리를 혼합하지 않는다.

Dəstək_VALUE: `açmaq_fayl`, `파일자료읽기`, `yazmaq_fayl_verilənlər`, `bağlamaq_fayl`, `axtarmaq_fayl`, `silmək_fayl_daxiletmə_ad`, `Dəst_fayl_uzunluq`, 보조 FUNCTION_VALUE `fayl_ölçünü_dəyişmək`. XƏTA 시 -1과 작업별 `오류번호`를 반환한다. `파일저장확정`은 RAM 파일이므로 ENOSYS를 반환한다. FAYL 16개, 각 16384바이트, Ad 63바이트, 서술자 16개이며 RAM 디렉터리·eynisəviyyəli_VALUE/절대 경로를 제공한다. icazə_VALUE/영속 저장은 없다.

사용자용 `포함/통신규약.h`는 faktiki_verilənlər 한국어 함수와 독립 구조체를 선언한다.
`통신종단점만들기`, `BIND_ünvan`, `자료전문보내기/받기`, `QOŞUN_Şəbəkə/기다리기/받기`는
`istifadəçi_körpü.c`에서 SVC를 호출하며 makros_VALUE 별칭이 아니다. `struct 인터넷통신주소`의
`ünvan_Ailə`, `접속번호`, `İnternet_ünvanı.ünvan_VALUE`을 사용한다. 상수는 enum의
`bulud_Ailə`, `전문통신`, `전문전송규약`, `axın_Şəbəkə`, `흐름전송규약`이다.
한국어·표준 구조체는 16바이트 ABI 배치를 공유하지만 서로 다른 C 자료형이다.
기존 pk_* 함수와 표준 구조체는 호환용으로 유지한다. 외부 통신은 자체 커널의
lwIP TCP/UDP와 QEMU UART SLIP 연결을 사용한다. faktiki_verilənlər Pi 4 GENET 드라이버는 미지원이다.
소켓도 faktiki_verilənlər FUNCTION_VALUE `bağlamaq_fayl`로 닫는다.

[사용법·구조·한계](../../platforms/rpi4-native/README.md), [istifadəçi ABI](../../platforms/rpi4-native/USER-ABI.md), [EL0 C++ FAYL 예제](../../platforms/rpi4-native/istifadəçi/파일예제.cpp), [UDP 루프백 예제](../../platforms/rpi4-native/istifadəçi/통신예제.cpp), [기존 nüvə_VALUE 내부 호출 시험](../../platforms/rpi4-native/시험/fayl_Zənglər.cpp)을 참고한다.

C11/C++11의 한글 identifikator_VALUE·헤더 사용, SDK qurmaq_sistem, ELF 업로드·icra_etmək_əmr, XƏTA/부분 giriş_çıxış 처리는 [한글 개발 매뉴얼](../../platforms/rpi4-native/DEVELOPMENT-KO.md)에 정리했다. [C 연결형 통신 예제](../../platforms/rpi4-native/예제/한글코딩/axın_VALUE.c)도 제공한다.
