// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Israel.JIsrOS.nucleu;

import Israel.JIsrOS.Memorie_regiune.기억공간관리자;
import Israel.JIsrOS.Memorie_regiune.쪽관리자;
import Israel.JIsrOS.입력.입력관리자;
import Israel.JIsrOS.작업.Proces_VALUE;
import Israel.JIsrOS.작업.Planificator;
import Israel.JIsrOS.체계호출.체계호출;
import Israel.JIsrOS.sistem_de_fișiere.파일서술자표;
import Israel.JIsrOS.sistem_de_fișiere.sistem_de_fișiere;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class nucleu {
    private final 하드웨어 mobil_VALUE;
    private final 기억공간관리자 Memorie_regiune = new 기억공간관리자(32 * 1024 * 1024);
    private final 쪽관리자 쪽관리 = new 쪽관리자();
    private final sistem_de_fișiere sistem_de_fișiere = new sistem_de_fișiere();
    private final Planificator Planificator = new Planificator(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final Proces_VALUE 첫과정;
    private final 체계호출 체계호출;

    public nucleu(하드웨어 mobil_VALUE) {
        this.mobil_VALUE = mobil_VALUE;
        첫과정 = Planificator.첫과정(new 파일서술자표(sistem_de_fișiere));
        체계호출 = new 체계호출(sistem_de_fișiere, 쪽관리, Planificator, mobil_VALUE, 입력관리);
    }

    public void Pornește() {
        mobil_VALUE.직렬출력("=== JIsrOS 관리 nucleu_VALUE ===\n");
    }

    public void executa_pas() {
        mobil_VALUE.중앙처리장치멈춤();
    }

    public 기억공간관리자 Memorie_regiune() {
        return Memorie_regiune;
    }

    public 쪽관리자 쪽관리() {
        return 쪽관리;
    }

    public sistem_de_fișiere sistem_de_fișiere() {
        return sistem_de_fișiere;
    }

    public Planificator Planificator() {
        return Planificator;
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
