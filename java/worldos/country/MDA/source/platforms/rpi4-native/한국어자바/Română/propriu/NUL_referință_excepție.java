// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Română.propriu;

/** 한국어로 declarație·던지기·잡기를 할 수 있는 NUL_referință_excepție. */
public class NUL_referință_excepție extends java.lang.NullPointerException {
    public NUL_referință_excepție() { super(); }
    public NUL_referință_excepție(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
