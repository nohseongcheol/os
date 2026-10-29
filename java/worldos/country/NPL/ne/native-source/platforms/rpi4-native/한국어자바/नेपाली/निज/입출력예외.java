// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package नेपाली.निज;

/** 한국어로 선언·던지기·잡기를 할 수 있는 입출력예외. */
public class 입출력예외 extends java.io.IOException {
    public 입출력예외() { super(); }
    public 입출력예외(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
