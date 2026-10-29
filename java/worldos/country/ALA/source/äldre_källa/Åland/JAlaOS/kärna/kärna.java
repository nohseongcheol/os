// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Åland.JAlaOS.kärna;

import Åland.JAlaOS.Minne_område.Minne_Ansvarig;
import Åland.JAlaOS.Minne_område.Sidhanteraren;
import Åland.JAlaOS.indata_värde.indata_Ansvarig;
import Åland.JAlaOS.작업.Process_värde;
import Åland.JAlaOS.작업.Scheduler;
import Åland.JAlaOS.systemanrop.systemanrop;
import Åland.JAlaOS.filsystem.파일서술자표;
import Åland.JAlaOS.filsystem.filsystem;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class kärna {
    private final maskinvara_värde enhet_värde;
    private final Minne_Ansvarig Minne_område = new Minne_Ansvarig(32 * 1024 * 1024);
    private final Sidhanteraren 쪽관리 = new Sidhanteraren();
    private final filsystem filsystem = new filsystem();
    private final Scheduler Scheduler = new Scheduler(쪽관리);
    private final indata_Ansvarig 입력관리 = new indata_Ansvarig(256);
    private final Process_värde 첫과정;
    private final systemanrop systemanrop;

    public kärna(maskinvara_värde enhet_värde) {
        this.enhet_värde = enhet_värde;
        첫과정 = Scheduler.첫과정(new 파일서술자표(filsystem));
        systemanrop = new systemanrop(filsystem, 쪽관리, Scheduler, enhet_värde, 입력관리);
    }

    public void Kör() {
        enhet_värde.직렬출력("=== JAlaOS 관리 kärna_värde ===\n");
    }

    public void köra_steg() {
        enhet_värde.중앙처리장치멈춤();
    }

    public Minne_Ansvarig Minne_område() {
        return Minne_område;
    }

    public Sidhanteraren 쪽관리() {
        return 쪽관리;
    }

    public filsystem filsystem() {
        return filsystem;
    }

    public Scheduler Scheduler() {
        return Scheduler;
    }

    public indata_Ansvarig 입력관리() {
        return 입력관리;
    }

    public Process_värde 첫과정() {
        return 첫과정;
    }

    public systemanrop systemanrop() {
        return systemanrop;
    }
}
