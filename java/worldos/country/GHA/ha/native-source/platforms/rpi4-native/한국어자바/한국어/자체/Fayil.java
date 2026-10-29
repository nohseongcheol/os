// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 Mai_anfani_da_kwamfuta 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class Fayil {
    private Fayil() {}
    public static byte[] 바이트읽기(String Suna) throws I_O_banbanchi {
        try {
        FileInputStream watsuwa_Daraja = new FileInputStream(Suna);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, Daraja;
            while ((Daraja = watsuwa_Daraja.read()) != -1) { if (수 == 임시.length) throw new I_O_banbanchi("Fayil Girma 제한"); 임시[수++] = (byte)Daraja; }
            byte[] 결과 = new byte[수]; System.arraycopy(임시, 0, 결과, 0, 수); return 결과;
        } finally { watsuwa_Daraja.close(); }
        } catch (java.io.IOException Kuskure) { throw 예외변환.I_O(Kuskure); }
        catch (RuntimeException Kuskure) { throw 예외변환.gudanar_Umarni(Kuskure); }
    }
    public static void Rubuta_bayit_Daraja(String Suna, byte[] kunshiya_Daraja) throws I_O_banbanchi {
        try {
        FileOutputStream watsuwa_Daraja = new FileOutputStream(Suna);
        try { for (int Warware_Indes = 0; Warware_Indes < kunshiya_Daraja.length; Warware_Indes++) watsuwa_Daraja.write(kunshiya_Daraja[Warware_Indes] & 255); } finally { watsuwa_Daraja.close(); }
        } catch (java.io.IOException Kuskure) { throw 예외변환.I_O(Kuskure); }
        catch (RuntimeException Kuskure) { throw 예외변환.gudanar_Umarni(Kuskure); }
    }
    public static String Yi_Karatu(String Suna) throws I_O_banbanchi {
        try { return 문자.Bude_Tarin_bayani(바이트읽기(Suna));
        } catch (java.io.IOException Kuskure) { throw 예외변환.I_O(Kuskure); }
        catch (RuntimeException Kuskure) { throw 예외변환.gudanar_Umarni(Kuskure); }
    }
    public static void Yi_Rubutu(String Suna, String kunshiya_Daraja) throws I_O_banbanchi {
        try { Rubuta_bayit_Daraja(Suna, 문자.부호화(kunshiya_Daraja));
        } catch (java.io.IOException Kuskure) { throw 예외변환.I_O(Kuskure); }
        catch (RuntimeException Kuskure) { throw 예외변환.gudanar_Umarni(Kuskure); }
    }
}
