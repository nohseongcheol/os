// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nederlands.Eigen;
/** Eigen JVM scherm 객체의 공통 계약. 표준 Swing 객체를 보관하지 않는다. */
public abstract class scherm_element {
    public native String 글읽기();
    public native void schrijven_sms(String tekst);
    public native void 자리정하기(int 가로, int Verticaal_functie, int 폭, int hoogte_WAARDE);
}
