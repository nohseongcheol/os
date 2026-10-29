// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package COD.JCodOS.intima;

import COD.JCodOS.기억공간.ububiko_Umugenzuzi;
import COD.JCodOS.기억공간.paji_Umugenzuzi;
import COD.JCodOS.입력.입력관리자;
import COD.JCodOS.작업.Inzira_agaciro;
import COD.JCodOS.작업.배정기;
import COD.JCodOS.체계호출.체계호출;
import COD.JCodOS.sisitemu_ya_dosiye.파일서술자표;
import COD.JCodOS.sisitemu_ya_dosiye.sisitemu_ya_dosiye;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class intima {
    private final 하드웨어 igendanwa_agaciro;
    private final ububiko_Umugenzuzi 기억공간 = new ububiko_Umugenzuzi(32 * 1024 * 1024);
    private final paji_Umugenzuzi 쪽관리 = new paji_Umugenzuzi();
    private final sisitemu_ya_dosiye sisitemu_ya_dosiye = new sisitemu_ya_dosiye();
    private final 배정기 배정기 = new 배정기(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final Inzira_agaciro 첫과정;
    private final 체계호출 체계호출;

    public intima(하드웨어 igendanwa_agaciro) {
        this.igendanwa_agaciro = igendanwa_agaciro;
        첫과정 = 배정기.첫과정(new 파일서술자표(sisitemu_ya_dosiye));
        체계호출 = new 체계호출(sisitemu_ya_dosiye, 쪽관리, 배정기, igendanwa_agaciro, 입력관리);
    }

    public void ihuriro() {
        igendanwa_agaciro.직렬출력("=== JCodOS 관리 intima_agaciro ===\n");
    }

    public void 한단계실행() {
        igendanwa_agaciro.중앙처리장치멈춤();
    }

    public ububiko_Umugenzuzi 기억공간() {
        return 기억공간;
    }

    public paji_Umugenzuzi 쪽관리() {
        return 쪽관리;
    }

    public sisitemu_ya_dosiye sisitemu_ya_dosiye() {
        return sisitemu_ya_dosiye;
    }

    public 배정기 배정기() {
        return 배정기;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public Inzira_agaciro 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
