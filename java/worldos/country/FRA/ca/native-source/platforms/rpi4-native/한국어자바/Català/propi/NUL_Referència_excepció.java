// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Català.propi;

/** 한국어로 declaració·던지기·잡기를 할 수 있는 NUL_Referència_excepció. */
public class NUL_Referència_excepció extends java.lang.NullPointerException {
    public NUL_Referència_excepció() { super(); }
    public NUL_Referència_excepció(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
