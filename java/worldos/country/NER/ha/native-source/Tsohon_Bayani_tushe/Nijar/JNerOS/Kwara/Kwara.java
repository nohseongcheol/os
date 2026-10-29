// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nijar.JNerOS.Kwara;

import Nijar.JNerOS.기억공간.Mahardatar_kwamfuta_Manaja;
import Nijar.JNerOS.기억공간.shafi_Manaja;
import Nijar.JNerOS.입력.입력관리자;
import Nijar.JNerOS.작업.haryar_aikin_na_ura_Daraja;
import Nijar.JNerOS.작업.배정기;
import Nijar.JNerOS.체계호출.체계호출;
import Nijar.JNerOS.tsarin_fayil_a_kwamfuta.파일서술자표;
import Nijar.JNerOS.tsarin_fayil_a_kwamfuta.tsarin_fayil_a_kwamfuta;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class Kwara {
    private final kayan_haɗi_na_kwamfuta_Daraja na_ura_Daraja;
    private final Mahardatar_kwamfuta_Manaja 기억공간 = new Mahardatar_kwamfuta_Manaja(32 * 1024 * 1024);
    private final shafi_Manaja 쪽관리 = new shafi_Manaja();
    private final tsarin_fayil_a_kwamfuta tsarin_fayil_a_kwamfuta = new tsarin_fayil_a_kwamfuta();
    private final 배정기 배정기 = new 배정기(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final haryar_aikin_na_ura_Daraja 첫과정;
    private final 체계호출 체계호출;

    public Kwara(kayan_haɗi_na_kwamfuta_Daraja na_ura_Daraja) {
        this.na_ura_Daraja = na_ura_Daraja;
        첫과정 = 배정기.첫과정(new 파일서술자표(tsarin_fayil_a_kwamfuta));
        체계호출 = new 체계호출(tsarin_fayil_a_kwamfuta, 쪽관리, 배정기, na_ura_Daraja, 입력관리);
    }

    public void Tafiyar_da() {
        na_ura_Daraja.직렬출력("=== JNerOS 관리 Kwara_Daraja ===\n");
    }

    public void 한단계실행() {
        na_ura_Daraja.중앙처리장치멈춤();
    }

    public Mahardatar_kwamfuta_Manaja 기억공간() {
        return 기억공간;
    }

    public shafi_Manaja 쪽관리() {
        return 쪽관리;
    }

    public tsarin_fayil_a_kwamfuta tsarin_fayil_a_kwamfuta() {
        return tsarin_fayil_a_kwamfuta;
    }

    public 배정기 배정기() {
        return 배정기;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public haryar_aikin_na_ura_Daraja 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
