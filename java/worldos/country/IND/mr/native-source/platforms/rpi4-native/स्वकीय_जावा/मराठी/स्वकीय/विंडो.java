// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package मराठी.स्वकीय;
/** स्वतःच्या JVM आणि केंद्रकाच्या खिडकी व्यवस्थापनाशी थेट जोडलेली खिडकी. */
public final class विंडो extends पडदा_घटक {
    public विंडो(String विंडो_शीर्षक, int रुंदी_विस्तार, int उंची_मूल्य) {
        throw new राज्य_अपवाद("स्वतःच्या JVM मध्ये मराठी API मधून खिडकी तयार करण्याची सोय आवश्यक आहे.");
    }
    public native void जोडा_घटक(पडदा_घटक घटक_मूल्य);
    public native void विंडो_शो();
    public native void बंद_करा();
    public native boolean आहे_दृश्य();
}
