// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros वापरकर्ता ELF साठीच API; Linux/JVM साठी JNI किंवा java.net API नाही. */
public final class प्रयोक्ता {
    public static native int संचिका_विवरणक_उघडा(int[] संचिका_प्रविष्टी_नाव, int सेटिंग्ज_उघडा);
    public static native int एक_संचिका_बाइट_वाचा(int संचिका_विवरणक);
    public static native int एक_संचिका_बाइट_लिहा(int संचिका_विवरणक, int बाइट_मूल्य);
    public static native int संचिका_विवरणक_मिटवा(int संचिका_विवरणक);
    public static native int स्थिरकरा_फाईल_संग्रहण(int संचिका_विवरणक);
    public static native int संचिका_वाचा(int[] नाव, int[] डेटा);
    public static native int वर्ण_मूल्य_लिहा(int वर्ण);
    public static native int संचिका_लिहा(int[] नाव, int[] डेटा, int लांबी_मूल्य);
    public static native int लेखन(String सामुग्री_मूल्य);
    public static native int वितर्क_संख्या_e5e1cf1c();
    public static native String बाबी(int अनुक्रमणिका);
    public static native int निष्पादन_परवानगी();
    public static native int संचारजाळे_उघडा(int स्थानिक_पॉर्ट);
    public static native int डेटा_पाठवा(int हाताळा_मूल्य, int पत्ता, int गंतव्यस्थान_पॉर्ट, int[] डेटा, int लांबी_मूल्य);
    public static native int डेटा_स्वीकारा(int हाताळा_मूल्य, int[] डेटा, int मर्यादा_मिलिसेकंद);
    public static native int संचारजाळे_मिटवा(int हाताळा_मूल्य);
    public static native int स्वकीय_पत्ता();
    public static native int पाठवलेले_पत्ता(int हाताळा_मूल्य);
    public static native int पाठवलेले_पॉर्ट(int हाताळा_मूल्य);
}
