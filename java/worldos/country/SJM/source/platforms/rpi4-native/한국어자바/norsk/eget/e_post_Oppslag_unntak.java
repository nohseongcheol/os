// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package norsk.eget;

/** 한국어로 erklæring·던지기·잡기를 할 nummer 있는 e_post_Oppslag_unntak. */
public class e_post_Oppslag_unntak extends I_U_unntak {
    public e_post_Oppslag_unntak() { super(); }
    public e_post_Oppslag_unntak(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
