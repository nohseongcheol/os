// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package hulanda.JNldOS.핵심;

import hulanda.JNldOS.기억공간.기억공간관리자;
import hulanda.JNldOS.기억공간.쪽관리자;
import hulanda.JNldOS.입력.입력관리자;
import hulanda.JNldOS.작업.과정;
import hulanda.JNldOS.작업.배정기;
import hulanda.JNldOS.체계호출.체계호출;
import hulanda.JNldOS.파일체계.파일서술자표;
import hulanda.JNldOS.파일체계.파일체계;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class 핵심 {
    private final 하드웨어 장치;
    private final 기억공간관리자 기억공간 = new 기억공간관리자(32 * 1024 * 1024);
    private final 쪽관리자 쪽관리 = new 쪽관리자();
    private final 파일체계 파일체계 = new 파일체계();
    private final 배정기 배정기 = new 배정기(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final 과정 첫과정;
    private final 체계호출 체계호출;

    public 핵심(하드웨어 장치) {
        this.장치 = 장치;
        첫과정 = 배정기.첫과정(new 파일서술자표(파일체계));
        체계호출 = new 체계호출(파일체계, 쪽관리, 배정기, 장치, 입력관리);
    }

    public void 시작() {
        장치.직렬출력("=== JNldOS 관리 커널 ===\n");
    }

    public void 한단계실행() {
        장치.중앙처리장치멈춤();
    }

    public 기억공간관리자 기억공간() {
        return 기억공간;
    }

    public 쪽관리자 쪽관리() {
        return 쪽관리;
    }

    public 파일체계 파일체계() {
        return 파일체계;
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
