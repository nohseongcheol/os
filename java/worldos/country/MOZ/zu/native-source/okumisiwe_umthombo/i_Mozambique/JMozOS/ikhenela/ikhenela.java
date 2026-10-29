// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package i_Mozambique.JMozOS.ikhenela;

import i_Mozambique.JMozOS.기억공간.inkumbulo_imeneja;
import i_Mozambique.JMozOS.기억공간.ikhasi_imeneja;
import i_Mozambique.JMozOS.입력.입력관리자;
import i_Mozambique.JMozOS.작업.Inqubo_inani;
import i_Mozambique.JMozOS.작업.배정기;
import i_Mozambique.JMozOS.체계호출.체계호출;
import i_Mozambique.JMozOS.isistimu_yefayela.파일서술자표;
import i_Mozambique.JMozOS.isistimu_yefayela.isistimu_yefayela;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class ikhenela {
    private final 하드웨어 idivayisi_inani;
    private final inkumbulo_imeneja 기억공간 = new inkumbulo_imeneja(32 * 1024 * 1024);
    private final ikhasi_imeneja 쪽관리 = new ikhasi_imeneja();
    private final isistimu_yefayela isistimu_yefayela = new isistimu_yefayela();
    private final 배정기 배정기 = new 배정기(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final Inqubo_inani 첫과정;
    private final 체계호출 체계호출;

    public ikhenela(하드웨어 idivayisi_inani) {
        this.idivayisi_inani = idivayisi_inani;
        첫과정 = 배정기.첫과정(new 파일서술자표(isistimu_yefayela));
        체계호출 = new 체계호출(isistimu_yefayela, 쪽관리, 배정기, idivayisi_inani, 입력관리);
    }

    public void Sebenzisa() {
        idivayisi_inani.직렬출력("=== JMozOS 관리 ikhenela_inani ===\n");
    }

    public void 한단계실행() {
        idivayisi_inani.중앙처리장치멈춤();
    }

    public inkumbulo_imeneja 기억공간() {
        return 기억공간;
    }

    public ikhasi_imeneja 쪽관리() {
        return 쪽관리;
    }

    public isistimu_yefayela isistimu_yefayela() {
        return isistimu_yefayela;
    }

    public 배정기 배정기() {
        return 배정기;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public Inqubo_inani 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
