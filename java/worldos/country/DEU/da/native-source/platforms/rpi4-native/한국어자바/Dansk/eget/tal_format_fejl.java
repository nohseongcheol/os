// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Dansk.eget;

/** 한국어로 erklæring·던지기·잡기를 할 tal 있는 tal_format_fejl. */
public class tal_format_fejl extends ugyldig_argument_undtagelse {
    public tal_format_fejl() { super(); }
    public tal_format_fejl(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
