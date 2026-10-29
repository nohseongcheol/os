// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ελληνικά.ίδιο;

/** 한국어로 δήλωση·던지기·잡기를 할 수 있는 Τύπος_Διανομή_εξαίρεση. */
public class Τύπος_Διανομή_εξαίρεση extends java.lang.ClassCastException {
    public Τύπος_Διανομή_εξαίρεση() { super(); }
    public Τύπος_Διανομή_εξαίρεση(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
