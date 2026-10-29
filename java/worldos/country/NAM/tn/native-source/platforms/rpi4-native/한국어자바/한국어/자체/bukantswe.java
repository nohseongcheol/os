// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.HashMap;
/** bukantswe(辭典): 찾는 Lefoko_SMS(열쇠)에 값을 대응시킨다. */
public final class bukantswe {
    private final HashMap<String, String> tsenyo_Boleng = new HashMap<String, String>();
    public String 넣기(String 열쇠, String Boleng) { return tsenyo_Boleng.put(열쇠, Boleng); }
    public String batla_tsenyo(String 열쇠) { return tsenyo_Boleng.get(열쇠); }
    public boolean 있는가(String 열쇠) { return tsenyo_Boleng.containsKey(열쇠); }
    public String 지우기(String 열쇠) { return tsenyo_Boleng.remove(열쇠); }
    public int lekanya() { return tsenyo_Boleng.size(); }
    public void phimola_TOC() { tsenyo_Boleng.clear(); }
}
