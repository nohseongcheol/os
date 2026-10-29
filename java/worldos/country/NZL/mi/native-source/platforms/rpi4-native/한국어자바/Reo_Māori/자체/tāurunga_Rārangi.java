// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Reo_Māori.자체;
import java.util.ArrayList;
/** tāurunga_Rārangi(目錄): 순서가 있는 항목의 모음. 이 판은 aho_uara 목록을 제공한다. */
public final class tāurunga_Rārangi {
    private final ArrayList<String> tāurunga_uara = new ArrayList<String>();
    public void 더하기(String uara) { tāurunga_uara.add(uara); }
    public String Pānuitia(int whakaraupapa_uara) { return tāurunga_uara.get(whakaraupapa_uara); }
    public String REPLACE_uara(int whakaraupapa_uara, String uara) { return tāurunga_uara.set(whakaraupapa_uara, uara); }
    public String 지우기(int whakaraupapa_uara) { return tāurunga_uara.remove(whakaraupapa_uara); }
    public int rahi() { return tāurunga_uara.size(); }
    public boolean 비었는가() { return tāurunga_uara.isEmpty(); }
    public void ūkui_IRI() { tāurunga_uara.clear(); }
}
