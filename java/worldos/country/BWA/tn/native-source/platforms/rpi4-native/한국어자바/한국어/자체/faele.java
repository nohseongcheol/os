// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 modirisi 용어를 보존한다. ga_jaana_selwana 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class faele {
    private faele() {}
    public static byte[] 바이트읽기(String leina) throws 입출력예외 {
        try {
        FileInputStream moela_Boleng = new FileInputStream(leina);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, Boleng;
            while ((Boleng = moela_Boleng.read()) != -1) { if (수 == 임시.length) throw new 입출력예외("faele lekanya 제한"); 임시[수++] = (byte)Boleng; }
            byte[] 결과 = new byte[수]; System.arraycopy(임시, 0, 결과, 0, 수); return 결과;
        } finally { moela_Boleng.close(); }
        } catch (java.io.IOException phoso) { throw 예외변환.I_O(phoso); }
        catch (RuntimeException phoso) { throw 예외변환.diragatsa_Taelo(phoso); }
    }
    public static void kwala_baete_Boleng(String leina, byte[] Diteng_Boleng) throws 입출력예외 {
        try {
        FileOutputStream moela_Boleng = new FileOutputStream(leina);
        try { for (int lupu_tshupane = 0; lupu_tshupane < Diteng_Boleng.length; lupu_tshupane++) moela_Boleng.write(Diteng_Boleng[lupu_tshupane] & 255); } finally { moela_Boleng.close(); }
        } catch (java.io.IOException phoso) { throw 예외변환.I_O(phoso); }
        catch (RuntimeException phoso) { throw 예외변환.diragatsa_Taelo(phoso); }
    }
    public static String 읽기(String leina) throws 입출력예외 {
        try { return 문자.Sirolola_tshedimosetso(바이트읽기(leina));
        } catch (java.io.IOException phoso) { throw 예외변환.I_O(phoso); }
        catch (RuntimeException phoso) { throw 예외변환.diragatsa_Taelo(phoso); }
    }
    public static void kwala(String leina, String Diteng_Boleng) throws 입출력예외 {
        try { kwala_baete_Boleng(leina, 문자.부호화(Diteng_Boleng));
        } catch (java.io.IOException phoso) { throw 예외변환.I_O(phoso); }
        catch (RuntimeException phoso) { throw 예외변환.diragatsa_Taelo(phoso); }
    }
}
