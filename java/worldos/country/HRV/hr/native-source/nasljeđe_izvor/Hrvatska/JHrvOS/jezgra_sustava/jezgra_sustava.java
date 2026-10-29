// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Hrvatska.JHrvOS.jezgra_sustava;

import Hrvatska.JHrvOS.Memorija_regije.Memorija_Upravitelj;
import Hrvatska.JHrvOS.Memorija_regije.dojaviti_Upravitelj;
import Hrvatska.JHrvOS.입력.입력관리자;
import Hrvatska.JHrvOS.작업.Proces_VALUE;
import Hrvatska.JHrvOS.작업.Alat_za_zakazivanje;
import Hrvatska.JHrvOS.체계호출.체계호출;
import Hrvatska.JHrvOS.datotečni_sustav.파일서술자표;
import Hrvatska.JHrvOS.datotečni_sustav.datotečni_sustav;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class jezgra_sustava {
    private final 하드웨어 uređaj_VALUE;
    private final Memorija_Upravitelj Memorija_regije = new Memorija_Upravitelj(32 * 1024 * 1024);
    private final dojaviti_Upravitelj 쪽관리 = new dojaviti_Upravitelj();
    private final datotečni_sustav datotečni_sustav = new datotečni_sustav();
    private final Alat_za_zakazivanje Alat_za_zakazivanje = new Alat_za_zakazivanje(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final Proces_VALUE 첫과정;
    private final 체계호출 체계호출;

    public jezgra_sustava(하드웨어 uređaj_VALUE) {
        this.uređaj_VALUE = uređaj_VALUE;
        첫과정 = Alat_za_zakazivanje.첫과정(new 파일서술자표(datotečni_sustav));
        체계호출 = new 체계호출(datotečni_sustav, 쪽관리, Alat_za_zakazivanje, uređaj_VALUE, 입력관리);
    }

    public void Pokreni() {
        uređaj_VALUE.직렬출력("=== JHrvOS 관리 jezgra_sustava_VALUE ===\n");
    }

    public void Izvrši_korak() {
        uređaj_VALUE.중앙처리장치멈춤();
    }

    public Memorija_Upravitelj Memorija_regije() {
        return Memorija_regije;
    }

    public dojaviti_Upravitelj 쪽관리() {
        return 쪽관리;
    }

    public datotečni_sustav datotečni_sustav() {
        return datotečni_sustav;
    }

    public Alat_za_zakazivanje Alat_za_zakazivanje() {
        return Alat_za_zakazivanje;
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
