// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 JVM과 커널의 цонх 관리 기능에 직접 연결되는 цонх. */
public final class цонх extends 화면구성요소 {
    public цонх(String цонх_Гарчиг, int 폭, int 높이) {
        throw new 상태예외("자체 JVM의 한국어 цонх 생성 기능이 필요합니다.");
    }
    public native void нэмэх_элемент(화면구성요소 элемент_утга);
    public native void үзүүлэх_цонх();
    public native void Хаах();
    public native boolean 보이는가();
}
