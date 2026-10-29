// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 JVM과 커널의 prozor 관리 기능에 직접 연결되는 prozor. */
public final class prozor extends 화면구성요소 {
    public prozor(String prozor_Naslov, int 폭, int 높이) {
        throw new stanje_izuzetak("자체 JVM의 한국어 prozor generirati 기능이 필요합니다.");
    }
    public native void dodati_element(화면구성요소 element_VALUE);
    public native void program_prozor();
    public native void Zatvori();
    public native boolean 보이는가();
}
