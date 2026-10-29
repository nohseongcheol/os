// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 वरील Java साधनांसाठी स्वतंत्र SVC जोडणी. विद्यमान x86 साधनांच्या स्रोतासोबत बांधणी होते. */
public final class प्रयोक्ता {
    public static native int संचिका_विवरणक_उघडा(int[] नाव, int संयोजना);
    public static native int एक_संचिका_बाइट_वाचा(int विवरणक_प्रविष्टी);
    public static native int एक_संचिका_बाइट_लिहा(int विवरणक_प्रविष्टी, int मूल्य);
    public static native int संचिका_विवरणक_मिटवा(int विवरणक_प्रविष्टी);
    public static native int संचिका_वाचा(int[] नाव, int[] डेटा);
    public static native int संचिका_लिहा(int[] नाव, int[] डेटा, int लांबी_मूल्य);
    public static native int लेखन(String पाठ्य);
    public static native int वर्ण_मूल्य_लिहा(int मूल्य);
    public static native int वितर्क_संख्या_e5e1cf1c();
    public static native String बाबी(int अनुक्रमणिका);
    public static native int साधन_संख्या();
    public static native int पडदा_कनेक्शन(int कृती, int अनुक्रमणिका, int पहिले_संकार्य, int दुसरे_संकार्य, int तिसरे_संकार्य, int चौथे_संकार्य);
    public static native int पडदा_मजकूर(int अनुक्रमणिका, int[] पाठ्य, int लांबी_मूल्य);
    public static native int पडदा_रुंदी();
    public static native int पडदा_उंची();
    public static native int प्रवाह_नियंत्रण(int कृती, int विवरणक_प्रविष्टी, int मूल्य);
    public static native int कनेक्ट_प्रवाह(int विवरणक_प्रविष्टी, int पत्ता, int पॉर्ट_मूल्य);
    public static native int संचारजाळे_उघडा(int पॉर्ट_मूल्य);
    public static native int संचारजाळे_पाठवा(int विवरणक_प्रविष्टी, int पत्ता, int पॉर्ट_मूल्य, int[] डेटा, int लांबी_मूल्य);
    public static native int संचारजाळे_स्वीकारा(int विवरणक_प्रविष्टी, int[] डेटा, int लांबी_मूल्य);
    public static native int संचारजाळे_पॉर्ट(int विवरणक_प्रविष्टी);
    public static native int मिलिसेकंद();
    public static native int प्रतीक्षा_करा_साठी_चित्र();
    public static native int आयत(int आडवे_स्थान, int अनुलंब_स्थान, int रुंदी_विस्तार, int उंची_मूल्य, int रंग_मूल्य);
}
