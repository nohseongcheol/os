// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package magyar.saját;

/** 한국어로 bevallás·던지기·잡기를 할 szám 있는 alaptalan_argumentum_kivétel. */
public class alaptalan_argumentum_kivétel extends java.lang.IllegalArgumentException {
    public alaptalan_argumentum_kivétel() { super(); }
    public alaptalan_argumentum_kivétel(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
