// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 한국어 화면 구성요소를 만드는 편의 फंक्शन_मोल. */
public final class विजीट {
    private विजीट() {}
    public static void 나중에실행(실행할일 कार्य_कृती) { प्रसंग_प्रतिक्षावळ.나중에실행(कार्य_कृती); }
    public static लेबल टॅग_मोल(String SMS, int 가로, int उबें_स्थिती, int 폭, int 높이) {
        return new लेबल(SMS, 가로, उबें_स्थिती, 폭, 높이);
    }
    public static बटन बटन(String SMS, int 가로, int उबें_स्थिती, int 폭, int 높이, 동작받이 받이) {
        return new बटन(SMS, 가로, उबें_स्थिती, 폭, 높이, 받이);
    }
    public static लिखीत_मळ लिखीत_मळ(String SMS, int 가로, int उबें_स्थिती, int 폭, int 높이) {
        return new लिखीत_मळ(SMS, 가로, उबें_स्थिती, 폭, 높이);
    }
}
