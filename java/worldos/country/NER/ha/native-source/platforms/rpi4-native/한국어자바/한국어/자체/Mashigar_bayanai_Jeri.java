// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.ArrayList;
/** Mashigar_bayanai_Jeri(目錄): 순서가 있는 항목의 모음. 이 판은 Zare_Daraja 목록을 제공한다. */
public final class Mashigar_bayanai_Jeri {
    private final ArrayList<String> Mashigar_bayanai_Daraja = new ArrayList<String>();
    public void 더하기(String Daraja) { Mashigar_bayanai_Daraja.add(Daraja); }
    public String Yi_Karatu(int Hanyar_jejjerawa_Daraja) { return Mashigar_bayanai_Daraja.get(Hanyar_jejjerawa_Daraja); }
    public String Maye_gurbi_Daraja(int Hanyar_jejjerawa_Daraja, String Daraja) { return Mashigar_bayanai_Daraja.set(Hanyar_jejjerawa_Daraja, Daraja); }
    public String share_Mashigar_bayanai(int Hanyar_jejjerawa_Daraja) { return Mashigar_bayanai_Daraja.remove(Hanyar_jejjerawa_Daraja); }
    public int Girma() { return Mashigar_bayanai_Daraja.size(); }
    public boolean kimiyar_bayanai_holoko_Daraja() { return Mashigar_bayanai_Daraja.isEmpty(); }
    public void Share_TOC() { Mashigar_bayanai_Daraja.clear(); }
}
