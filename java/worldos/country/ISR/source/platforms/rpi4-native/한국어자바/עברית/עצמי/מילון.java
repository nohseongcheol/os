// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package עברית.עצמי;
import java.util.HashMap;
/** מילון(辭典): 찾는 מילים_טקסט(열쇠)에 값을 대응시킨다. */
public final class מילון {
    private final HashMap<String, String> ערך_ערך = new HashMap<String, String>();
    public String 넣기(String 열쇠, String ערך) { return ערך_ערך.put(열쇠, ערך); }
    public String חפש_ערך_832f7474(String 열쇠) { return ערך_ערך.get(열쇠); }
    public boolean 있는가(String 열쇠) { return ערך_ערך.containsKey(열쇠); }
    public String מחק_ערך(String 열쇠) { return ערך_ערך.remove(열쇠); }
    public int גודל() { return ערך_ערך.size(); }
    public void נקה_תוכן() { ערך_ערך.clear(); }
}
