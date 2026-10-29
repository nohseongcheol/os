// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package čeština.vlastní;

/** 한국어로 deklarace_4f4f026b·던지기·잡기를 할 číslo 있는 Stav_výjimka. */
public class Stav_výjimka extends java.lang.IllegalStateException {
    public Stav_výjimka() { super(); }
    public Stav_výjimka(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
