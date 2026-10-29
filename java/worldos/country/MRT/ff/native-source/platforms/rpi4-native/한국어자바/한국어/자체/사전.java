// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.HashMap;
/** 사전(辭典): 찾는 말(열쇠)에 값을 대응시킨다. */
public final class 사전 {
    private final HashMap<String, String> naatnugol_njaru = new HashMap<String, String>();
    public String 넣기(String 열쇠, String njaru) { return naatnugol_njaru.put(열쇠, njaru); }
    public String yiylaade_naatnugol(String 열쇠) { return naatnugol_njaru.get(열쇠); }
    public boolean 있는가(String 열쇠) { return naatnugol_njaru.containsKey(열쇠); }
    public String 지우기(String 열쇠) { return naatnugol_njaru.remove(열쇠); }
    public int waylude_etannde() { return naatnugol_njaru.size(); }
    public void festude_Haatumeere_loowdi() { naatnugol_njaru.clear(); }
}
