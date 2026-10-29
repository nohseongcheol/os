// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.HashMap;
/** rečnik(辭典): 찾는 Word_SMS(열쇠)에 값을 대응시킨다. */
public final class rečnik {
    private final HashMap<String, String> stavka_VALUE = new HashMap<String, String>();
    public String 넣기(String 열쇠, String VALUE) { return stavka_VALUE.put(열쇠, VALUE); }
    public String FIND_stavka(String 열쇠) { return stavka_VALUE.get(열쇠); }
    public boolean 있는가(String 열쇠) { return stavka_VALUE.containsKey(열쇠); }
    public String obrisati_stavka(String 열쇠) { return stavka_VALUE.remove(열쇠); }
    public int promeniti_veličinu() { return stavka_VALUE.size(); }
    public void obrisati_Sadržaj() { stavka_VALUE.clear(); }
}
