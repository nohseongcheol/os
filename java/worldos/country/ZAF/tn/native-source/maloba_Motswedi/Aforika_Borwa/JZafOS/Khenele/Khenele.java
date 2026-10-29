// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Aforika_Borwa.JZafOS.Khenele;

import Aforika_Borwa.JZafOS.기억공간.memori_motsamaisi;
import Aforika_Borwa.JZafOS.기억공간.tsebe_motsamaisi;
import Aforika_Borwa.JZafOS.입력.입력관리자;
import Aforika_Borwa.JZafOS.작업.Thulaganyo_Boleng;
import Aforika_Borwa.JZafOS.작업.배정기;
import Aforika_Borwa.JZafOS.체계호출.체계호출;
import Aforika_Borwa.JZafOS.setsamaisadifaele.파일서술자표;
import Aforika_Borwa.JZafOS.setsamaisadifaele.setsamaisadifaele;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class Khenele {
    private final 하드웨어 mobaele_Boleng;
    private final memori_motsamaisi 기억공간 = new memori_motsamaisi(32 * 1024 * 1024);
    private final tsebe_motsamaisi 쪽관리 = new tsebe_motsamaisi();
    private final setsamaisadifaele setsamaisadifaele = new setsamaisadifaele();
    private final 배정기 배정기 = new 배정기(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final Thulaganyo_Boleng 첫과정;
    private final 체계호출 체계호출;

    public Khenele(하드웨어 mobaele_Boleng) {
        this.mobaele_Boleng = mobaele_Boleng;
        첫과정 = 배정기.첫과정(new 파일서술자표(setsamaisadifaele));
        체계호출 = new 체계호출(setsamaisadifaele, 쪽관리, 배정기, mobaele_Boleng, 입력관리);
    }

    public void dirisa() {
        mobaele_Boleng.직렬출력("=== JZafOS 관리 Khenele_Boleng ===\n");
    }

    public void 한단계실행() {
        mobaele_Boleng.중앙처리장치멈춤();
    }

    public memori_motsamaisi 기억공간() {
        return 기억공간;
    }

    public tsebe_motsamaisi 쪽관리() {
        return 쪽관리;
    }

    public setsamaisadifaele setsamaisadifaele() {
        return setsamaisadifaele;
    }

    public 배정기 배정기() {
        return 배정기;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public Thulaganyo_Boleng 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
