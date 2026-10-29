// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lietuvių.savas;
import java.util.HashMap;
/** žodynas(辭典): 찾는 Word_SMS(열쇠)에 값을 대응시킨다. */
public final class žodynas {
    private final HashMap<String, String> įrašas_VALUE = new HashMap<String, String>();
    public String 넣기(String 열쇠, String VALUE) { return įrašas_VALUE.put(열쇠, VALUE); }
    public String FIND_įrašas(String 열쇠) { return įrašas_VALUE.get(열쇠); }
    public boolean 있는가(String 열쇠) { return įrašas_VALUE.containsKey(열쇠); }
    public String ištrinti_įrašas(String 열쇠) { return įrašas_VALUE.remove(열쇠); }
    public int Dydis() { return įrašas_VALUE.size(); }
    public void apmokėti_Turinys() { įrašas_VALUE.clear(); }
}
