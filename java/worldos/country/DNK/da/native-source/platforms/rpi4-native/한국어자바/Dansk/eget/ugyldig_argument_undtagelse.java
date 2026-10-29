// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Dansk.eget;

/** 한국어로 erklæring·던지기·잡기를 할 tal 있는 ugyldig_argument_undtagelse. */
public class ugyldig_argument_undtagelse extends java.lang.IllegalArgumentException {
    public ugyldig_argument_undtagelse() { super(); }
    public ugyldig_argument_undtagelse(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
