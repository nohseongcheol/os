// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Senegaal.JSenOS.xoox;

import Senegaal.JSenOS.기억공간.fatlekookaay_doxalkat;
import Senegaal.JSenOS.기억공간.xët_doxalkat;
import Senegaal.JSenOS.입력.입력관리자;
import Senegaal.JSenOS.작업.yokkute_xëyma;
import Senegaal.JSenOS.작업.배정기;
import Senegaal.JSenOS.체계호출.체계호출;
import Senegaal.JSenOS.barabu_boolebdenc_yu_ñu_bennal.파일서술자표;
import Senegaal.JSenOS.barabu_boolebdenc_yu_ñu_bennal.barabu_boolebdenc_yu_ñu_bennal;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class xoox {
    private final jumtukaay_xëyma toftal_xëyma;
    private final fatlekookaay_doxalkat 기억공간 = new fatlekookaay_doxalkat(32 * 1024 * 1024);
    private final xët_doxalkat 쪽관리 = new xët_doxalkat();
    private final barabu_boolebdenc_yu_ñu_bennal barabu_boolebdenc_yu_ñu_bennal = new barabu_boolebdenc_yu_ñu_bennal();
    private final 배정기 배정기 = new 배정기(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final yokkute_xëyma 첫과정;
    private final 체계호출 체계호출;

    public xoox(jumtukaay_xëyma toftal_xëyma) {
        this.toftal_xëyma = toftal_xëyma;
        첫과정 = 배정기.첫과정(new 파일서술자표(barabu_boolebdenc_yu_ñu_bennal));
        체계호출 = new 체계호출(barabu_boolebdenc_yu_ñu_bennal, 쪽관리, 배정기, toftal_xëyma, 입력관리);
    }

    public void daw() {
        toftal_xëyma.직렬출력("=== JSenOS 관리 xoox_xëyma ===\n");
    }

    public void 한단계실행() {
        toftal_xëyma.중앙처리장치멈춤();
    }

    public fatlekookaay_doxalkat 기억공간() {
        return 기억공간;
    }

    public xët_doxalkat 쪽관리() {
        return 쪽관리;
    }

    public barabu_boolebdenc_yu_ñu_bennal barabu_boolebdenc_yu_ñu_bennal() {
        return barabu_boolebdenc_yu_ñu_bennal;
    }

    public 배정기 배정기() {
        return 배정기;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public yokkute_xëyma 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
