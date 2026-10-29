// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 मेशिन 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class बोर्ड {
    public static native int 표시화소읽기(int 가로, int ठाडो_राख्नुहोस्);
    public static native void लेख्नुहोस्_प्रदर्शन_पेल(int 가로, int ठाडो_राख्नुहोस्, int 색);
    public static native int स्याडोइङ(int 종류, int कार्य);
    public static native void समाप्त_गर्नुहोस्_दूर_आदेश(int स्थिति_मान);
    public static native void 원격대기(int स्थिति_मान);
    public static native void 직렬쓰기(int मान);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int प्रोसेसर_अनुमति_स्तर();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int ठाडो_राख्नुहोस्, int 색);
    public static native void स्थगन_गर्नुहोस्_प्रोसेसर();
    public static native int सिर्जना_कार्य(int अनुक्रमणिका);
    public static native int कार्य_स्थिति(int अनुक्रमणिका);
    public static native void रोक्नुहोस्(int स्थिति_मान);
    public static native int 씨플러스시험();
    public static native int चलाउनुहोस्_प्रयोगकर्ता_अनुप्रयोग(int अनुक्रमणिका);
    public static native int चेक_प्रयोगकर्ता_अनुप्रयोग();
    public static native int 인수준비(int 개수);
    public static native int कार्यान्वयन_गर्नुहोस्_प्रयोगकर्ता_फाइल();
    public static native int 리눅스파일실행();
    public static native int तर्क_बाइट(int अनुक्रमणिका, int स्थिति, int मान);
    public static native int टर्मिनल(int कार्य);
    public static native int नियन्त्रण_प्रयोगकर्ता_अनुप्रयोग(int कार्य);
    public static native void 입출력전환(int कार्य);
    public static native int फाइल_ट्रान्सफर_सेवा(int कार्य);
    public static native int सञ्जाल_स्थिति(int प्रविष्टि_मान, int अनुक्रमणिका);
    public static native int सञ्जाल_सेटिङहरू(int कार्य, int ठेगाना, int मकुन्डो_मान, int गेटवे_मान);
    public static native int 응답보내기(int ठेगाना, int अर्डर_मान);
    public static native int 응답읽기(int प्रविष्टि_मान);
    public static native int क्वेरी_प्रणाली(int प्रविष्टि_मान, int अनुक्रमणिका);
    public static native void 전원끄기();
}
