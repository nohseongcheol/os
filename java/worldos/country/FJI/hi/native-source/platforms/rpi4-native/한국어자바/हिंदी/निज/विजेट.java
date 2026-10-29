// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package हिंदी.निज;
/** हिंदी 화면 구성요소를 만드는 편의 फ़ंक्_शन_मान. */
public final class विजेट {
    private विजेट() {}
    public static void 나중에실행(실행할일 कार्य_एक्शन) { घटना_कतार.나중에실행(कार्य_एक्शन); }
    public static लेबल टैग_मान(String पाठ, int 가로, int अनुलंब_पद, int 폭, int 높이) {
        return new लेबल(पाठ, 가로, अनुलंब_पद, 폭, 높이);
    }
    public static बटन बटन(String पाठ, int 가로, int अनुलंब_पद, int 폭, int 높이, 동작받이 받이) {
        return new बटन(पाठ, 가로, अनुलंब_पद, 폭, 높이, 받이);
    }
    public static पाठ_फ़ील्ड पाठ_फ़ील्ड(String पाठ, int 가로, int अनुलंब_पद, int 폭, int 높이) {
        return new पाठ_फ़ील्ड(पाठ, 가로, अनुलंब_पद, 폭, 높이);
    }
}
