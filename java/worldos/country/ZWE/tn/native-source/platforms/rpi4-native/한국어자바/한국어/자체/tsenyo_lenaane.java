// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.ArrayList;
/** tsenyo_lenaane(目錄): 순서가 있는 항목의 모음. 이 판은 dikwalwa_Boleng 목록을 제공한다. */
public final class tsenyo_lenaane {
    private final ArrayList<String> tsenyo_Boleng = new ArrayList<String>();
    public void 더하기(String Boleng) { tsenyo_Boleng.add(Boleng); }
    public String 읽기(int thulaganyo_Boleng) { return tsenyo_Boleng.get(thulaganyo_Boleng); }
    public String emisetsa_Boleng(int thulaganyo_Boleng, String Boleng) { return tsenyo_Boleng.set(thulaganyo_Boleng, Boleng); }
    public String 지우기(int thulaganyo_Boleng) { return tsenyo_Boleng.remove(thulaganyo_Boleng); }
    public int lekanya() { return tsenyo_Boleng.size(); }
    public boolean 비었는가() { return tsenyo_Boleng.isEmpty(); }
    public void phimola_TOC() { tsenyo_Boleng.clear(); }
}
