// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Oʻzbekiston.JUzbOS.o_zak;

import Oʻzbekiston.JUzbOS.기억공간.Xotira_menejer;
import Oʻzbekiston.JUzbOS.기억공간.sahifa_menejer;
import Oʻzbekiston.JUzbOS.입력.입력관리자;
import Oʻzbekiston.JUzbOS.작업.Jarayon_VALUE;
import Oʻzbekiston.JUzbOS.작업.Jadval_tuzuvchi;
import Oʻzbekiston.JUzbOS.체계호출.체계호출;
import Oʻzbekiston.JUzbOS.fayllar_tizimi.파일서술자표;
import Oʻzbekiston.JUzbOS.fayllar_tizimi.fayllar_tizimi;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class o_zak {
    private final 하드웨어 qurilma_VALUE;
    private final Xotira_menejer 기억공간 = new Xotira_menejer(32 * 1024 * 1024);
    private final sahifa_menejer 쪽관리 = new sahifa_menejer();
    private final fayllar_tizimi fayllar_tizimi = new fayllar_tizimi();
    private final Jadval_tuzuvchi Jadval_tuzuvchi = new Jadval_tuzuvchi(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final Jarayon_VALUE 첫과정;
    private final 체계호출 체계호출;

    public o_zak(하드웨어 qurilma_VALUE) {
        this.qurilma_VALUE = qurilma_VALUE;
        첫과정 = Jadval_tuzuvchi.첫과정(new 파일서술자표(fayllar_tizimi));
        체계호출 = new 체계호출(fayllar_tizimi, 쪽관리, Jadval_tuzuvchi, qurilma_VALUE, 입력관리);
    }

    public void Bajarish() {
        qurilma_VALUE.직렬출력("=== JUzbOS 관리 o_zak_VALUE ===\n");
    }

    public void 한단계실행() {
        qurilma_VALUE.중앙처리장치멈춤();
    }

    public Xotira_menejer 기억공간() {
        return 기억공간;
    }

    public sahifa_menejer 쪽관리() {
        return 쪽관리;
    }

    public fayllar_tizimi fayllar_tizimi() {
        return fayllar_tizimi;
    }

    public Jadval_tuzuvchi Jadval_tuzuvchi() {
        return Jadval_tuzuvchi;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public Jarayon_VALUE 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
