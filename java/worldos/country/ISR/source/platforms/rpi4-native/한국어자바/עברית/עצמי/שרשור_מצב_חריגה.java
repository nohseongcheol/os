// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package עברית.עצמי;

/** 한국어로 הצהרה·던지기·잡기를 할 수 있는 שרשור_מצב_חריגה. */
public class שרשור_מצב_חריגה extends java.lang.IllegalThreadStateException {
    public שרשור_מצב_חריגה() { super(); }
    public שרשור_מצב_חריגה(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
