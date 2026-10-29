// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Isi_Zulu.자체;
import java.util.ArrayList;
/** okufakwayo_Uhlu(目錄): 순서가 있는 항목의 모음. 이 판은 uchunge_inani 목록을 제공한다. */
public final class okufakwayo_Uhlu {
    private final ArrayList<String> okufakwayo_inani = new ArrayList<String>();
    public void 더하기(String inani) { okufakwayo_inani.add(inani); }
    public String Funda(int ukuhleleka_inani) { return okufakwayo_inani.get(ukuhleleka_inani); }
    public String faka_endaweni_inani(int ukuhleleka_inani, String inani) { return okufakwayo_inani.set(ukuhleleka_inani, inani); }
    public String 지우기(int ukuhleleka_inani) { return okufakwayo_inani.remove(ukuhleleka_inani); }
    public int Ubungako() { return okufakwayo_inani.size(); }
    public boolean 비었는가() { return okufakwayo_inani.isEmpty(); }
    public void sula_i_TOC() { okufakwayo_inani.clear(); }
}
