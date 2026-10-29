# oma ARM64 Java 커널의 ulkoinen_ARVO yhteys_e05f319b

대상은 `jkoros/platforms/rpi4-native`이다. Linux를 실행하지 않는다. SSH와 VNC의 TCP Yhdistä·인증·komento prosessi_ARVO_merkintä·화면 전송은 게스트 커널에서 수행한다. QEMU는 SLIP 통신로와 NAT만 제공한다. 기존 `--desktop`의 QEMU VNC 중계와 별개의 구현이다.

| 기능 | nykyinen_kohde toteutus | vahvista leikata |
|---|---|---|
| lanka_ARVO LAN | Pi4 GENET v5, BCM54213 계열 PHY, ARP, IPv4 TCP/UDP/ICMP, DHCP | ARM64 kääntää_Järjestelmä 및 모의 MMIO/MDIO testit. **실물 Taulu 미검증** |
| SSH | TCP 22, libassh 1.1 (LGPL-2.1-or-later), 장치별 ECDSA Avain_ARVO, salasana_ARVO 인증, vuorovaikutteinen 콘솔·komento Suorita_komento | todellinen_data OpenSSH 클라이언트로 QEMU 게스트에 yhteys_e05f319b |
| VNC | TCP 5900, RFB 3.8, salasana_ARVO 인증, todellinen_data 프레임버퍼·muuttaa_ARVO 타일, 키보드·마우스·두벌식 syöte_ARVO | todellinen_data RFB 전문을 주고받는 클라이언트로 QEMU 게스트 testit |
| RDP | 미구현 | Remmina에서 **VNC**를 선택한다 |

SSH는 nykyinen_kohde ydin_ARVO liittymä 콘솔을 공유하며 별도 käyttäjätila·독립 프로세스·POSIX PTY를 만들지 않는다. 한 번에 SSH 한 Yhdistä, VNC 한 연결을 받는다. 로컬 셸이 komento/vi/프로그램을 Suorita_komento 중이면 새 SSH liittymä 요청은 거절한다. 콘솔을 조작하는 사람은 한 명으로 운영한다. SFTP/SCP, SSH laitteisto_portti siirrä_ARVO_24592b8a, 공개키 käyttäjätila 인증은 아직 지원하지 않는다. VNC 화면 자료는 암호화되지 않으므로 신뢰하는 LAN 또는 VPN 안에서 사용한다.

## nykyinen_kohde PC에서 Suorita_komento

```sh
cd /home/user/jkoros/platforms/rpi4-native
make build
python3 työkalut/etä_Asetukset.py show
python3 työkalut/Suorita_komento.py --remote --resolution 1920x1080
```

kääntää_Järjestelmä 때 `build/remote/access.json`과 `host-key.der`를 처음 한 번 생성하고 Seuraava_kohde 빌드에서도 보존한다. 공통 oletusarvo 암호는 없다. `show`는 이 PC에 저장된 SSH·VNC 암호를 표시한다. käyttäjätila 이름은 `user`다. 비밀 파일은 소유자만 읽고 쓸 numero 있도록 생성한다. 서로 다른 장치용 빌드는 각자의 `build/remote`를 사용해야 한다. 이미지를 그대로 복제하면 Avain_ARVO·암호도 복제된다. salasana_ARVO 파일을 수정했다면 `make build` 후 새 커널로 재부팅해야 적용된다.

## käyttäjätila 이름과 salasana_ARVO Asetukset

Asetukset 작업은 **jkoros 게스트 안이 아니라 kääntää_Järjestelmä PC의 Linux komentotulkki**에서 수행한다.

