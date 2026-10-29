// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package An_Rìoghachd_Aonaichte.JGbrOS.eitean;

import An_Rìoghachd_Aonaichte.JGbrOS.기억공간.cuimhne_manaidsear;
import An_Rìoghachd_Aonaichte.JGbrOS.기억공간.duilleag_manaidsear;
import An_Rìoghachd_Aonaichte.JGbrOS.입력.입력관리자;
import An_Rìoghachd_Aonaichte.JGbrOS.작업.Pròiseas_VALUE;
import An_Rìoghachd_Aonaichte.JGbrOS.작업.sgeidealaiche;
import An_Rìoghachd_Aonaichte.JGbrOS.체계호출.체계호출;
import An_Rìoghachd_Aonaichte.JGbrOS.siostam_fhaidhlichean.파일서술자표;
import An_Rìoghachd_Aonaichte.JGbrOS.siostam_fhaidhlichean.siostam_fhaidhlichean;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class eitean {
    private final 하드웨어 uidheam_VALUE;
    private final cuimhne_manaidsear 기억공간 = new cuimhne_manaidsear(32 * 1024 * 1024);
    private final duilleag_manaidsear 쪽관리 = new duilleag_manaidsear();
    private final siostam_fhaidhlichean siostam_fhaidhlichean = new siostam_fhaidhlichean();
    private final sgeidealaiche sgeidealaiche = new sgeidealaiche(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final Pròiseas_VALUE 첫과정;
    private final 체계호출 체계호출;

    public eitean(하드웨어 uidheam_VALUE) {
        this.uidheam_VALUE = uidheam_VALUE;
        첫과정 = sgeidealaiche.첫과정(new 파일서술자표(siostam_fhaidhlichean));
        체계호출 = new 체계호출(siostam_fhaidhlichean, 쪽관리, sgeidealaiche, uidheam_VALUE, 입력관리);
    }

    public void ruith() {
        uidheam_VALUE.직렬출력("=== JGbrOS 관리 eitean_VALUE ===\n");
    }

    public void 한단계실행() {
        uidheam_VALUE.중앙처리장치멈춤();
    }

    public cuimhne_manaidsear 기억공간() {
        return 기억공간;
    }

    public duilleag_manaidsear 쪽관리() {
        return 쪽관리;
    }

    public siostam_fhaidhlichean siostam_fhaidhlichean() {
        return siostam_fhaidhlichean;
    }

    public sgeidealaiche sgeidealaiche() {
        return sgeidealaiche;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public Pròiseas_VALUE 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
