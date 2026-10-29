// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Svenska.eget;

/** 한국어로 deklaration·던지기·잡기를 할 nummer 있는 MATRIS_Store_fel. */
public class MATRIS_Store_fel extends java.lang.ArrayStoreException {
    public MATRIS_Store_fel() { super(); }
    public MATRIS_Store_fel(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
