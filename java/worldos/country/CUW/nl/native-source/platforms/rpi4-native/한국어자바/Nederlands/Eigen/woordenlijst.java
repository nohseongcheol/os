// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nederlands.Eigen;
import java.util.HashMap;
/** woordenlijst(辭典): 찾는 Word_sms(열쇠)에 값을 대응시킨다. */
public final class woordenlijst {
    private final HashMap<String, String> invoer_WAARDE_962f286b = new HashMap<String, String>();
    public String 넣기(String 열쇠, String WAARDE) { return invoer_WAARDE_962f286b.put(열쇠, WAARDE); }
    public String Zoeken_invoer(String 열쇠) { return invoer_WAARDE_962f286b.get(열쇠); }
    public boolean 있는가(String 열쇠) { return invoer_WAARDE_962f286b.containsKey(열쇠); }
    public String wissen_invoer(String 열쇠) { return invoer_WAARDE_962f286b.remove(열쇠); }
    public int Grootte() { return invoer_WAARDE_962f286b.size(); }
    public void wissen_Inhoud() { invoer_WAARDE_962f286b.clear(); }
}
