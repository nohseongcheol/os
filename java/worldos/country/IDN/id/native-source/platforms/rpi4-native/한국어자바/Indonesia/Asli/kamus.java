// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Indonesia.Asli;
import java.util.HashMap;
/** kamus(辭典): 찾는 Kata_SMS(열쇠)에 값을 대응시킨다. */
public final class kamus {
    private final HashMap<String, String> entri_VALUE = new HashMap<String, String>();
    public String 넣기(String 열쇠, String VALUE) { return entri_VALUE.put(열쇠, VALUE); }
    public String FIND_entri(String 열쇠) { return entri_VALUE.get(열쇠); }
    public boolean 있는가(String 열쇠) { return entri_VALUE.containsKey(열쇠); }
    public String hapus_entri_c8dbc399(String 열쇠) { return entri_VALUE.remove(열쇠); }
    public int Ukuran() { return entri_VALUE.size(); }
    public void bersihkan_Isi() { entri_VALUE.clear(); }
}
