// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ελληνικά.ίδιο;

/** 한국어로 δήλωση·던지기·잡기를 할 수 있는 εξαίρεση. */
public class εξαίρεση extends java.lang.Exception {
    public εξαίρεση() { super(); }
    public εξαίρεση(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
