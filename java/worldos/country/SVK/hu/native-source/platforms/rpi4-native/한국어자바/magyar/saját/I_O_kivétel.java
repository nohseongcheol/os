// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package magyar.saját;

/** 한국어로 bevallás·던지기·잡기를 할 szám 있는 I_O_kivétel. */
public class I_O_kivétel extends java.io.IOException {
    public I_O_kivétel() { super(); }
    public I_O_kivétel(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
