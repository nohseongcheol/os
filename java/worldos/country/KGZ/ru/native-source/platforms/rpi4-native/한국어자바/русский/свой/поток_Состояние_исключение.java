// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package русский.свой;

/** 한국어로 декларация·던지기·잡기를 할 수 있는 поток_Состояние_исключение. */
public class поток_Состояние_исключение extends java.lang.IllegalThreadStateException {
    public поток_Состояние_исключение() { super(); }
    public поток_Состояние_исключение(String описание) { super(описание); }
    public String описание() { return getMessage(); }
}
