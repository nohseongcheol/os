// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package עברית.עצמי;

/** 한국어로 הצהרה·던지기·잡기를 할 수 있는 קלט_פלט_חריגה. */
public class קלט_פלט_חריגה extends java.io.IOException {
    public קלט_פלט_חריגה() { super(); }
    public קלט_פלט_חריגה(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
