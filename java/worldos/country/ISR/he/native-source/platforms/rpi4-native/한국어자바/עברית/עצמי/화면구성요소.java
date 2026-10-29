// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package עברית.עצמי;
/** עצמי JVM 화면 객체의 공통 계약. 표준 Swing 객체를 보관하지 않는다. */
public abstract class 화면구성요소 {
    public native String 글읽기();
    public native void כתיבה_טקסט(String טקסט);
    public native void 자리정하기(int 가로, int אנכי_עמדה, int 폭, int גובה_ערך);
}
