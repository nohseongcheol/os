// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.ArrayList;
/** Iliniku_Titiqpalliagaq(目錄): 순서가 있는 항목의 모음. 이 판은 qimiaq_atuutilik 목록을 제공한다. */
public final class Iliniku_Titiqpalliagaq {
    private final ArrayList<String> Iliniku_atuutilik = new ArrayList<String>();
    public void 더하기(String atuutilik) { Iliniku_atuutilik.add(atuutilik); }
    public String 읽기(int agguijjut_atuutilik) { return Iliniku_atuutilik.get(agguijjut_atuutilik); }
    public String kinguvvirli_atuutilik(int agguijjut_atuutilik, String atuutilik) { return Iliniku_atuutilik.set(agguijjut_atuutilik, atuutilik); }
    public String 지우기(int agguijjut_atuutilik) { return Iliniku_atuutilik.remove(agguijjut_atuutilik); }
    public int anininga() { return Iliniku_atuutilik.size(); }
    public boolean 비었는가() { return Iliniku_atuutilik.isEmpty(); }
    public void piijarli_TOC() { Iliniku_atuutilik.clear(); }
}
