// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package עברית.עצמי;

/** 한국어로 הצהרה·던지기·잡기를 할 수 있는 חריגה. */
public class חריגה extends java.lang.Exception {
    public חריגה() { super(); }
    public חריגה(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
