// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Y_Deyrnas_Unedig.JGbrOS.cnewyllyn;

import Y_Deyrnas_Unedig.JGbrOS.기억공간.Cof_rheolwr;
import Y_Deyrnas_Unedig.JGbrOS.기억공간.tudalen_rheolwr;
import Y_Deyrnas_Unedig.JGbrOS.입력.입력관리자;
import Y_Deyrnas_Unedig.JGbrOS.작업.Proses_VALUE;
import Y_Deyrnas_Unedig.JGbrOS.작업.Trefnwr;
import Y_Deyrnas_Unedig.JGbrOS.체계호출.체계호출;
import Y_Deyrnas_Unedig.JGbrOS.system_ffeiliau.파일서술자표;
import Y_Deyrnas_Unedig.JGbrOS.system_ffeiliau.system_ffeiliau;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class cnewyllyn {
    private final 하드웨어 dyfais_VALUE;
    private final Cof_rheolwr 기억공간 = new Cof_rheolwr(32 * 1024 * 1024);
    private final tudalen_rheolwr 쪽관리 = new tudalen_rheolwr();
    private final system_ffeiliau system_ffeiliau = new system_ffeiliau();
    private final Trefnwr Trefnwr = new Trefnwr(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final Proses_VALUE 첫과정;
    private final 체계호출 체계호출;

    public cnewyllyn(하드웨어 dyfais_VALUE) {
        this.dyfais_VALUE = dyfais_VALUE;
        첫과정 = Trefnwr.첫과정(new 파일서술자표(system_ffeiliau));
        체계호출 = new 체계호출(system_ffeiliau, 쪽관리, Trefnwr, dyfais_VALUE, 입력관리);
    }

    public void Gweithredu_2() {
        dyfais_VALUE.직렬출력("=== JGbrOS 관리 cnewyllyn_VALUE ===\n");
    }

    public void 한단계실행() {
        dyfais_VALUE.중앙처리장치멈춤();
    }

    public Cof_rheolwr 기억공간() {
        return 기억공간;
    }

    public tudalen_rheolwr 쪽관리() {
        return 쪽관리;
    }

    public system_ffeiliau system_ffeiliau() {
        return system_ffeiliau;
    }

    public Trefnwr Trefnwr() {
        return Trefnwr;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public Proses_VALUE 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
