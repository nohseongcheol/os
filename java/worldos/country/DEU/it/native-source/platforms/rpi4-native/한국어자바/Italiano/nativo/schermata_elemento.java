// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Italiano.nativo;
/** nativo JVM schermata 객체의 공통 계약. 표준 Swing 객체를 보관하지 않는다. */
public abstract class schermata_elemento {
    public native String 글읽기();
    public native void scrivere_SMS(String testo);
    public native void 자리정하기(int 가로, int Verticale_funzione, int 폭, int altezza_VALORE);
}
