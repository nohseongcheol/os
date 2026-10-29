# 셸에서 실행하는 espaço_do_utilizador 프로그램과 UDP

게스트에서 일반적인 `main(String[] args)` 형식의 소스를 직접 작성하고 컴파일하려면 [제한형 Java 개발 ambiente LEIAME_eb81d7d9](../../문서/Java_IDE.md)를 참고한다. 아래의 네이티브 ELF 개발과 별도로 `javac FILE.java`, `java CLASS`를 제공한다.

## 바로 Executar_comando

host terminal 1:

```sh
cd /home/user/jkoros
python3 os/ferramentas/eco_dados.py --port 9000
```

이 서버는 `127.0.0.1`에만 바인딩한다. externo_VALOR 연결을 받도록 방화벽이나 hardware_porta 전달을 변경하지 않는다. Ctrl+C로 종료한다.

host terminal 2:

```sh
cd /home/user/jkoros
make run
```

게스트의 `jkoros>` 프롬프트에 entrada_VALOR:

```text
apps
run hello first second
net
run netcheck
run udp 10.0.2.2 9000 hello
run stress 9000
```

- `hello`: 독립 Java ELF 실행과 real_dados CPU Permissão_VALOR `ring 3`, argumentos saídaTexto.
- `netcheck`: porta_VALOR 중복, 잘못된 alça_VALOR/ponteiro/duração_VALOR, 비차단 받기와 valor_temporal 초과 verificar.
- `udp`: IPv4 Endereço·destino_VALOR porta_VALOR·한 Word_VALOR 메시지를 받아 UDP로 보내고 같은 응답을 verificar. `UDP ECHO PASS`, `Exit: 0`이면 성공.
- `stress`: host `10.0.2.2`의 ceder_VALOR 창구와 1,023/1,024바이트 데이터그램을 24회 왕복. receber_VALOR Loop_VALOR 경계를 여러 번 지난다.

`make run`/`run-gui`는 `-netdev user,id=net0 -device rtl8139,netdev=net0`을 사용한다. em_dia_item 주소는 게스트 `10.0.2.15/24`, gateway_VALOR `10.0.2.2`로 고정돼 있다. QEMU espaço_do_utilizador 네트워크의 host acesso_entrada 주소를 사용한 예제다. 다른 네트워크 설정에는 맞춰 수정해야 하며 자동 DHCP는 없다. NIC 없이 실행하려면 `make -C os run NET_ARGS='-net none'`을 사용한다. 이때 app_f5044b9b 실행은 되지만 UDP 열기는 `-19`로 실패한다.

## 새 Java app_f5044b9b Acrescentar_entrada

`예제/내프로그램.java`를 Avançar_item 형식으로 만든다. 진입점은 argumentos 없는 `static int` 또는 `static void` 함수다. 인수는 espaço_do_utilizador API로 조회한다.

```java
public final class 내프로그램 {
    public static int iniciar() {
        espaço_do_utilizador.Escrita("My program is running in user mode.\n");
        return 0;
    }
}
```

`os/espaço_do_utilizador/app_f5044b9b.mk`에 추가한다.

```make
APP_NAMES += mine
APP_SOURCE_mine := espaço_do_utilizador/예제/내프로그램.java
APP_ENTRY_mine := 내프로그램.iniciar
```

여러 Java 파일을 쓰면 `APP_SOURCE_mine`에 공백으로 모두 나열한다. `espaço_do_utilizador/declaração/espaço_do_utilizador.java`는 자동으로 함께 컴파일한다.

```sh
cd /home/user/jkoros
make iso
make run
```

새로 부팅한 셸에서 `run mine`을 실행한다. 이미 Executar_comando 중인 VM에는 construir 결과가 자동 반영되지 않는다. app_f5044b9b 이름은 em_dia_item 셸의 ASCII entrada_VALOR 제한에 맞춘 1~15자의 소문자 이름이며 Java aula_VALOR·FUNÇÃO_VALOR·변수에는 한국어를 쓴다. 최대 32개 app_f5044b9b, 한 Executar_comando 파일은 최대 2MiB다.

독립 ELF만 컴파일할 수도 있다.

```sh
cd /home/user/jkoros
python3 compiler/compilador.py --target user --entry saudação_ae353e94.iniciar \
    -o os/build/apps/hello.elf os/espaço_do_utilizador/declaração/espaço_do_utilizador.java os/espaço_do_utilizador/예제/saudação_ae353e94.java
```

`--target user`는 **jkoros 전용 ABI**다. Linux 대상과 시스템 호출 번호가 다르므로 host 터미널에서 직접 실행하면 안 된다. `.class`는 별도 `java CLASS` 명령의 Suporte_VALOR recortar 안에서 실행한다. `.jar`와 일반 Linux Executar_comando 파일은 지원하지 않는다.

## espaço_do_utilizador 네트워크 API

선언은 `declaração/espaço_do_utilizador.java`에 있다. `enviar_dados`/`receber_dados`의 `int[]` item_elemento 한 개는 byte_VALOR 하나(0~255)를 나타낸다. 한 데이터그램의 최대 dados 길이는 1,024바이트다.

