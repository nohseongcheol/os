// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Turska.JTurOS.jezgro;

import Turska.JTurOS.Memorija_oblast.Memorija_menadžer;
import Turska.JTurOS.Memorija_oblast.stranica_menadžer;
import Turska.JTurOS.입력.입력관리자;
import Turska.JTurOS.작업.Proces_VALUE;
import Turska.JTurOS.작업.Planer;
import Turska.JTurOS.체계호출.체계호출;
import Turska.JTurOS.sistem_datoteka.파일서술자표;
import Turska.JTurOS.sistem_datoteka.sistem_datoteka;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class jezgro {
    private final 하드웨어 uređaj_VALUE;
    private final Memorija_menadžer Memorija_oblast = new Memorija_menadžer(32 * 1024 * 1024);
    private final stranica_menadžer 쪽관리 = new stranica_menadžer();
    private final sistem_datoteka sistem_datoteka = new sistem_datoteka();
    private final Planer Planer = new Planer(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final Proces_VALUE 첫과정;
    private final 체계호출 체계호출;

    public jezgro(하드웨어 uređaj_VALUE) {
        this.uređaj_VALUE = uređaj_VALUE;
        첫과정 = Planer.첫과정(new 파일서술자표(sistem_datoteka));
        체계호출 = new 체계호출(sistem_datoteka, 쪽관리, Planer, uređaj_VALUE, 입력관리);
    }

    public void koristiti() {
        uređaj_VALUE.직렬출력("=== JTurOS 관리 jezgro_VALUE ===\n");
    }

    public void Izvrši_korak() {
        uređaj_VALUE.중앙처리장치멈춤();
    }

    public Memorija_menadžer Memorija_oblast() {
        return Memorija_oblast;
    }

    public stranica_menadžer 쪽관리() {
        return 쪽관리;
    }

    public sistem_datoteka sistem_datoteka() {
        return sistem_datoteka;
    }

    public Planer Planer() {
        return Planer;
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
