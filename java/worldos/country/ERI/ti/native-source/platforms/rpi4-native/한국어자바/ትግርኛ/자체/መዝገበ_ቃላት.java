// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ትግርኛ.자체;
import java.util.HashMap;
/** መዝገበ_ቃላት(辭典): 찾는 ናይ_ቃል_ጸወታ_ጽሑፍ(열쇠)에 값을 대응시킨다. */
public final class መዝገበ_ቃላት {
    private final HashMap<String, String> ምእታው_ዋጋ = new HashMap<String, String>();
    public String 넣기(String 열쇠, String ዋጋ) { return ምእታው_ዋጋ.put(열쇠, ዋጋ); }
    public String ርኸብ_ምእታው(String 열쇠) { return ምእታው_ዋጋ.get(열쇠); }
    public boolean 있는가(String 열쇠) { return ምእታው_ዋጋ.containsKey(열쇠); }
    public String 지우기(String 열쇠) { return ምእታው_ዋጋ.remove(열쇠); }
    public int መጠን() { return ምእታው_ዋጋ.size(); }
    public void ኣልግስ_ትሕዝቶታት() { ምእታው_ዋጋ.clear(); }
}
