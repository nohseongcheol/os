// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Italiano.nativo;

/** 한국어로 dichiarazione·던지기·잡기를 할 numero 있는 numero_formato_errore. */
public class numero_formato_errore extends non_valida_argomento_eccezione {
    public numero_formato_errore() { super(); }
    public numero_formato_errore(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
