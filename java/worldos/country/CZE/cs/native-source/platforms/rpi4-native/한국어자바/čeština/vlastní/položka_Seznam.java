// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package čeština.vlastní;
import java.util.ArrayList;
/** položka_Seznam(目錄): 순서가 있는 항목의 모음. 이 판은 řetězec_HODNOTA 목록을 제공한다. */
public final class položka_Seznam {
    private final ArrayList<String> položka_HODNOTA = new ArrayList<String>();
    public void 더하기(String HODNOTA) { položka_HODNOTA.add(HODNOTA); }
    public String Čtení(int pořadí_HODNOTA) { return položka_HODNOTA.get(pořadí_HODNOTA); }
    public String NAHRADIT_HODNOTA(int pořadí_HODNOTA, String HODNOTA) { return položka_HODNOTA.set(pořadí_HODNOTA, HODNOTA); }
    public String vymazat_položka(int pořadí_HODNOTA) { return položka_HODNOTA.remove(pořadí_HODNOTA); }
    public int Velikost() { return položka_HODNOTA.size(); }
    public boolean 비었는가() { return položka_HODNOTA.isEmpty(); }
    public void vymazat_Obsah() { položka_HODNOTA.clear(); }
}
