// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package हिंदी.निज;

/** 한국어로 घोषणा·던지기·잡기를 할 수 있는 इनपुट_आउटपुट_अपवाद. */
public class इनपुट_आउटपुट_अपवाद extends java.io.IOException {
    public इनपुट_आउटपुट_अपवाद() { super(); }
    public इनपुट_आउटपुट_अपवाद(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
