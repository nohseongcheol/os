// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Malti.자체;
import java.util.ArrayList;
/** entrata_Lista(目錄): 순서가 있는 항목의 모음. 이 판은 string_VALUE 목록을 제공한다. */
public final class entrata_Lista {
    private final ArrayList<String> entrata_VALUE = new ArrayList<String>();
    public void 더하기(String VALUE) { entrata_VALUE.add(VALUE); }
    public String 읽기(int ordni_VALUE) { return entrata_VALUE.get(ordni_VALUE); }
    public String REPLACE_VALUE(int ordni_VALUE, String VALUE) { return entrata_VALUE.set(ordni_VALUE, VALUE); }
    public String 지우기(int ordni_VALUE) { return entrata_VALUE.remove(ordni_VALUE); }
    public int daqqas() { return entrata_VALUE.size(); }
    public boolean 비었는가() { return entrata_VALUE.isEmpty(); }
    public void neħħa_TOC() { entrata_VALUE.clear(); }
}
