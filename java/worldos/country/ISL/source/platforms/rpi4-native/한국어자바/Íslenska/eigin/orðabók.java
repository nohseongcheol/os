// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Íslenska.eigin;
import java.util.HashMap;
/** orðabók(辭典): 찾는 Word_SMS(열쇠)에 값을 대응시킨다. */
public final class orðabók {
    private final HashMap<String, String> færsla_VALUE = new HashMap<String, String>();
    public String 넣기(String 열쇠, String VALUE) { return færsla_VALUE.put(열쇠, VALUE); }
    public String FIND_færsla(String 열쇠) { return færsla_VALUE.get(열쇠); }
    public boolean 있는가(String 열쇠) { return færsla_VALUE.containsKey(열쇠); }
    public String eyða_færsla(String 열쇠) { return færsla_VALUE.remove(열쇠); }
    public int Stærð() { return færsla_VALUE.size(); }
    public void hreinsa_Innihald() { færsla_VALUE.clear(); }
}
