// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Dansk.eget;
/** eget JVM skærmbillede 객체의 공통 계약. 표준 Swing 객체를 보관하지 않는다. */
public abstract class skærmbillede_element {
    public native String 글읽기();
    public native void skrive_sms(String Tekst);
    public native void 자리정하기(int 가로, int Lodret_placere, int 폭, int 높이);
}
