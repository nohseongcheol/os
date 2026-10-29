// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package norsk.eget;
import java.util.HashMap;
/** ordliste(辭典): 찾는 ord_SMS(열쇠)에 값을 대응시킨다. */
public final class ordliste {
    private final HashMap<String, String> oppføring_VERDI = new HashMap<String, String>();
    public String 넣기(String 열쇠, String VERDI) { return oppføring_VERDI.put(열쇠, VERDI); }
    public String Søk_oppføring(String 열쇠) { return oppføring_VERDI.get(열쇠); }
    public boolean 있는가(String 열쇠) { return oppføring_VERDI.containsKey(열쇠); }
    public String slette_oppføring(String 열쇠) { return oppføring_VERDI.remove(열쇠); }
    public int Størrelse() { return oppføring_VERDI.size(); }
    public void tømme_Innhold() { oppføring_VERDI.clear(); }
}
