// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.HashMap;
/** لغت(辭典): 찾는 لفظ_متن(열쇠)에 값을 대응시킨다. */
public final class لغت {
    private final HashMap<String, String> داخلہ_قدر = new HashMap<String, String>();
    public String 넣기(String 열쇠, String قدر) { return داخلہ_قدر.put(열쇠, قدر); }
    public String ڈھونڈو_داخلہ(String 열쇠) { return داخلہ_قدر.get(열쇠); }
    public boolean 있는가(String 열쇠) { return داخلہ_قدر.containsKey(열쇠); }
    public String 지우기(String 열쇠) { return داخلہ_قدر.remove(열쇠); }
    public int سائز() { return داخلہ_قدر.size(); }
    public void صاف_کرو_مواد() { داخلہ_قدر.clear(); }
}
