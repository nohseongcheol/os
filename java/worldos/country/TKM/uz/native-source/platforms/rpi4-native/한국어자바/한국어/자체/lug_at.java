// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.HashMap;
/** lug_at(辭典): 찾는 Word_SMS(열쇠)에 값을 대응시킨다. */
public final class lug_at {
    private final HashMap<String, String> kiritish_VALUE = new HashMap<String, String>();
    public String 넣기(String 열쇠, String VALUE) { return kiritish_VALUE.put(열쇠, VALUE); }
    public String FIND_kiritish(String 열쇠) { return kiritish_VALUE.get(열쇠); }
    public boolean 있는가(String 열쇠) { return kiritish_VALUE.containsKey(열쇠); }
    public String tozalash_kiritish(String 열쇠) { return kiritish_VALUE.remove(열쇠); }
    public int Hajmi() { return kiritish_VALUE.size(); }
    public void tozalamoq_TOC() { kiritish_VALUE.clear(); }
}
