// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Eesti.oma;

/** 한국어로 deklaratsioon·던지기·잡기를 할 number 있는 kehtetu_argument_erand. */
public class kehtetu_argument_erand extends java.lang.IllegalArgumentException {
    public kehtetu_argument_erand() { super(); }
    public kehtetu_argument_erand(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
