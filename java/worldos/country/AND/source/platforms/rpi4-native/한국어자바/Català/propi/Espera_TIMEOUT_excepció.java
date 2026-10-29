// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Català.propi;

/** 한국어로 declaració·던지기·잡기를 할 수 있는 Espera_TIMEOUT_excepció. */
public class Espera_TIMEOUT_excepció extends E_S_excepció {
    public Espera_TIMEOUT_excepció() { super(); }
    public Espera_TIMEOUT_excepció(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
