// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package COL.JColOS.keetnerü;

import COL.JColOS.기억공간.기억공간관리자;
import COL.JColOS.기억공간.쪽관리자;
import COL.JColOS.입력.입력관리자;
import COL.JColOS.작업.과정;
import COL.JColOS.작업.배정기;
import COL.JColOS.체계호출.체계호출;
import COL.JColOS.a_yatawaajiraaya_anaajaalaairua.파일서술자표;
import COL.JColOS.a_yatawaajiraaya_anaajaalaairua.a_yatawaajiraaya_anaajaalaairua;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class keetnerü {
    private final 하드웨어 serulaalü_ajutuu;
    private final 기억공간관리자 기억공간 = new 기억공간관리자(32 * 1024 * 1024);
    private final 쪽관리자 쪽관리 = new 쪽관리자();
    private final a_yatawaajiraaya_anaajaalaairua a_yatawaajiraaya_anaajaalaairua = new a_yatawaajiraaya_anaajaalaairua();
    private final 배정기 배정기 = new 배정기(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final 과정 첫과정;
    private final 체계호출 체계호출;

    public keetnerü(하드웨어 serulaalü_ajutuu) {
        this.serulaalü_ajutuu = serulaalü_ajutuu;
        첫과정 = 배정기.첫과정(new 파일서술자표(a_yatawaajiraaya_anaajaalaairua));
        체계호출 = new 체계호출(a_yatawaajiraaya_anaajaalaairua, 쪽관리, 배정기, serulaalü_ajutuu, 입력관리);
    }

    public void 시작() {
        serulaalü_ajutuu.직렬출력("=== JColOS 관리 keetnerü_ajutuu ===\n");
    }

    public void 한단계실행() {
        serulaalü_ajutuu.중앙처리장치멈춤();
    }

    public 기억공간관리자 기억공간() {
        return 기억공간;
    }

    public 쪽관리자 쪽관리() {
        return 쪽관리;
    }

    public a_yatawaajiraaya_anaajaalaairua a_yatawaajiraaya_anaajaalaairua() {
        return a_yatawaajiraaya_anaajaalaairua;
    }

    public 배정기 배정기() {
        return 배정기;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public 과정 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
