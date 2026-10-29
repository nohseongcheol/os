// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ශ්_රී_ලංකාව.JLkaOS.කර්නලය;

import ශ්_රී_ලංකාව.JLkaOS.기억공간.මතකය_කළමනාකරු;
import ශ්_රී_ලංකාව.JLkaOS.기억공간.පිටුව_කළමනාකරු;
import ශ්_රී_ලංකාව.JLkaOS.입력.입력관리자;
import ශ්_රී_ලංකාව.JLkaOS.작업.ක්_රියාවලිය_අගය;
import ශ්_රී_ලංකාව.JLkaOS.작업.배정기;
import ශ්_රී_ලංකාව.JLkaOS.체계호출.체계호출;
import ශ්_රී_ලංකාව.JLkaOS.ගොනු_පද්ධතිය.파일서술자표;
import ශ්_රී_ලංකාව.JLkaOS.ගොනු_පද්ධතිය.ගොනු_පද්ධතිය;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class කර්නලය {
    private final 하드웨어 ජංගම_අගය;
    private final මතකය_කළමනාකරු 기억공간 = new මතකය_කළමනාකරු(32 * 1024 * 1024);
    private final පිටුව_කළමනාකරු 쪽관리 = new පිටුව_කළමනාකරු();
    private final ගොනු_පද්ධතිය ගොනු_පද්ධතිය = new ගොනු_පද්ධතිය();
    private final 배정기 배정기 = new 배정기(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final ක්_රියාවලිය_අගය 첫과정;
    private final 체계호출 체계호출;

    public කර්නලය(하드웨어 ජංගම_අගය) {
        this.ජංගම_අගය = ජංගම_අගය;
        첫과정 = 배정기.첫과정(new 파일서술자표(ගොනු_පද්ධතිය));
        체계호출 = new 체계호출(ගොනු_පද්ධතිය, 쪽관리, 배정기, ජංගම_අගය, 입력관리);
    }

    public void ක්_රියාත්මක_කරන්න_2() {
        ජංගම_අගය.직렬출력("=== JLkaOS 관리 කර්නලය_අගය ===\n");
    }

    public void 한단계실행() {
        ජංගම_අගය.중앙처리장치멈춤();
    }

    public මතකය_කළමනාකරු 기억공간() {
        return 기억공간;
    }

    public පිටුව_කළමනාකරු 쪽관리() {
        return 쪽관리;
    }

    public ගොනු_පද්ධතිය ගොනු_පද්ධතිය() {
        return ගොනු_පද්ධතිය;
    }

    public 배정기 배정기() {
        return 배정기;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public ක්_රියාවලිය_අගය 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
