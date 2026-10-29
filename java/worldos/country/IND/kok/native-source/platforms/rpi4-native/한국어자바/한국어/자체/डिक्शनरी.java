// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.HashMap;
/** डिक्शनरी(辭典): 찾는 Word_SMS(열쇠)에 값을 대응시킨다. */
public final class डिक्शनरी {
    private final HashMap<String, String> प्रवेश_मोल = new HashMap<String, String>();
    public String 넣기(String 열쇠, String मोल) { return प्रवेश_मोल.put(열쇠, मोल); }
    public String FIND_प्रवेश(String 열쇠) { return प्रवेश_मोल.get(열쇠); }
    public boolean 있는가(String 열쇠) { return प्रवेश_मोल.containsKey(열쇠); }
    public String 지우기(String 열쇠) { return प्रवेश_मोल.remove(열쇠); }
    public int आवाठ() { return प्रवेश_मोल.size(); }
    public void पुसचें_TOC() { प्रवेश_मोल.clear(); }
}
