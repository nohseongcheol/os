// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.HashMap;
/** lüğət(辭典): 찾는 Söz_SMS(열쇠)에 값을 대응시킨다. */
public final class lüğət {
    private final HashMap<String, String> daxiletmə_VALUE = new HashMap<String, String>();
    public String 넣기(String 열쇠, String VALUE) { return daxiletmə_VALUE.put(열쇠, VALUE); }
    public String FIND_daxiletmə(String 열쇠) { return daxiletmə_VALUE.get(열쇠); }
    public boolean 있는가(String 열쇠) { return daxiletmə_VALUE.containsKey(열쇠); }
    public String silmək_daxiletmə_c8dbc399(String 열쇠) { return daxiletmə_VALUE.remove(열쇠); }
    public int Böyüklük() { return daxiletmə_VALUE.size(); }
    public void təmizləmək_TOC() { daxiletmə_VALUE.clear(); }
}
