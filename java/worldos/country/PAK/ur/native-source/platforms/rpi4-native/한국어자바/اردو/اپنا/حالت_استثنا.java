// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package اردو.اپنا;

/** 한국어로 선언·던지기·잡기를 할 수 있는 حالت_استثنا. */
public class حالت_استثنا extends java.lang.IllegalStateException {
    public حالت_استثنا() { super(); }
    public حالت_استثنا(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
