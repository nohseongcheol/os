// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Türkçe.Öz;
import java.util.HashMap;
/** sözlük(辭典): 찾는 Word_SMS(tuş_malzeme)에 값을 대응시킨다. */
public final class sözlük {
    private final HashMap<String, String> girdi_değer = new HashMap<String, String>();
    public String 넣기(String tuş_malzeme, String değer) { return girdi_değer.put(tuş_malzeme, değer); }
    public String BUL_girdi(String tuş_malzeme) { return girdi_değer.get(tuş_malzeme); }
    public boolean 있는가(String tuş_malzeme) { return girdi_değer.containsKey(tuş_malzeme); }
    public String silmek_girdi(String tuş_malzeme) { return girdi_değer.remove(tuş_malzeme); }
    public int Boyut() { return girdi_değer.size(); }
    public void takas_içindekiler() { girdi_değer.clear(); }
}
