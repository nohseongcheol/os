// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package русский.свой;

/** 한국어로 декларация·던지기·잡기를 할 수 있는 문자열범위예외. */
public class 문자열범위예외 extends 범위예외 {
    public 문자열범위예외() { super(); }
    public 문자열범위예외(String описание) { super(описание); }
    public String описание() { return getMessage(); }
}
