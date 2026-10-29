// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Italija.JItaOS.jedro;

import Italija.JItaOS.pomnilnik_območje.pomnilnik_Upravitelj;
import Italija.JItaOS.pomnilnik_območje.stran_Upravitelj;
import Italija.JItaOS.입력.입력관리자;
import Italija.JItaOS.작업.Proces_VALUE;
import Italija.JItaOS.작업.Načrtovalec;
import Italija.JItaOS.체계호출.체계호출;
import Italija.JItaOS.datotečni_sistem.파일서술자표;
import Italija.JItaOS.datotečni_sistem.datotečni_sistem;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class jedro {
    private final strojna_oprema_VALUE naprava_VALUE;
    private final pomnilnik_Upravitelj pomnilnik_območje = new pomnilnik_Upravitelj(32 * 1024 * 1024);
    private final stran_Upravitelj 쪽관리 = new stran_Upravitelj();
    private final datotečni_sistem datotečni_sistem = new datotečni_sistem();
    private final Načrtovalec Načrtovalec = new Načrtovalec(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final Proces_VALUE 첫과정;
    private final 체계호출 체계호출;

    public jedro(strojna_oprema_VALUE naprava_VALUE) {
        this.naprava_VALUE = naprava_VALUE;
        첫과정 = Načrtovalec.첫과정(new 파일서술자표(datotečni_sistem));
        체계호출 = new 체계호출(datotečni_sistem, 쪽관리, Načrtovalec, naprava_VALUE, 입력관리);
    }

    public void Zaženi() {
        naprava_VALUE.직렬출력("=== JItaOS 관리 jedro_VALUE ===\n");
    }

    public void Izvedi_korak() {
        naprava_VALUE.중앙처리장치멈춤();
    }

    public pomnilnik_Upravitelj pomnilnik_območje() {
        return pomnilnik_območje;
    }

    public stran_Upravitelj 쪽관리() {
        return 쪽관리;
    }

    public datotečni_sistem datotečni_sistem() {
        return datotečni_sistem;
    }

    public Načrtovalec Načrtovalec() {
        return Načrtovalec;
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
