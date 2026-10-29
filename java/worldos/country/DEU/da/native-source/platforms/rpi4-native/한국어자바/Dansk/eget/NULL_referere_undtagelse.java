// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Dansk.eget;

/** 한국어로 erklæring·던지기·잡기를 할 tal 있는 NULL_referere_undtagelse. */
public class NULL_referere_undtagelse extends java.lang.NullPointerException {
    public NULL_referere_undtagelse() { super(); }
    public NULL_referere_undtagelse(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
