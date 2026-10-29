// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Română.propriu;

/** 한국어로 declarație·던지기·잡기를 할 수 있는 nul_argument_excepție. */
public class nul_argument_excepție extends java.lang.IllegalArgumentException {
    public nul_argument_excepție() { super(); }
    public nul_argument_excepție(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
