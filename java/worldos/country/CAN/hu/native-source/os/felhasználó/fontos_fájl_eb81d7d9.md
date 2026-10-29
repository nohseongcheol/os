# 셸에서 실행하는 felhasználó 프로그램과 UDP

게스트에서 일반적인 `main(String[] args)` 형식의 소스를 직접 작성하고 컴파일하려면 [제한형 Java 개발 környezet_5d36e09c fontos_fájl_eb81d7d9](../../문서/Java_IDE.md)를 참고한다. 아래의 네이티브 ELF 개발과 별도로 `javac FILE.java`, `java CLASS`를 제공한다.

## 바로 végrehajt_parancs

gazda Terminál 1:

```sh
cd /home/user/jkoros
python3 os/Eszközök/visszhang_adat.py --port 9000
```

이 서버는 `127.0.0.1`에만 바인딩한다. külső_ÉRTÉK 연결을 받도록 방화벽이나 hardver_port 전달을 변경하지 않는다. Ctrl+C로 종료한다.

gazda Terminál 2:

```sh
cd /home/user/jkoros
make run
```

게스트의 `jkoros>` 프롬프트에 bevitel_ÉRTÉK:

```text
apps
run hello first second
net
run netcheck
run udp 10.0.2.2 9000 hello
run stress 9000
```

- `hello`: 독립 Java ELF 실행과 tényleges_adat CPU engedély_ÉRTÉK `ring 3`, Argumentumok Kimenet.
- `netcheck`: port_ÉRTÉK 중복, 잘못된 leíró_ÉRTÉK/mutató/hossz_ÉRTÉK, 비차단 받기와 IDŐ_ÉRTÉK 초과 igazol.
- `udp`: IPv4 CÍM·cél_ÉRTÉK port_ÉRTÉK·한 szó_ÉRTÉK 메시지를 받아 UDP로 보내고 같은 응답을 igazol. `UDP ECHO PASS`, `Exit: 0`이면 성공.
- `stress`: gazda `10.0.2.2`의 átruház_ÉRTÉK 창구와 1,023/1,024바이트 데이터그램을 24회 왕복. fogad_ÉRTÉK Loop_ÉRTÉK 경계를 여러 번 지난다.

`make run`/`run-gui`는 `-netdev user,id=net0 -device rtl8139,netdev=net0`을 사용한다. aktuális_cikk 주소는 게스트 `10.0.2.15/24`, átjáró_ÉRTÉK `10.0.2.2`로 고정돼 있다. QEMU felhasználó 네트워크의 gazda hozzáfér_bejegyzés 주소를 사용한 예제다. 다른 네트워크 설정에는 맞춰 수정해야 하며 자동 DHCP는 없다. NIC 없이 실행하려면 `make -C os run NET_ARGS='-net none'`을 사용한다. 이때 app_f5044b9b 실행은 되지만 UDP 열기는 `-19`로 실패한다.

## 새 Java app_f5044b9b hozzáfűz_bejegyzés

`예제/내프로그램.java`를 Tovább_cikk 형식으로 만든다. 진입점은 Argumentumok 없는 `static int` 또는 `static void` 함수다. 인수는 felhasználó API로 조회한다.

```java
public final class 내프로그램 {
    public static int Futtatás() {
        felhasználó.Írás("My program is running in user mode.\n");
        return 0;
    }
}
```

`os/felhasználó/app_f5044b9b.mk`에 추가한다.

```make
APP_NAMES += mine
APP_SOURCE_mine := felhasználó/예제/내프로그램.java
APP_ENTRY_mine := 내프로그램.Futtatás
```

여러 Java 파일을 쓰면 `APP_SOURCE_mine`에 공백으로 모두 나열한다. `felhasználó/bevallás/felhasználó.java`는 자동으로 함께 컴파일한다.

```sh
cd /home/user/jkoros
make iso
make run
```

