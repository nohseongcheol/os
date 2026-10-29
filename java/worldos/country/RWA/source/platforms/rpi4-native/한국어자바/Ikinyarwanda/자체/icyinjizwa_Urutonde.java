// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ikinyarwanda.자체;
import java.util.ArrayList;
/** icyinjizwa_Urutonde(目錄): 순서가 있는 항목의 모음. 이 판은 igicenteruro_agaciro 목록을 제공한다. */
public final class icyinjizwa_Urutonde {
    private final ArrayList<String> icyinjizwa_agaciro = new ArrayList<String>();
    public void 더하기(String agaciro) { icyinjizwa_agaciro.add(agaciro); }
    public String 읽기(int umujyo_agaciro) { return icyinjizwa_agaciro.get(umujyo_agaciro); }
    public String gusimbuza_agaciro(int umujyo_agaciro, String agaciro) { return icyinjizwa_agaciro.set(umujyo_agaciro, agaciro); }
    public String 지우기(int umujyo_agaciro) { return icyinjizwa_agaciro.remove(umujyo_agaciro); }
    public int Ingano() { return icyinjizwa_agaciro.size(); }
    public boolean 비었는가() { return icyinjizwa_agaciro.isEmpty(); }
    public void gukuraho_TOC() { icyinjizwa_agaciro.clear(); }
}
