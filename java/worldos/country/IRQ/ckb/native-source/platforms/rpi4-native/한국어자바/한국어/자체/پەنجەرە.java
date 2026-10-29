// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 JVM과 커널의 پەنجەرە 관리 기능에 직접 연결되는 پەنجەرە. */
public final class پەنجەرە extends 화면구성요소 {
    public پەنجەرە(String پەنجەرە_سەردێڕ, int 폭, int 높이) {
        throw new 상태예외("자체 JVM의 한국어 پەنجەرە 생성 기능이 필요합니다.");
    }
    public native void زێدە_کردن_هێمان(화면구성요소 هێمان_نرخ);
    public native void نیشاندان_پەنجەرە();
    public native void داخستن();
    public native boolean 보이는가();
}
