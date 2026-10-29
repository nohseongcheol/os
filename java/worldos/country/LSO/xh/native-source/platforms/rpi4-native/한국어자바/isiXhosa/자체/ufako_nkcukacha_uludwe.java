// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package isiXhosa.자체;
import java.util.ArrayList;
/** ufako_nkcukacha_uludwe(目錄): 순서가 있는 항목의 모음. 이 판은 uluhlu_lweekharektha_ixabiso 목록을 제공한다. */
public final class ufako_nkcukacha_uludwe {
    private final ArrayList<String> ufako_nkcukacha_ixabiso = new ArrayList<String>();
    public void 더하기(String ixabiso) { ufako_nkcukacha_ixabiso.add(ixabiso); }
    public String Funda(int ulandelelwano_ixabiso) { return ufako_nkcukacha_ixabiso.get(ulandelelwano_ixabiso); }
    public String faka_endaweni_yenye_ixabiso(int ulandelelwano_ixabiso, String ixabiso) { return ufako_nkcukacha_ixabiso.set(ulandelelwano_ixabiso, ixabiso); }
    public String 지우기(int ulandelelwano_ixabiso) { return ufako_nkcukacha_ixabiso.remove(ulandelelwano_ixabiso); }
    public int Ubukhulu() { return ufako_nkcukacha_ixabiso.size(); }
    public boolean 비었는가() { return ufako_nkcukacha_ixabiso.isEmpty(); }
    public void susa_i_TOC() { ufako_nkcukacha_ixabiso.clear(); }
}