새로 부팅한 셸에서 `run mine`을 실행한다. 이미 végrehajt_parancs 중인 VM에는 épít_Rendszer 결과가 자동 반영되지 않는다. app_f5044b9b 이름은 aktuális_cikk 셸의 ASCII bevitel_ÉRTÉK 제한에 맞춘 1~15자의 소문자 이름이며 Java tanóra_ÉRTÉK·FÜGGVÉNY_ÉRTÉK·변수에는 한국어를 쓴다. 최대 32개 app_f5044b9b, 한 végrehajt_parancs 파일은 최대 2MiB다.

독립 ELF만 컴파일할 수도 있다.

```sh
cd /home/user/jkoros
python3 compiler/fordítóprogram.py --target user --entry 인사.Futtatás \
    -o os/build/apps/hello.elf os/felhasználó/bevallás/felhasználó.java os/felhasználó/예제/인사.java
```

`--target user`는 **jkoros 전용 ABI**다. Linux 대상과 시스템 호출 번호가 다르므로 gazda 터미널에서 직접 실행하면 안 된다. `.class`는 별도 `java CLASS` 명령의 támogat_ÉRTÉK klip 안에서 실행한다. `.jar`와 일반 Linux végrehajt_parancs 파일은 지원하지 않는다.

## felhasználó 네트워크 API

선언은 `bevallás/felhasználó.java`에 있다. `küld_adat`/`fogad_adat`의 `int[]` cikk_elem 한 개는 bájt_ÉRTÉK 하나(0~255)를 나타낸다. 한 데이터그램의 최대 adat 길이는 1,024바이트다.

```java
int leíró_ÉRTÉK = felhasználó.készít_hálózat(0); // 0: 임시 helyi_hatókör UDP port_ÉRTÉK 자동 kijelölés_ÉRTÉK
int[] adat = new int[32];
adat[0] = 'H'; adat[1] = 'i';
int 보낸길이 = felhasználó.küld_adat(leíró_ÉRTÉK, 0x0a000202, 9000, adat, 2);
int KAPOTT_hossz = felhasználó.fogad_adat(leíró_ÉRTÉK, adat, 1500);
felhasználó.bezár_hálózat(leíró_ÉRTÉK);
```

tényleges_adat 프로그램에서는 Megnyitás·küld·받기의 음수 반환값을 각각 검사한다. 완성된 예제는 `예제/adat_kommunikáció.java`에 있다. `fogad_adat`의 várj_ÉRTÉK 시간은 0~2,000밀리초이며 0은 즉시 반환이다. 받은 데이터그램이 배열보다 크면 해당 데이터그램을 버리고 `-90`을 반환한다. 창구당 fogad_ÉRTÉK 대기열은 한 개뿐이므로 hozzáfűz_bejegyzés 도착분은 버린다. `보낸주소`와 `보낸창구`로 마지막으로 받은 상대를 조회한다.

| 반환값 | 의미 |
| --- | --- |
| 0 이상 | leíró_ÉRTÉK·folyamat_ÉRTÉK_bejegyzés hossz_ÉRTÉK·성공 등 해당 함수의 KR |
| -5 | mobil_ÉRTÉK küld_ÉRTÉK hiba_ÉRTÉK |
| -9 | 잘못되었거나 닫힌 kommunikáció leíró_ÉRTÉK |
| -11 | 비차단 받기에서 도착한 adat 없음 |
| -14 | felhasználó mutató/TÖMB_ÉRTÉK klip HIBA |
| -19 | támogat_ÉRTÉK NIC 없음 |
| -22 | port_ÉRTÉK/várj_ÉRTÉK IDŐ_ÉRTÉK/Argumentumok ÉRTÉK HIBA |
| -24 | 열린 hálózat_port 4개 한도 |
| -38 | 알 szám 없는 시스템 호출 |
| -90 | adat 또는 fogad_ÉRTÉK TÖMB_ÉRTÉK Méret 문제 |
| -98 | helyi_hatókör port_ÉRTÉK INDEX 중복 |
| -101 | 지원하지 않는 cél_ÉRTÉK CÍM |
| -110 | ARP·mobil_ÉRTÉK·fogad_ÉRTÉK IDŐ_ÉRTÉK 초과 |

