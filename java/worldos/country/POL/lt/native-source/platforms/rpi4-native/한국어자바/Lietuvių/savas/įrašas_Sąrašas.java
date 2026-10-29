// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lietuvių.savas;
import java.util.ArrayList;
/** įrašas_Sąrašas(目錄): 순서가 있는 항목의 모음. 이 판은 eilutė_VALUE 목록을 제공한다. */
public final class įrašas_Sąrašas {
    private final ArrayList<String> įrašas_VALUE = new ArrayList<String>();
    public void 더하기(String VALUE) { įrašas_VALUE.add(VALUE); }
    public String Skaitymas(int tvarka_VALUE) { return įrašas_VALUE.get(tvarka_VALUE); }
    public String REPLACE_VALUE(int tvarka_VALUE, String VALUE) { return įrašas_VALUE.set(tvarka_VALUE, VALUE); }
    public String ištrinti_įrašas(int tvarka_VALUE) { return įrašas_VALUE.remove(tvarka_VALUE); }
    public int Dydis() { return įrašas_VALUE.size(); }
    public boolean 비었는가() { return įrašas_VALUE.isEmpty(); }
    public void apmokėti_Turinys() { įrašas_VALUE.clear(); }
}
