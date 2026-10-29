// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package EMzantsi_Afrika.JZafOS.ikheneli;

import EMzantsi_Afrika.JZafOS.기억공간.imemori_umphathi;
import EMzantsi_Afrika.JZafOS.기억공간.ikhasi_umphathi;
import EMzantsi_Afrika.JZafOS.입력.입력관리자;
import EMzantsi_Afrika.JZafOS.작업.Inkqubo_ixabiso;
import EMzantsi_Afrika.JZafOS.작업.배정기;
import EMzantsi_Afrika.JZafOS.체계호출.체계호출;
import EMzantsi_Afrika.JZafOS.uhlobo_loseto_lwefayile.파일서술자표;
import EMzantsi_Afrika.JZafOS.uhlobo_loseto_lwefayile.uhlobo_loseto_lwefayile;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class ikheneli {
    private final 하드웨어 isixhobo_ixabiso;
    private final imemori_umphathi 기억공간 = new imemori_umphathi(32 * 1024 * 1024);
    private final ikhasi_umphathi 쪽관리 = new ikhasi_umphathi();
    private final uhlobo_loseto_lwefayile uhlobo_loseto_lwefayile = new uhlobo_loseto_lwefayile();
    private final 배정기 배정기 = new 배정기(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final Inkqubo_ixabiso 첫과정;
    private final 체계호출 체계호출;

    public ikheneli(하드웨어 isixhobo_ixabiso) {
        this.isixhobo_ixabiso = isixhobo_ixabiso;
        첫과정 = 배정기.첫과정(new 파일서술자표(uhlobo_loseto_lwefayile));
        체계호출 = new 체계호출(uhlobo_loseto_lwefayile, 쪽관리, 배정기, isixhobo_ixabiso, 입력관리);
    }

    public void Phumeza() {
        isixhobo_ixabiso.직렬출력("=== JZafOS 관리 ikheneli_ixabiso ===\n");
    }

    public void 한단계실행() {
        isixhobo_ixabiso.중앙처리장치멈춤();
    }

    public imemori_umphathi 기억공간() {
        return 기억공간;
    }

    public ikhasi_umphathi 쪽관리() {
        return 쪽관리;
    }

    public uhlobo_loseto_lwefayile uhlobo_loseto_lwefayile() {
        return uhlobo_loseto_lwefayile;
    }

    public 배정기 배정기() {
        return 배정기;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public Inkqubo_ixabiso 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
