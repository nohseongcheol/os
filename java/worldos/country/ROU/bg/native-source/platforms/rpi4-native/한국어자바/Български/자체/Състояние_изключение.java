// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Български.자체;

/** 한국어로 декларация·던지기·잡기를 할 수 있는 Състояние_изключение. */
public class Състояние_изключение extends java.lang.IllegalStateException {
    public Състояние_изключение() { super(); }
    public Състояние_изключение(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
