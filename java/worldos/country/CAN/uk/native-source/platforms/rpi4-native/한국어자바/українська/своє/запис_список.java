// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package українська.своє;
import java.util.ArrayList;
/** запис_список(目錄): 순서가 있는 항목의 모음. 이 판은 рядок_значення 목록을 제공한다. */
public final class запис_список {
    private final ArrayList<String> запис_значення_962f286b = new ArrayList<String>();
    public void 더하기(String значення) { запис_значення_962f286b.add(значення); }
    public String Читання(int порядок_значення) { return запис_значення_962f286b.get(порядок_значення); }
    public String 바꾸기(int порядок_значення, String значення) { return запис_значення_962f286b.set(порядок_значення, значення); }
    public String видаляти_запис(int порядок_значення) { return запис_значення_962f286b.remove(порядок_значення); }
    public int Розмір() { return запис_значення_962f286b.size(); }
    public boolean 비었는가() { return запис_значення_962f286b.isEmpty(); }
    public void очищати_Зміст() { запис_значення_962f286b.clear(); }
}
