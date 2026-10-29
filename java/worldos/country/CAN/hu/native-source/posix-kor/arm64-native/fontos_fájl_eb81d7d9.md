# saját ARM64 Java 커널의 C/C++ Fájl·루프백 Kapcsolódás

이 디렉터리는 `platforms/rpi4-native` saját kernel_ÉRTÉK 전용이다. 기존 i386 `int 0x80` 라이브러리나 ARM64 Linux libc용 라이브러리가 아니다.

`포함/파일규약.h`는 magyar 함수명과 `extern "C"` ABI를 제공한다. `Kapcsolódás.c`는 kernel_ÉRTÉK 안에서 AOT Java Fájl 메서드에 직접 연결하고, `felhasználó_híd.c`는 독립 EL0 프로그램에서 SVC로 커널을 호출한다. tényleges_adat Fájl 처리는 `Memória_Files.java`, 루프백 datagram 처리는 `visszacsatolt_hálózat.java`, 연결형 흐름은 `Stream_hálózat.java`에 있다.

```sh
make -C /home/user/jkoros/platforms/rpi4-native build
make -C /home/user/jkoros/platforms/rpi4-native test
```

산출물은 kernel_ÉRTÉK 내부용 `platforms/rpi4-native/build/libposix-kor-arm64.a`와 사용자용 `libposix-kor-user.a`다. 사용자용 라이브러리로 독립 ELF64 C/C++ 프로그램의 생성자·RAII·lebegőpontos_szám_ÉRTÉK műtét_ÉRTÉK·Fájl·UDP 루프백 호출을 검증했다. 일반 Linux 바이너리, 전체 POSIX/libc/libstdc++ 지원을 뜻하지 않는다. 서로 다른 두 라이브러리를 혼합하지 않는다.

támogat_ÉRTÉK: `készít_Fájl`, `파일자료읽기`, `ír_Fájl_adat`, `bezár_Fájl`, `keres_Fájl`, `eltávolít_Fájl_bejegyzés_név`, `halmaz_Fájl_hossz`, 보조 FÜGGVÉNY_ÉRTÉK `fájlméret`. HIBA 시 -1과 작업별 `hibaszám`를 반환한다. `véglegesít_Files`은 RAM 파일이므로 ENOSYS를 반환한다. Fájl 16개, 각 16384바이트, Név 63바이트, 서술자 16개이며 RAM 디렉터리·társ_ÉRTÉK/절대 경로를 제공한다. engedély_ÉRTÉK/영속 저장은 없다.

사용자용 `포함/통신규약.h`는 tényleges_adat magyar 함수와 독립 구조체를 선언한다.
`készít_végpont`, `BIND_CÍM`, `küld_datagram_adat/fogad`, `KAPCSOLAT_hálózat/기다리기/fogad`는
`felhasználó_híd.c`에서 SVC를 호출하며 makró_ÉRTÉK 별칭이 아니다. `struct háló_szoftvercsatorna_CÍM`의
`CÍM_Család`, `portszám`, `internetcím.CÍM_ÉRTÉK`을 사용한다. 상수는 enum의
`háló_Család`, `datagram_szoftvercsatorna`, `datagram_protokoll`, `Stream_hálózat`, `Stream_átviteli_protokoll`이다.
magyar·표준 구조체는 16바이트 ABI 배치를 공유하지만 서로 다른 C 자료형이다.
기존 pk_* 함수와 표준 구조체는 호환용으로 유지한다. külső_ÉRTÉK 통신은 saját 커널의
lwIP TCP/UDP와 QEMU UART SLIP 연결을 사용한다. tényleges_adat Pi 4 GENET 드라이버는 미지원이다.
소켓도 tényleges_adat FÜGGVÉNY_ÉRTÉK `bezár_Fájl`로 닫는다.

[사용법·architektúra·한계](../../platforms/rpi4-native/README.md), [felhasználó ABI](../../platforms/rpi4-native/USER-ABI.md), [EL0 C++ Fájl 예제](../../platforms/rpi4-native/felhasználó/FájlPélda.cpp), [UDP 루프백 예제](../../platforms/rpi4-native/felhasználó/통신예제.cpp), [기존 kernel_ÉRTÉK 내부 호출 시험](../../platforms/rpi4-native/시험/Fájl_Hívások.cpp)을 참고한다.

C11/C++11의 한글 azonosító_ÉRTÉK·헤더 használ_ÉRTÉK, SDK épít_Rendszer, ELF 업로드·végrehajt_parancs, HIBA/부분 I_O 처리는 [한글 개발 매뉴얼](../../platforms/rpi4-native/DEVELOPMENT-KO.md)에 정리했다. [C 연결형 kommunikáció 예제](../../platforms/rpi4-native/예제/한글코딩/Stream_ÉRTÉK.c)도 제공한다.
