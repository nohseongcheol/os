// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** केवळ x86 सूचना आणि भौतिक पत्त्यांच्या वापरासाठी संकलकाची मर्यादित native सीमा. */
public final class मोबाइल_मूल्य {
    public static native int संचिका_स्मृती();
    public static native int जावा_संचिका_बंडल();
    public static native int जावा_संचिका_बंडल_आकारा();
    public static native int आदानप्रदान_बाइट_वाचा(int अनुक्रमणिका);
    public static native void आदानप्रदान_बाइट_लिहा(int अनुक्रमणिका, int मूल्य);
    public static native int स्मृती_वाचा(int पत्ता);
    public static native void स्मृती_लिहा(int पत्ता, int मूल्य);
    public static native int प्रणालीप्रारंभ_खूण();
    public static native int प्रणालीप्रारंभ_माहिती();
    public static native int ऍरे_वापर();
    public static native void निलंबित_करा_क्षणभर();
    public static native void थांबवा_निष्पादन();
    public static native void समाप्त_चाचणी(int मूल्य);
    public static native int आदानप्रदान_पूर्णांक_वाचा(int अनुक्रमणिका);
    public static native void आदानप्रदान_पूर्णांक_लिहा(int अनुक्रमणिका, int मूल्य);
    public static native void आदानप्रदान_लघु_लिहा(int अनुक्रमणिका, int मूल्य);
    public static native int आदानप्रदान_लघु_वाचा(int अनुक्रमणिका);
    public static native void तयार_करणे_प्रयोक्ता_अनुप्रयोग();
    public static native void प्रयोक्ता_साफ_करा_सामुग्री();
    public static native int रन_प्रयोक्ता_अनुप्रयोग(int प्रविष्टी_पत्ता, int संकार्य_स्टॅक_पत्ता);
    public static native int मिलिसेकंद();
    public static native int प्रयोक्ता_उर्वरित_मिलिसेकंद();
    public static native int निष्पादनीय_बंडल();
    public static native int निष्पादनीय_बंडल_आकारा();
    public static native int संचारजाळे_स्मृती();
}
