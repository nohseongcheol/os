// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 한국어로 선언·던지기·잡기를 할 수 있는 TYPE_Emitiranje_izuzetak. */
public class TYPE_Emitiranje_izuzetak extends java.lang.ClassCastException {
    public TYPE_Emitiranje_izuzetak() { super(); }
    public TYPE_Emitiranje_izuzetak(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
