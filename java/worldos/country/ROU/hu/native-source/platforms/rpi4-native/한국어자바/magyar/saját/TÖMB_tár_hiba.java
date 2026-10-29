// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package magyar.saját;

/** 한국어로 bevallás·던지기·잡기를 할 szám 있는 TÖMB_tár_hiba. */
public class TÖMB_tár_hiba extends java.lang.ArrayStoreException {
    public TÖMB_tár_hiba() { super(); }
    public TÖMB_tár_hiba(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
