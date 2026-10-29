// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Norge.JNorOS.kjerne;

import Norge.JNorOS.Minne_område.Minne_overordnet;
import Norge.JNorOS.Minne_område.Sidebehandling;
import Norge.JNorOS.inndata_VERDI.inndata_overordnet;
import Norge.JNorOS.작업.Prosess_VERDI;
import Norge.JNorOS.작업.Scheduler;
import Norge.JNorOS.체계호출.체계호출;
import Norge.JNorOS.filsystem.파일서술자표;
import Norge.JNorOS.filsystem.filsystem;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class kjerne {
    private final maskinvare_VERDI enhet_VERDI;
    private final Minne_overordnet Minne_område = new Minne_overordnet(32 * 1024 * 1024);
    private final Sidebehandling 쪽관리 = new Sidebehandling();
    private final filsystem filsystem = new filsystem();
    private final Scheduler Scheduler = new Scheduler(쪽관리);
    private final inndata_overordnet 입력관리 = new inndata_overordnet(256);
    private final Prosess_VERDI 첫과정;
    private final 체계호출 체계호출;

    public kjerne(maskinvare_VERDI enhet_VERDI) {
        this.enhet_VERDI = enhet_VERDI;
        첫과정 = Scheduler.첫과정(new 파일서술자표(filsystem));
        체계호출 = new 체계호출(filsystem, 쪽관리, Scheduler, enhet_VERDI, 입력관리);
    }

    public void Kjør_2() {
        enhet_VERDI.직렬출력("=== JNorOS 관리 kjerne_VERDI ===\n");
    }

    public void Utfør_trinn() {
        enhet_VERDI.중앙처리장치멈춤();
    }

    public Minne_overordnet Minne_område() {
        return Minne_område;
    }

    public Sidebehandling 쪽관리() {
        return 쪽관리;
    }

    public filsystem filsystem() {
        return filsystem;
    }

    public Scheduler Scheduler() {
        return Scheduler;
    }

    public inndata_overordnet 입력관리() {
        return 입력관리;
    }

    public Prosess_VERDI 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
