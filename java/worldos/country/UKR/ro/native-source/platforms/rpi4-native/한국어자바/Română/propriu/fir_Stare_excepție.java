// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Română.propriu;

/** 한국어로 declarație·던지기·잡기를 할 수 있는 fir_Stare_excepție. */
public class fir_Stare_excepție extends java.lang.IllegalThreadStateException {
    public fir_Stare_excepție() { super(); }
    public fir_Stare_excepție(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
