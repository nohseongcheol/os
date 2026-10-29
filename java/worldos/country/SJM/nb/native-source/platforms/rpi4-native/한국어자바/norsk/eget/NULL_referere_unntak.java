// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package norsk.eget;

/** 한국어로 erklæring·던지기·잡기를 할 nummer 있는 NULL_referere_unntak. */
public class NULL_referere_unntak extends java.lang.NullPointerException {
    public NULL_referere_unntak() { super(); }
    public NULL_referere_unntak(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
