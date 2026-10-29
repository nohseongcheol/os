// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Italiano.nativo;

/** 한국어로 dichiarazione·던지기·잡기를 할 numero 있는 aritmetico_errore. */
public class aritmetico_errore extends java.lang.ArithmeticException {
    public aritmetico_errore() { super(); }
    public aritmetico_errore(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
