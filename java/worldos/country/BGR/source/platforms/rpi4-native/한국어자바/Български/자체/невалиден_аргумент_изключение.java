// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Български.자체;

/** 한국어로 декларация·던지기·잡기를 할 수 있는 невалиден_аргумент_изключение. */
public class невалиден_аргумент_изключение extends java.lang.IllegalArgumentException {
    public невалиден_аргумент_изключение() { super(); }
    public невалиден_аргумент_изключение(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
