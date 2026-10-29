// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package العربية.ذاتي;

/** 한국어로 إعلان·던지기·잡기를 할 رقم 있는 통신예외. */
public class 통신예외 extends إدخال_إخراج_استثناء {
    public 통신예외() { super(); }
    public 통신예외(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
