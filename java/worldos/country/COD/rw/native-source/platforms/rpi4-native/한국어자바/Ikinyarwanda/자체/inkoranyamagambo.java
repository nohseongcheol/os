// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ikinyarwanda.자체;
import java.util.HashMap;
/** inkoranyamagambo(辭典): 찾는 Ijambo_SMS(열쇠)에 값을 대응시킨다. */
public final class inkoranyamagambo {
    private final HashMap<String, String> icyinjizwa_agaciro = new HashMap<String, String>();
    public String 넣기(String 열쇠, String agaciro) { return icyinjizwa_agaciro.put(열쇠, agaciro); }
    public String gushaka_icyinjizwa(String 열쇠) { return icyinjizwa_agaciro.get(열쇠); }
    public boolean 있는가(String 열쇠) { return icyinjizwa_agaciro.containsKey(열쇠); }
    public String 지우기(String 열쇠) { return icyinjizwa_agaciro.remove(열쇠); }
    public int Ingano() { return icyinjizwa_agaciro.size(); }
    public void gukuraho_TOC() { icyinjizwa_agaciro.clear(); }
}
