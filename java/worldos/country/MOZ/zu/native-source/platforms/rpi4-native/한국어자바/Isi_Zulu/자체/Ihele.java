// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Isi_Zulu.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 umsebenzisi 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class Ihele {
    private Ihele() {}
    public static byte[] 바이트읽기(String Igama) throws 입출력예외 {
        try {
        FileInputStream Stream_inani = new FileInputStream(Igama);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, inani;
            while ((inani = Stream_inani.read()) != -1) { if (수 == 임시.length) throw new 입출력예외("Ihele Ubungako 제한"); 임시[수++] = (byte)inani; }
            byte[] 결과 = new byte[수]; System.arraycopy(임시, 0, 결과, 0, 수); return 결과;
        } finally { Stream_inani.close(); }
        } catch (java.io.IOException Iphutha) { throw 예외변환.i_I_O(Iphutha); }
        catch (RuntimeException Iphutha) { throw 예외변환.yenza_umyalo(Iphutha); }
    }
    public static void bhala_ibhayithi_inani(String Igama, byte[] Okuqukethwe_inani) throws 입출력예외 {
        try {
        FileOutputStream Stream_inani = new FileOutputStream(Igama);
        try { for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < Okuqukethwe_inani.length; iluphu_thola_inkomba++) Stream_inani.write(Okuqukethwe_inani[iluphu_thola_inkomba] & 255); } finally { Stream_inani.close(); }
        } catch (java.io.IOException Iphutha) { throw 예외변환.i_I_O(Iphutha); }
        catch (RuntimeException Iphutha) { throw 예외변환.yenza_umyalo(Iphutha); }
    }
    public static String Funda(String Igama) throws 입출력예외 {
        try { return 문자.guqulela_imininingwane(바이트읽기(Igama));
        } catch (java.io.IOException Iphutha) { throw 예외변환.i_I_O(Iphutha); }
        catch (RuntimeException Iphutha) { throw 예외변환.yenza_umyalo(Iphutha); }
    }
    public static void Bhala(String Igama, String Okuqukethwe_inani) throws 입출력예외 {
        try { bhala_ibhayithi_inani(Igama, 문자.부호화(Okuqukethwe_inani));
        } catch (java.io.IOException Iphutha) { throw 예외변환.i_I_O(Iphutha); }
        catch (RuntimeException Iphutha) { throw 예외변환.yenza_umyalo(Iphutha); }
    }
}
