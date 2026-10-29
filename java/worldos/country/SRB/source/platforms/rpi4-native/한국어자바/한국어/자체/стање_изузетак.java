// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 한국어로 декларација·던지기·잡기를 할 수 있는 стање_изузетак. */
public class стање_изузетак extends java.lang.IllegalStateException {
    public стање_изузетак() { super(); }
    public стање_изузетак(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
