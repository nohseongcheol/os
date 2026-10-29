// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package slovenščina.lastno;

/** 한국어로 deklaracija·던지기·잡기를 할 수 있는 Tip_pretvorba_izjema. */
public class Tip_pretvorba_izjema extends java.lang.ClassCastException {
    public Tip_pretvorba_izjema() { super(); }
    public Tip_pretvorba_izjema(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
