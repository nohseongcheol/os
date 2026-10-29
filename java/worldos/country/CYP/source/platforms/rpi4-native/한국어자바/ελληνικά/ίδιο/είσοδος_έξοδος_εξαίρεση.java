// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ελληνικά.ίδιο;

/** 한국어로 δήλωση·던지기·잡기를 할 수 있는 είσοδος_έξοδος_εξαίρεση. */
public class είσοδος_έξοδος_εξαίρεση extends java.io.IOException {
    public είσοδος_έξοδος_εξαίρεση() { super(); }
    public είσοδος_έξοδος_εξαίρεση(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
