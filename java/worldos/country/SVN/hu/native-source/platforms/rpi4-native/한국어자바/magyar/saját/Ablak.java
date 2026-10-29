// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package magyar.saját;
/** saját JVM과 커널의 Ablak 관리 기능에 직접 연결되는 Ablak. */
public final class Ablak extends 화면구성요소 {
    public Ablak(String ablak_Cím, int 폭, int 높이) {
        throw new Állapot_kivétel("saját JVM의 magyar Ablak generálás 기능이 필요합니다.");
    }
    public native void hozzáad_elem(화면구성요소 elem_ÉRTÉK);
    public native void bemutató_ablak();
    public native void Bezárás();
    public native boolean 보이는가();
}
