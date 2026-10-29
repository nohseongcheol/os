// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Malta.JMltOS.kernel;

import Malta.JMltOS.기억공간.Memorja_maniġer;
import Malta.JMltOS.기억공간.paġna_maniġer;
import Malta.JMltOS.입력.입력관리자;
import Malta.JMltOS.작업.Proċess_VALUE;
import Malta.JMltOS.작업.Skedatur;
import Malta.JMltOS.체계호출.체계호출;
import Malta.JMltOS.sistema_tal_fajls.파일서술자표;
import Malta.JMltOS.sistema_tal_fajls.sistema_tal_fajls;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class kernel {
    private final 하드웨어 mowbajl_VALUE;
    private final Memorja_maniġer 기억공간 = new Memorja_maniġer(32 * 1024 * 1024);
    private final paġna_maniġer 쪽관리 = new paġna_maniġer();
    private final sistema_tal_fajls sistema_tal_fajls = new sistema_tal_fajls();
    private final Skedatur Skedatur = new Skedatur(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final Proċess_VALUE 첫과정;
    private final 체계호출 체계호출;

    public kernel(하드웨어 mowbajl_VALUE) {
        this.mowbajl_VALUE = mowbajl_VALUE;
        첫과정 = Skedatur.첫과정(new 파일서술자표(sistema_tal_fajls));
        체계호출 = new 체계호출(sistema_tal_fajls, 쪽관리, Skedatur, mowbajl_VALUE, 입력관리);
    }

    public void serje() {
        mowbajl_VALUE.직렬출력("=== JMltOS 관리 kernel_VALUE ===\n");
    }

    public void 한단계실행() {
        mowbajl_VALUE.중앙처리장치멈춤();
    }

    public Memorja_maniġer 기억공간() {
        return 기억공간;
    }

    public paġna_maniġer 쪽관리() {
        return 쪽관리;
    }

    public sistema_tal_fajls sistema_tal_fajls() {
        return sistema_tal_fajls;
    }

    public Skedatur Skedatur() {
        return Skedatur;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public Proċess_VALUE 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
