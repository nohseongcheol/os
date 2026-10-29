// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.HashMap;
/** 사전(辭典): 찾는 말(열쇠)에 값을 대응시킨다. */
public final class 사전 {
    private final HashMap<String, String> Iliniku_atuutilik = new HashMap<String, String>();
    public String 넣기(String 열쇠, String atuutilik) { return Iliniku_atuutilik.put(열쇠, atuutilik); }
    public String nanili_Iliniku(String 열쇠) { return Iliniku_atuutilik.get(열쇠); }
    public boolean 있는가(String 열쇠) { return Iliniku_atuutilik.containsKey(열쇠); }
    public String 지우기(String 열쇠) { return Iliniku_atuutilik.remove(열쇠); }
    public int anininga() { return Iliniku_atuutilik.size(); }
    public void piijarli_TOC() { Iliniku_atuutilik.clear(); }
}
