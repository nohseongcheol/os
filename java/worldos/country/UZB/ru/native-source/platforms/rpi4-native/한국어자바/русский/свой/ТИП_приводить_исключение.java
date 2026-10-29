// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package русский.свой;

/** 한국어로 декларация·던지기·잡기를 할 수 있는 ТИП_приводить_исключение. */
public class ТИП_приводить_исключение extends java.lang.ClassCastException {
    public ТИП_приводить_исключение() { super(); }
    public ТИП_приводить_исключение(String описание) { super(описание); }
    public String описание() { return getMessage(); }
}
