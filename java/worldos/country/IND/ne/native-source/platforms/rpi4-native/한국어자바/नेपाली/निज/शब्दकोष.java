// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package नेपाली.निज;
import java.util.HashMap;
/** शब्दकोष(辭典): 찾는 शब्द_पाठ(열쇠)에 값을 대응시킨다. */
public final class शब्दकोष {
    private final HashMap<String, String> प्रविष्टि_मान = new HashMap<String, String>();
    public String 넣기(String 열쇠, String मान) { return प्रविष्टि_मान.put(열쇠, मान); }
    public String खोज_गर्नुहोस्_प्रविष्टि(String 열쇠) { return प्रविष्टि_मान.get(열쇠); }
    public boolean 있는가(String 열쇠) { return प्रविष्टि_मान.containsKey(열쇠); }
    public String 지우기(String 열쇠) { return प्रविष्टि_मान.remove(열쇠); }
    public int आकार() { return प्रविष्टि_मान.size(); }
    public void खाली_गर्नुहोस्_टिओसी() { प्रविष्टि_मान.clear(); }
}
