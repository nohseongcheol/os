// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 यंत्र 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class बोर्ड {
    public static native int प्रदर्शितचित्रांशपढ़ना(int 가로, int अनुलंब_पद);
    public static native void प्रदर्शितचित्रांशलिखना(int 가로, int अनुलंब_पद, int 색);
    public static native int शैडोइंग(int 종류, int क्रिया);
    public static native void समाप्त_करें_दूरस्थ_आदेश(int अवस्था_मान);
    public static native void दूरस्थ_प्रतीक्षा_करें(int अवस्था_मान);
    public static native void 직렬쓰기(int मान);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int प्रोसेसर_अनुमति_लेवल();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int अनुलंब_पद, int 색);
    public static native void स्थगित_करें_संसाधक();
    public static native int बनाएँ_कार्य(int इंडेक्स);
    public static native int कार्य_अवस्था(int इंडेक्स);
    public static native void रोकें(int अवस्था_मान);
    public static native int 씨플러스시험();
    public static native int चलाएँ_उपयोगकर्ता_ऐप(int इंडेक्स);
    public static native int जाँचें_उपयोगकर्ता_ऐप();
    public static native int 인수준비(int 개수);
    public static native int निष्पादित_करें_उपयोगकर्ता_फ़ाइल();
    public static native int 리눅스파일실행();
    public static native int तर्क_बाइट(int इंडेक्स, int स्थान, int मान);
    public static native int आदेशपटल(int क्रिया);
    public static native int नियंत्रण_उपयोगकर्ता_ऐप(int क्रिया);
    public static native void 입출력전환(int क्रिया);
    public static native int फ़ाइल_स्थानांतरण_सेवा(int क्रिया);
    public static native int नेटवर्क_स्थिति(int एन्ट्री_मान, int इंडेक्स);
    public static native int नेटवर्क_सेटिंग(int क्रिया, int पता, int मास्क_मान, int गेटवे_मान);
    public static native int भेजें_प्रतिसाद(int पता, int क्रम_मान);
    public static native int पढें_प्रतिसाद(int एन्ट्री_मान);
    public static native int क्वेरी_सिस्टम(int एन्ट्री_मान, int इंडेक्स);
    public static native void 전원끄기();
}
