// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 한국어로 deklarata·던지기·잡기를 할 수 있는 ARRAY_Store_dështim. */
public class ARRAY_Store_dështim extends java.lang.ArrayStoreException {
    public ARRAY_Store_dështim() { super(); }
    public ARRAY_Store_dështim(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
