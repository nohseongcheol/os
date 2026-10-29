// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Éire.JIrlOS.eithne;

import Éire.JIrlOS.기억공간.Cuimhne_bainisteoir;
import Éire.JIrlOS.기억공간.leathanach_bainisteoir;
import Éire.JIrlOS.입력.입력관리자;
import Éire.JIrlOS.작업.Próiseas_VALUE;
import Éire.JIrlOS.작업.Sceidealóir;
import Éire.JIrlOS.체계호출.체계호출;
import Éire.JIrlOS.córas_comhad.파일서술자표;
import Éire.JIrlOS.córas_comhad.córas_comhad;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class eithne {
    private final 하드웨어 gléas_VALUE;
    private final Cuimhne_bainisteoir 기억공간 = new Cuimhne_bainisteoir(32 * 1024 * 1024);
    private final leathanach_bainisteoir 쪽관리 = new leathanach_bainisteoir();
    private final córas_comhad córas_comhad = new córas_comhad();
    private final Sceidealóir Sceidealóir = new Sceidealóir(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final Próiseas_VALUE 첫과정;
    private final 체계호출 체계호출;

    public eithne(하드웨어 gléas_VALUE) {
        this.gléas_VALUE = gléas_VALUE;
        첫과정 = Sceidealóir.첫과정(new 파일서술자표(córas_comhad));
        체계호출 = new 체계호출(córas_comhad, 쪽관리, Sceidealóir, gléas_VALUE, 입력관리);
    }

    public void Rith_2() {
        gléas_VALUE.직렬출력("=== JIrlOS 관리 eithne_VALUE ===\n");
    }

    public void 한단계실행() {
        gléas_VALUE.중앙처리장치멈춤();
    }

    public Cuimhne_bainisteoir 기억공간() {
        return 기억공간;
    }

    public leathanach_bainisteoir 쪽관리() {
        return 쪽관리;
    }

    public córas_comhad córas_comhad() {
        return córas_comhad;
    }

    public Sceidealóir Sceidealóir() {
        return Sceidealóir;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public Próiseas_VALUE 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
