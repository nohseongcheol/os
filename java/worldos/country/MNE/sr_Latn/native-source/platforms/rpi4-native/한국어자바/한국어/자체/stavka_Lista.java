// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.ArrayList;
/** stavka_Lista(目錄): 순서가 있는 항목의 모음. 이 판은 niska_VALUE 목록을 제공한다. */
public final class stavka_Lista {
    private final ArrayList<String> stavka_VALUE = new ArrayList<String>();
    public void 더하기(String VALUE) { stavka_VALUE.add(VALUE); }
    public String 읽기(int poručiti_VALUE) { return stavka_VALUE.get(poručiti_VALUE); }
    public String REPLACE_VALUE(int poručiti_VALUE, String VALUE) { return stavka_VALUE.set(poručiti_VALUE, VALUE); }
    public String obrisati_stavka(int poručiti_VALUE) { return stavka_VALUE.remove(poručiti_VALUE); }
    public int promeniti_veličinu() { return stavka_VALUE.size(); }
    public boolean 비었는가() { return stavka_VALUE.isEmpty(); }
    public void obrisati_Sadržaj() { stavka_VALUE.clear(); }
}
