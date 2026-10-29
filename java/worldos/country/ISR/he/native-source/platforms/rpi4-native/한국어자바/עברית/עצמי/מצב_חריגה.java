// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package עברית.עצמי;

/** 한국어로 הצהרה·던지기·잡기를 할 수 있는 מצב_חריגה. */
public class מצב_חריגה extends java.lang.IllegalStateException {
    public מצב_חריגה() { super(); }
    public מצב_חריגה(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
