// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package русский.свой;

/** 한국어로 декларация·던지기·잡기를 할 수 있는 неверный_аргумент_исключение. */
public class неверный_аргумент_исключение extends java.lang.IllegalArgumentException {
    public неверный_аргумент_исключение() { super(); }
    public неверный_аргумент_исключение(String описание) { super(описание); }
    public String описание() { return getMessage(); }
}
