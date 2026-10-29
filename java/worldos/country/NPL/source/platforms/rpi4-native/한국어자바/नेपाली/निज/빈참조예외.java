// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package नेपाली.निज;

/** 한국어로 선언·던지기·잡기를 할 수 있는 빈참조예외. */
public class 빈참조예외 extends java.lang.NullPointerException {
    public 빈참조예외() { super(); }
    public 빈참조예외(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
