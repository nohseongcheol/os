// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Melayu.Asli;
import java.util.HashMap;
/** kamus(辭典): 찾는 Word_SMS(열쇠)에 값을 대응시킨다. */
public final class kamus {
    private final HashMap<String, String> pemasukan_VALUE = new HashMap<String, String>();
    public String 넣기(String 열쇠, String VALUE) { return pemasukan_VALUE.put(열쇠, VALUE); }
    public String Cari_pemasukan(String 열쇠) { return pemasukan_VALUE.get(열쇠); }
    public boolean 있는가(String 열쇠) { return pemasukan_VALUE.containsKey(열쇠); }
    public String padam_pemasukan(String 열쇠) { return pemasukan_VALUE.remove(열쇠); }
    public int Saiz() { return pemasukan_VALUE.size(); }
    public void buang_TOC() { pemasukan_VALUE.clear(); }
}
