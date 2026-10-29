// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package मराठी.स्वकीय;

/** प्रमाणित catch चा अर्थ न बदलता मराठी API सीमेवर प्रमाणित Java त्रुटींचे रूपांतर करते. */
final class रूपांतरकरा_अपवाद {
    private रूपांतरकरा_अपवाद() {}
    public static इनपुट_आउटपुट_अपवाद इनपुट_आउटपुट(java.io.IOException त्रुटी) {
        if (त्रुटी instanceof इनपुट_आउटपुट_अपवाद) return (इनपुट_आउटपुट_अपवाद)त्रुटी;
        if (त्रुटी instanceof java.net.SocketTimeoutException) return new प्रतीक्षा_करा_प्रतीक्षामर्यादा_अपवाद("संपर्काची प्रतीक्षा वेळ संपली.");
        if (त्रुटी instanceof java.net.UnknownHostException) return new पत्ता_लुकअप_अपवाद("पत्ता शोधता आला नाही. सध्या अंकांमधील IPv4 पत्ता वापरा.");
        if (त्रुटी instanceof java.io.FileNotFoundException) return new अनुपस्थित_संचिका_अपवाद("संचिका उघडता आली नाही.");
        if (त्रुटी instanceof java.net.SocketException) return new संचार_अपवाद("संपर्क जोडणी अयशस्वी: " + त्रुटी.getMessage());
        return new इनपुट_आउटपुट_अपवाद("आदानप्रदान क्रिया अयशस्वी: " + त्रुटी.getMessage());
    }
    public static RuntimeException आज्ञा_कार्यवाही_करा(RuntimeException त्रुटी) {
        if (त्रुटी instanceof java.lang.NumberFormatException) return new संख्या_स्वरूप_बिघाड("संख्येचे स्वरूप आणि मर्यादा तपासा.");
        if (त्रुटी instanceof java.lang.IllegalArgumentException) return new अवैध_वितर्क_अपवाद("युक्तिवादाचे मूल्य आणि मर्यादा तपासा.");
        if (त्रुटी instanceof java.lang.ArrayIndexOutOfBoundsException) return new ऍरे_सीमा_अपवाद("सरणीची मर्यादा ओलांडली.");
        if (त्रुटी instanceof java.lang.StringIndexOutOfBoundsException) return new स्ट्रींग_सीमा_अपवाद("अक्षरमालिकेची मर्यादा ओलांडली.");
        if (त्रुटी instanceof java.lang.IndexOutOfBoundsException) return new सीमा_अपवाद("परवानगीची मर्यादा ओलांडली.");
        if (त्रुटी instanceof java.lang.NullPointerException) return new नल_संदर्भ_अपवाद("संदर्भ रिकामा आहे.");
        return new निष्पादन_अपवाद(त्रुटी.getMessage());
    }
}
