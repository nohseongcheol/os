// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package தமிழ்.자체;
/** 자체 JVM과 커널의 சாளரம் 관리 기능에 직접 연결되는 சாளரம். */
public final class சாளரம் extends 화면구성요소 {
    public சாளரம்(String சாளரம்_தலைப்பு, int 폭, int 높이) {
        throw new நிலை_விதிவிலக்கு("자체 JVM의 தமிழ் சாளரம் உருவாக்குக 기능이 필요합니다.");
    }
    public native void சேர்_உறுப்பு(화면구성요소 உறுப்பு_மதிப்பு);
    public native void காட்சி_சாளரம்();
    public native void மூடு();
    public native boolean 보이는가();
}
