// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Msumbiji.JMozOS.kiini;

import Msumbiji.JMozOS.기억공간.kumbukumbu_msimamizi;
import Msumbiji.JMozOS.기억공간.ukurasa_msimamizi;
import Msumbiji.JMozOS.입력.입력관리자;
import Msumbiji.JMozOS.작업.Mchakato_thamani;
import Msumbiji.JMozOS.작업.배정기;
import Msumbiji.JMozOS.체계호출.체계호출;
import Msumbiji.JMozOS.mfumo_ya_mafaili.파일서술자표;
import Msumbiji.JMozOS.mfumo_ya_mafaili.mfumo_ya_mafaili;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class kiini {
    private final 하드웨어 kifaa_thamani;
    private final kumbukumbu_msimamizi 기억공간 = new kumbukumbu_msimamizi(32 * 1024 * 1024);
    private final ukurasa_msimamizi 쪽관리 = new ukurasa_msimamizi();
    private final mfumo_ya_mafaili mfumo_ya_mafaili = new mfumo_ya_mafaili();
    private final 배정기 배정기 = new 배정기(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final Mchakato_thamani 첫과정;
    private final 체계호출 체계호출;

    public kiini(하드웨어 kifaa_thamani) {
        this.kifaa_thamani = kifaa_thamani;
        첫과정 = 배정기.첫과정(new 파일서술자표(mfumo_ya_mafaili));
        체계호출 = new 체계호출(mfumo_ya_mafaili, 쪽관리, 배정기, kifaa_thamani, 입력관리);
    }

    public void endesha() {
        kifaa_thamani.직렬출력("=== JMozOS 관리 kiini_thamani_0611a8a8 ===\n");
    }

    public void 한단계실행() {
        kifaa_thamani.중앙처리장치멈춤();
    }

    public kumbukumbu_msimamizi 기억공간() {
        return 기억공간;
    }

    public ukurasa_msimamizi 쪽관리() {
        return 쪽관리;
    }

    public mfumo_ya_mafaili mfumo_ya_mafaili() {
        return mfumo_ya_mafaili;
    }

    public 배정기 배정기() {
        return 배정기;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public Mchakato_thamani 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