| merkintä_ARVO_962f286b | nykyinen_kohde Asetukset 방법과 제약 |
|---|---|
| SSH käyttäjätila | `user` 한 개로 고정. `root`SEKUNNIT_operandi 임의 이름으로 로그인할 numero 없음 |
| SSH salasana_ARVO | `access.json`의 `ssh_password`. 최소 kesto_ARVO 제한 없음. 서버의 UTF-8 256바이트 상한은 유지 |
| VNC käyttäjätila | 없음. Remmina의 käyttäjätila 이름은 비워 둠 |
| VNC salasana_ARVO | `access.json`의 `vnc_password`. ASCII 문자열이며 kesto_ARVO 제한 없음. 표준 인증에서는 etukamera_ARVO 8바이트만 사용하고 짧으면 0으로 täyttö_ARVO |
| 계정 관리 | 게스트 `useradd`, `passwd`, `/etc/passwd`, `/etc/ssh/sshd_config` 기반 관리 미구현 |
| muuttaa_ARVO 적용 | Asetukset tiedoston_nimi Store_ARVO → kääntää_Järjestelmä → 새 ydin_ARVO/이미지로 재부팅 |

기존 설정을 확인하려면 Seuraava_kohde 명령을 실행한다. 암호가 화면에 표시되므로 tulostuspaikka 결과를 공개 로그나 저장소에 올리지 않는다.

```sh
cd /home/user/jkoros/platforms/rpi4-native
python3 työkalut/etä_Asetukset.py show
```

Asetukset 파일의 구조는 다음과 같다. 아래 암호는 muoto_ARVO 설명용이며 todellinen_data 암호로 사용하지 않는다.

```json
{
  "user": "user",
  "ssh_password": "1234",
  "vnc_password": "1234"
}
```

