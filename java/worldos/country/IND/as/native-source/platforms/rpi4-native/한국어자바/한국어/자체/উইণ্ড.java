// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 JVM과 커널의 উইণ্ড 관리 기능에 직접 연결되는 উইণ্ড. */
public final class উইণ্ড extends 화면구성요소 {
    public উইণ্ড(String উইণ্ড_শিৰোনাম, int 폭, int 높이) {
        throw new 상태예외("자체 JVM의 한국어 উইণ্ড সৃষ্টি_কৰক 기능이 필요합니다.");
    }
    public native void যোগ_কৰক_উপাদান(화면구성요소 উপাদান_মান);
    public native void শ্ব_উইণ্ড();
    public native void বন্ধ_কৰক();
    public native boolean 보이는가();
}
