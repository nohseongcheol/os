// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Gaeilge.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 úsáideoir 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class Comhad {
    private Comhad() {}
    public static byte[] 바이트읽기(String Ainm) throws I_O_eisceacht {
        try {
        FileInputStream sruth_VALUE = new FileInputStream(Ainm);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, VALUE;
            while ((VALUE = sruth_VALUE.read()) != -1) { if (수 == 임시.length) throw new I_O_eisceacht("Comhad Méid 제한"); 임시[수++] = (byte)VALUE; }
            byte[] tomhas = new byte[수]; System.arraycopy(임시, 0, tomhas, 0, 수); return tomhas;
        } finally { sruth_VALUE.close(); }
        } catch (java.io.IOException ERREÁID) { throw CONVERT_eisceacht.I_O(ERREÁID); }
        catch (RuntimeException ERREÁID) { throw CONVERT_eisceacht.Rith_ordú(ERREÁID); }
    }
    public static void scríobh_beart_VALUE(String Ainm, byte[] Inneachar_VALUE) throws I_O_eisceacht {
        try {
        FileOutputStream sruth_VALUE = new FileOutputStream(Ainm);
        try { for (int lúb_INDEX = 0; lúb_INDEX < Inneachar_VALUE.length; lúb_INDEX++) sruth_VALUE.write(Inneachar_VALUE[lúb_INDEX] & 255); } finally { sruth_VALUE.close(); }
        } catch (java.io.IOException ERREÁID) { throw CONVERT_eisceacht.I_O(ERREÁID); }
        catch (RuntimeException ERREÁID) { throw CONVERT_eisceacht.Rith_ordú(ERREÁID); }
    }
    public static String Léigh(String Ainm) throws I_O_eisceacht {
        try { return 문자.díchriptigh_sonraí(바이트읽기(Ainm));
        } catch (java.io.IOException ERREÁID) { throw CONVERT_eisceacht.I_O(ERREÁID); }
        catch (RuntimeException ERREÁID) { throw CONVERT_eisceacht.Rith_ordú(ERREÁID); }
    }
    public static void Scríobh(String Ainm, String Inneachar_VALUE) throws I_O_eisceacht {
        try { scríobh_beart_VALUE(Ainm, 문자.부호화(Inneachar_VALUE));
        } catch (java.io.IOException ERREÁID) { throw CONVERT_eisceacht.I_O(ERREÁID); }
        catch (RuntimeException ERREÁID) { throw CONVERT_eisceacht.Rith_ordú(ERREÁID); }
    }
}
