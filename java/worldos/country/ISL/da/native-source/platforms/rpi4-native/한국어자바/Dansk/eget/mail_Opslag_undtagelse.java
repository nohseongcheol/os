// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Dansk.eget;

/** 한국어로 erklæring·던지기·잡기를 할 tal 있는 mail_Opslag_undtagelse. */
public class mail_Opslag_undtagelse extends I_O_undtagelse {
    public mail_Opslag_undtagelse() { super(); }
    public mail_Opslag_undtagelse(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
