// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 JVM과 커널의 كۆزنەك 관리 기능에 직접 연결되는 كۆزنەك. */
public final class كۆزنەك extends 화면구성요소 {
    public كۆزنەك(String كۆزنەك_تېما, int 폭, int 높이) {
        throw new 상태예외("자체 JVM의 한국어 كۆزنەك ھاسىل_قىلىش 기능이 필요합니다.");
    }
    public native void قوشماق_ئېلېمېنت(화면구성요소 ئېلېمېنت_قىممىتى);
    public native void كۆرسەتمەك_كۆزنەك();
    public native void ياپ();
    public native boolean 보이는가();
}
