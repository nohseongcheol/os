// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package भारत.JIndOS.सिस्टम_कॉल_आवाहन;

public final class सिस्टम_तपशील {
    private final String सिस्टम_नाव;
    private final String नोड_नाव;
    private final String भाषावृत्ती_मूल्य;
    private final String आवृत्ती_मूल्य;
    private final String मशीन;

    public सिस्टम_तपशील(String सिस्टम_नाव, String नोड_नाव, String भाषावृत्ती_मूल्य, String आवृत्ती_मूल्य, String मशीन) {
        this.सिस्टम_नाव = सिस्टम_नाव;
        this.नोड_नाव = नोड_नाव;
        this.भाषावृत्ती_मूल्य = भाषावृत्ती_मूल्य;
        this.आवृत्ती_मूल्य = आवृत्ती_मूल्य;
        this.मशीन = मशीन;
    }

    public String सिस्टम_नाव() { return सिस्टम_नाव; }
    public String नोड_नाव() { return नोड_नाव; }
    public String भाषावृत्ती_मूल्य() { return भाषावृत्ती_मूल्य; }
    public String आवृत्ती_मूल्य() { return आवृत्ती_मूल्य; }
    public String मशीन() { return मशीन; }
}
