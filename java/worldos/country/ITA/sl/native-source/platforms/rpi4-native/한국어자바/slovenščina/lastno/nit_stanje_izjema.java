// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package slovenščina.lastno;

/** 한국어로 deklaracija·던지기·잡기를 할 수 있는 nit_stanje_izjema. */
public class nit_stanje_izjema extends java.lang.IllegalThreadStateException {
    public nit_stanje_izjema() { super(); }
    public nit_stanje_izjema(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
