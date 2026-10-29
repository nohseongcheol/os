// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.HashMap;
/** ڊڪشنري(辭典): 찾는 ورڊ_متن(열쇠)에 값을 대응시킨다. */
public final class ڊڪشنري {
    private final HashMap<String, String> داخلا_قدر = new HashMap<String, String>();
    public String 넣기(String 열쇠, String قدر) { return داخلا_قدر.put(열쇠, قدر); }
    public String ڳوليو_داخلا(String 열쇠) { return داخلا_قدر.get(열쇠); }
    public boolean 있는가(String 열쇠) { return داخلا_قدر.containsKey(열쇠); }
    public String 지우기(String 열쇠) { return داخلا_قدر.remove(열쇠); }
    public int سائيز() { return داخلا_قدر.size(); }
    public void صاف_ڪريو_موادَ() { داخلا_قدر.clear(); }
}
