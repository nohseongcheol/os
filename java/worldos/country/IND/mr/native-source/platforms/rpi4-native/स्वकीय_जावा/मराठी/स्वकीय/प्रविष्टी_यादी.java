// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package मराठी.स्वकीय;
import java.util.ArrayList;
/** क्रमबद्ध घटकांचा संग्रह. ही आवृत्ती अक्षरमालांच्या याद्या देते. */
public final class प्रविष्टी_यादी {
    private final ArrayList<String> प्रविष्टी_मूल्य = new ArrayList<String>();
    public void जोडा_मूल्ये(String मूल्य) { प्रविष्टी_मूल्य.add(मूल्य); }
    public String वाचन(int क्रम_मूल्य) { return प्रविष्टी_मूल्य.get(क्रम_मूल्य); }
    public String बदलावे_मूल्य(int क्रम_मूल्य, String मूल्य) { return प्रविष्टी_मूल्य.set(क्रम_मूल्य, मूल्य); }
    public String पुसा_प्रविष्टी(int क्रम_मूल्य) { return प्रविष्टी_मूल्य.remove(क्रम_मूल्य); }
    public int आकार() { return प्रविष्टी_मूल्य.size(); }
    public boolean आहे_रिक्त_मूल्य() { return प्रविष्टी_मूल्य.isEmpty(); }
    public void साफ_करा_सामुग्री() { प्रविष्टी_मूल्य.clear(); }
}
