// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package עברית.עצמי;
/** עצמי JVM과 커널의 חלון 관리 기능에 직접 연결되는 חלון. */
public final class חלון extends 화면구성요소 {
    public חלון(String חלון_כותר, int 폭, int גובה_ערך) {
        throw new מצב_חריגה("עצמי JVM의 עברית חלון יצר 기능이 필요합니다.");
    }
    public native void הוסף_רכיב(화면구성요소 רכיב_ערך);
    public native void הופעה_חלון();
    public native void סגירה();
    public native boolean 보이는가();
}
