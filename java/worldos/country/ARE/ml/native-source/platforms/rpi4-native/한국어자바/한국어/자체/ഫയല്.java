// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 ഉപയോക്താവ് 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class ഫയല് {
    private ഫയല്() {}
    public static byte[] 바이트읽기(String പേരു്) throws ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്_ഒഴിവാക്കൽ {
        try {
        FileInputStream സ്ട്രീം_മൂല്യം = new FileInputStream(പേരു്);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, മൂല്യം;
            while ((മൂല്യം = സ്ട്രീം_മൂല്യം.read()) != -1) { if (수 == 임시.length) throw new ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്_ഒഴിവാക്കൽ("ഫയല് വലിപ്പം 제한"); 임시[수++] = (byte)മൂല്യം; }
            byte[] അളവ് = new byte[수]; System.arraycopy(임시, 0, അളവ്, 0, 수); return അളവ്;
        } finally { സ്ട്രീം_മൂല്യം.close(); }
        } catch (java.io.IOException പിശക്) { throw 예외변환.ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്(പിശക്); }
        catch (RuntimeException പിശക്) { throw 예외변환.നടപ്പാക്കുക_കമാന്_ഡ്(പിശക്); }
    }
    public static void റൈറ്റ്_ചെയ്യുക_బైట్_മൂല്യം(String പേരു്, byte[] ഉള്ളടക്കം_മൂല്യം) throws ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്_ഒഴിവാക്കൽ {
        try {
        FileOutputStream സ്ട്രീം_മൂല്യം = new FileOutputStream(പേരു്);
        try { for (int ലൂപ്_സൂചിക = 0; ലൂപ്_സൂചിക < ഉള്ളടക്കം_മൂല്യം.length; ലൂപ്_സൂചിക++) സ്ട്രീം_മൂല്യം.write(ഉള്ളടക്കം_മൂല്യം[ലൂപ്_സൂചിക] & 255); } finally { സ്ട്രീം_മൂല്യം.close(); }
        } catch (java.io.IOException പിശക്) { throw 예외변환.ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്(പിശക്); }
        catch (RuntimeException പിശക്) { throw 예외변환.നടപ്പാക്കുക_കമാന്_ഡ്(പിശക്); }
    }
    public static String വായന(String പേരു്) throws ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്_ഒഴിവാക്കൽ {
        try { return 문자.ഗൂഢഭാഷമാറ്റുക_ഡാറ്റാ(바이트읽기(പേരു്));
        } catch (java.io.IOException പിശക്) { throw 예외변환.ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്(പിശക്); }
        catch (RuntimeException പിശക്) { throw 예외변환.നടപ്പാക്കുക_കമാന്_ഡ്(പിശക്); }
    }
    public static void എഴുത്തു്(String പേരു്, String ഉള്ളടക്കം_മൂല്യം) throws ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്_ഒഴിവാക്കൽ {
        try { റൈറ്റ്_ചെയ്യുക_బైట్_മൂല്യം(പേരു്, 문자.부호화(ഉള്ളടക്കം_മൂല്യം));
        } catch (java.io.IOException പിശക്) { throw 예외변환.ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്(പിശക്); }
        catch (RuntimeException പിശക്) { throw 예외변환.നടപ്പാക്കുക_കമാന്_ഡ്(പിശക്); }
    }
}
