// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 корисник 용어를 보존한다. актуелно_ставка 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class Датотека {
    private Датотека() {}
    public static byte[] 바이트읽기(String Назив) throws У_И_изузетак {
        try {
        FileInputStream ток_вриједност = new FileInputStream(Назив);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, вриједност;
            while ((вриједност = ток_вриједност.read()) != -1) { if (수 == 임시.length) throw new У_И_изузетак("Датотека Величина 제한"); 임시[수++] = (byte)вриједност; }
            byte[] ИСХОД = new byte[수]; System.arraycopy(임시, 0, ИСХОД, 0, 수); return ИСХОД;
        } finally { ток_вриједност.close(); }
        } catch (java.io.IOException ГРЕШКА) { throw конвертовати_изузетак.У_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw конвертовати_изузетак.Изврши_команда(ГРЕШКА); }
    }
    public static void писати_бајт_вриједност(String Назив, byte[] Садржај_вриједност) throws У_И_изузетак {
        try {
        FileOutputStream ток_вриједност = new FileOutputStream(Назив);
        try { for (int петља_индекс = 0; петља_индекс < Садржај_вриједност.length; петља_индекс++) ток_вриједност.write(Садржај_вриједност[петља_индекс] & 255); } finally { ток_вриједност.close(); }
        } catch (java.io.IOException ГРЕШКА) { throw конвертовати_изузетак.У_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw конвертовати_изузетак.Изврши_команда(ГРЕШКА); }
    }
    public static String Чита(String Назив) throws У_И_изузетак {
        try { return 문자.дешифровати_подаци(바이트읽기(Назив));
        } catch (java.io.IOException ГРЕШКА) { throw конвертовати_изузетак.У_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw конвертовати_изузетак.Изврши_команда(ГРЕШКА); }
    }
    public static void Пише(String Назив, String Садржај_вриједност) throws У_И_изузетак {
        try { писати_бајт_вриједност(Назив, 문자.부호화(Садржај_вриједност));
        } catch (java.io.IOException ГРЕШКА) { throw конвертовати_изузетак.У_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw конвертовати_изузетак.Изврши_команда(ГРЕШКА); }
    }
}
