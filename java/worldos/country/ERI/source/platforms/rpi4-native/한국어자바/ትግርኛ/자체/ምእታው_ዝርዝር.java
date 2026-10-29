// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ትግርኛ.자체;
import java.util.ArrayList;
/** ምእታው_ዝርዝር(目錄): 순서가 있는 항목의 모음. 이 판은 ሕብረ_ቁምፊ_ዋጋ 목록을 제공한다. */
public final class ምእታው_ዝርዝር {
    private final ArrayList<String> ምእታው_ዋጋ = new ArrayList<String>();
    public void 더하기(String ዋጋ) { ምእታው_ዋጋ.add(ዋጋ); }
    public String 읽기(int ተርታ_ዋጋ) { return ምእታው_ዋጋ.get(ተርታ_ዋጋ); }
    public String ተክእ_ዋጋ(int ተርታ_ዋጋ, String ዋጋ) { return ምእታው_ዋጋ.set(ተርታ_ዋጋ, ዋጋ); }
    public String 지우기(int ተርታ_ዋጋ) { return ምእታው_ዋጋ.remove(ተርታ_ዋጋ); }
    public int መጠን() { return ምእታው_ዋጋ.size(); }
    public boolean 비었는가() { return ምእታው_ዋጋ.isEmpty(); }
    public void ኣልግስ_ትሕዝቶታት() { ምእታው_ዋጋ.clear(); }
}
