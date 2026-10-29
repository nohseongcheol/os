// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Latviešu.savs;

/** 한국어로 deklarācija·던지기·잡기를 할 numurs 있는 통신예외. */
public class 통신예외 extends ievadizvade_izņēmums {
    public 통신예외() { super(); }
    public 통신예외(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
