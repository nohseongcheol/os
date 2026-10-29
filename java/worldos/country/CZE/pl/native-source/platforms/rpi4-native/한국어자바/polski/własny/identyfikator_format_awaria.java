// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package polski.własny;

/** 한국어로 deklaracja·던지기·잡기를 할 identyfikator 있는 identyfikator_format_awaria. */
public class identyfikator_format_awaria extends nieważny_argument_wyjątek {
    public identyfikator_format_awaria() { super(); }
    public identyfikator_format_awaria(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
