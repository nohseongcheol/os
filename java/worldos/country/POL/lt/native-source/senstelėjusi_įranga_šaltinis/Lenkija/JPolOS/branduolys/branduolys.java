// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lenkija.JPolOS.branduolys;

import Lenkija.JPolOS.atmintis_sritis.기억공간관리자;
import Lenkija.JPolOS.atmintis_sritis.쪽관리자;
import Lenkija.JPolOS.입력.입력관리자;
import Lenkija.JPolOS.작업.Procesas_VALUE;
import Lenkija.JPolOS.작업.planuotojas;
import Lenkija.JPolOS.체계호출.체계호출;
import Lenkija.JPolOS.failų_sistema.파일서술자표;
import Lenkija.JPolOS.failų_sistema.failų_sistema;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class branduolys {
    private final aparatūra_VALUE įrenginys_VALUE;
    private final 기억공간관리자 atmintis_sritis = new 기억공간관리자(32 * 1024 * 1024);
    private final 쪽관리자 쪽관리 = new 쪽관리자();
    private final failų_sistema failų_sistema = new failų_sistema();
    private final planuotojas planuotojas = new planuotojas(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final Procesas_VALUE 첫과정;
    private final 체계호출 체계호출;

    public branduolys(aparatūra_VALUE įrenginys_VALUE) {
        this.įrenginys_VALUE = įrenginys_VALUE;
        첫과정 = planuotojas.첫과정(new 파일서술자표(failų_sistema));
        체계호출 = new 체계호출(failų_sistema, 쪽관리, planuotojas, įrenginys_VALUE, 입력관리);
    }

    public void Paleisti() {
        įrenginys_VALUE.직렬출력("=== JPolOS 관리 branduolys_VALUE ===\n");
    }

    public void Vykdyti_veiksmas() {
        įrenginys_VALUE.중앙처리장치멈춤();
    }

    public 기억공간관리자 atmintis_sritis() {
        return atmintis_sritis;
    }

    public 쪽관리자 쪽관리() {
        return 쪽관리;
    }

    public failų_sistema failų_sistema() {
        return failų_sistema;
    }

    public planuotojas planuotojas() {
        return planuotojas;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public Procesas_VALUE 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
