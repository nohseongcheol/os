// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Singapura.JSgpOS.kernel;

import Singapura.JSgpOS.Memori_rantau.Memori_pengurus;
import Singapura.JSgpOS.Memori_rantau.halaman_pengurus;
import Singapura.JSgpOS.입력.입력관리자;
import Singapura.JSgpOS.작업.Proses_VALUE;
import Singapura.JSgpOS.작업.Penjadual;
import Singapura.JSgpOS.panggilan_sistem.panggilan_sistem;
import Singapura.JSgpOS.sistem_fail.파일서술자표;
import Singapura.JSgpOS.sistem_fail.sistem_fail;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class kernel {
    private final 하드웨어 peranti_VALUE;
    private final Memori_pengurus Memori_rantau = new Memori_pengurus(32 * 1024 * 1024);
    private final halaman_pengurus 쪽관리 = new halaman_pengurus();
    private final sistem_fail sistem_fail = new sistem_fail();
    private final Penjadual Penjadual = new Penjadual(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final Proses_VALUE 첫과정;
    private final panggilan_sistem panggilan_sistem;

    public kernel(하드웨어 peranti_VALUE) {
        this.peranti_VALUE = peranti_VALUE;
        첫과정 = Penjadual.첫과정(new 파일서술자표(sistem_fail));
        panggilan_sistem = new panggilan_sistem(sistem_fail, 쪽관리, Penjadual, peranti_VALUE, 입력관리);
    }

    public void Jalan() {
        peranti_VALUE.직렬출력("=== JSgpOS 관리 kernel_VALUE ===\n");
    }

    public void laksanakan_langkah() {
        peranti_VALUE.중앙처리장치멈춤();
    }

    public Memori_pengurus Memori_rantau() {
        return Memori_rantau;
    }

    public halaman_pengurus 쪽관리() {
        return 쪽관리;
    }

    public sistem_fail sistem_fail() {
        return sistem_fail;
    }

    public Penjadual Penjadual() {
        return Penjadual;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public Proses_VALUE 첫과정() {
        return 첫과정;
    }

    public panggilan_sistem panggilan_sistem() {
        return panggilan_sistem;
    }
}
