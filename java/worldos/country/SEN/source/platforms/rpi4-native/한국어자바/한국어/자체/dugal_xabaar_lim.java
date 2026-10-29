// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.ArrayList;
/** dugal_xabaar_lim(目錄): 순서가 있는 항목의 모음. 이 판은 araf_yu_bennoo_xëyma 목록을 제공한다. */
public final class dugal_xabaar_lim {
    private final ArrayList<String> dugal_xabaar_xëyma = new ArrayList<String>();
    public void 더하기(String xëyma) { dugal_xabaar_xëyma.add(xëyma); }
    public String 읽기(int toftale_xëyma) { return dugal_xabaar_xëyma.get(toftale_xëyma); }
    public String delloosi_xëyma(int toftale_xëyma, String xëyma) { return dugal_xabaar_xëyma.set(toftale_xëyma, xëyma); }
    public String 지우기(int toftale_xëyma) { return dugal_xabaar_xëyma.remove(toftale_xëyma); }
    public int tolluwaay() { return dugal_xabaar_xëyma.size(); }
    public boolean 비었는가() { return dugal_xabaar_xëyma.isEmpty(); }
    public void efaase_TOC() { dugal_xabaar_xëyma.clear(); }
}
