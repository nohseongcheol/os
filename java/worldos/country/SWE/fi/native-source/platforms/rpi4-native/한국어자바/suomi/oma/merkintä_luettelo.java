// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package suomi.oma;
import java.util.ArrayList;
/** merkintä_luettelo(目錄): 순서가 있는 항목의 모음. 이 판은 merkkijono_ARVO 목록을 제공한다. */
public final class merkintä_luettelo {
    private final ArrayList<String> merkintä_ARVO_962f286b = new ArrayList<String>();
    public void 더하기(String ARVO) { merkintä_ARVO_962f286b.add(ARVO); }
    public String Luku(int tilata_ARVO) { return merkintä_ARVO_962f286b.get(tilata_ARVO); }
    public String KORVAA_ARVO(int tilata_ARVO, String ARVO) { return merkintä_ARVO_962f286b.set(tilata_ARVO, ARVO); }
    public String poistaa_merkintä_c8dbc399(int tilata_ARVO) { return merkintä_ARVO_962f286b.remove(tilata_ARVO); }
    public int Koko() { return merkintä_ARVO_962f286b.size(); }
    public boolean 비었는가() { return merkintä_ARVO_962f286b.isEmpty(); }
    public void selvittää_Sisällys() { merkintä_ARVO_962f286b.clear(); }
}
