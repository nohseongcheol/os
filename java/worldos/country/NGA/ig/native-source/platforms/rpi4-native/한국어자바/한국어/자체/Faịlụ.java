// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 òjìàrụ 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class Faịlụ {
    private Faịlụ() {}
    public static byte[] 바이트읽기(String Aha) throws 입출력예외 {
        try {
        FileInputStream agịrị_valuu = new FileInputStream(Aha);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, valuu;
            while ((valuu = agịrị_valuu.read()) != -1) { if (수 == 임시.length) throw new 입출력예외("Faịlụ Ụhara 제한"); 임시[수++] = (byte)valuu; }
            byte[] 결과 = new byte[수]; System.arraycopy(임시, 0, 결과, 0, 수); return 결과;
        } finally { agịrị_valuu.close(); }
        } catch (java.io.IOException mmejọ) { throw 예외변환.I_O(mmejọ); }
        catch (RuntimeException mmejọ) { throw 예외변환.mee_nnyemiwu(mmejọ); }
    }
    public static void dee_baịtị_valuu(String Aha, byte[] ndịnà_valuu) throws 입출력예외 {
        try {
        FileOutputStream agịrị_valuu = new FileOutputStream(Aha);
        try { for (int memmenwè_indèks = 0; memmenwè_indèks < ndịnà_valuu.length; memmenwè_indèks++) agịrị_valuu.write(ndịnà_valuu[memmenwè_indèks] & 255); } finally { agịrị_valuu.close(); }
        } catch (java.io.IOException mmejọ) { throw 예외변환.I_O(mmejọ); }
        catch (RuntimeException mmejọ) { throw 예외변환.mee_nnyemiwu(mmejọ); }
    }
    public static String Wepụta_ọzi(String Aha) throws 입출력예외 {
        try { return 문자.tụghee_edenzizo_datà(바이트읽기(Aha));
        } catch (java.io.IOException mmejọ) { throw 예외변환.I_O(mmejọ); }
        catch (RuntimeException mmejọ) { throw 예외변환.mee_nnyemiwu(mmejọ); }
    }
    public static void Chekwaa_ozi(String Aha, String ndịnà_valuu) throws 입출력예외 {
        try { dee_baịtị_valuu(Aha, 문자.부호화(ndịnà_valuu));
        } catch (java.io.IOException mmejọ) { throw 예외변환.I_O(mmejọ); }
        catch (RuntimeException mmejọ) { throw 예외변환.mee_nnyemiwu(mmejọ); }
    }
}
