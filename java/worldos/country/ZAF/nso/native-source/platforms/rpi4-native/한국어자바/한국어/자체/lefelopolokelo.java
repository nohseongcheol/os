// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.HashMap;
/** lefelopolokelo(辭典): 찾는 Thalokontšu_SMS(열쇠)에 값을 대응시킨다. */
public final class lefelopolokelo {
    private final HashMap<String, String> go_tsenya_tshedimošo_boleng = new HashMap<String, String>();
    public String 넣기(String 열쇠, String boleng) { return go_tsenya_tshedimošo_boleng.put(열쇠, boleng); }
    public String hwetša_go_tsenya_tshedimošo(String 열쇠) { return go_tsenya_tshedimošo_boleng.get(열쇠); }
    public boolean 있는가(String 열쇠) { return go_tsenya_tshedimošo_boleng.containsKey(열쇠); }
    public String 지우기(String 열쇠) { return go_tsenya_tshedimošo_boleng.remove(열쇠); }
    public int Bogolo() { return go_tsenya_tshedimošo_boleng.size(); }
    public void tloša_TOC() { go_tsenya_tshedimošo_boleng.clear(); }
}
