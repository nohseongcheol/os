// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 օգտվող 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class Ֆայլ {
    private Ֆայլ() {}
    public static byte[] 바이트읽기(String Անուն) throws 입출력예외 {
        try {
        FileInputStream հոսք_արժեք = new FileInputStream(Անուն);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, արժեք;
            while ((արժեք = հոսք_արժեք.read()) != -1) { if (수 == 임시.length) throw new 입출력예외("Ֆայլ Չափս 제한"); 임시[수++] = (byte)արժեք; }
            byte[] չափ = new byte[수]; System.arraycopy(임시, 0, չափ, 0, 수); return չափ;
        } finally { հոսք_արժեք.close(); }
        } catch (java.io.IOException Սխալ) { throw 예외변환.ներածում_արտածում(Սխալ); }
        catch (RuntimeException Սխալ) { throw 예외변환.կատարել_հրաման(Սխալ); }
    }
    public static void գրել_բայթ_արժեք(String Անուն, byte[] Բովանդակություն_արժեք) throws 입출력예외 {
        try {
        FileOutputStream հոսք_արժեք = new FileOutputStream(Անուն);
        try { for (int օղակում_դասիչ = 0; օղակում_դասիչ < Բովանդակություն_արժեք.length; օղակում_դասիչ++) հոսք_արժեք.write(Բովանդակություն_արժեք[օղակում_դասիչ] & 255); } finally { հոսք_արժեք.close(); }
        } catch (java.io.IOException Սխալ) { throw 예외변환.ներածում_արտածում(Սխալ); }
        catch (RuntimeException Սխալ) { throw 예외변환.կատարել_հրաման(Սխալ); }
    }
    public static String Ընթերցում(String Անուն) throws 입출력예외 {
        try { return 문자.վերծանել_տվյալ(바이트읽기(Անուն));
        } catch (java.io.IOException Սխալ) { throw 예외변환.ներածում_արտածում(Սխալ); }
        catch (RuntimeException Սխալ) { throw 예외변환.կատարել_հրաման(Սխալ); }
    }
    public static void Գրել(String Անուն, String Բովանդակություն_արժեք) throws 입출력예외 {
        try { գրել_բայթ_արժեք(Անուն, 문자.부호화(Բովանդակություն_արժեք));
        } catch (java.io.IOException Սխալ) { throw 예외변환.ներածում_արտածում(Սխալ); }
        catch (RuntimeException Սխալ) { throw 예외변환.կատարել_հրաման(Սխալ); }
    }
}
