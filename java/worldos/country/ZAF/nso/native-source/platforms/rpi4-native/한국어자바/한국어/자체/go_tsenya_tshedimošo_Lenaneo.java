// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.ArrayList;
/** go_tsenya_tshedimošo_Lenaneo(目錄): 순서가 있는 항목의 모음. 이 판은 molokoloko_boleng 목록을 제공한다. */
public final class go_tsenya_tshedimošo_Lenaneo {
    private final ArrayList<String> go_tsenya_tshedimošo_boleng = new ArrayList<String>();
    public void 더하기(String boleng) { go_tsenya_tshedimošo_boleng.add(boleng); }
    public String Bala(int thulaganyo_boleng) { return go_tsenya_tshedimošo_boleng.get(thulaganyo_boleng); }
    public String fetola_boleng(int thulaganyo_boleng, String boleng) { return go_tsenya_tshedimošo_boleng.set(thulaganyo_boleng, boleng); }
    public String 지우기(int thulaganyo_boleng) { return go_tsenya_tshedimošo_boleng.remove(thulaganyo_boleng); }
    public int Bogolo() { return go_tsenya_tshedimošo_boleng.size(); }
    public boolean 비었는가() { return go_tsenya_tshedimošo_boleng.isEmpty(); }
    public void tloša_TOC() { go_tsenya_tshedimošo_boleng.clear(); }
}
