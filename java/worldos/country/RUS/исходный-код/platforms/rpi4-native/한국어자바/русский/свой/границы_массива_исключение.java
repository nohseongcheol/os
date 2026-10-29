// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package русский.свой;

/** 한국어로 декларация·던지기·잡기를 할 수 있는 границы_массива_исключение. */
public class границы_массива_исключение extends 범위예외 {
    public границы_массива_исключение() { super(); }
    public границы_массива_исключение(String описание) { super(описание); }
    public String описание() { return getMessage(); }
}
