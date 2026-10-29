// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 JVM과 커널의 کړکۍ 관리 기능에 직접 연결되는 کړکۍ. */
public final class کړکۍ extends 화면구성요소 {
    public کړکۍ(String 제목, int 폭, int 높이) {
        throw new 상태예외("자체 JVM의 한국어 کړکۍ 생성 기능이 필요합니다.");
    }
    public native void 담기(화면구성요소 توک_ارزښت);
    public native void 보이기();
    public native void بندول();
    public native boolean 보이는가();
}
