// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Indonesia.Asli;
import java.util.ArrayList;
/** entri_Daftar(目錄): 순서가 있는 항목의 모음. 이 판은 string_VALUE 목록을 제공한다. */
public final class entri_Daftar {
    private final ArrayList<String> entri_VALUE = new ArrayList<String>();
    public void 더하기(String VALUE) { entri_VALUE.add(VALUE); }
    public String Baca(int urutan_VALUE) { return entri_VALUE.get(urutan_VALUE); }
    public String ganti_VALUE(int urutan_VALUE, String VALUE) { return entri_VALUE.set(urutan_VALUE, VALUE); }
    public String hapus_entri_c8dbc399(int urutan_VALUE) { return entri_VALUE.remove(urutan_VALUE); }
    public int Ukuran() { return entri_VALUE.size(); }
    public boolean teknologi_informasi_kosong_VALUE() { return entri_VALUE.isEmpty(); }
    public void bersihkan_Isi() { entri_VALUE.clear(); }
}
