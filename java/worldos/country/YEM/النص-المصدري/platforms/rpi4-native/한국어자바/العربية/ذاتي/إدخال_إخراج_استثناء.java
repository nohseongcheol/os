// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package العربية.ذاتي;

/** 한국어로 إعلان·던지기·잡기를 할 رقم 있는 إدخال_إخراج_استثناء. */
public class إدخال_إخراج_استثناء extends java.io.IOException {
    public إدخال_إخراج_استثناء() { super(); }
    public إدخال_إخراج_استثناء(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
