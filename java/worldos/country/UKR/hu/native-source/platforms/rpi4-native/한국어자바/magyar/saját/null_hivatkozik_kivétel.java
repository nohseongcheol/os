// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package magyar.saját;

/** 한국어로 bevallás·던지기·잡기를 할 szám 있는 null_hivatkozik_kivétel. */
public class null_hivatkozik_kivétel extends java.lang.NullPointerException {
    public null_hivatkozik_kivétel() { super(); }
    public null_hivatkozik_kivétel(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
