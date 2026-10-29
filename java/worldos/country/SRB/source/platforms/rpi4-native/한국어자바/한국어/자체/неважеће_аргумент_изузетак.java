// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 한국어로 декларација·던지기·잡기를 할 수 있는 неважеће_аргумент_изузетак. */
public class неважеће_аргумент_изузетак extends java.lang.IllegalArgumentException {
    public неважеће_аргумент_изузетак() { super(); }
    public неважеће_аргумент_изузетак(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
