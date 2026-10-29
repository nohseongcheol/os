// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Česko.JCzeOS.jádro;

import Česko.JCzeOS.Paměť_oblast.Paměť_Správce;
import Česko.JCzeOS.Paměť_oblast.stránka_Správce;
import Česko.JCzeOS.vstup_HODNOTA.vstup_Správce;
import Česko.JCzeOS.작업.Proces_HODNOTA;
import Česko.JCzeOS.작업.Plánovač;
import Česko.JCzeOS.systémové_volání.systémové_volání;
import Česko.JCzeOS.systém_souborů.Soubor_popisovač_tabulka;
import Česko.JCzeOS.systém_souborů.systém_souborů;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class jádro {
    private final hardware_HODNOTA mobilní_HODNOTA;
    private final Paměť_Správce Paměť_oblast = new Paměť_Správce(32 * 1024 * 1024);
    private final stránka_Správce 쪽관리 = new stránka_Správce();
    private final systém_souborů systém_souborů = new systém_souborů();
    private final Plánovač Plánovač = new Plánovač(쪽관리);
    private final vstup_Správce 입력관리 = new vstup_Správce(256);
    private final Proces_HODNOTA 첫과정;
    private final systémové_volání systémové_volání;

    public jádro(hardware_HODNOTA mobilní_HODNOTA) {
        this.mobilní_HODNOTA = mobilní_HODNOTA;
        첫과정 = Plánovač.첫과정(new Soubor_popisovač_tabulka(systém_souborů));
        systémové_volání = new systémové_volání(systém_souborů, 쪽관리, Plánovač, mobilní_HODNOTA, 입력관리);
    }

    public void Spustit_2() {
        mobilní_HODNOTA.직렬출력("=== JCzeOS 관리 jádro_HODNOTA ===\n");
    }

    public void Provést_krok() {
        mobilní_HODNOTA.중앙처리장치멈춤();
    }

    public Paměť_Správce Paměť_oblast() {
        return Paměť_oblast;
    }

    public stránka_Správce 쪽관리() {
        return 쪽관리;
    }

    public systém_souborů systém_souborů() {
        return systém_souborů;
    }

    public Plánovač Plánovač() {
        return Plánovač;
    }

    public vstup_Správce 입력관리() {
        return 입력관리;
    }

    public Proces_HODNOTA 첫과정() {
        return 첫과정;
    }

    public systémové_volání systémové_volání() {
        return systémové_volání;
    }
}
