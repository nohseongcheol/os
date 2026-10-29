// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Senegaal.JSenOS.aaluude;

import Senegaal.JSenOS.기억공간.teskordu_kisnoowo;
import Senegaal.JSenOS.기억공간.hello_kisnoowo;
import Senegaal.JSenOS.입력.입력관리자;
import Senegaal.JSenOS.작업.Yuɓɓo_golle_njaru;
import Senegaal.JSenOS.작업.배정기;
import Senegaal.JSenOS.체계호출.체계호출;
import Senegaal.JSenOS.yuɓɓo_piille.파일서술자표;
import Senegaal.JSenOS.yuɓɓo_piille.yuɓɓo_piille;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class aaluude {
    private final 하드웨어 kaɓirgal_njaru;
    private final teskordu_kisnoowo 기억공간 = new teskordu_kisnoowo(32 * 1024 * 1024);
    private final hello_kisnoowo 쪽관리 = new hello_kisnoowo();
    private final yuɓɓo_piille yuɓɓo_piille = new yuɓɓo_piille();
    private final 배정기 배정기 = new 배정기(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final Yuɓɓo_golle_njaru 첫과정;
    private final 체계호출 체계호출;

    public aaluude(하드웨어 kaɓirgal_njaru) {
        this.kaɓirgal_njaru = kaɓirgal_njaru;
        첫과정 = 배정기.첫과정(new 파일서술자표(yuɓɓo_piille));
        체계호출 = new 체계호출(yuɓɓo_piille, 쪽관리, 배정기, kaɓirgal_njaru, 입력관리);
    }

    public void huutoraade() {
        kaɓirgal_njaru.직렬출력("=== JSenOS 관리 aaluude_njaru ===\n");
    }

    public void 한단계실행() {
        kaɓirgal_njaru.중앙처리장치멈춤();
    }

    public teskordu_kisnoowo 기억공간() {
        return 기억공간;
    }

    public hello_kisnoowo 쪽관리() {
        return 쪽관리;
    }

    public yuɓɓo_piille yuɓɓo_piille() {
        return yuɓɓo_piille;
    }

    public 배정기 배정기() {
        return 배정기;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public Yuɓɓo_golle_njaru 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
