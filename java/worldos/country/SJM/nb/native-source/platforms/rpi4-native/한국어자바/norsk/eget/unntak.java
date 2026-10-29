// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package norsk.eget;

/** 한국어로 erklæring·던지기·잡기를 할 nummer 있는 unntak. */
public class unntak extends java.lang.Exception {
    public unntak() { super(); }
    public unntak(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
