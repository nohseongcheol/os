// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package বাংলা.নিজ;
import java.util.HashMap;
/** অভিধান(辭典): 찾는 শব্দ_পাঠ(열쇠)에 값을 대응시킨다. */
public final class অভিধান {
    private final HashMap<String, String> ভুক্তি_মান = new HashMap<String, String>();
    public String 넣기(String 열쇠, String মান) { return ভুক্তি_মান.put(열쇠, মান); }
    public String খোঁজা_ভুক্তি(String 열쇠) { return ভুক্তি_মান.get(열쇠); }
    public boolean 있는가(String 열쇠) { return ভুক্তি_মান.containsKey(열쇠); }
    public String মুছুন_ভুক্তি(String 열쇠) { return ভুক্তি_মান.remove(열쇠); }
    public int আকার() { return ভুক্তি_মান.size(); }
    public void মুছে_দিন_সূচী() { ভুক্তি_মান.clear(); }
}
