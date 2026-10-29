// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package русский.свой;

/** 한국어로 декларация·던지기·잡기를 할 수 있는 МАССИВ_Store_сбой. */
public class МАССИВ_Store_сбой extends java.lang.ArrayStoreException {
    public МАССИВ_Store_сбой() { super(); }
    public МАССИВ_Store_сбой(String описание) { super(описание); }
    public String описание() { return getMessage(); }
}
