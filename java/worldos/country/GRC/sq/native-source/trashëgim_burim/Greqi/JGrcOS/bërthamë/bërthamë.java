// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Greqi.JGrcOS.bërthamë;

import Greqi.JGrcOS.기억공간.Memorie_menaxher;
import Greqi.JGrcOS.기억공간.faqe_menaxher;
import Greqi.JGrcOS.입력.입력관리자;
import Greqi.JGrcOS.작업.Proces_VALUE;
import Greqi.JGrcOS.작업.Planifikuesi;
import Greqi.JGrcOS.체계호출.체계호출;
import Greqi.JGrcOS.sistemi_i_skedarëve.파일서술자표;
import Greqi.JGrcOS.sistemi_i_skedarëve.sistemi_i_skedarëve;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class bërthamë {
    private final 하드웨어 pajisje_VALUE;
    private final Memorie_menaxher 기억공간 = new Memorie_menaxher(32 * 1024 * 1024);
    private final faqe_menaxher 쪽관리 = new faqe_menaxher();
    private final sistemi_i_skedarëve sistemi_i_skedarëve = new sistemi_i_skedarëve();
    private final Planifikuesi Planifikuesi = new Planifikuesi(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final Proces_VALUE 첫과정;
    private final 체계호출 체계호출;

    public bërthamë(하드웨어 pajisje_VALUE) {
        this.pajisje_VALUE = pajisje_VALUE;
        첫과정 = Planifikuesi.첫과정(new 파일서술자표(sistemi_i_skedarëve));
        체계호출 = new 체계호출(sistemi_i_skedarëve, 쪽관리, Planifikuesi, pajisje_VALUE, 입력관리);
    }

    public void Ekzekuto() {
        pajisje_VALUE.직렬출력("=== JGrcOS 관리 bërthamë_VALUE ===\n");
    }

    public void 한단계실행() {
        pajisje_VALUE.중앙처리장치멈춤();
    }

    public Memorie_menaxher 기억공간() {
        return 기억공간;
    }

    public faqe_menaxher 쪽관리() {
        return 쪽관리;
    }

    public sistemi_i_skedarëve sistemi_i_skedarëve() {
        return sistemi_i_skedarëve;
    }

    public Planifikuesi Planifikuesi() {
        return Planifikuesi;
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
