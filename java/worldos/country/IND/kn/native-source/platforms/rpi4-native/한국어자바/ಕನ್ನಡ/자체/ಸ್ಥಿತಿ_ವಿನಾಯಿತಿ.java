// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ಕನ್ನಡ.자체;

/** 한국어로 ದೃಢೀಕರಣ·던지기·잡기를 할 수 있는 ಸ್ಥಿತಿ_ವಿನಾಯಿತಿ. */
public class ಸ್ಥಿತಿ_ವಿನಾಯಿತಿ extends java.lang.IllegalStateException {
    public ಸ್ಥಿತಿ_ವಿನಾಯಿತಿ() { super(); }
    public ಸ್ಥಿತಿ_ವಿನಾಯಿತಿ(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
