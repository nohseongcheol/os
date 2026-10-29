// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Română.propriu;

/** 한국어로 declarație·던지기·잡기를 할 수 있는 adresa_LOOKUP_excepție. */
public class adresa_LOOKUP_excepție extends I_O_excepție {
    public adresa_LOOKUP_excepție() { super(); }
    public adresa_LOOKUP_excepție(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