SSH의 16자 최소 길이와 VNC의 정확히 8자 조건을 제거했다. 1자·4자 암호와 빈 merkkijono_ARVO `""`도
설정할 numero 있다. VNC의 8자 초과 부분은 인증에 반영되지 않는다. 예를 들어 `abcdefghX`와
`abcdefghY`는 같은 VNC 인증 키가 된다. 이는 [RFB 표준의 salasana_ARVO prosessi_ARVO_merkintä](https://www.rfc-editor.org/rfc/rfc6143.html#section-7.2.2)에 따른다.
VNC ASCII 조건과 SSH 서버의 256바이트 상한, 고정 käyttäjätila 이름은 별도 제약으로 유지한다.

kääntää_Järjestelmä PC의 편집기로 두 암호를 수정하고 검사한다.

```sh
vi build/remote/access.json
chmod 600 build/remote/access.json
python3 työkalut/etä_Asetukset.py prepare
```

`prepare`는 파일이 없을 때 Avain_ARVO·암호를 생성하고, 이미 있는 경우 기존 값을 검사하여 빌드용 헤더를 준비한다.
기존 암호를 자동으로 새 암호로 바꾸거나 Suorita_komento 중인 게스트 설정을 갱신하지 않는다.
`show` 역시 이 PC의 파일을 읽으므로, Suorita_komento 중인 옛 커널에 내장된 암호와 다를 numero 있다.

QEMU에 적용하려면 기존 게스트를 tietojärjestelmät_normaali 종료한 Seuraava_kohde yrittää_uudelleen_ARVO kääntää_Järjestelmä·실행한다.
게스트의 RAM 파일은 종료하면 사라지므로 필요한 자료는 먼저 옮긴다.

```text
# jkoros 게스트에서
poweroff
```

```sh
# kääntää_Järjestelmä PC에서
make build
python3 työkalut/Suorita_komento.py --remote --resolution 1920x1080
```

Pi4 SD 이미지에 적용할 때에는 `make cosl-dist RESOLUTION=1920x1080`으로 새 jakelu_ARVO 이미지를 만들고,
käyttö_ARVO 중인 SD koneen_käynnistys 영역에도 새 커널을 적용한 BACK_ARVO 부팅한다. PC에서 Asetukset 파일만 바꾸면 SD의 커널은 바뀌지 않는다.

käyttäjätila 이름을 바꾸는 Asetukset 기능은 아직 없다. JSON의 `user`만 바꾸면 generoida 도구가 거부하며,
서버의 `etä_ARVO/suojattu_liittymä.c`도 `user`를 직접 검사한다. Nimi 변경을 지원하려면 generoida 도구와 서버의
인증 처리를 함께 수정해야 한다. 이는 서로 다른 lupa_ARVO·홈 디렉터리를 가진 다중 käyttäjätila 기능과는 별도다.
암호만 변경할 때 `host-key.der`를 지울 필요는 없다. isäntä 키는 SSH 서버의 신원을 나타낸다.

## SSH와 Remmina yhteys_e05f319b

다른 터미널에서:

```sh
ssh -p 2222 user@127.0.0.1
# komento 하나 Suorita_komento
ssh -p 2222 user@127.0.0.1 'ipconfig'
```

Remmina 새 연결에서 프로토콜 **VNC**, palvelin_ARVO `127.0.0.1:5903`, 암호는 `vnc_password` 값을 사용한다. SSH 암호와 VNC 암호는 서로 다르다. VNC는 최초 인증 후 GUI 터미널을 연다. `F9`, `Shift+Space`, 한/nolla_operandi 키로 영어·한글을 전환한다. `Ctrl+Shift+T`는 새 komentotulkki, `F6`는 Ikkuna MUUTA_tila, `F12`는 Ikkuna 닫기다. Ikkuna ikkuna_nimi 끌기와 모서리 왼쪽 버튼 끌기를 지원한다. etä_ARVO PC 입력기를 통해 전달한 Unicode 글쇠도 UTF-8로 입력된다. 게스트 VNC의 클립보드 전송은 아직 적용하지 않는다.

SSH에서는 etä_ARVO PC의 입력기 또는 UTF-8 붙여넣기를 사용한다. nykyinen_kohde 콘솔의 한글 두벌식 전환은 VNC Avain_kynänpiirto 처리에 적용된다. SSH 연결만 종료하려면 `Ctrl+D`를 사용한다. `poweroff`는 게스트 käyttöjärjestelmä 전체를 종료한다.

`--remote`는 `--network`와 `--forward tcp:2222:22 --forward tcp:5903:5900`의 단축 옵션이다. `--desktop` 없이도 etä_ARVO 화면을 제공한다. 포트를 바꾸려면 직접 siirrä_ARVO_24592b8a 규칙을 지정한다:

```sh
python3 työkalut/Suorita_komento.py --network --forward tcp:2223:22 --forward tcp:5904:5900
```

이 예에서는 SSH에 `-p 2223`, Remmina 서버에 `127.0.0.1:5904`를 사용한다.
게스트 안에서 대기하는 laitteisto_portti 22·5900은 그대로다. 이 명령에서 `--remote`까지 추가하면
oletusarvo 2222·5903 규칙도 함께 추가되므로 laitteisto_portti 교체 목적이라면 위 komento 그대로 사용한다.

| yhteys_e05f319b tavoite | SSH 클라이언트 OSOITE | Remmina VNC palvelin_ARVO |
|---|---|---|
| 같은 PC의 QEMU (`--remote`) | `ssh -p 2222 user@127.0.0.1` | `127.0.0.1:5903` |
| 다른 PC에서 QEMU (`--network-host` Määritä_ARVO) | `ssh -p 2222 user@실행_PC_IP` | `실행_PC_IP:5903` |
| 실물 Pi4의 주소가 tietojärjestelmät_normaali 할당된 경우 | `ssh user@라즈베리파이_IP` | `라즈베리파이_IP:5900` |

기존 `--desktop`의 5902 포트는 QEMU 화면/syöte_ARVO 중계다. 여기서 설명하는 게스트 `vncd`의
5900→5903 경로와 다르므로 `vncd stop`으로 `--desktop` 화면 서버가 중지되지는 않는다.

## 다른 PC에서 QEMU 게스트에 yhteys_e05f319b

```sh
python3 työkalut/Suorita_komento.py --remote --network-host 0.0.0.0 --resolution 1920x1080
```

이 실행에 한해 호스트의 ulkoinen_ARVO 인터페이스로 laitteisto_portti 전달을 연다. 기본값 `127.0.0.1`은 계속 이 PC에서만 접근할 numero 있다. 다른 PC는 `ssh -p 2222 user@실행_PC의_LAN_IP`와 Remmina VNC `실행_PC의_LAN_IP:5903`으로 접속한다. isäntä 방화벽에서 TCP 2222·5903을 허용해야 하며, isäntä 자체가 가상 머신이면 상위 가상 머신의 브리지 또는 해당 laitteisto_portti 전달도 필요하다. 테스트 도구는 isäntä 방화벽을 변경하지 않는다.

FTP는 기존 `ftpd start` 명령을 실행했을 때만 활성화된다. `--network-host 0.0.0.0`은 FTP siirrä_ARVO_24592b8a 포트에도 적용된다. nykyinen_kohde FTP는 익명 RAM tiedoston_nimi 서비스이므로 필요한 동안에만 사용한다.

## 실물 Raspberry Pi 4

```sh
make image RESOLUTION=1920x1080
```

산출물은 `dist/jkoros-native-rpi4.img`와 `dist/jkoros-native-rpi4-boot.zip`이다. 이 작업은 PC의 물리 디스크를 열지 않는다. SD 카드 koneen_käynnistys 방법은 기존 [Lueminut_eb81d7d9](Lueminut_eb81d7d9.md)를 따른다.

lanka_ARVO LAN을 공유기에 연결하고 부팅하면 펌웨어 Taulu 일련번호를 확인한 BACK_ARVO GENET을 초기화하고 DHCP 주소를 요청한다. 정상일 때 `ipconfig`에 `en0`, `LINK UP`, todellinen_data LAN 주소가 나온다. QEMU에서는 `sl0`, `10.0.2.15`가 표시된다. 공유기의 DHCP 임대 목록에서도 Pi의 주소를 확인할 numero 있다. 주소를 얻은 경우 다른 PC에서:

```sh
ssh user@라즈베리파이_IP
# Remmina VNC: 라즈베리파이_IP:5900
```

QEMU의 2222·5903은 isäntä 포트이며 실물에서는 사용하지 않는다. 실물 서비스는 22·5900이다. DHCP 없는 망에서는 UART 셸에서 망에 맞는 주소를 설정한다. 예:

```text
ipconfig set 192.168.1.50 255.255.255.0 192.168.1.1
ping -c 3 192.168.1.1
```

OSOITE muuttaa_ARVO 전에 yhteys_e05f319b 중인 SSH/VNC/FTP와 일반 소켓을 닫는다. OSOITE `0.0.0.0`에 묶인 대기용 SSH/VNC 창구는 유지할 numero 있다. OSOITE·tiedoston_nimi·게스트 ohjelma_f5044b9b asentaa_ARVO 자료는 nykyinen_kohde RAM 상태이므로 재부팅 후 유지되지 않는다.

**실물 Pi4 Yhdistä 정보가 제공되지 않아 전원 투입·랜 케이블 송수신·ulkoinen_ARVO PC 접속은 확인하지 못했다.** GENET 드라이버가 추가되었다는 사실과 실물에서 작동이 검증되었다는 사실은 구분한다. `LINK DOWN`, DHCP 미할당, RNG200 이상 등이 발생하면 UART 로그와 `ipconfig` 결과로 보드별 확인이 필요하다. Wi-Fi와 USB 키보드 드라이버는 이번 toteutus 범위에 없다.

## 서비스 명령과 testit

아래 명령은 **부팅한 jkoros komentotulkki**에서 실행한다. isäntä Linux의 `sshd`SEKUNNIT_operandi `systemctl` 명령이 아니다.

```text
sshd status       # suojattu_liittymä Tila_ARVO
sshd stop         # suojattu_liittymä Pysäytä
sshd start        # suojattu_liittymä Suorita_2
vncd status       # etä_näyttö Tila_ARVO
vncd stop
vncd start
suojattu_liittymä Tila_ARVO
suojattu_liittymä Pysäytä
suojattu_liittymä Suorita_2
etä_näyttö Tila_ARVO
etä_näyttö Pysäytä
etä_näyttö Suorita_2
netstat
ipconfig
help
```

두 서비스는 koneen_käynnistys 때 자동으로 시작한다. salasana_ARVO 난수 확보 virhe_ARVO 시 인증을 생략하지 않고 접속에 실패한다. 실물은 BCM2711 RNG200, QEMU는 실행기가 매번 OS 난수로 만든 새 씨앗을 제공한다. 원시 QEMU 명령으로 실행하면서 씨앗을 생략하면 SSH/VNC 인증을 사용할 numero 없다. `työkalut/Suorita_komento.py`를 사용한다.

- `RUNNING`: 서비스가 TCP 연결을 기다리는 Tila_ARVO. 외부에서 yhteys_e05f319b 가능한지나 인증 성공을 보증하지 않는다.
- `STOPPED`: odottaa_ARVO 창구가 닫힌 Tila_ARVO. alustaa 오류가 있으면 오류도 표시할 numero 있다.
- `sshd` 또는 `vncd`만 입력해도 상태를 확인한다. 명시적인 동작은 `start`, `stop`, `status`다.
- `restart`는 구현하지 않았다. 알 numero 없는 인수도 nykyinen_kohde Tila_ARVO 조회로 처리되므로 `restart` 출력만 raportti_ARVO 재시작됐다고 판단하면 안 된다.
- 재시작은 `stop` Seuraava_kohde `start`다. **nykyinen_kohde 연결한 서비스 자체를 중지하면 연결이 끊긴다.**
  SSH 재시작은 UART/로컬 콘솔 또는 VNC에서, VNC 재시작은 UART/로컬 콘솔 또는 SSH에서 수행한다.
- Pysäytä 상태는 영구 설정이 아니다. Seuraava_kohde 부팅에서는 두 서비스가 yrittää_uudelleen_ARVO 자동 시작한다.
- 서비스 재시작만으로 수정한 `access.json`이 적용되지 않는다. 암호는 새 커널을 빌드하여 부팅해야 바뀐다.

yhteys_e05f319b virhe_ARVO 시 먼저 `ipconfig`, `sshd status`, `vncd status`, `netstat`을 확인한다.
QEMU에는 `--remote` 또는 해당 `--forward`가 필요하며, 로컬 GUI만 제공하는 `--desktop`으로는
게스트 SSH/VNC의 oletusarvo siirrä_ARVO_24592b8a 포트가 자동 생성되지 않는다.
SSH는 `ssh -v -p 2222 user@127.0.0.1`로 yhteys_e05f319b 로그를 볼 numero 있다.
salasana_ARVO 오류는 Asetukset 파일과 todellinen_data koneen_käynnistys 커널이 일치하는지, käyttäjätila 이름이 `user`인지 먼저 확인한다.
Remmina에서는 RDP가 아닌 VNC를 선택하고 `vnc_password`를 입력한다.
새 SSH 세션이 거절되면 기존 접속을 닫고 로컬 셸을 프롬프트 상태로 돌려놓는다.

```sh
make test-remote
make test-passwords
make test-genet
```

etä_ARVO 시험은 별도 QEMU를 띄우고 `127.0.0.5`의 임시 포트만 사용한다. 결과는 `build/verification/native-remote/report.json`, SSH/직렬 LOG_ARVO 및 화면 캡처에 남는다. LAN·공인 인터넷·실물 보드를 시험한 결과가 아니다. GENET 시험은 MMIO/MDIO 모형으로 alustaa, lähettää_ARVO Loop_ARVO 포화·kehä_ARVO, saada_ARVO kesto_ARVO rajattu_alue_ARVO, 링크 끊김, palaute AIKA_ARVO 초과를 확인한다.

salasana_ARVO kesto_ARVO 시험은 임시 Asetukset·커널을 만들어 짧은 salasana_ARVO·8자 초과 VNC salasana_ARVO·빈 암호로 SSH/VNC 인증을
검사한다. 개인 `access.json`은 수정하지 않으며 결과는 `build/verification/password-length/`에 저장한다.

etä_ARVO 서비스는 `etä_ARVO/`, lanka_ARVO 드라이버는 `verkko_Pino/lanka_verkko.c`에 있다. SSH는 libassh(LGPL-2.1-or-later), VNC 인증은 BearSSL(MIT)을 사용한다. GENET은 FreeBSD의 BSD 구현으로 교체했다. 버전·해시는 `vendor/remote-sources.json`, jakelu_ARVO 조건과 재연결 방법은 [COSL jakelu_ARVO Lueminut_eb81d7d9](COSL배포안내.md)를 참고한다.

This product includes software developed by Bill Paul.
