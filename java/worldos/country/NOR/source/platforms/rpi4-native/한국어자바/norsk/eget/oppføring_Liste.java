// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package norsk.eget;
import java.util.ArrayList;
/** oppføring_Liste(目錄): 순서가 있는 항목의 모음. 이 판은 streng_VERDI 목록을 제공한다. */
public final class oppføring_Liste {
    private final ArrayList<String> oppføring_VERDI = new ArrayList<String>();
    public void 더하기(String VERDI) { oppføring_VERDI.add(VERDI); }
    public String Les(int ordre_VERDI) { return oppføring_VERDI.get(ordre_VERDI); }
    public String ERSTATT_VERDI(int ordre_VERDI, String VERDI) { return oppføring_VERDI.set(ordre_VERDI, VERDI); }
    public String slette_oppføring(int ordre_VERDI) { return oppføring_VERDI.remove(ordre_VERDI); }
    public int Størrelse() { return oppføring_VERDI.size(); }
    public boolean informasjonssystemer_tom_VERDI() { return oppføring_VERDI.isEmpty(); }
    public void tømme_Innhold() { oppføring_VERDI.clear(); }
}
