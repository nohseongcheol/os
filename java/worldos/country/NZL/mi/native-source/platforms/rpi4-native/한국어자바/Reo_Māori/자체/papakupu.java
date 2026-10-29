// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Reo_Māori.자체;
import java.util.HashMap;
/** papakupu(辭典): 찾는 Word_TEXT(열쇠)에 값을 대응시킨다. */
public final class papakupu {
    private final HashMap<String, String> tāurunga_uara = new HashMap<String, String>();
    public String 넣기(String 열쇠, String uara) { return tāurunga_uara.put(열쇠, uara); }
    public String FIND_tāurunga(String 열쇠) { return tāurunga_uara.get(열쇠); }
    public boolean 있는가(String 열쇠) { return tāurunga_uara.containsKey(열쇠); }
    public String 지우기(String 열쇠) { return tāurunga_uara.remove(열쇠); }
    public int rahi() { return tāurunga_uara.size(); }
    public void ūkui_IRI() { tāurunga_uara.clear(); }
}