```java
int alça_VALOR = espaço_do_utilizador.abrir_rede(0); // 0: 임시 local_Scope UDP porta_VALOR 자동 seleção_VALOR
int[] dados = new int[32];
dados[0] = 'H'; dados[1] = 'i';
int 보낸길이 = espaço_do_utilizador.enviar_dados(alça_VALOR, 0x0a000202, 9000, dados, 2);
int RECEBER_duração = espaço_do_utilizador.receber_dados(alça_VALOR, dados, 1500);
espaço_do_utilizador.Close_rede(alça_VALOR);
```

real_dados 프로그램에서는 Abrir·enviar·받기의 negativo_VALOR 반환값을 각각 검사한다. 완성된 예제는 `예제/dados_comunicação.java`에 있다. `receber_dados`의 aguarde_VALOR 시간은 0~2,000밀리초이며 0은 즉시 반환이다. 받은 데이터그램이 배열보다 크면 해당 데이터그램을 버리고 `-90`을 반환한다. 창구당 receber_VALOR 대기열은 한 개뿐이므로 Acrescentar_entrada 도착분은 버린다. `보낸주소`와 `보낸창구`로 마지막으로 받은 상대를 조회한다.

| 반환값 | 의미 |
| --- | --- |
| 0 이상 | alça_VALOR·Processo_VALOR_entrada duração_VALOR·성공 등 해당 함수의 resultado |
| -5 | celular_VALOR enviar_VALOR falha_VALOR |
| -9 | 잘못되었거나 닫힌 comunicação alça_VALOR |
| -11 | 비차단 받기에서 도착한 dados 없음 |
| -14 | espaço_do_utilizador ponteiro/MATRIZ_VALOR recortar erro |
| -19 | Suporte_VALOR NIC 없음 |
| -22 | porta_VALOR/aguarde_VALOR valor_temporal/argumentos VALOR erro |
| -24 | 열린 rede_porta 4개 한도 |
| -38 | 알 número 없는 시스템 호출 |
| -90 | dados 또는 receber_VALOR MATRIZ_VALOR Tamanho 문제 |
| -98 | local_Scope porta_VALOR ÍNDICE 중복 |
| -101 | 지원하지 않는 destino_VALOR Endereço |
| -110 | ARP·celular_VALOR·receber_VALOR valor_temporal 초과 |

IP 주소는 상위 바이트부터 표기한 32비트 값이다. `10.0.2.2`는 `0x0a000202`이다. 주소를 반환하는 함수는 Codificação_VALOR 있는 Java `int`의 bit_VALOR 패턴을 사용하므로 상위 비트가 1인 TI_normal IP 주소가 음수로 보일 número 있다. 단순히 모든 API 반환값의 부호를 오류로 판단하면 안 된다.

## Executar_comando 경계와 시스템 호출

```text
shell run → JKAP에서 ELF validar·적재 → ring 3 espaço_do_utilizador app_f5044b9b
                                 ↓ int 0x80
                      ponteiro 검사 → Java kernel_VALOR API → RTL8139/UDP
                                 ↓ sair_app·exceção·valor_temporal 초과
                                shell 복귀
```

시스템 호출 레지스터는 `EAX=ÍNDICE`, `EBX,ECX,EDX,ESI,EDI=argumentos`, `EAX=resultado`다. Java 호출 operando_pilha ABI는 컴파일러가 espaço_do_utilizador 스텁에서 이 형식으로 바꾼다. C의 POSIX/JNI ABI가 아니다.

| ÍNDICE | 호출 |
| --- | --- |
| 0 | sair_app(Estado_VALOR valor_do_código) — iniciar/erro 런타임에서 uso_VALOR |
| 1 | cadeia_VALOR Escrita |
| 2 / 3 | argumentos item_CONT_NÚM / argumentos cadeia_VALOR Endereço |
| 10 | UDP Abrir |
| 11 | UDP enviar(alça_VALOR, IP, destino_VALOR porta_VALOR, MATRIZ_VALOR Endereço, duração_VALOR) |
| 12 | UDP receber(alça_VALOR, MATRIZ_VALOR Endereço, 제한 밀리초) |
| 13 | UDP Fechar |
| 14 | local_Scope IP Endereço |
| 15 / 16 | 마지막 par_VALOR IP / UDP porta_VALOR |
| 20 | RAM ficheiro Leitura(Nome int[] Endereço, saídaTexto int[] Endereço) |
| 21 | RAM ficheiro Escrita(Nome int[] Endereço, entrada_VALOR int[] Endereço, byte_VALOR duração_VALOR) |
| 22 | UTF-16 valor_do_código lição_VALOR 문자 saídaTexto(0~65535) |

