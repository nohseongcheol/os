// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package नेपाली.निज;
import java.util.ArrayList;
/** प्रविष्टि_सूची(目錄): 순서가 있는 항목의 모음. 이 판은 स्ट्रिङ_मान 목록을 제공한다. */
public final class प्रविष्टि_सूची {
    private final ArrayList<String> प्रविष्टि_मान = new ArrayList<String>();
    public void 더하기(String मान) { प्रविष्टि_मान.add(मान); }
    public String पढनुहोस्(int अर्डर_मान) { return प्रविष्टि_मान.get(अर्डर_मान); }
    public String बदल्नुहोस्_मान(int अर्डर_मान, String मान) { return प्रविष्टि_मान.set(अर्डर_मान, मान); }
    public String 지우기(int अर्डर_मान) { return प्रविष्टि_मान.remove(अर्डर_मान); }
    public int आकार() { return प्रविष्टि_मान.size(); }
    public boolean 비었는가() { return प्रविष्टि_मान.isEmpty(); }
    public void खाली_गर्नुहोस्_टिओसी() { प्रविष्टि_मान.clear(); }
}
