// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Български.자체;

/** 한국어로 декларация·던지기·잡기를 할 수 있는 Тип_прехвърлям_изключение. */
public class Тип_прехвърлям_изключение extends java.lang.ClassCastException {
    public Тип_прехвърлям_изключение() { super(); }
    public Тип_прехвърлям_изключение(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
