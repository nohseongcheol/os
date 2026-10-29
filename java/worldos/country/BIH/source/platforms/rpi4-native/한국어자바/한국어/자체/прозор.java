// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 JVM과 커널의 прозор 관리 기능에 직접 연결되는 прозор. */
public final class прозор extends 화면구성요소 {
    public прозор(String 제목, int 폭, int 높이) {
        throw new 상태예외("자체 JVM의 한국어 прозор 생성 기능이 필요합니다.");
    }
    public native void додати_елемент(화면구성요소 елемент_вриједност);
    public native void приказати_прозор();
    public native void затворити();
    public native boolean 보이는가();
}
