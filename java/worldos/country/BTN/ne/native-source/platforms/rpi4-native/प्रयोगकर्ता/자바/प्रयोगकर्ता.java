// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 उपकरणहरू 전용 SVC जडान. 기존 x86 उपकरणहरू 원문을 함께 빌드한다. */
public final class प्रयोगकर्ता {
    public static native int 파일서술자열기(int[] नाम, int सेटिङ);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int मान);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] नाम, int[] लगत);
    public static native int लेख्नुहोस्_फाइल(int[] नाम, int[] लगत, int लम्बाइ_मान);
    public static native int लेख्नुहोस्(String पाठ);
    public static native int लेख्नुहोस्_वर्ण_मान(int मान);
    public static native int 인수개수();
    public static native String तर्क(int अनुक्रमणिका);
    public static native int 도구번호();
    public static native int 화면연결(int कार्य, int अनुक्रमणिका, int 가, int 나, int 다, int 라);
    public static native int 화면글(int अनुक्रमणिका, int[] पाठ, int लम्बाइ_मान);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int प्रवाह_नियन्त्रण(int कार्य, int 서술자, int मान);
    public static native int कनेक्ट_प्रवाह(int 서술자, int ठेगाना, int पोर्ट_मान);
    public static native int सिर्जना_सञ्जाल(int पोर्ट_मान);
    public static native int पठाउनुहोस्_सञ्जाल(int 서술자, int ठेगाना, int पोर्ट_मान, int[] लगत, int लम्बाइ_मान);
    public static native int 통신받기(int 서술자, int[] लगत, int लम्बाइ_मान);
    public static native int सञ्जाल_पोर्ट(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int 사각형(int 가로, int ठाडो_राख्नुहोस्, int 폭, int 높이, int 색);
}
