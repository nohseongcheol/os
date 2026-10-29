// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Suid_Afrika.JZafOS.kern;

import Suid_Afrika.JZafOS.기억공간.Geheue_bestuurder;
import Suid_Afrika.JZafOS.기억공간.bladsy_bestuurder;
import Suid_Afrika.JZafOS.입력.입력관리자;
import Suid_Afrika.JZafOS.작업.Proses_VALUE;
import Suid_Afrika.JZafOS.작업.Skeduleerder;
import Suid_Afrika.JZafOS.체계호출.체계호출;
import Suid_Afrika.JZafOS.lêerstelsel.파일서술자표;
import Suid_Afrika.JZafOS.lêerstelsel.lêerstelsel;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class kern {
    private final hardeware_VALUE mobiel_VALUE;
    private final Geheue_bestuurder 기억공간 = new Geheue_bestuurder(32 * 1024 * 1024);
    private final bladsy_bestuurder 쪽관리 = new bladsy_bestuurder();
    private final lêerstelsel lêerstelsel = new lêerstelsel();
    private final Skeduleerder Skeduleerder = new Skeduleerder(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final Proses_VALUE 첫과정;
    private final 체계호출 체계호출;

    public kern(hardeware_VALUE mobiel_VALUE) {
        this.mobiel_VALUE = mobiel_VALUE;
        첫과정 = Skeduleerder.첫과정(new 파일서술자표(lêerstelsel));
        체계호출 = new 체계호출(lêerstelsel, 쪽관리, Skeduleerder, mobiel_VALUE, 입력관리);
    }

    public void Loop() {
        mobiel_VALUE.직렬출력("=== JZafOS 관리 kern_VALUE ===\n");
    }

    public void 한단계실행() {
        mobiel_VALUE.중앙처리장치멈춤();
    }

    public Geheue_bestuurder 기억공간() {
        return 기억공간;
    }

    public bladsy_bestuurder 쪽관리() {
        return 쪽관리;
    }

    public lêerstelsel lêerstelsel() {
        return lêerstelsel;
    }

    public Skeduleerder Skeduleerder() {
        return Skeduleerder;
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
