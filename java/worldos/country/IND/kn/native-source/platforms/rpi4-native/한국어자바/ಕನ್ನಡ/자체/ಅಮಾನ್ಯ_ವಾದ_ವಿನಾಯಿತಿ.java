// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ಕನ್ನಡ.자체;

/** 한국어로 ದೃಢೀಕರಣ·던지기·잡기를 할 수 있는 ಅಮಾನ್ಯ_ವಾದ_ವಿನಾಯಿತಿ. */
public class ಅಮಾನ್ಯ_ವಾದ_ವಿನಾಯಿತಿ extends java.lang.IllegalArgumentException {
    public ಅಮಾನ್ಯ_ವಾದ_ವಿನಾಯಿತಿ() { super(); }
    public ಅಮಾನ್ಯ_ವಾದ_ವಿನಾಯಿತಿ(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
