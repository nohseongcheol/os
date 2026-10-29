// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Eesti.oma;

/** 한국어로 deklaratsioon·던지기·잡기를 할 number 있는 Olek_erand. */
public class Olek_erand extends java.lang.IllegalStateException {
    public Olek_erand() { super(); }
    public Olek_erand(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
