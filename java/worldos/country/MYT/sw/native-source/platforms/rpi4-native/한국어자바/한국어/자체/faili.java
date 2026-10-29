// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 mtumiaji 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class faili {
    private faili() {}
    public static byte[] 바이트읽기(String Jina) throws I_T_vighairi {
        try {
        FileInputStream Stream_thamani = new FileInputStream(Jina);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, thamani;
            while ((thamani = Stream_thamani.read()) != -1) { if (수 == 임시.length) throw new I_T_vighairi("faili panga_ukubwa 제한"); 임시[수++] = (byte)thamani; }
            byte[] 결과 = new byte[수]; System.arraycopy(임시, 0, 결과, 0, 수); return 결과;
        } finally { Stream_thamani.close(); }
        } catch (java.io.IOException kosa) { throw 예외변환.I_T(kosa); }
        catch (RuntimeException kosa) { throw 예외변환.tekeleza_amri(kosa); }
    }
    public static void andika_baiti_thamani(String Jina, byte[] maudhui_thamani) throws I_T_vighairi {
        try {
        FileOutputStream Stream_thamani = new FileOutputStream(Jina);
        try { for (int kitanzi_kielezo = 0; kitanzi_kielezo < maudhui_thamani.length; kitanzi_kielezo++) Stream_thamani.write(maudhui_thamani[kitanzi_kielezo] & 255); } finally { Stream_thamani.close(); }
        } catch (java.io.IOException kosa) { throw 예외변환.I_T(kosa); }
        catch (RuntimeException kosa) { throw 예외변환.tekeleza_amri(kosa); }
    }
    public static String 읽기(String Jina) throws I_T_vighairi {
        try { return 문자.simbua_fiche_data(바이트읽기(Jina));
        } catch (java.io.IOException kosa) { throw 예외변환.I_T(kosa); }
        catch (RuntimeException kosa) { throw 예외변환.tekeleza_amri(kosa); }
    }
    public static void andika(String Jina, String maudhui_thamani) throws I_T_vighairi {
        try { andika_baiti_thamani(Jina, 문자.부호화(maudhui_thamani));
        } catch (java.io.IOException kosa) { throw 예외변환.I_T(kosa); }
        catch (RuntimeException kosa) { throw 예외변환.tekeleza_amri(kosa); }
    }
}
