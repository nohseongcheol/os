// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package slovenščina.lastno;

/** 한국어로 deklaracija·던지기·잡기를 할 수 있는 V_I_izjema. */
public class V_I_izjema extends java.io.IOException {
    public V_I_izjema() { super(); }
    public V_I_izjema(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
