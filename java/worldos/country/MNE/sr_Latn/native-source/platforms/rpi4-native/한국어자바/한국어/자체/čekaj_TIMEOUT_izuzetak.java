// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 한국어로 deklaracija·던지기·잡기를 할 수 있는 čekaj_TIMEOUT_izuzetak. */
public class čekaj_TIMEOUT_izuzetak extends U_I_izuzetak {
    public čekaj_TIMEOUT_izuzetak() { super(); }
    public čekaj_TIMEOUT_izuzetak(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
