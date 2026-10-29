// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package فارسی.بومی;

/** 한국어로 اعلامیه·던지기·잡기를 할 수 있는 استثنا. */
public class استثنا extends java.lang.Exception {
    public استثنا() { super(); }
    public استثنا(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
