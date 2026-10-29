// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Gaeilge.자체;
import java.util.ArrayList;
/** iontráil_Liosta(目錄): 순서가 있는 항목의 모음. 이 판은 teaghrán_VALUE 목록을 제공한다. */
public final class iontráil_Liosta {
    private final ArrayList<String> iontráil_VALUE = new ArrayList<String>();
    public void 더하기(String VALUE) { iontráil_VALUE.add(VALUE); }
    public String Léigh(int ord_VALUE) { return iontráil_VALUE.get(ord_VALUE); }
    public String REPLACE_VALUE(int ord_VALUE, String VALUE) { return iontráil_VALUE.set(ord_VALUE, VALUE); }
    public String 지우기(int ord_VALUE) { return iontráil_VALUE.remove(ord_VALUE); }
    public int Méid() { return iontráil_VALUE.size(); }
    public boolean teicneolaíocht_faisnéise_folamh_VALUE() { return iontráil_VALUE.isEmpty(); }
    public void glan_TOC() { iontráil_VALUE.clear(); }
}
