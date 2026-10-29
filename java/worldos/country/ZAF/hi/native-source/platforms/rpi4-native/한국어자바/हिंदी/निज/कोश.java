// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package हिंदी.निज;
import java.util.HashMap;
/** कोश(辭典): 찾는 शब्द_पाठ(열쇠)에 값을 대응시킨다. */
public final class कोश {
    private final HashMap<String, String> एन्ट्री_मान = new HashMap<String, String>();
    public String 넣기(String 열쇠, String मान) { return एन्ट्री_मान.put(열쇠, मान); }
    public String खोजें_एन्ट्री(String 열쇠) { return एन्ट्री_मान.get(열쇠); }
    public boolean 있는가(String 열쇠) { return एन्ट्री_मान.containsKey(열쇠); }
    public String मिटाएँ_एन्ट्री(String 열쇠) { return एन्ट्री_मान.remove(열쇠); }
    public int आकार() { return एन्ट्री_मान.size(); }
    public void साफ_करें_सामग्री() { एन्ट्री_मान.clear(); }
}
