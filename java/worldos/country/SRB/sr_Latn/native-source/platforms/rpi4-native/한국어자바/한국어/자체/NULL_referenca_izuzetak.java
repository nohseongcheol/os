// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 한국어로 deklaracija·던지기·잡기를 할 수 있는 NULL_referenca_izuzetak. */
public class NULL_referenca_izuzetak extends java.lang.NullPointerException {
    public NULL_referenca_izuzetak() { super(); }
    public NULL_referenca_izuzetak(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
