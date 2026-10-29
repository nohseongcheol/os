# nativo ARM64 Java 커널의 C/C++ ficheiro·루프백 Ligar

이 디렉터리는 `platforms/rpi4-native` nativo kernel_VALOR 전용이다. 기존 i386 `int 0x80` 라이브러리나 ARM64 Linux libc용 라이브러리가 아니다.

`declarações/Arquivo_ABI.h`는 Português 함수명과 `extern "C"` ABI를 제공한다. `Ligar.c`는 kernel_VALOR 안에서 AOT Java ficheiro 메서드에 직접 연결하고, `usuário_ponte.c`는 독립 EL0 프로그램에서 SVC로 커널을 호출한다. real_dados ficheiro 처리는 `FicheirosMemória.java`, 루프백 datagrama 처리는 `loopback_rede.java`, 연결형 흐름은 `fluxo_rede.java`에 있다.

```sh
make -C /home/user/jkoros/platforms/rpi4-native build
make -C /home/user/jkoros/platforms/rpi4-native test
```

산출물은 kernel_VALOR 내부용 `platforms/rpi4-native/build/libposix-kor-arm64.a`와 사용자용 `libposix-kor-user.a`다. 사용자용 라이브러리로 독립 ELF64 C/C++ 프로그램의 생성자·RAII·ponto_flutuante_VALOR cirurgia_VALOR·ficheiro·UDP 루프백 호출을 검증했다. 일반 Linux 바이너리, 전체 POSIX/libc/libstdc++ 지원을 뜻하지 않는다. 서로 다른 두 라이브러리를 혼합하지 않는다.

Suporte_VALOR: `abrir_Arquivo`, `leitura_Arquivo_dados`, `gravar_Arquivo_dados`, `Close_Arquivo`, `busca_Arquivo`, `remover_Arquivo_entrada_nome`, `set_Arquivo_duração`, 보조 FUNÇÃO_VALOR `tamanho_do_arquivo`. erro 시 -1과 작업별 `número_do_erro`를 반환한다. `commit_Arquivos`은 RAM 파일이므로 ENOSYS를 반환한다. ficheiro 16개, 각 16384바이트, Nome 63바이트, descritor_entrada 16개이며 RAM 디렉터리·par_VALOR/절대 경로를 제공한다. Permissão_VALOR/영속 저장은 없다.

사용자용 `declarações/rede_ABI.h`는 real_dados Português 함수와 독립 구조체를 선언한다.
`Criar_empresa`, `BIND_email`, `enviar_datagrama_dados/receber`, `Conexão_rede/기다리기/receber`는
`usuário_ponte.c`에서 SVC를 호출하며 macro_VALOR 별칭이 아니다. `struct malha_soquete_email`의
`email_Família`, `número_da_porta`, `endereço_na_Internet.email_VALOR`을 사용한다. 상수는 enum의
`malha_Família`, `datagrama_soquete`, `datagrama_protocolo`, `fluxo_rede`, `fluxo_protocolo_de_transporte`이다.
Português·표준 구조체는 16바이트 ABI 배치를 공유하지만 서로 다른 C 자료형이다.
기존 pk_* 함수와 표준 구조체는 호환용으로 유지한다. externo_VALOR 통신은 nativo 커널의
lwIP TCP/UDP와 QEMU UART SLIP 연결을 사용한다. real_dados Pi 4 GENET 드라이버는 미지원이다.
소켓도 real_dados FUNÇÃO_VALOR `Close_Arquivo`로 닫는다.

[사용법·arquitetura·한계](../../platforms/rpi4-native/README.md), [espaço_do_utilizador ABI](../../platforms/rpi4-native/USER-ABI.md), [EL0 C++ ficheiro 예제](../../platforms/rpi4-native/espaço_do_utilizador/ExemploFicheiro.cpp), [UDP 루프백 예제](../../platforms/rpi4-native/espaço_do_utilizador/통신예제.cpp), [기존 kernel_VALOR 내부 호출 testes](../../platforms/rpi4-native/testes/Arquivo_Chamadas.cpp)을 참고한다.

C11/C++11의 한글 identificador_VALOR·헤더 uso_VALOR, SDK construir, ELF 업로드·Executar_comando, erro/부분 E_S 처리는 [한글 개발 매뉴얼](../../platforms/rpi4-native/DEVELOPMENT-KO.md)에 정리했다. [C 연결형 comunicação 예제](../../platforms/rpi4-native/예제/한글코딩/fluxo_VALOR.c)도 제공한다.
