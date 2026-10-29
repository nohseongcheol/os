// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package متحده_عرب_امارات.JAreOS.نوغی;

import متحده_عرب_امارات.JAreOS.기억공간.기억공간관리자;
import متحده_عرب_امارات.JAreOS.기억공간.쪽관리자;
import متحده_عرب_امارات.JAreOS.입력.입력관리자;
import متحده_عرب_امارات.JAreOS.작업.과정;
import متحده_عرب_امارات.JAreOS.작업.배정기;
import متحده_عرب_امارات.JAreOS.체계호출.체계호출;
import متحده_عرب_امارات.JAreOS.دوتنه_سېسټم.파일서술자표;
import متحده_عرب_امارات.JAreOS.دوتنه_سېسټم.دوتنه_سېسټم;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class نوغی {
    private final 하드웨어 وزله_ارزښت;
    private final 기억공간관리자 기억공간 = new 기억공간관리자(32 * 1024 * 1024);
    private final 쪽관리자 쪽관리 = new 쪽관리자();
    private final دوتنه_سېسټم دوتنه_سېسټم = new دوتنه_سېسټم();
    private final 배정기 배정기 = new 배정기(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final 과정 첫과정;
    private final 체계호출 체계호출;

    public نوغی(하드웨어 وزله_ارزښت) {
        this.وزله_ارزښت = وزله_ارزښت;
        첫과정 = 배정기.첫과정(new 파일서술자표(دوتنه_سېسټم));
        체계호출 = new 체계호출(دوتنه_سېسټم, 쪽관리, 배정기, وزله_ارزښت, 입력관리);
    }

    public void ځغلول() {
        وزله_ارزښت.직렬출력("=== JAreOS 관리 نوغی_ارزښت ===\n");
    }

    public void 한단계실행() {
        وزله_ارزښت.중앙처리장치멈춤();
    }

    public 기억공간관리자 기억공간() {
        return 기억공간;
    }

    public 쪽관리자 쪽관리() {
        return 쪽관리;
    }

    public دوتنه_سېسټم دوتنه_سېسټم() {
        return دوتنه_سېسټم;
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
