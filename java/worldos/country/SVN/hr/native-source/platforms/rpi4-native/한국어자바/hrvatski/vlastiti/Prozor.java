// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package hrvatski.vlastiti;
/** vlastiti JVM과 커널의 Prozor 관리 기능에 직접 연결되는 Prozor. */
public final class Prozor extends 화면구성요소 {
    public Prozor(String prozor_Naslov, int 폭, int 높이) {
        throw new Stanje_iznimka("vlastiti JVM의 hrvatski Prozor generirati 기능이 필요합니다.");
    }
    public native void Dodaj_element(화면구성요소 element_VALUE);
    public native void emisija_prozor();
    public native void Zatvori();
    public native boolean 보이는가();
}
