// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Română.propriu;
import java.util.ArrayList;
/** intrare_Listă(目錄): 순서가 있는 항목의 모음. 이 판은 șir_VALUE 목록을 제공한다. */
public final class intrare_Listă {
    private final ArrayList<String> intrare_VALUE = new ArrayList<String>();
    public void 더하기(String VALUE) { intrare_VALUE.add(VALUE); }
    public String Citire(int ordine_VALUE) { return intrare_VALUE.get(ordine_VALUE); }
    public String REPLACE_VALUE(int ordine_VALUE, String VALUE) { return intrare_VALUE.set(ordine_VALUE, VALUE); }
    public String șterge_intrare(int ordine_VALUE) { return intrare_VALUE.remove(ordine_VALUE); }
    public int Mărime() { return intrare_VALUE.size(); }
    public boolean 비었는가() { return intrare_VALUE.isEmpty(); }
    public void goli_TOC() { intrare_VALUE.clear(); }
}
