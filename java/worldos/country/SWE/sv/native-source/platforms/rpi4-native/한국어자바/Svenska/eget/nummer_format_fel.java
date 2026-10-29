// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Svenska.eget;

/** 한국어로 deklaration·던지기·잡기를 할 nummer 있는 nummer_format_fel. */
public class nummer_format_fel extends ogiltig_argument_fel {
    public nummer_format_fel() { super(); }
    public nummer_format_fel(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
