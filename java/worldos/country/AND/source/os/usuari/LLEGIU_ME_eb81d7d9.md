# 셸에서 실행하는 usuari 프로그램과 UDP

게스트에서 일반적인 `main(String[] args)` 형식의 소스를 직접 작성하고 컴파일하려면 [제한형 Java 개발 entorn LLEGIU_ME_eb81d7d9](../../문서/자바개발환경.md)를 참고한다. 아래의 네이티브 ELF 개발과 별도로 `javac FILE.java`, `java CLASS`를 제공한다.

## 바로 Executa_ordre

allotjar Terminal 1:

```sh
cd /home/user/jkoros
python3 os/Eines/eco_dades.py --port 9000
```

이 서버는 `127.0.0.1`에만 바인딩한다. extern_VALOR 연결을 받도록 방화벽이나 포트 전달을 변경하지 않는다. Ctrl+C로 종료한다.

allotjar Terminal 2:

```sh
cd /home/user/jkoros
make run
```

게스트의 `jkoros>` 프롬프트에 입력:

```text
apps
run hello first second
net
run netcheck
run udp 10.0.2.2 9000 hello
run stress 9000
```

- `hello`: 독립 Java ELF 실행과 real_dades CPU permís_VALOR `ring 3`, 인수 Sortida.
- `netcheck`: port_VALOR 중복, 잘못된 control_VALOR_f011887b/punter/durada_VALOR, 비차단 받기와 Hora_VALOR 초과 verificar.
- `udp`: IPv4 Adreça·destinació_VALOR port_VALOR·한 Word_VALOR 메시지를 받아 UDP로 보내고 같은 응답을 verificar. `UDP ECHO PASS`, `Exit: 0`이면 성공.
- `stress`: allotjar `10.0.2.2`의 cedir_VALOR 창구와 1,023/1,024바이트 데이터그램을 24회 왕복. rebre_VALOR Loop_VALOR 경계를 여러 번 지난다.

`make run`/`run-gui`는 `-netdev user,id=net0 -device rtl8139,netdev=net0`을 사용한다. 현재 주소는 게스트 `10.0.2.15/24`, passarel_la_VALOR `10.0.2.2`로 고정돼 있다. QEMU usuari 네트워크의 allotjar accés_introducció 주소를 사용한 예제다. 다른 네트워크 설정에는 맞춰 수정해야 하며 자동 DHCP는 없다. NIC 없이 실행하려면 `make -C os run NET_ARGS='-net none'`을 사용한다. 이때 programa_f5044b9b 실행은 되지만 UDP 열기는 `-19`로 실패한다.

## 새 Java programa_f5044b9b Annexa_introducció

`예제/내프로그램.java`를 Següent_element 형식으로 만든다. 진입점은 인수 없는 `static int` 또는 `static void` 함수다. 인수는 usuari API로 조회한다.

```java
public final class 내프로그램 {
    public static int Executa_2() {
        usuari.Escriptura("My program is running in user mode.\n");
        return 0;
    }
}
```

`os/usuari/programa_f5044b9b.mk`에 추가한다.

```make
APP_NAMES += mine
APP_SOURCE_mine := usuari/예제/내프로그램.java
APP_ENTRY_mine := 내프로그램.Executa_2
```

여러 Java 파일을 쓰면 `APP_SOURCE_mine`에 공백으로 모두 나열한다. `usuari/declaració/usuari.java`는 자동으로 함께 컴파일한다.

```sh
cd /home/user/jkoros
make iso
make run
```

새로 부팅한 셸에서 `run mine`을 실행한다. 이미 Executa_ordre 중인 VM에는 generar_sistema 결과가 자동 반영되지 않는다. programa_f5044b9b 이름은 현재 셸의 ASCII 입력 제한에 맞춘 1~15자의 소문자 이름이며 Java Classe_VALOR·FUNCIÓ_VALOR·변수에는 한국어를 쓴다. 최대 32개 programa_f5044b9b, 한 Executa_ordre 파일은 최대 2MiB다.

독립 ELF만 컴파일할 수도 있다.

```sh
cd /home/user/jkoros
python3 compiler/컴파일러.py --target user --entry 인사.Executa_2 \
    -o os/build/apps/hello.elf os/usuari/declaració/usuari.java os/usuari/예제/인사.java
```

`--target user`는 **jkoros 전용 ABI**다. Linux 대상과 시스템 호출 번호가 다르므로 allotjar 터미널에서 직접 실행하면 안 된다. `.class`는 별도 `java CLASS` 명령의 suport_VALOR clip 안에서 실행한다. `.jar`와 일반 Linux Executa_ordre 파일은 지원하지 않는다.

## usuari 네트워크 API

선언은 `declaració/usuari.java`에 있다. `enviar_dades`/`rebre_dades`의 `int[]` element_element 한 개는 byte_VALOR 하나(0~255)를 나타낸다. 한 데이터그램의 최대 dades 길이는 1,024바이트다.

