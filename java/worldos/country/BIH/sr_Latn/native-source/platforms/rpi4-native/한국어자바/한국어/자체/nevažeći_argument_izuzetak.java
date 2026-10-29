// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 한국어로 deklaracija·던지기·잡기를 할 수 있는 nevažeći_argument_izuzetak. */
public class nevažeći_argument_izuzetak extends java.lang.IllegalArgumentException {
    public nevažeći_argument_izuzetak() { super(); }
    public nevažeći_argument_izuzetak(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
