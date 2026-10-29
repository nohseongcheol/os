// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 JVM과 커널의 کھڑکی 관리 기능에 직접 연결되는 کھڑکی. */
public final class کھڑکی extends 화면구성요소 {
    public کھڑکی(String کھڑکی_عنوان, int 폭, int 높이) {
        throw new 상태예외("자체 JVM의 한국어 کھڑکی 생성 기능이 필요합니다.");
    }
    public native void اضافہ_کرو_عنصر(화면구성요소 عنصر_قدر);
    public native void نمایش_کرو_کھڑکی();
    public native void بند_کرو();
    public native boolean 보이는가();
}
