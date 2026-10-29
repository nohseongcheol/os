// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 пайдаланушы 용어를 보존한다. ток_элемент 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class Файл {
    private Файл() {}
    public static byte[] 바이트읽기(String Аты) throws енгізу_шығару_ерекшелік {
        try {
        FileInputStream ағым_мән = new FileInputStream(Аты);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, мән;
            while ((мән = ағым_мән.read()) != -1) { if (수 == 임시.length) throw new енгізу_шығару_ерекшелік("Файл Өлшемі 제한"); 임시[수++] = (byte)мән; }
            byte[] НӘТИЖЕ = new byte[수]; System.arraycopy(임시, 0, НӘТИЖЕ, 0, 수); return НӘТИЖЕ;
        } finally { ағым_мән.close(); }
        } catch (java.io.IOException Қате) { throw Түрлендіру_ерекшелік.енгізу_шығару(Қате); }
        catch (RuntimeException Қате) { throw Түрлендіру_ерекшелік.орындау_пәрмен(Қате); }
    }
    public static void жазу_байт_мән(String Аты, byte[] мазмұн_мән) throws енгізу_шығару_ерекшелік {
        try {
        FileOutputStream ағым_мән = new FileOutputStream(Аты);
        try { for (int тұйық_индекс = 0; тұйық_индекс < мазмұн_мән.length; тұйық_индекс++) ағым_мән.write(мазмұн_мән[тұйық_индекс] & 255); } finally { ағым_мән.close(); }
        } catch (java.io.IOException Қате) { throw Түрлендіру_ерекшелік.енгізу_шығару(Қате); }
        catch (RuntimeException Қате) { throw Түрлендіру_ерекшелік.орындау_пәрмен(Қате); }
    }
    public static String Оқу(String Аты) throws енгізу_шығару_ерекшелік {
        try { return 문자.шифрді_шешу_деректер(바이트읽기(Аты));
        } catch (java.io.IOException Қате) { throw Түрлендіру_ерекшелік.енгізу_шығару(Қате); }
        catch (RuntimeException Қате) { throw Түрлендіру_ерекшелік.орындау_пәрмен(Қате); }
    }
    public static void Жазу(String Аты, String мазмұн_мән) throws енгізу_шығару_ерекшелік {
        try { жазу_байт_мән(Аты, 문자.부호화(мазмұн_мән));
        } catch (java.io.IOException Қате) { throw Түрлендіру_ерекшелік.енгізу_шығару(Қате); }
        catch (RuntimeException Қате) { throw Түрлендіру_ерекшелік.орындау_пәрмен(Қате); }
    }
}
