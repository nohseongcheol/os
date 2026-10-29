# nativo ARM64 Java 커널의 C/C++ file·루프백 Connetti

이 디렉터리는 `platforms/rpi4-native` nativo kernel_VALORE 전용이다. 기존 i386 `int 0x80` 라이브러리나 ARM64 Linux libc용 라이브러리가 아니다.

`dichiarazioni/File_ABI.h`는 Italiano 함수명과 `extern "C"` ABI를 제공한다. `Connetti.c`는 kernel_VALORE 안에서 AOT Java file 메서드에 직접 연결하고, `USER_bridge.c`는 독립 EL0 프로그램에서 SVC로 커널을 호출한다. effettivo_dati file 처리는 `FileMemoria.java`, 루프백 datagramma 처리는 `loopback_rete.java`, 연결형 흐름은 `Stream_rete.java`에 있다.

```sh
make -C /home/user/jkoros/platforms/rpi4-native build
make -C /home/user/jkoros/platforms/rpi4-native test
```

산출물은 kernel_VALORE 내부용 `platforms/rpi4-native/build/libposix-kor-arm64.a`와 사용자용 `libposix-kor-user.a`다. 사용자용 라이브러리로 독립 ELF64 C/C++ 프로그램의 생성자·RAII·virgola_mobile_VALORE operazione_VALORE·file·UDP 루프백 호출을 검증했다. 일반 Linux 바이너리, 전체 POSIX/libc/libstdc++ 지원을 뜻하지 않는다. 서로 다른 두 라이브러리를 혼합하지 않는다.

Supporto_VALORE: `aperto_File`, `파일자료읽기`, `scrivere_File_dati`, `Chiudi_File`, `cercare_File`, `rimuovere_File_voce_nome`, `set_File_durata`, 보조 FUNZIONE_VALORE `dimensioni_del_file`. errore 시 -1과 작업별 `numero_errore`를 반환한다. `commit_File`은 RAM 파일이므로 ENOSYS를 반환한다. file 16개, 각 16384바이트, Nome 63바이트, descrittore_voce 16개이며 RAM 디렉터리·peer_VALORE/절대 경로를 제공한다. privilegio_VALORE/영속 저장은 없다.

사용자용 `dichiarazioni/rete_ABI.h`는 effettivo_dati Italiano 함수와 독립 구조체를 선언한다.
`Crea_endpoint`, `BIND_e_mail`, `inviare_datagramma_dati/ricevere`, `CONNETTI_rete/기다리기/ricevere`는
`USER_bridge.c`에서 SVC를 호출하며 macro_VALORE 별칭이 아니다. `struct cloud_socket_e_mail`의
`e_mail_serie`, `numero_di_porta`, `indirizzo_Internet.e_mail_VALORE`을 사용한다. 상수는 enum의
`cloud_serie`, `socket_di_datagramma`, `datagramma_protocollo`, `Stream_rete`, `Stream_protocollo_di_trasporto`이다.
Italiano·표준 구조체는 16바이트 ABI 배치를 공유하지만 서로 다른 C 자료형이다.
기존 pk_* 함수와 표준 구조체는 호환용으로 유지한다. esterno_VALORE 통신은 nativo 커널의
lwIP TCP/UDP와 QEMU UART SLIP 연결을 사용한다. effettivo_dati Pi 4 GENET 드라이버는 미지원이다.
소켓도 effettivo_dati FUNZIONE_VALORE `Chiudi_File`로 닫는다.

[사용법·architettura·한계](../../platforms/rpi4-native/README.md), [spazio_utente ABI](../../platforms/rpi4-native/USER-ABI.md), [EL0 C++ file 예제](../../platforms/rpi4-native/spazio_utente/EsempioFile.cpp), [UDP 루프백 예제](../../platforms/rpi4-native/spazio_utente/통신예제.cpp), [기존 kernel_VALORE 내부 호출 prove](../../platforms/rpi4-native/prove/File_Chiamate.cpp)을 참고한다.

C11/C++11의 한글 identificatore_VALORE·헤더 usare_VALORE, SDK costruire, ELF 업로드·Esegui_comando, errore/부분 I_O 처리는 [한글 sviluppo 매뉴얼](../../platforms/rpi4-native/DEVELOPMENT-KO.md)에 정리했다. [C 연결형 comunicazione 예제](../../platforms/rpi4-native/예제/한글코딩/Stream_VALORE.c)도 제공한다.
