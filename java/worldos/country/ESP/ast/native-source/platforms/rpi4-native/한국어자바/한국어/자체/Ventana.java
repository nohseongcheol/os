// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 JVM과 커널의 Ventana 관리 기능에 직접 연결되는 Ventana. */
public final class Ventana extends 화면구성요소 {
    public Ventana(String 제목, int 폭, int 높이) {
        throw new 상태예외("자체 JVM의 한국어 Ventana 생성 기능이 필요합니다.");
    }
    public native void 담기(화면구성요소 요소);
    public native void 보이기();
    public native void Zarrar();
    public native boolean 보이는가();
}
