// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Latviešu.savs;
import java.util.ArrayList;
/** ievade_Saraksts(目錄): 순서가 있는 항목의 모음. 이 판은 virkne_VALUE 목록을 제공한다. */
public final class ievade_Saraksts {
    private final ArrayList<String> ievade_VALUE = new ArrayList<String>();
    public void 더하기(String VALUE) { ievade_VALUE.add(VALUE); }
    public String Lasīt(int secība_VALUE) { return ievade_VALUE.get(secība_VALUE); }
    public String REPLACE_VALUE(int secība_VALUE, String VALUE) { return ievade_VALUE.set(secība_VALUE, VALUE); }
    public String dzēst_ievade(int secība_VALUE) { return ievade_VALUE.remove(secība_VALUE); }
    public int Izmērs() { return ievade_VALUE.size(); }
    public boolean 비었는가() { return ievade_VALUE.isEmpty(); }
    public void nodzēst_Satura_rādītājs() { ievade_VALUE.clear(); }
}
