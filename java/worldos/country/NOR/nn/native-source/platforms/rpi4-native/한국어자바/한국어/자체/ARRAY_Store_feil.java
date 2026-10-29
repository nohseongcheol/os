// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 한국어로 erklæring·던지기·잡기를 할 수 있는 ARRAY_Store_feil. */
public class ARRAY_Store_feil extends java.lang.ArrayStoreException {
    public ARRAY_Store_feil() { super(); }
    public ARRAY_Store_feil(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
