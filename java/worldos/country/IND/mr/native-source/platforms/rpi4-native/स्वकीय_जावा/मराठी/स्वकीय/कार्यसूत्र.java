// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package मराठी.स्वकीय;
/** स्वतःच्या JVM च्या नियोजकाने सांभाळलेला कार्यप्रवाह; प्रमाणित Thread भोवती आवरण नाही. */
public final class कार्यसूत्र {
    public कार्यसूत्र(चालवण्यायोग्य_कार्य कार्य_क्रिया) {
        throw new राज्य_अपवाद("स्वतःच्या JVM मध्ये मराठी API मधून कार्यधागे तयार करण्याची सोय आवश्यक आहे.");
    }
    public native void प्रारंभ_कार्य() throws कार्यसूत्र_राज्य_अपवाद;
    public native void प्रतीक्षाकरा() throws प्रतीक्षा_करा_खंडित_अपवाद;
    public native boolean आहे_कार्यरत();
    public static native void निलंबित_करा_कार्य();
}
