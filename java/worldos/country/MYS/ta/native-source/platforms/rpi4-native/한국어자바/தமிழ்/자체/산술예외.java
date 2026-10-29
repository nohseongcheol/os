// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package தமிழ்.자체;

/** 한국어로 அறிவிப்பு·던지기·잡기를 할 수 있는 산술예외. */
public class 산술예외 extends java.lang.ArithmeticException {
    public 산술예외() { super(); }
    public 산술예외(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
