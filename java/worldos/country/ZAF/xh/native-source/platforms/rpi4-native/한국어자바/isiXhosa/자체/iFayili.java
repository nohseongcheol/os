// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package isiXhosa.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 umsebenzisi 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class iFayili {
    private iFayili() {}
    public static byte[] 바이트읽기(String Igama) throws 입출력예외 {
        try {
        FileInputStream Stream_ixabiso = new FileInputStream(Igama);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, ixabiso;
            while ((ixabiso = Stream_ixabiso.read()) != -1) { if (수 == 임시.length) throw new 입출력예외("iFayili Ubukhulu 제한"); 임시[수++] = (byte)ixabiso; }
            byte[] 결과 = new byte[수]; System.arraycopy(임시, 0, 결과, 0, 수); return 결과;
        } finally { Stream_ixabiso.close(); }
        } catch (java.io.IOException Impazamo) { throw 예외변환.i_I_O(Impazamo); }
        catch (RuntimeException Impazamo) { throw 예외변환.ukwenza_umyalelo(Impazamo); }
    }
    public static void bhala_ibhayithi_ixabiso(String Igama, byte[] Isiqulatho_ixabiso) throws 입출력예외 {
        try {
        FileOutputStream Stream_ixabiso = new FileOutputStream(Igama);
        try { for (int iluphu_indeksa = 0; iluphu_indeksa < Isiqulatho_ixabiso.length; iluphu_indeksa++) Stream_ixabiso.write(Isiqulatho_ixabiso[iluphu_indeksa] & 255); } finally { Stream_ixabiso.close(); }
        } catch (java.io.IOException Impazamo) { throw 예외변환.i_I_O(Impazamo); }
        catch (RuntimeException Impazamo) { throw 예외변환.ukwenza_umyalelo(Impazamo); }
    }
    public static String Funda(String Igama) throws 입출력예외 {
        try { return 문자.buyisela_ubhalo_oluqhelekileyo_iingcombolo(바이트읽기(Igama));
        } catch (java.io.IOException Impazamo) { throw 예외변환.i_I_O(Impazamo); }
        catch (RuntimeException Impazamo) { throw 예외변환.ukwenza_umyalelo(Impazamo); }
    }
    public static void Bhala(String Igama, String Isiqulatho_ixabiso) throws 입출력예외 {
        try { bhala_ibhayithi_ixabiso(Igama, 문자.부호화(Isiqulatho_ixabiso));
        } catch (java.io.IOException Impazamo) { throw 예외변환.i_I_O(Impazamo); }
        catch (RuntimeException Impazamo) { throw 예외변환.ukwenza_umyalelo(Impazamo); }
    }
}
