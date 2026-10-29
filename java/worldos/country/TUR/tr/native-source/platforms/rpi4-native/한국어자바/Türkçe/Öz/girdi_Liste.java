// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Türkçe.Öz;
import java.util.ArrayList;
/** girdi_Liste(目錄): 순서가 있는 항목의 모음. 이 판은 dize_değer 목록을 제공한다. */
public final class girdi_Liste {
    private final ArrayList<String> girdi_değer = new ArrayList<String>();
    public void 더하기(String değer) { girdi_değer.add(değer); }
    public String Okuma(int düzen_değer) { return girdi_değer.get(düzen_değer); }
    public String DEĞİŞTİR_değer(int düzen_değer, String değer) { return girdi_değer.set(düzen_değer, değer); }
    public String silmek_girdi(int düzen_değer) { return girdi_değer.remove(düzen_değer); }
    public int Boyut() { return girdi_değer.size(); }
    public boolean bilgi_teknolojisi_boş_değer() { return girdi_değer.isEmpty(); }
    public void takas_içindekiler() { girdi_değer.clear(); }
}
