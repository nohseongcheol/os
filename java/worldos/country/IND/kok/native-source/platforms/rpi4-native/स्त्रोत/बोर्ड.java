// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 यंत्र 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class बोर्ड {
    public static native int 표시화소읽기(int 가로, int उबें_स्थिती);
    public static native void बरोवचें_प्रदर्शन_पिक्सॅल(int 가로, int उबें_स्थिती, int 색);
    public static native int छायांकन(int 종류, int कृती);
    public static native void सोपोवचें_दुर्मीळ_आदेश(int स्थिती_मोल_e10195a1);
    public static native void 원격대기(int स्थिती_मोल_e10195a1);
    public static native void 직렬쓰기(int मोल);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int CPU_अनुमती_पांवडो();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int उबें_स्थिती, int 색);
    public static native void YIELD_CPU();
    public static native int निर्माण_करचें_कार्य(int INDEX);
    public static native int कार्य_स्थिती(int INDEX);
    public static native void थांबचें(int स्थिती_मोल_e10195a1);
    public static native int 씨플러스시험();
    public static native int चलोवप_उपेगकर्तो_एप्लिकेशन(int INDEX);
    public static native int तपासचें_उपेगकर्तो_एप्लिकेशन();
    public static native int 인수준비(int आयटम_COUNT);
    public static native int पाळो_दिवचो_उपेगकर्तो_फायल();
    public static native int 리눅스파일실행();
    public static native int युक्तीवाद_बायट(int INDEX, int स्थिती, int मोल);
    public static native int टर्मिनल(int कृती);
    public static native int नियंत्रण_उपेगकर्तो_एप्लिकेशन(int कृती);
    public static native void 입출력전환(int कृती);
    public static native int फायल_ट्रान्सफर_सेवा(int कृती);
    public static native int नॅटवर्क_स्थिती(int प्रवेश_मोल, int INDEX);
    public static native int नॅटवर्क_मांडावळी(int कृती, int नामो, int मास्क_मोल, int गेटवे_मोल);
    public static native int 응답보내기(int नामो, int क्रम_मोल);
    public static native int 응답읽기(int प्रवेश_मोल);
    public static native int क्वॅरी_प्रणाली(int प्रवेश_मोल, int INDEX);
    public static native void 전원끄기();
}
