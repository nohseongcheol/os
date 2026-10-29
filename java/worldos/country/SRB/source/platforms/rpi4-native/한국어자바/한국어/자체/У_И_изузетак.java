// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 한국어로 декларација·던지기·잡기를 할 수 있는 У_И_изузетак. */
public class У_И_изузетак extends java.io.IOException {
    public У_И_изузетак() { super(); }
    public У_И_изузетак(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
