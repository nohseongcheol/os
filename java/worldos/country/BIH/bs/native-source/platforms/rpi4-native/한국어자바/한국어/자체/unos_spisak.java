// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.ArrayList;
/** unos_spisak(目錄): 순서가 있는 항목의 모음. 이 판은 string_VALUE 목록을 제공한다. */
public final class unos_spisak {
    private final ArrayList<String> unos_VALUE = new ArrayList<String>();
    public void 더하기(String VALUE) { unos_VALUE.add(VALUE); }
    public String Čitaj(int redoslijed_VALUE) { return unos_VALUE.get(redoslijed_VALUE); }
    public String REPLACE_VALUE(int redoslijed_VALUE, String VALUE) { return unos_VALUE.set(redoslijed_VALUE, VALUE); }
    public String 지우기(int redoslijed_VALUE) { return unos_VALUE.remove(redoslijed_VALUE); }
    public int Veličina() { return unos_VALUE.size(); }
    public boolean odjel_za_informacijske_tehnologije_prazno_VALUE() { return unos_VALUE.isEmpty(); }
    public void obrisati_TOC() { unos_VALUE.clear(); }
}