IP 주소는 상위 바이트부터 표기한 32비트 값이다. `10.0.2.2`는 `0x0a000202`이다. 주소를 반환하는 함수는 kódolás_ÉRTÉK 있는 Java `int`의 bit_ÉRTÉK 패턴을 사용하므로 상위 비트가 1인 informatikai_részleg_normál IP 주소가 음수로 보일 szám 있다. 단순히 모든 API 반환값의 부호를 오류로 판단하면 안 된다.

## végrehajt_parancs 경계와 시스템 호출

```text
felület run → JKAP에서 ELF ellenőriz·적재 → ring 3 felhasználó app_f5044b9b
                                 ↓ int 0x80
                      mutató 검사 → Java kernel_ÉRTÉK API → RTL8139/UDP
                                 ↓ kilép_app·kivétel·IDŐ_ÉRTÉK 초과
                                felület 복귀
```

시스템 호출 레지스터는 `EAX=INDEX`, `EBX,ECX,EDX,ESI,EDI=Argumentumok`, `EAX=KR`다. Java 호출 operandus_Sor ABI는 컴파일러가 felhasználó 스텁에서 이 형식으로 바꾼다. C의 POSIX/JNI ABI가 아니다.

| INDEX | 호출 |
| --- | --- |
| 0 | kilép_app(Állapot_ÉRTÉK KÓD_ÉRTÉK) — Futtatás/HIBA 런타임에서 használ_ÉRTÉK |
| 1 | sztring_ÉRTÉK Írás |
| 2 / 3 | Argumentumok cikk_DARAB / Argumentumok sztring_ÉRTÉK CÍM |
| 10 | UDP Megnyitás |
| 11 | UDP küld(leíró_ÉRTÉK, IP, cél_ÉRTÉK port_ÉRTÉK, TÖMB_ÉRTÉK CÍM, hossz_ÉRTÉK) |
| 12 | UDP fogad(leíró_ÉRTÉK, TÖMB_ÉRTÉK CÍM, 제한 밀리초) |
| 13 | UDP Bezárás |
| 14 | helyi_hatókör IP CÍM |
| 15 / 16 | 마지막 társ_ÉRTÉK IP / UDP port_ÉRTÉK |
| 20 | RAM Fájl Olvasás(Név int[] CÍM, Kimenet int[] CÍM) |
| 21 | RAM Fájl Írás(Név int[] CÍM, bevitel_ÉRTÉK int[] CÍM, bájt_ÉRTÉK hossz_ÉRTÉK) |
| 22 | UTF-16 KÓD_ÉRTÉK lecke_ÉRTÉK 문자 Kimenet(0~65535) |

Fájl API는 `felhasználó.파일읽기(int[] Név, int[] adat)`와 `felhasználó.ír_Fájl(int[] Név, int[] adat, int hossz_ÉRTÉK)`다. 이름은 ASCII KÓD_ÉRTÉK TÖMB_ÉRTÉK(최대 64칸, 0 kilép_app 또는 TÖMB_ÉRTÉK 끝), adat cikk_elem 하나는 한 바이트다. 반환값은 읽거나 쓴 길이이며 Fájl 없음 `-2`, mutató HIBA `-14`, Név/hossz_ÉRTÉK HIBA `-22`, Fájl tárolóhely_ÉRTÉK 부족 `-28`, Méret 초과 `-90`을 반환한다. 쓰기는 ellenőriz 후 Fájl 전체를 대체한다. `felhasználó.ír_karakter_ÉRTÉK(int)`는 문자를 단말에 출력한다. Java 프로그램의 일반 `java.io` 구현은 아니다.

`végrehajtás_engedély()`은 시스템 호출이 아니라 felhasználó 모드에서 CS의 하위 비트를 직접 읽으므로 tényleges_adat végrehajt_parancs 권한을 확인한다. kernel_ÉRTÉK hardver_port 접근용 `mobil_ÉRTÉK` native 함수는 felhasználó cél 컴파일에서 거부한다. ELF에 직접 특권 명령을 넣더라도 CPU가 차단한다.

## 범위와 제한

