// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ᑲᓇᑕᒥ.JCanOS.kernel;

import ᑲᓇᑕᒥ.JCanOS.기억공간.puigujjaikkut_aulattiji;
import ᑲᓇᑕᒥ.JCanOS.기억공간.mappigaq_aulattiji;
import ᑲᓇᑕᒥ.JCanOS.입력.입력관리자;
import ᑲᓇᑕᒥ.JCanOS.작업.Pivallianiq_atuutilik;
import ᑲᓇᑕᒥ.JCanOS.작업.배정기;
import ᑲᓇᑕᒥ.JCanOS.체계호출.체계호출;
import ᑲᓇᑕᒥ.JCanOS.inikkuvik.파일서술자표;
import ᑲᓇᑕᒥ.JCanOS.inikkuvik.inikkuvik;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class kernel {
    private final 하드웨어 sunakkutaaq_atuutilik;
    private final puigujjaikkut_aulattiji 기억공간 = new puigujjaikkut_aulattiji(32 * 1024 * 1024);
    private final mappigaq_aulattiji 쪽관리 = new mappigaq_aulattiji();
    private final inikkuvik inikkuvik = new inikkuvik();
    private final 배정기 배정기 = new 배정기(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final Pivallianiq_atuutilik 첫과정;
    private final 체계호출 체계호출;

    public kernel(하드웨어 sunakkutaaq_atuutilik) {
        this.sunakkutaaq_atuutilik = sunakkutaaq_atuutilik;
        첫과정 = 배정기.첫과정(new 파일서술자표(inikkuvik));
        체계호출 = new 체계호출(inikkuvik, 쪽관리, 배정기, sunakkutaaq_atuutilik, 입력관리);
    }

    public void 시작() {
        sunakkutaaq_atuutilik.직렬출력("=== JCanOS 관리 kernel_atuutilik ===\n");
    }

    public void 한단계실행() {
        sunakkutaaq_atuutilik.중앙처리장치멈춤();
    }

    public puigujjaikkut_aulattiji 기억공간() {
        return 기억공간;
    }

    public mappigaq_aulattiji 쪽관리() {
        return 쪽관리;
    }

    public inikkuvik inikkuvik() {
        return inikkuvik;
    }

    public 배정기 배정기() {
        return 배정기;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public Pivallianiq_atuutilik 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
