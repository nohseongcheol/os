// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nederlands.Eigen;
import java.util.ArrayList;
/** invoer_Lijst_f07b3200(目錄): 순서가 있는 항목의 모음. 이 판은 tekenreeks_WAARDE 목록을 제공한다. */
public final class invoer_Lijst_f07b3200 {
    private final ArrayList<String> invoer_WAARDE_962f286b = new ArrayList<String>();
    public void 더하기(String WAARDE) { invoer_WAARDE_962f286b.add(WAARDE); }
    public String Lezen(int order_WAARDE) { return invoer_WAARDE_962f286b.get(order_WAARDE); }
    public String VERVANGEN_WAARDE(int order_WAARDE, String WAARDE) { return invoer_WAARDE_962f286b.set(order_WAARDE, WAARDE); }
    public String wissen_invoer(int order_WAARDE) { return invoer_WAARDE_962f286b.remove(order_WAARDE); }
    public int Grootte() { return invoer_WAARDE_962f286b.size(); }
    public boolean informatie_leeg_WAARDE() { return invoer_WAARDE_962f286b.isEmpty(); }
    public void wissen_Inhoud() { invoer_WAARDE_962f286b.clear(); }
}
