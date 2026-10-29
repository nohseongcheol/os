// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Italiano.nativo;

/** 한국어로 dichiarazione·던지기·잡기를 할 numero 있는 non_valida_argomento_eccezione. */
public class non_valida_argomento_eccezione extends java.lang.IllegalArgumentException {
    public non_valida_argomento_eccezione() { super(); }
    public non_valida_argomento_eccezione(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
