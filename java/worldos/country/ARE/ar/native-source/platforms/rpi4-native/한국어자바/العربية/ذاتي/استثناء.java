// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package العربية.ذاتي;

/** 한국어로 إعلان·던지기·잡기를 할 رقم 있는 استثناء. */
public class استثناء extends java.lang.Exception {
    public استثناء() { super(); }
    public استثناء(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
