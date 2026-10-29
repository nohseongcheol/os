// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Eýran.JIrnOS.ýadro;

import Eýran.JIrnOS.기억공간.ýat_iş_dolandyryjy;
import Eýran.JIrnOS.기억공간.sahypa_iş_dolandyryjy;
import Eýran.JIrnOS.입력.입력관리자;
import Eýran.JIrnOS.작업.Proses_baha;
import Eýran.JIrnOS.작업.배정기;
import Eýran.JIrnOS.체계호출.체계호출;
import Eýran.JIrnOS.faýl_ulgamy.파일서술자표;
import Eýran.JIrnOS.faýl_ulgamy.faýl_ulgamy;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class ýadro {
    private final 하드웨어 enjam_baha;
    private final ýat_iş_dolandyryjy 기억공간 = new ýat_iş_dolandyryjy(32 * 1024 * 1024);
    private final sahypa_iş_dolandyryjy 쪽관리 = new sahypa_iş_dolandyryjy();
    private final faýl_ulgamy faýl_ulgamy = new faýl_ulgamy();
    private final 배정기 배정기 = new 배정기(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final Proses_baha 첫과정;
    private final 체계호출 체계호출;

    public ýadro(하드웨어 enjam_baha) {
        this.enjam_baha = enjam_baha;
        첫과정 = 배정기.첫과정(new 파일서술자표(faýl_ulgamy));
        체계호출 = new 체계호출(faýl_ulgamy, 쪽관리, 배정기, enjam_baha, 입력관리);
    }

    public void Bitir() {
        enjam_baha.직렬출력("=== JIrnOS 관리 ýadro_baha ===\n");
    }

    public void 한단계실행() {
        enjam_baha.중앙처리장치멈춤();
    }

    public ýat_iş_dolandyryjy 기억공간() {
        return 기억공간;
    }

    public sahypa_iş_dolandyryjy 쪽관리() {
        return 쪽관리;
    }

    public faýl_ulgamy faýl_ulgamy() {
        return faýl_ulgamy;
    }

    public 배정기 배정기() {
        return 배정기;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public Proses_baha 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
