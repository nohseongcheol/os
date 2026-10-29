// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Català.propi;

/** 한국어로 declaració·던지기·잡기를 할 수 있는 TIPUS_conversió_excepció. */
public class TIPUS_conversió_excepció extends java.lang.ClassCastException {
    public TIPUS_conversió_excepció() { super(); }
    public TIPUS_conversió_excepció(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
