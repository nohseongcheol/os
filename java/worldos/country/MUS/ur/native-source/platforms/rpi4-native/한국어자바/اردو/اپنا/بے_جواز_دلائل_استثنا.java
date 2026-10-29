// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package اردو.اپنا;

/** 한국어로 선언·던지기·잡기를 할 수 있는 بے_جواز_دلائل_استثنا. */
public class بے_جواز_دلائل_استثنا extends java.lang.IllegalArgumentException {
    public بے_جواز_دلائل_استثنا() { super(); }
    public بے_جواز_دلائل_استثنا(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
