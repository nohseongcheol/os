// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 JVM과 커널의 palanteer 관리 기능에 직접 연결되는 palanteer. */
public final class palanteer extends 화면구성요소 {
    public palanteer(String palanteer_Tur, int 폭, int 높이) {
        throw new 상태예외("자체 JVM의 한국어 palanteer 생성 기능이 필요합니다.");
    }
    public native void mottal_cër(화면구성요소 cër_xëyma);
    public native void féeñal_palanteer();
    public native void Tej();
    public native boolean 보이는가();
}
