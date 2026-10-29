// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Bẹ̀nẹ̀.JBenOS.kánẹ́ẹ̀lì;

import Bẹ̀nẹ̀.JBenOS.기억공간.ibi_ìpamọ́_alákòóso;
import Bẹ̀nẹ̀.JBenOS.기억공간.ojú_ìwé_alákòóso;
import Bẹ̀nẹ̀.JBenOS.입력.입력관리자;
import Bẹ̀nẹ̀.JBenOS.작업.Ìlànà_iye;
import Bẹ̀nẹ̀.JBenOS.작업.배정기;
import Bẹ̀nẹ̀.JBenOS.체계호출.체계호출;
import Bẹ̀nẹ̀.JBenOS.ìlànà_ètò_fáìlì.파일서술자표;
import Bẹ̀nẹ̀.JBenOS.ìlànà_ètò_fáìlì.ìlànà_ètò_fáìlì;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class kánẹ́ẹ̀lì {
    private final ohun_èlò_alárídìmú_iye ohun_èlò_iye;
    private final ibi_ìpamọ́_alákòóso 기억공간 = new ibi_ìpamọ́_alákòóso(32 * 1024 * 1024);
    private final ojú_ìwé_alákòóso 쪽관리 = new ojú_ìwé_alákòóso();
    private final ìlànà_ètò_fáìlì ìlànà_ètò_fáìlì = new ìlànà_ètò_fáìlì();
    private final 배정기 배정기 = new 배정기(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final Ìlànà_iye 첫과정;
    private final 체계호출 체계호출;

    public kánẹ́ẹ̀lì(ohun_èlò_alárídìmú_iye ohun_èlò_iye) {
        this.ohun_èlò_iye = ohun_èlò_iye;
        첫과정 = 배정기.첫과정(new 파일서술자표(ìlànà_ètò_fáìlì));
        체계호출 = new 체계호출(ìlànà_ètò_fáìlì, 쪽관리, 배정기, ohun_èlò_iye, 입력관리);
    }

    public void Rọ́ọ̀nù() {
        ohun_èlò_iye.직렬출력("=== JBenOS 관리 kánẹ́ẹ̀lì_iye ===\n");
    }

    public void 한단계실행() {
        ohun_èlò_iye.중앙처리장치멈춤();
    }

    public ibi_ìpamọ́_alákòóso 기억공간() {
        return 기억공간;
    }

    public ojú_ìwé_alákòóso 쪽관리() {
        return 쪽관리;
    }

    public ìlànà_ètò_fáìlì ìlànà_ètò_fáìlì() {
        return ìlànà_ètò_fáìlì;
    }

    public 배정기 배정기() {
        return 배정기;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public Ìlànà_iye 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
