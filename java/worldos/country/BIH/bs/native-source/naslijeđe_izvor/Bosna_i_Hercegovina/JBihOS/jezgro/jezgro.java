// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Bosna_i_Hercegovina.JBihOS.jezgro;

import Bosna_i_Hercegovina.JBihOS.기억공간.Memorija_menadžer;
import Bosna_i_Hercegovina.JBihOS.기억공간.stranica_menadžer;
import Bosna_i_Hercegovina.JBihOS.입력.입력관리자;
import Bosna_i_Hercegovina.JBihOS.작업.proces_VALUE;
import Bosna_i_Hercegovina.JBihOS.작업.Planer;
import Bosna_i_Hercegovina.JBihOS.체계호출.체계호출;
import Bosna_i_Hercegovina.JBihOS.fajl_sistem.파일서술자표;
import Bosna_i_Hercegovina.JBihOS.fajl_sistem.fajl_sistem;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class jezgro {
    private final hardver_VALUE uređaj_VALUE;
    private final Memorija_menadžer 기억공간 = new Memorija_menadžer(32 * 1024 * 1024);
    private final stranica_menadžer 쪽관리 = new stranica_menadžer();
    private final fajl_sistem fajl_sistem = new fajl_sistem();
    private final Planer Planer = new Planer(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final proces_VALUE 첫과정;
    private final 체계호출 체계호출;

    public jezgro(hardver_VALUE uređaj_VALUE) {
        this.uređaj_VALUE = uređaj_VALUE;
        첫과정 = Planer.첫과정(new 파일서술자표(fajl_sistem));
        체계호출 = new 체계호출(fajl_sistem, 쪽관리, Planer, uređaj_VALUE, 입력관리);
    }

    public void Pokreni() {
        uređaj_VALUE.직렬출력("=== JBihOS 관리 jezgro_VALUE ===\n");
    }

    public void 한단계실행() {
        uređaj_VALUE.중앙처리장치멈춤();
    }

    public Memorija_menadžer 기억공간() {
        return 기억공간;
    }

    public stranica_menadžer 쪽관리() {
        return 쪽관리;
    }

    public fajl_sistem fajl_sistem() {
        return fajl_sistem;
    }

    public Planer Planer() {
        return Planer;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public proces_VALUE 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
