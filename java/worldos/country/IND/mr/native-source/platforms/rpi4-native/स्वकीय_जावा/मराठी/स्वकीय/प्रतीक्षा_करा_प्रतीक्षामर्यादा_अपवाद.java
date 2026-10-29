// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package मराठी.स्वकीय;

/** मराठी API मधून घोषित करता येणारा, फेकता येणारा आणि पकडता येणारा प्रतीक्षा_करा_प्रतीक्षामर्यादा_अपवाद अपवाद. */
public class प्रतीक्षा_करा_प्रतीक्षामर्यादा_अपवाद extends इनपुट_आउटपुट_अपवाद {
    public प्रतीक्षा_करा_प्रतीक्षामर्यादा_अपवाद() { super(); }
    public प्रतीक्षा_करा_प्रतीक्षामर्यादा_अपवाद(String वर्णन) { super(वर्णन); }
    public String वर्णन() { return getMessage(); }
}
