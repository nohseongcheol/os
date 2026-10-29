// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 한국어로 декларација·던지기·잡기를 할 수 있는 тип_Емитовање_изузетак. */
public class тип_Емитовање_изузетак extends java.lang.ClassCastException {
    public тип_Емитовање_изузетак() { super(); }
    public тип_Емитовање_изузетак(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
