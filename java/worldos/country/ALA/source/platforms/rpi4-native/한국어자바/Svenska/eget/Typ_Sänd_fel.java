// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Svenska.eget;

/** 한국어로 deklaration·던지기·잡기를 할 nummer 있는 Typ_Sänd_fel. */
public class Typ_Sänd_fel extends java.lang.ClassCastException {
    public Typ_Sänd_fel() { super(); }
    public Typ_Sänd_fel(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
