// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 यंत्रसीमा. दर्शक कापून Java int मध्ये देऊ नये. */
public final class बोर्ड {
    public static native int प्रदर्शन_पिक्सेल_वाचा(int आडवे_स्थान, int अनुलंब_स्थान);
    public static native void प्रदर्शन_पिक्सेल_लिहा(int आडवे_स्थान, int अनुलंब_स्थान, int रंग_मूल्य);
    public static native int शॅडोइंग(int प्रकार_मूल्य, int कृती);
    public static native void शेवट_करा_दूरस्_थ_आज्ञा(int राज्य_मूल्य);
    public static native void दूरस्_थ_प्रतीक्षा_करा(int राज्य_मूल्य);
    public static native void अनुक्रमिक_लिहा(int मूल्य);
    public static native int अनुक्रमिक_वाचा();
    public static native int मिलिसेकंद();
    public static native int प्रोसेसर_विशेषाधिकार_स्तर();
    public static native int तयार_करणे_पडदा();
    public static native int पडदा_रुंदी();
    public static native int पडदा_उंची();
    public static native void ठेवा_पडदा_पिक्सेल(int आडवे_स्थान, int अनुलंब_स्थान, int रंग_मूल्य);
    public static native void निलंबित_करा_प्रोसेसर();
    public static native int कार्य_तयार_करा(int अनुक्रमणिका);
    public static native int कार्य_राज्य(int अनुक्रमणिका);
    public static native void थांबा(int राज्य_मूल्य);
    public static native int सीप्लसप्लस_चाचणी();
    public static native int रन_प्रयोक्ता_अनुप्रयोग(int अनुक्रमणिका);
    public static native int प्रयोक्ता_अनुप्रयोग_तपासा();
    public static native int तयार_करणे_वितर्क(int आयटम_संख्या);
    public static native int प्रयोक्ता_संचिका_कार्यवाही_करा();
    public static native int लिनक्स_संचिका_कार्यवाही_करा();
    public static native int वितर्क_बाइट(int अनुक्रमणिका, int जागा, int मूल्य);
    public static native int टर्मिनल(int कृती);
    public static native int नियंत्रण_प्रयोक्ता_अनुप्रयोग(int कृती);
    public static native void स्विच_आदानप्रदान(int कृती);
    public static native int संचिका_स्थानांतर_सेवा(int कृती);
    public static native int संचारजाळे_राज्य(int प्रविष्टी_मूल्य, int अनुक्रमणिका);
    public static native int संचारजाळे_सेटिंग्ज(int कृती, int पत्ता, int मास्क_मूल्य, int गेटवे_मूल्य);
    public static native int प्रतिसाद_पाठवा(int पत्ता, int क्रम_मूल्य);
    public static native int प्रतिसाद_वाचा(int प्रविष्टी_मूल्य);
    public static native int क्वेरी_सिस्टम(int प्रविष्टी_मूल्य, int अनुक्रमणिका);
    public static native void पॉवर_बंद();
}
