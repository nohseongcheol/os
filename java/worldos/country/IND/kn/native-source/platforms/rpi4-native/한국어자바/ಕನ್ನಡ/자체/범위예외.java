// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ಕನ್ನಡ.자체;

/** 한국어로 ದೃಢೀಕರಣ·던지기·잡기를 할 수 있는 범위예외. */
public class 범위예외 extends java.lang.IndexOutOfBoundsException {
    public 범위예외() { super(); }
    public 범위예외(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
