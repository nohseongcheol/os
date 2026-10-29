// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package norsk.eget;

/** 한국어로 erklæring·던지기·잡기를 할 nummer 있는 kjøring_unntak. */
public class kjøring_unntak extends java.lang.RuntimeException {
    public kjøring_unntak() { super(); }
    public kjøring_unntak(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
