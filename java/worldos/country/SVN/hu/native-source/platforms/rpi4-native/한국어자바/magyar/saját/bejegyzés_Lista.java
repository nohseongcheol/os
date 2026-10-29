// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package magyar.saját;
import java.util.ArrayList;
/** bejegyzés_Lista(目錄): 순서가 있는 항목의 모음. 이 판은 sztring_ÉRTÉK 목록을 제공한다. */
public final class bejegyzés_Lista {
    private final ArrayList<String> bejegyzés_ÉRTÉK = new ArrayList<String>();
    public void 더하기(String ÉRTÉK) { bejegyzés_ÉRTÉK.add(ÉRTÉK); }
    public String Olvasás(int rendel_ÉRTÉK) { return bejegyzés_ÉRTÉK.get(rendel_ÉRTÉK); }
    public String CSERE_ÉRTÉK(int rendel_ÉRTÉK, String ÉRTÉK) { return bejegyzés_ÉRTÉK.set(rendel_ÉRTÉK, ÉRTÉK); }
    public String töröl_bejegyzés(int rendel_ÉRTÉK) { return bejegyzés_ÉRTÉK.remove(rendel_ÉRTÉK); }
    public int Méret() { return bejegyzés_ÉRTÉK.size(); }
    public boolean informatikai_részleg_üres_ÉRTÉK() { return bejegyzés_ÉRTÉK.isEmpty(); }
    public void töröl_Tartalom() { bejegyzés_ÉRTÉK.clear(); }
}
