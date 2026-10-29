// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ਪੰਜਾਬੀ.자체;

/** 한국어로 선언·던지기·잡기를 할 수 있는 상태예외. */
public class 상태예외 extends java.lang.IllegalStateException {
    public 상태예외() { super(); }
    public 상태예외(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
