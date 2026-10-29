// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package தமிழ்.자체;
/** தமிழ் 화면 구성요소를 만드는 편의 செயல்பாடு_மதிப்பு. */
public final class விட்ஜெட் {
    private விட்ஜெட்() {}
    public static void 나중에실행(실행할일 பணி_செயல்) { நிகழ்வு_சாரை.나중에실행(பணி_செயல்); }
    public static விளக்கச்சீட்டு குறிக்குழு_மதிப்பு(String உரை, int 가로, int வெர்டிகல்_நிலை, int 폭, int 높이) {
        return new விளக்கச்சீட்டு(உரை, 가로, வெர்டிகல்_நிலை, 폭, 높이);
    }
    public static பொத்தான் பொத்தான்(String உரை, int 가로, int வெர்டிகல்_நிலை, int 폭, int 높이, 동작받이 받이) {
        return new பொத்தான்(உரை, 가로, வெர்டிகல்_நிலை, 폭, 높이, 받이);
    }
    public static உரைப்_புலம் உரைப்_புலம்(String உரை, int 가로, int வெர்டிகல்_நிலை, int 폭, int 높이) {
        return new உரைப்_புலம்(உரை, 가로, வெர்டிகல்_நிலை, 폭, 높이);
    }
}
