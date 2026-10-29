// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.HashMap;
/** kamus(辭典): 찾는 Microsoft_Word_SMS(열쇠)에 값을 대응시킨다. */
public final class kamus {
    private final HashMap<String, String> Mashigar_bayanai_Daraja = new HashMap<String, String>();
    public String 넣기(String 열쇠, String Daraja) { return Mashigar_bayanai_Daraja.put(열쇠, Daraja); }
    public String nema_Mashigar_bayanai(String 열쇠) { return Mashigar_bayanai_Daraja.get(열쇠); }
    public boolean 있는가(String 열쇠) { return Mashigar_bayanai_Daraja.containsKey(열쇠); }
    public String share_Mashigar_bayanai(String 열쇠) { return Mashigar_bayanai_Daraja.remove(열쇠); }
    public int Girma() { return Mashigar_bayanai_Daraja.size(); }
    public void Share_TOC() { Mashigar_bayanai_Daraja.clear(); }
}
