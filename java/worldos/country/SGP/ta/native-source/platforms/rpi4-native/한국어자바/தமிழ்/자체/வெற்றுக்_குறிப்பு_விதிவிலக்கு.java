// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package தமிழ்.자체;

/** 한국어로 அறிவிப்பு·던지기·잡기를 할 수 있는 வெற்றுக்_குறிப்பு_விதிவிலக்கு. */
public class வெற்றுக்_குறிப்பு_விதிவிலக்கு extends java.lang.NullPointerException {
    public வெற்றுக்_குறிப்பு_விதிவிலக்கு() { super(); }
    public வெற்றுக்_குறிப்பு_விதிவிலக்கு(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
