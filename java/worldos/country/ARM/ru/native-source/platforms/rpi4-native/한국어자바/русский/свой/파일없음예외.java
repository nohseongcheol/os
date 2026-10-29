// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package русский.свой;

/** 한국어로 декларация·던지기·잡기를 할 수 있는 파일없음예외. */
public class 파일없음예외 extends входные_данные_выход_исключение {
    public 파일없음예외() { super(); }
    public 파일없음예외(String описание) { super(описание); }
    public String описание() { return getMessage(); }
}
