// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package magyar.saját;

/** 한국어로 bevallás·던지기·잡기를 할 szám 있는 szám_formáz_hiba. */
public class szám_formáz_hiba extends alaptalan_argumentum_kivétel {
    public szám_formáz_hiba() { super(); }
    public szám_formáz_hiba(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