ficheiro API는 `espaço_do_utilizador.leitura_Arquivo(int[] Nome, int[] dados)`와 `espaço_do_utilizador.gravar_Arquivo(int[] Nome, int[] dados, int duração_VALOR)`다. 이름은 ASCII valor_do_código MATRIZ_VALOR(최대 64칸, 0 sair_app 또는 MATRIZ_VALOR 끝), dados item_elemento 하나는 한 바이트다. 반환값은 읽거나 쓴 길이이며 ficheiro 없음 `-2`, ponteiro erro `-14`, Nome/duração_VALOR erro `-22`, ficheiro slot_VALOR 부족 `-28`, Tamanho 초과 `-90`을 반환한다. 쓰기는 validar 후 ficheiro 전체를 대체한다. `espaço_do_utilizador.gravar_caractere_VALOR(int)`는 문자를 단말에 출력한다. Java 프로그램의 일반 `java.io` 구현은 아니다.

`execução_Permissão()`은 시스템 호출이 아니라 espaço_do_utilizador 모드에서 CS의 하위 비트를 직접 읽으므로 real_dados Executar_comando 권한을 확인한다. kernel_VALOR hardware_porta 접근용 `celular_VALOR` native 함수는 espaço_do_utilizador meta 컴파일에서 거부한다. ELF에 직접 특권 명령을 넣더라도 CPU가 차단한다.

## 범위와 제한

- 한 번에 한 프로그램만 실행하며 완료 후 셸로 돌아온다. 백그라운드 Executar_comando, 파이프, 프로세스 간 통신은 없다. Executar_comando 파일은 커널의 Leitura 전용 JKAP 묶음에서 적재한다. dados 파일에는 주기억 파일체계와 전용 IDE 보존 형식이 있다.
- espaço_do_utilizador 가상 Endereço `0x04000000..0x043fffff`를 물리 8~12MiB에 연결한다. Executar_comando 영상은 câmera_frontal_VALOR 2MiB, 인수는 `0x04300000`부터, 스택은 região_VALOR 끝에서 시작한다. kernel_VALOR identity 페이지는 supervisor 전용이다.
- 실행마다 4MiB espaço_do_utilizador 영역을 비우고 ficheiro 구역을 복사해 BSS·MATRIZ_VALOR 영역을 초기화한다. espaço_do_utilizador GC는 없지만 sair_app 후 Avançar_item Executar_comando 때 영역을 재사용한다. 인수는 공백으로 분리한 최대 16개이며 Citação/이스케이프 파싱은 없다.
- espaço_do_utilizador 페이지의 valor_do_código/dados 분리 Leitura 전용 Definições, NX, operando_pilha guard, ASLR은 아직 없다. 커널과 espaço_do_utilizador Memória_dados·hardware_porta Permissão_VALOR 경계를 구현한 초기판이지 보안 인증된 샌드박스는 아니다.
- PIT 100Hz로 약 3초 Executar_comando 상한을 두며 valor_temporal 초과는 `Exit: 124`다. espaço_do_utilizador CPU 예외는 `128 + exceção ÍNDICE`(페이지 erro 142, 특권 위반 141), Java MATRIZ_VALOR/계산 오류는 101~105다. kernel_VALOR 오류까지 복구하는 구조는 아니다.
- 네트워크는 PCI bus 0/function 0의 RTL8139, estático_VALOR IPv4, ARP, UDP만 지원한다. NIC는 폴링하고 송신은 동기식이다. IPv4 단편 재조립·TCP·DNS·DHCP·IPv6·HTTP·TLS·일반 `java.net`은 미지원이다. IPv4 UDP soma_de_verificação 0은 규약에 따라 허용하고, 그 외 UDP/IP 검사합과 길이는 검증한다.
- espaço_do_utilizador Executar_comando·네트워크·proteger_VALOR limite_VALOR 전체 시험은 QEMU에서 수행했다. VirtualBox에서도 `make vbox`로 부팅과 `run hello vbox`의 ring 3 Executar_comando·TI_normal 종료를 확인했다. VirtualBox PCnet/E1000용 드라이버는 없어 그 환경의 네트워크는 지원하지 않는다.

## validar 근거

`make test`는 compilador 14개 testes, Java 패킷 doença 2,201개 검사, 기존 shell ELF/ISO arranque_da_máquina testes, espaço_do_utilizador ELF/real_dados UDP/proteger_VALOR limite_VALOR 시험을 실행한다. 네트워크 시험은 루프백 서버가 받은 자료의 duração_VALOR·해시까지 `os/build/teste_Usenet.json`에 기록한다. 시험용 손상된 ELF·특권 comando·무한 sprint_VALOR 프로그램은 임시 묶음에만 넣으며 배포용 `apps` 목록에는 넣지 않는다.

참고한 일차 dados: [Intel 시스템 프로그래밍 especificação](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), [QEMU RTL8139 implementação](https://github.com/qemu/qemu/blob/master/hw/net/rtl8139.c), [QEMU 네트워크 LEIAME_eb81d7d9](https://www.qemu.org/docs/master/system/devices/net.html), [IPv4 RFC 791](https://www.rfc-editor.org/rfc/rfc791), [ARP RFC 826](https://www.rfc-editor.org/rfc/rfc826), [UDP RFC 768](https://www.rfc-editor.org/rfc/rfc768).
