// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovensko.JSvkOS.jadro;

import Slovensko.JSvkOS.Pamäť_oblasť.기억공간관리자;
import Slovensko.JSvkOS.Pamäť_oblasť.쪽관리자;
import Slovensko.JSvkOS.vstup_VALUE.입력관리자;
import Slovensko.JSvkOS.작업.Proces_VALUE;
import Slovensko.JSvkOS.작업.Plánovač;
import Slovensko.JSvkOS.체계호출.체계호출;
import Slovensko.JSvkOS.systém_súborov.파일서술자표;
import Slovensko.JSvkOS.systém_súborov.systém_súborov;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class jadro {
    private final hardvér_VALUE telefón_VALUE;
    private final 기억공간관리자 Pamäť_oblasť = new 기억공간관리자(32 * 1024 * 1024);
    private final 쪽관리자 쪽관리 = new 쪽관리자();
    private final systém_súborov systém_súborov = new systém_súborov();
    private final Plánovač Plánovač = new Plánovač(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final Proces_VALUE 첫과정;
    private final 체계호출 체계호출;

    public jadro(hardvér_VALUE telefón_VALUE) {
        this.telefón_VALUE = telefón_VALUE;
        첫과정 = Plánovač.첫과정(new 파일서술자표(systém_súborov));
        체계호출 = new 체계호출(systém_súborov, 쪽관리, Plánovač, telefón_VALUE, 입력관리);
    }

    public void Spustiť_2() {
        telefón_VALUE.직렬출력("=== JSvkOS 관리 jadro_VALUE ===\n");
    }

    public void Vykonať_krok() {
        telefón_VALUE.중앙처리장치멈춤();
    }

    public 기억공간관리자 Pamäť_oblasť() {
        return Pamäť_oblasť;
    }

    public 쪽관리자 쪽관리() {
        return 쪽관리;
    }

    public systém_súborov systém_súborov() {
        return systém_súborov;
    }

    public Plánovač Plánovač() {
        return Plánovač;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public Proces_VALUE 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
