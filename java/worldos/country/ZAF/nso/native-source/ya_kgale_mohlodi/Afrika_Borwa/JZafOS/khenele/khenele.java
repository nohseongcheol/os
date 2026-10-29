// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Afrika_Borwa.JZafOS.khenele;

import Afrika_Borwa.JZafOS.기억공간.memori_molaodi;
import Afrika_Borwa.JZafOS.기억공간.letlakala_molaodi;
import Afrika_Borwa.JZafOS.입력.입력관리자;
import Afrika_Borwa.JZafOS.작업.tiragalo_boleng;
import Afrika_Borwa.JZafOS.작업.배정기;
import Afrika_Borwa.JZafOS.체계호출.체계호출;
import Afrika_Borwa.JZafOS.tshepedišo_ya_difaele.파일서술자표;
import Afrika_Borwa.JZafOS.tshepedišo_ya_difaele.tshepedišo_ya_difaele;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class khenele {
    private final 하드웨어 sedirišwa_boleng;
    private final memori_molaodi 기억공간 = new memori_molaodi(32 * 1024 * 1024);
    private final letlakala_molaodi 쪽관리 = new letlakala_molaodi();
    private final tshepedišo_ya_difaele tshepedišo_ya_difaele = new tshepedišo_ya_difaele();
    private final 배정기 배정기 = new 배정기(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final tiragalo_boleng 첫과정;
    private final 체계호출 체계호출;

    public khenele(하드웨어 sedirišwa_boleng) {
        this.sedirišwa_boleng = sedirišwa_boleng;
        첫과정 = 배정기.첫과정(new 파일서술자표(tshepedišo_ya_difaele));
        체계호출 = new 체계호출(tshepedišo_ya_difaele, 쪽관리, 배정기, sedirišwa_boleng, 입력관리);
    }

    public void Diriša() {
        sedirišwa_boleng.직렬출력("=== JZafOS 관리 khenele_boleng ===\n");
    }

    public void 한단계실행() {
        sedirišwa_boleng.중앙처리장치멈춤();
    }

    public memori_molaodi 기억공간() {
        return 기억공간;
    }

    public letlakala_molaodi 쪽관리() {
        return 쪽관리;
    }

    public tshepedišo_ya_difaele tshepedišo_ya_difaele() {
        return tshepedišo_ya_difaele;
    }

    public 배정기 배정기() {
        return 배정기;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public tiragalo_boleng 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