```java
int control_VALOR_f011887b = usuari.crear_xarxa(0); // 0: 임시 local_Àmbit UDP port_VALOR 자동 selecció_VALOR
int[] dades = new int[32];
dades[0] = 'H'; dades[1] = 'i';
int 보낸길이 = usuari.enviar_dades(control_VALOR_f011887b, 0x0a000202, 9000, dades, 2);
int CANTIDAD_RECIBIDA_durada = usuari.rebre_dades(control_VALOR_f011887b, dades, 1500);
usuari.Tanca_xarxa(control_VALOR_f011887b);
```

real_dades 프로그램에서는 Obre·enviar·받기의 음수 반환값을 각각 검사한다. 완성된 예제는 `예제/자료통신.java`에 있다. `rebre_dades`의 Espera_VALOR 시간은 0~2,000밀리초이며 0은 즉시 반환이다. 받은 데이터그램이 배열보다 크면 해당 데이터그램을 버리고 `-90`을 반환한다. 창구당 rebre_VALOR 대기열은 한 개뿐이므로 Annexa_introducció 도착분은 버린다. `보낸주소`와 `보낸창구`로 마지막으로 받은 상대를 조회한다.

| 반환값 | 의미 |
| --- | --- |
| 0 이상 | control_VALOR_f011887b·Procés_VALOR_introducció durada_VALOR·성공 등 해당 함수의 RESULTAT |
| -5 | dispositiu_VALOR enviar_VALOR error_VALOR |
| -9 | 잘못되었거나 닫힌 통신 control_VALOR_f011887b |
| -11 | 비차단 받기에서 도착한 dades 없음 |
| -14 | usuari punter/MATRIU_VALOR clip s_ha_produït_un_error |
| -19 | suport_VALOR NIC 없음 |
| -22 | port_VALOR/Espera_VALOR Hora_VALOR/인수 VALOR s_ha_produït_un_error |
| -24 | 열린 xarxa_port 4개 한도 |
| -38 | 알 수 없는 시스템 호출 |
| -90 | dades 또는 rebre_VALOR MATRIU_VALOR Mida 문제 |
| -98 | local_Àmbit port_VALOR INDEX 중복 |
| -101 | 지원하지 않는 destinació_VALOR Adreça |
| -110 | ARP·dispositiu_VALOR·rebre_VALOR Hora_VALOR 초과 |

IP 주소는 상위 바이트부터 표기한 32비트 값이다. `10.0.2.2`는 `0x0a000202`이다. 주소를 반환하는 함수는 codificació_VALOR 있는 Java `int`의 bit_VALOR 패턴을 사용하므로 상위 비트가 1인 정상 IP 주소가 음수로 보일 수 있다. 단순히 모든 API 반환값의 부호를 오류로 판단하면 안 된다.

## Executa_ordre 경계와 시스템 호출

```text
shell run → JKAP에서 ELF validar·적재 → ring 3 usuari programa_f5044b9b
                                 ↓ int 0x80
                      punter 검사 → Java nucli_VALOR API → RTL8139/UDP
                                 ↓ Surt_programa·excepció·Hora_VALOR 초과
                                shell 복귀
```

시스템 호출 레지스터는 `EAX=INDEX`, `EBX,ECX,EDX,ESI,EDI=인수`, `EAX=RESULTAT`다. Java 호출 스택 ABI는 컴파일러가 usuari 스텁에서 이 형식으로 바꾼다. C의 POSIX/JNI ABI가 아니다.

| INDEX | 호출 |
| --- | --- |
| 0 | Surt_programa(Estat_VALOR CODI_VALOR) — Executa_2/s_ha_produït_un_error 런타임에서 ús_VALOR |
| 1 | cadena_VALOR Escriptura |
| 2 / 3 | 인수 element_COMPT / 인수 cadena_VALOR Adreça |
| 10 | UDP Obre |
| 11 | UDP enviar(control_VALOR_f011887b, IP, destinació_VALOR port_VALOR, MATRIU_VALOR Adreça, durada_VALOR) |
| 12 | UDP rebre(control_VALOR_f011887b, MATRIU_VALOR Adreça, 제한 밀리초) |
| 13 | UDP Tanca |
| 14 | local_Àmbit IP Adreça |
| 15 / 16 | 마지막 homòleg_VALOR IP / UDP port_VALOR |
| 20 | RAM Fitxer Lectura(Nom int[] Adreça, Sortida int[] Adreça) |
| 21 | RAM Fitxer Escriptura(Nom int[] Adreça, 입력 int[] Adreça, byte_VALOR durada_VALOR) |
| 22 | UTF-16 CODI_VALOR lliçó_VALOR 문자 Sortida(0~65535) |

