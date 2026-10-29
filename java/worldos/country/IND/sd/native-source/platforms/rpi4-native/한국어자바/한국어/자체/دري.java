// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 JVM과 커널의 دري 관리 기능에 직접 연결되는 دري. */
public final class دري extends 화면구성요소 {
    public دري(String دري_عنوان, int 폭, int 높이) {
        throw new 상태예외("자체 JVM의 한국어 دري 생성 기능이 필요합니다.");
    }
    public native void اضافو_ڪريو_عنصر(화면구성요소 عنصر_قدر);
    public native void نمائش_ڪريو_دري();
    public native void بند_ڪرڻ();
    public native boolean 보이는가();
}
