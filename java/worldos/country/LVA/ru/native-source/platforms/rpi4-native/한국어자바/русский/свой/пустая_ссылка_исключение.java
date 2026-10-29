// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package русский.свой;

/** 한국어로 декларация·던지기·잡기를 할 수 있는 пустая_ссылка_исключение. */
public class пустая_ссылка_исключение extends java.lang.NullPointerException {
    public пустая_ссылка_исключение() { super(); }
    public пустая_ссылка_исключение(String описание) { super(описание); }
    public String описание() { return getMessage(); }
}
