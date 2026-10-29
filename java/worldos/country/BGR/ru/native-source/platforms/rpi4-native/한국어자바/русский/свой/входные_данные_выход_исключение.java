// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package русский.свой;

/** 한국어로 декларация·던지기·잡기를 할 수 있는 входные_данные_выход_исключение. */
public class входные_данные_выход_исключение extends java.io.IOException {
    public входные_данные_выход_исключение() { super(); }
    public входные_данные_выход_исключение(String описание) { super(описание); }
    public String описание() { return getMessage(); }
}
