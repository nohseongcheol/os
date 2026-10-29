// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package मराठी.स्वकीय;
import java.util.HashMap;
/** शोधकळीला मूल्य जोडते. */
public final class शब्दकोश {
    private final HashMap<String, String> प्रविष्टी_मूल्य = new HashMap<String, String>();
    public String ठेवा_मूल्य(String कळ_सामग्री, String मूल्य) { return प्रविष्टी_मूल्य.put(कळ_सामग्री, मूल्य); }
    public String प्रविष्टी_शोधा(String कळ_सामग्री) { return प्रविष्टी_मूल्य.get(कळ_सामग्री); }
    public boolean करते_अस्तित्व(String कळ_सामग्री) { return प्रविष्टी_मूल्य.containsKey(कळ_सामग्री); }
    public String पुसा_प्रविष्टी(String कळ_सामग्री) { return प्रविष्टी_मूल्य.remove(कळ_सामग्री); }
    public int आकार() { return प्रविष्टी_मूल्य.size(); }
    public void साफ_करा_सामुग्री() { प्रविष्टी_मूल्य.clear(); }
}
