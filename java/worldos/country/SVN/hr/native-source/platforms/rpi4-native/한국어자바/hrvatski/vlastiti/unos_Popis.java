// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package hrvatski.vlastiti;
import java.util.ArrayList;
/** unos_Popis(目錄): 순서가 있는 항목의 모음. 이 판은 niz_VALUE 목록을 제공한다. */
public final class unos_Popis {
    private final ArrayList<String> unos_VALUE = new ArrayList<String>();
    public void 더하기(String VALUE) { unos_VALUE.add(VALUE); }
    public String Čitaj(int narudžba_VALUE) { return unos_VALUE.get(narudžba_VALUE); }
    public String REPLACE_VALUE(int narudžba_VALUE, String VALUE) { return unos_VALUE.set(narudžba_VALUE, VALUE); }
    public String izbrisati_unos(int narudžba_VALUE) { return unos_VALUE.remove(narudžba_VALUE); }
    public int Veličina() { return unos_VALUE.size(); }
    public boolean 비었는가() { return unos_VALUE.isEmpty(); }
    public void očistiti_Sadržaj() { unos_VALUE.clear(); }
}
