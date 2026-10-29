// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 한국어로 ప్రకటన·던지기·잡기를 할 수 있는 స్థితి_మినహాయింపు. */
public class స్థితి_మినహాయింపు extends java.lang.IllegalStateException {
    public స్థితి_మినహాయింపు() { super(); }
    public స్థితి_మినహాయింపు(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
