// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 한국어로 deklaracija·던지기·잡기를 할 수 있는 Status_izuzetak. */
public class Status_izuzetak extends java.lang.IllegalStateException {
    public Status_izuzetak() { super(); }
    public Status_izuzetak(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
