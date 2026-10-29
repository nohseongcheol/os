// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package मराठी.स्वकीय;

/** कार्यच संपले असे नसून, धाग्याची वाट पाहणाऱ्या क्रियेत व्यत्यय आला आहे असे दर्शवते. */
public class प्रतीक्षा_करा_खंडित_अपवाद extends java.lang.InterruptedException {
    public प्रतीक्षा_करा_खंडित_अपवाद() { super(); }
    public प्रतीक्षा_करा_खंडित_अपवाद(String वर्णन) { super(वर्णन); }
    public String वर्णन() { return getMessage(); }
}
