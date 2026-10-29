// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package suomi.oma;
import java.util.HashMap;
/** sanakirja(辭典): 찾는 Word_SMS(열쇠)에 값을 대응시킨다. */
public final class sanakirja {
    private final HashMap<String, String> merkintä_ARVO_962f286b = new HashMap<String, String>();
    public String 넣기(String 열쇠, String ARVO) { return merkintä_ARVO_962f286b.put(열쇠, ARVO); }
    public String ETSI_merkintä(String 열쇠) { return merkintä_ARVO_962f286b.get(열쇠); }
    public boolean 있는가(String 열쇠) { return merkintä_ARVO_962f286b.containsKey(열쇠); }
    public String poistaa_merkintä_c8dbc399(String 열쇠) { return merkintä_ARVO_962f286b.remove(열쇠); }
    public int Koko() { return merkintä_ARVO_962f286b.size(); }
    public void selvittää_Sisällys() { merkintä_ARVO_962f286b.clear(); }
}
