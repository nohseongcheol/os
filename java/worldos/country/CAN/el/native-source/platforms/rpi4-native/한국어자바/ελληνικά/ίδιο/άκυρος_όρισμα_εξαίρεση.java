// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ελληνικά.ίδιο;

/** 한국어로 δήλωση·던지기·잡기를 할 수 있는 άκυρος_όρισμα_εξαίρεση. */
public class άκυρος_όρισμα_εξαίρεση extends java.lang.IllegalArgumentException {
    public άκυρος_όρισμα_εξαίρεση() { super(); }
    public άκυρος_όρισμα_εξαίρεση(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
