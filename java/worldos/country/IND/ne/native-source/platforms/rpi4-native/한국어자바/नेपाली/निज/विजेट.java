// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package नेपाली.निज;
/** नेपाली 화면 구성요소를 만드는 편의 प्रकार्य_मान. */
public final class विजेट {
    private विजेट() {}
    public static void 나중에실행(실행할일 कार्य_कार्य) { घटना_लाइन.나중에실행(कार्य_कार्य); }
    public static लेबुल ट्याग_मान(String पाठ, int 가로, int ठाडो_राख्नुहोस्, int 폭, int 높이) {
        return new लेबुल(पाठ, 가로, ठाडो_राख्नुहोस्, 폭, 높이);
    }
    public static बटन बटन(String पाठ, int 가로, int ठाडो_राख्नुहोस्, int 폭, int 높이, 동작받이 받이) {
        return new बटन(पाठ, 가로, ठाडो_राख्नुहोस्, 폭, 높이, 받이);
    }
    public static पाठ_क्षेत्र पाठ_क्षेत्र(String पाठ, int 가로, int ठाडो_राख्नुहोस्, int 폭, int 높이) {
        return new पाठ_क्षेत्र(पाठ, 가로, ठाडो_राख्नुहोस्, 폭, 높이);
    }
}
