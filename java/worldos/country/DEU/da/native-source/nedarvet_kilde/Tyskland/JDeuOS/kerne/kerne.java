// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Tyskland.JDeuOS.kerne;

import Tyskland.JDeuOS.Hukommelse_område.Hukommelse_Leder;
import Tyskland.JDeuOS.Hukommelse_område.Sidestyring;
import Tyskland.JDeuOS.input_VÆRDI.input_Leder;
import Tyskland.JDeuOS.작업.Proces_VÆRDI;
import Tyskland.JDeuOS.작업.Scheduler;
import Tyskland.JDeuOS.체계호출.체계호출;
import Tyskland.JDeuOS.filsystem.파일서술자표;
import Tyskland.JDeuOS.filsystem.filsystem;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class kerne {
    private final hardware_VÆRDI enhed_VÆRDI;
    private final Hukommelse_Leder Hukommelse_område = new Hukommelse_Leder(32 * 1024 * 1024);
    private final Sidestyring 쪽관리 = new Sidestyring();
    private final filsystem filsystem = new filsystem();
    private final Scheduler Scheduler = new Scheduler(쪽관리);
    private final input_Leder 입력관리 = new input_Leder(256);
    private final Proces_VÆRDI 첫과정;
    private final 체계호출 체계호출;

    public kerne(hardware_VÆRDI enhed_VÆRDI) {
        this.enhed_VÆRDI = enhed_VÆRDI;
        첫과정 = Scheduler.첫과정(new 파일서술자표(filsystem));
        체계호출 = new 체계호출(filsystem, 쪽관리, Scheduler, enhed_VÆRDI, 입력관리);
    }

    public void Kør_2() {
        enhed_VÆRDI.직렬출력("=== JDeuOS 관리 kerne_VÆRDI ===\n");
    }

    public void Udfør_trin() {
        enhed_VÆRDI.중앙처리장치멈춤();
    }

    public Hukommelse_Leder Hukommelse_område() {
        return Hukommelse_område;
    }

    public Sidestyring 쪽관리() {
        return 쪽관리;
    }

    public filsystem filsystem() {
        return filsystem;
    }

    public Scheduler Scheduler() {
        return Scheduler;
    }

    public input_Leder 입력관리() {
        return 입력관리;
    }

    public Proces_VÆRDI 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
