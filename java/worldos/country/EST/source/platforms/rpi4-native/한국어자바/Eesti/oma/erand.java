// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Eesti.oma;

/** 한국어로 deklaratsioon·던지기·잡기를 할 number 있는 erand. */
public class erand extends java.lang.Exception {
    public erand() { super(); }
    public erand(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
