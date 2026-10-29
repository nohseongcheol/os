// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package हिंदी.निज;
import java.util.ArrayList;
/** एन्ट्री_सूची(目錄): 순서가 있는 항목의 모음. 이 판은 स्ट्रिंग_मान 목록을 제공한다. */
public final class एन्ट्री_सूची {
    private final ArrayList<String> एन्ट्री_मान = new ArrayList<String>();
    public void 더하기(String मान) { एन्ट्री_मान.add(मान); }
    public String पढ़ें(int क्रम_मान) { return एन्ट्री_मान.get(क्रम_मान); }
    public String बदलें_मान(int क्रम_मान, String मान) { return एन्ट्री_मान.set(क्रम_मान, मान); }
    public String मिटाएँ_एन्ट्री(int क्रम_मान) { return एन्ट्री_मान.remove(क्रम_मान); }
    public int आकार() { return एन्ट्री_मान.size(); }
    public boolean 비었는가() { return एन्ट्री_मान.isEmpty(); }
    public void साफ_करें_सामग्री() { एन्ट्री_मान.clear(); }
}
