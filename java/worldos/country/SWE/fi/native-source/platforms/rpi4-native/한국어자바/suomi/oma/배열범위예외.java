// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package suomi.oma;

/** 한국어로 esittely·던지기·잡기를 할 numero 있는 배열범위예외. */
public class 배열범위예외 extends 범위예외 {
    public 배열범위예외() { super(); }
    public 배열범위예외(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
