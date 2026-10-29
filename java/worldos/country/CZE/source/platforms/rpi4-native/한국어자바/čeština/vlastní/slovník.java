// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package čeština.vlastní;
import java.util.HashMap;
/** slovník(辭典): 찾는 Word_SMS(Klíč_materiál)에 값을 대응시킨다. */
public final class slovník {
    private final HashMap<String, String> položka_HODNOTA = new HashMap<String, String>();
    public String 넣기(String Klíč_materiál, String HODNOTA) { return položka_HODNOTA.put(Klíč_materiál, HODNOTA); }
    public String NAJÍT_položka(String Klíč_materiál) { return položka_HODNOTA.get(Klíč_materiál); }
    public boolean 있는가(String Klíč_materiál) { return položka_HODNOTA.containsKey(Klíč_materiál); }
    public String vymazat_položka(String Klíč_materiál) { return položka_HODNOTA.remove(Klíč_materiál); }
    public int Velikost() { return položka_HODNOTA.size(); }
    public void vymazat_Obsah() { položka_HODNOTA.clear(); }
}
