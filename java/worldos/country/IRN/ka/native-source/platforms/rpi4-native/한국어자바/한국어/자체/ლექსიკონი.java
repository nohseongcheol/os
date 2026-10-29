// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.HashMap;
/** ლექსიკონი(辭典): 찾는 სიტყვები_ტექსტი(열쇠)에 값을 대응시킨다. */
public final class ლექსიკონი {
    private final HashMap<String, String> შენატანი_მნიშვნელობა = new HashMap<String, String>();
    public String 넣기(String 열쇠, String მნიშვნელობა) { return შენატანი_მნიშვნელობა.put(열쇠, მნიშვნელობა); }
    public String ძებნა_შენატანი(String 열쇠) { return შენატანი_მნიშვნელობა.get(열쇠); }
    public boolean 있는가(String 열쇠) { return შენატანი_მნიშვნელობა.containsKey(열쇠); }
    public String 지우기(String 열쇠) { return შენატანი_მნიშვნელობა.remove(열쇠); }
    public int ზომა() { return შენატანი_მნიშვნელობა.size(); }
    public void გასუფთავება_სარჩევი() { შენატანი_მნიშვნელობა.clear(); }
}
