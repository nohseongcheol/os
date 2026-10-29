// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package русский.свой;

/** 한국어로 декларация·던지기·잡기를 할 수 있는 коммуникация_исключение. */
public class коммуникация_исключение extends входные_данные_выход_исключение {
    public коммуникация_исключение() { super(); }
    public коммуникация_исключение(String описание) { super(описание); }
    public String описание() { return getMessage(); }
}
