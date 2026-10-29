# espaço_do_utilizador 호출 limite_VALOR

대상은 jkoros i386 ELF32다. Linux i386의 호출 번호와 바이너리 호환이 아니다. C의 cdecl 인수를 `computador/SO_Chamadas.s`에서 EAX(ÍNDICE), EBX·ECX·EDX·ESI·EDI(첫째~다섯째 argumentos)로 변환한다. EBX·ESI·EDI·EBP를 보존하며 결과는 EAX다. kernel_VALOR 실패는 negativo_VALOR erro ÍNDICE, C biblioteca 실패는 -1과 양수 errno다.

커널은 0x04000000 이상, 0x04400000 미만의 espaço_do_utilizador região_VALOR 안에 자료의 전체 길이가 들어가는지 확인한다. 단순 널 검사가 아니다. C dados 주소는 byte_VALOR 주소이며, 기존 Java AOT `int[]` 포인터와 혼용하지 않는다. Java ficheiro 흐름의 어셈블리 경계가 별도 byte_VALOR 버퍼를 마련하여 같은 호출을 사용한다.

| ÍNDICE | Acção | argumentos |
|---|---|---|
| 30 | abrir_Arquivo | NUL 끝 Nome Endereço, Definições, concessão_Permissão |
| 31 | leitura_Arquivo_dados | descritor_entrada, dados Endereço, byte_VALOR número |
| 32 | gravar_Arquivo_dados | descritor_entrada, dados Endereço, byte_VALOR número |
| 33 | Close_Arquivo | descritor_entrada |
| 34 | busca_Arquivo | descritor_entrada, Codificação_VALOR 있는 DESLOC_VALOR, ação_raiz |
| 35 | Duplicar_Arquivo_descritor | descritor_entrada |
| 36 | 파일서술자지정복제 | descritor_entrada, 새 descritor_entrada |
| 37 | leitura_Arquivo_Status | descritor_entrada, 48바이트 Estado_VALOR Endereço |
| 38 | remover_Arquivo_entrada_nome | NUL 끝 Nome Endereço |
| 39 | set_Arquivo_duração | descritor_entrada, 새 duração_VALOR |
| 40 | visual_Arquivo_descritor | descritor_entrada, comando, VALOR |
| 41 | Criar_empresa | Endereço SO_VALOR, Tipo_VALOR, valor_do_contrato ÍNDICE |
| 42 | BIND_email | descritor_entrada, sockaddr_in Endereço, duração_VALOR |
| 43 | enviar_datagrama_dados | descritor_entrada, dados Endereço, duração_VALOR, Definições, solicitação Endereço |
| 44 | receber_datagrama_dados | descritor_entrada, dados Endereço, duração_VALOR, Definições, solicitação Endereço |
| 45 | leitura_soquete_email | descritor_entrada, sockaddr Endereço, socklen_t Endereço |
| 46 | set_receber_TEMPOLIMITE | descritor_entrada, 0~2000 밀리초 |
| 47 | commit_Arquivos | descritor_entrada |

43번 요청은 32비트 주소와 32비트 길이의 두 칸이다. 44번 요청은 32비트 주소와 길이를 담은 32비트 값의 Endereço 두 칸이다. receber_VALOR 주소가 NULL이면 par_VALOR Endereço 기록을 생략한다. sockaddr_in은 16바이트이며 Endereço 체계는 celular_VALOR byte_VALOR SEQUÊNCIA_VALOR, 접속번호와 IP 주소는 네트워크 byte_VALOR 차례다. 축소된 Endereço 버퍼에도 들어가는 앞부분을 쓰고 전체 Endereço Tamanho 16을 반환한다.

0~22번의 기존 Java AOT 호출은 유지한다. 0은 sair_app, 2·3은 기존 argumentos 조회다. em_dia_item 커널의 argumentos 목록이 Executar_comando 이름을 제외하므로 C 진입기는 argv[0]에 고정 cadeia_VALOR `jkoros-app`을 넣고 이후 인수를 전달한다. argv 끝에는 NULL이 있다. 이 제한도 일반 UNIX Processo_VALOR ABI와 다른 점이다.

표준 헤더의 inteiro Tamanho, 플래그 VALOR, stat valor_do_campo 순서는 `códigoFonte/declarações/`에 정의한다. 동적 Ligar·다중 Processo_VALOR·스레드가 추가되면 erro ÍNDICE 저장과 recurso_VALOR 수명, 호출 경계도 함께 검토해야 한다.
