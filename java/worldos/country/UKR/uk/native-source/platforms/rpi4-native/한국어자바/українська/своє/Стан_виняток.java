// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package українська.своє;

/** 한국어로 оголошення_4f4f026b·던지기·잡기를 할 수 있는 Стан_виняток. */
public class Стан_виняток extends java.lang.IllegalStateException {
    public Стан_виняток() { super(); }
    public Стан_виняток(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
