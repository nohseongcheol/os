// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.ArrayList;
/** ndebà_ndepụta(目錄): 순서가 있는 항목의 모음. 이 판은 ùsòròokwū_valuu 목록을 제공한다. */
public final class ndebà_ndepụta {
    private final ArrayList<String> ndebà_valuu = new ArrayList<String>();
    public void 더하기(String valuu) { ndebà_valuu.add(valuu); }
    public String Wepụta_ọzi(int ùsòrò_valuu) { return ndebà_valuu.get(ùsòrò_valuu); }
    public String doghachi_valuu(int ùsòrò_valuu, String valuu) { return ndebà_valuu.set(ùsòrò_valuu, valuu); }
    public String 지우기(int ùsòrò_valuu) { return ndebà_valuu.remove(ùsòrò_valuu); }
    public int Ụhara() { return ndebà_valuu.size(); }
    public boolean 비었는가() { return ndebà_valuu.isEmpty(); }
    public void hichaa_TOC() { ndebà_valuu.clear(); }
}
