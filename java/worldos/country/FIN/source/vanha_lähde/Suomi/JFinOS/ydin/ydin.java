// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Suomi.JFinOS.ydin;

import Suomi.JFinOS.Muisti_alue.Muisti_Valvoja;
import Suomi.JFinOS.Muisti_alue.page_Valvoja;
import Suomi.JFinOS.syöte_ARVO.syöte_Valvoja;
import Suomi.JFinOS.작업.prosessi_ARVO;
import Suomi.JFinOS.작업.Aikataulutus;
import Suomi.JFinOS.järjestelmäkutsu.järjestelmäkutsu;
import Suomi.JFinOS.tiedostojärjestelmä.파일서술자표;
import Suomi.JFinOS.tiedostojärjestelmä.tiedostojärjestelmä;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class ydin {
    private final laitteisto_ARVO laite_ARVO;
    private final Muisti_Valvoja Muisti_alue = new Muisti_Valvoja(32 * 1024 * 1024);
    private final page_Valvoja 쪽관리 = new page_Valvoja();
    private final tiedostojärjestelmä tiedostojärjestelmä = new tiedostojärjestelmä();
    private final Aikataulutus Aikataulutus = new Aikataulutus(쪽관리);
    private final syöte_Valvoja 입력관리 = new syöte_Valvoja(256);
    private final prosessi_ARVO 첫과정;
    private final järjestelmäkutsu järjestelmäkutsu;

    public ydin(laitteisto_ARVO laite_ARVO) {
        this.laite_ARVO = laite_ARVO;
        첫과정 = Aikataulutus.첫과정(new 파일서술자표(tiedostojärjestelmä));
        järjestelmäkutsu = new järjestelmäkutsu(tiedostojärjestelmä, 쪽관리, Aikataulutus, laite_ARVO, 입력관리);
    }

    public void Suorita_2() {
        laite_ARVO.직렬출력("=== JFinOS 관리 ydin_ARVO ===\n");
    }

    public void Suorita_vaihe() {
        laite_ARVO.중앙처리장치멈춤();
    }

    public Muisti_Valvoja Muisti_alue() {
        return Muisti_alue;
    }

    public page_Valvoja 쪽관리() {
        return 쪽관리;
    }

    public tiedostojärjestelmä tiedostojärjestelmä() {
        return tiedostojärjestelmä;
    }

    public Aikataulutus Aikataulutus() {
        return Aikataulutus;
    }

    public syöte_Valvoja 입력관리() {
        return 입력관리;
    }

    public prosessi_ARVO 첫과정() {
        return 첫과정;
    }

    public järjestelmäkutsu järjestelmäkutsu() {
        return järjestelmäkutsu;
    }
}