- 한 번에 한 프로그램만 실행하며 완료 후 셸로 돌아온다. 백그라운드 végrehajt_parancs, 파이프, 프로세스 간 통신은 없다. végrehajt_parancs 파일은 커널의 Olvasás 전용 JKAP 묶음에서 적재한다. adat 파일에는 주기억 파일체계와 전용 IDE 보존 형식이 있다.
- felhasználó 가상 CÍM `0x04000000..0x043fffff`를 물리 8~12MiB에 연결한다. végrehajt_parancs 영상은 elülső_kamera_ÉRTÉK 2MiB, 인수는 `0x04300000`부터, 스택은 régió_ÉRTÉK 끝에서 시작한다. kernel_ÉRTÉK identity 페이지는 supervisor 전용이다.
- 실행마다 4MiB felhasználó 영역을 비우고 Fájl 구역을 복사해 BSS·TÖMB_ÉRTÉK 영역을 초기화한다. felhasználó GC는 없지만 kilép_app 후 Tovább_cikk végrehajt_parancs 때 영역을 재사용한다. 인수는 공백으로 분리한 최대 16개이며 Idézet/이스케이프 파싱은 없다.
- felhasználó 페이지의 KÓD_ÉRTÉK/adat 분리 Olvasás 전용 Beállítások, NX, operandus_Sor guard, ASLR은 아직 없다. 커널과 felhasználó Memória_adat·hardver_port engedély_ÉRTÉK 경계를 구현한 초기판이지 보안 인증된 샌드박스는 아니다.
- PIT 100Hz로 약 3초 végrehajt_parancs 상한을 두며 IDŐ_ÉRTÉK 초과는 `Exit: 124`다. felhasználó CPU 예외는 `128 + kivétel INDEX`(페이지 HIBA 142, 특권 위반 141), Java TÖMB_ÉRTÉK/계산 오류는 101~105다. kernel_ÉRTÉK 오류까지 복구하는 구조는 아니다.
- 네트워크는 PCI bus 0/function 0의 RTL8139, statikus_ÉRTÉK IPv4, ARP, UDP만 지원한다. NIC는 폴링하고 송신은 동기식이다. IPv4 단편 재조립·TCP·DNS·DHCP·IPv6·HTTP·TLS·일반 `java.net`은 미지원이다. IPv4 UDP ellenőrzőösszeg 0은 규약에 따라 허용하고, 그 외 UDP/IP 검사합과 길이는 검증한다.
- felhasználó végrehajt_parancs·네트워크·véd_ÉRTÉK határ_ÉRTÉK 전체 시험은 QEMU에서 수행했다. VirtualBox에서도 `make vbox`로 부팅과 `run hello vbox`의 ring 3 végrehajt_parancs·informatikai_részleg_normál 종료를 확인했다. VirtualBox PCnet/E1000용 드라이버는 없어 그 환경의 네트워크는 지원하지 않는다.

## ellenőriz 근거

`make test`는 fordítóprogram 14개 시험, Java 패킷 állapot 2,201개 검사, 기존 felület ELF/ISO 부팅 시험, felhasználó ELF/tényleges_adat UDP/véd_ÉRTÉK határ_ÉRTÉK 시험을 실행한다. 네트워크 시험은 루프백 서버가 받은 자료의 hossz_ÉRTÉK·해시까지 `os/build/teszt_felhasználó_hálózat.json`에 기록한다. 시험용 손상된 ELF·특권 Parancs·무한 futam_ÉRTÉK 프로그램은 임시 묶음에만 넣으며 배포용 `apps` 목록에는 넣지 않는다.

참고한 일차 adat: [Intel 시스템 프로그래밍 명세](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), [QEMU RTL8139 구현](https://github.com/qemu/qemu/blob/master/hw/net/rtl8139.c), [QEMU 네트워크 fontos_fájl_eb81d7d9](https://www.qemu.org/docs/master/system/devices/net.html), [IPv4 RFC 791](https://www.rfc-editor.org/rfc/rfc791), [ARP RFC 826](https://www.rfc-editor.org/rfc/rfc826), [UDP RFC 768](https://www.rfc-editor.org/rfc/rfc768).
