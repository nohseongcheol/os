// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package हिंदी.निज;

/** 한국어로 घोषणा·던지기·잡기를 할 수 있는 대기시간초과예외. */
public class 대기시간초과예외 extends इनपुट_आउटपुट_अपवाद {
    public 대기시간초과예외() { super(); }
    public 대기시간초과예외(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
