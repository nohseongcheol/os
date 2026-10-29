// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovenský.vlastné;
import java.util.HashMap;
/** slovník(辭典): 찾는 Word_SMS(열쇠)에 값을 대응시킨다. */
public final class slovník {
    private final HashMap<String, String> položka_VALUE = new HashMap<String, String>();
    public String 넣기(String 열쇠, String VALUE) { return položka_VALUE.put(열쇠, VALUE); }
    public String FIND_položka(String 열쇠) { return položka_VALUE.get(열쇠); }
    public boolean 있는가(String 열쇠) { return položka_VALUE.containsKey(열쇠); }
    public String vymazať_položka(String 열쇠) { return položka_VALUE.remove(열쇠); }
    public int Veľkosť() { return položka_VALUE.size(); }
    public void vymazať_Obsah() { položka_VALUE.clear(); }
}
