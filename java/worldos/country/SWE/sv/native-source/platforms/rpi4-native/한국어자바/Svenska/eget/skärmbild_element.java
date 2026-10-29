// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Svenska.eget;
/** eget JVM skärmbild 객체의 공통 계약. 표준 Swing 객체를 보관하지 않는다. */
public abstract class skärmbild_element {
    public native String läsa_SMS();
    public native void skriva_SMS(String text);
    public native void 자리정하기(int 가로, int bransch_placera, int 폭, int 높이);
}
