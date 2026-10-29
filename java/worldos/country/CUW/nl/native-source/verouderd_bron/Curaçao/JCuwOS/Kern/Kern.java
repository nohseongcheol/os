// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Curaçao.JCuwOS.Kern;

import Curaçao.JCuwOS.Geheugen_regio.Geheugen_Manager;
import Curaçao.JCuwOS.Geheugen_regio.Paginabeheer;
import Curaçao.JCuwOS.invoer_WAARDE.invoer_Manager;
import Curaçao.JCuwOS.작업.Proces_WAARDE;
import Curaçao.JCuwOS.작업.Planner;
import Curaçao.JCuwOS.systeemaanroep.systeemaanroep;
import Curaçao.JCuwOS.bestandssysteem.파일서술자표;
import Curaçao.JCuwOS.bestandssysteem.bestandssysteem;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class Kern {
    private final hardware_WAARDE mobiel_WAARDE;
    private final Geheugen_Manager Geheugen_regio = new Geheugen_Manager(32 * 1024 * 1024);
    private final Paginabeheer 쪽관리 = new Paginabeheer();
    private final bestandssysteem bestandssysteem = new bestandssysteem();
    private final Planner Planner = new Planner(쪽관리);
    private final invoer_Manager 입력관리 = new invoer_Manager(256);
    private final Proces_WAARDE 첫과정;
    private final systeemaanroep systeemaanroep;

    public Kern(hardware_WAARDE mobiel_WAARDE) {
        this.mobiel_WAARDE = mobiel_WAARDE;
        첫과정 = Planner.첫과정(new 파일서술자표(bestandssysteem));
        systeemaanroep = new systeemaanroep(bestandssysteem, 쪽관리, Planner, mobiel_WAARDE, 입력관리);
    }

    public void starten() {
        mobiel_WAARDE.직렬출력("=== JCuwOS 관리 kernel_WAARDE ===\n");
    }

    public void Uitvoeren_stap() {
        mobiel_WAARDE.중앙처리장치멈춤();
    }

    public Geheugen_Manager Geheugen_regio() {
        return Geheugen_regio;
    }

    public Paginabeheer 쪽관리() {
        return 쪽관리;
    }

    public bestandssysteem bestandssysteem() {
        return bestandssysteem;
    }

    public Planner Planner() {
        return Planner;
    }

    public invoer_Manager 입력관리() {
        return 입력관리;
    }

    public Proces_WAARDE 첫과정() {
        return 첫과정;
    }

    public systeemaanroep systeemaanroep() {
        return systeemaanroep;
    }
}
