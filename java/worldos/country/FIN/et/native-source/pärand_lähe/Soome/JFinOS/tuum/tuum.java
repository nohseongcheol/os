// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Soome.JFinOS.tuum;

import Soome.JFinOS.Mälu_regioon.기억공간관리자;
import Soome.JFinOS.Mälu_regioon.쪽관리자;
import Soome.JFinOS.입력.입력관리자;
import Soome.JFinOS.작업.Joonis_VALUE;
import Soome.JFinOS.작업.plaanija;
import Soome.JFinOS.체계호출.체계호출;
import Soome.JFinOS.failisüsteem.파일서술자표;
import Soome.JFinOS.failisüsteem.failisüsteem;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class tuum {
    private final 하드웨어 seade_VALUE;
    private final 기억공간관리자 Mälu_regioon = new 기억공간관리자(32 * 1024 * 1024);
    private final 쪽관리자 쪽관리 = new 쪽관리자();
    private final failisüsteem failisüsteem = new failisüsteem();
    private final plaanija plaanija = new plaanija(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final Joonis_VALUE 첫과정;
    private final 체계호출 체계호출;

    public tuum(하드웨어 seade_VALUE) {
        this.seade_VALUE = seade_VALUE;
        첫과정 = plaanija.첫과정(new 파일서술자표(failisüsteem));
        체계호출 = new 체계호출(failisüsteem, 쪽관리, plaanija, seade_VALUE, 입력관리);
    }

    public void Käivita_2() {
        seade_VALUE.직렬출력("=== JFinOS 관리 tuum_VALUE ===\n");
    }

    public void Täida_samm() {
        seade_VALUE.중앙처리장치멈춤();
    }

    public 기억공간관리자 Mälu_regioon() {
        return Mälu_regioon;
    }

    public 쪽관리자 쪽관리() {
        return 쪽관리;
    }

    public failisüsteem failisüsteem() {
        return failisüsteem;
    }

    public plaanija plaanija() {
        return plaanija;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public Joonis_VALUE 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
