// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package हिंदी.निज;
/** निज JVM 화면 객체의 공통 계약. 표준 Swing 객체를 보관하지 않는다. */
public abstract class 화면구성요소 {
    public native String पढें_पाठ();
    public native void लिखना_पाठ(String पाठ);
    public native void 자리정하기(int 가로, int अनुलंब_पद, int 폭, int 높이);
}