Fitxer API는 `usuari.tancar_arxiu(int[] Nom, int[] dades)`와 `usuari.escriure_arxiu(int[] Nom, int[] dades, int durada_VALOR)`다. 이름은 ASCII CODI_VALOR MATRIU_VALOR(최대 64칸, 0 Surt_programa 또는 MATRIU_VALOR 끝), dades element_element 하나는 한 바이트다. 반환값은 읽거나 쓴 길이이며 Fitxer 없음 `-2`, punter s_ha_produït_un_error `-14`, Nom/durada_VALOR s_ha_produït_un_error `-22`, Fitxer 슬롯 부족 `-28`, Mida 초과 `-90`을 반환한다. 쓰기는 validar 후 Fitxer 전체를 대체한다. `usuari.escriure_caràcter_VALOR(int)`는 문자를 단말에 출력한다. Java 프로그램의 일반 `java.io` 구현은 아니다.

`실행권한()`은 시스템 호출이 아니라 usuari 모드에서 CS의 하위 비트를 직접 읽으므로 real_dades Executa_ordre 권한을 확인한다. nucli_VALOR 포트 접근용 `dispositiu_VALOR` native 함수는 usuari objectiu 컴파일에서 거부한다. ELF에 직접 특권 명령을 넣더라도 CPU가 차단한다.

## 범위와 제한

- 한 번에 한 프로그램만 실행하며 완료 후 셸로 돌아온다. 백그라운드 Executa_ordre, 파이프, 프로세스 간 통신은 없다. Executa_ordre 파일은 커널의 Lectura 전용 JKAP 묶음에서 적재한다. dades 파일에는 주기억 파일체계와 전용 IDE 보존 형식이 있다.
- usuari 가상 Adreça `0x04000000..0x043fffff`를 물리 8~12MiB에 연결한다. Executa_ordre 영상은 frontal_VALOR 2MiB, 인수는 `0x04300000`부터, 스택은 영역 끝에서 시작한다. nucli_VALOR identity 페이지는 supervisor 전용이다.
- 실행마다 4MiB usuari 영역을 비우고 Fitxer 구역을 복사해 BSS·MATRIU_VALOR 영역을 초기화한다. usuari GC는 없지만 Surt_programa 후 Següent_element Executa_ordre 때 영역을 재사용한다. 인수는 공백으로 분리한 최대 16개이며 oferta/이스케이프 파싱은 없다.
- usuari 페이지의 CODI_VALOR/dades 분리 Lectura 전용 Ajusts, NX, 스택 guard, ASLR은 아직 없다. 커널과 usuari Memòria_dades·포트 permís_VALOR 경계를 구현한 초기판이지 보안 인증된 샌드박스는 아니다.
- PIT 100Hz로 약 3초 Executa_ordre 상한을 두며 Hora_VALOR 초과는 `Exit: 124`다. usuari CPU 예외는 `128 + excepció INDEX`(페이지 s_ha_produït_un_error 142, 특권 위반 141), Java MATRIU_VALOR/계산 오류는 101~105다. nucli_VALOR 오류까지 복구하는 구조는 아니다.
- 네트워크는 PCI bus 0/function 0의 RTL8139, estàtic_VALOR IPv4, ARP, UDP만 지원한다. NIC는 폴링하고 송신은 동기식이다. IPv4 단편 재조립·TCP·DNS·DHCP·IPv6·HTTP·TLS·일반 `java.net`은 미지원이다. IPv4 UDP suma_de_comprovació 0은 규약에 따라 허용하고, 그 외 UDP/IP 검사합과 길이는 검증한다.
- usuari Executa_ordre·네트워크·protegir_VALOR 경계 전체 시험은 QEMU에서 수행했다. VirtualBox에서도 `make vbox`로 부팅과 `run hello vbox`의 ring 3 Executa_ordre·정상 종료를 확인했다. VirtualBox PCnet/E1000용 드라이버는 없어 그 환경의 네트워크는 지원하지 않는다.

## validar 근거

`make test`는 컴파일러 14개 시험, Java 패킷 condició 2,201개 검사, 기존 shell ELF/ISO 부팅 시험, usuari ELF/real_dades UDP/protegir_VALOR 경계 시험을 실행한다. 네트워크 시험은 루프백 서버가 받은 자료의 durada_VALOR·해시까지 `os/build/사용자통신시험.json`에 기록한다. 시험용 손상된 ELF·특권 Ordre·무한 esprint_VALOR 프로그램은 임시 묶음에만 넣으며 배포용 `apps` 목록에는 넣지 않는다.

참고한 일차 dades: [Intel 시스템 프로그래밍 명세](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), [QEMU RTL8139 구현](https://github.com/qemu/qemu/blob/master/hw/net/rtl8139.c), [QEMU 네트워크 LLEGIU_ME_eb81d7d9](https://www.qemu.org/docs/master/system/devices/net.html), [IPv4 RFC 791](https://www.rfc-editor.org/rfc/rfc791), [ARP RFC 826](https://www.rfc-editor.org/rfc/rfc826), [UDP RFC 768](https://www.rfc-editor.org/rfc/rfc768).
