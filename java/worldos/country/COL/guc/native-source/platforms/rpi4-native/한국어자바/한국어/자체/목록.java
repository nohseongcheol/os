// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.ArrayList;
/** 목록(目錄): 순서가 있는 항목의 모음. 이 판은 kaleena_ajutuu 목록을 제공한다. */
public final class 목록 {
    private final ArrayList<String> ekeroliaa_ajutuu = new ArrayList<String>();
    public void 더하기(String ajutuu) { ekeroliaa_ajutuu.add(ajutuu); }
    public String 읽기(int anaajiaakua_ipa_ajutuu) { return ekeroliaa_ajutuu.get(anaajiaakua_ipa_ajutuu); }
    public String 바꾸기(int anaajiaakua_ipa_ajutuu, String ajutuu) { return ekeroliaa_ajutuu.set(anaajiaakua_ipa_ajutuu, ajutuu); }
    public String 지우기(int anaajiaakua_ipa_ajutuu) { return ekeroliaa_ajutuu.remove(anaajiaakua_ipa_ajutuu); }
    public int 크기() { return ekeroliaa_ajutuu.size(); }
    public boolean 비었는가() { return ekeroliaa_ajutuu.isEmpty(); }
    public void ama_inrüinjiraa_TA() { ekeroliaa_ajutuu.clear(); }
}
