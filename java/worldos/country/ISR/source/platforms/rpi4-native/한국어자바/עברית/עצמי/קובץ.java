// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package עברית.עצמי;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 משתמש 용어를 보존한다. נוכחי_פריט 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class קובץ {
    private קובץ() {}
    public static byte[] 바이트읽기(String שם) throws קלט_פלט_חריגה {
        try {
        FileInputStream זרם_ערך = new FileInputStream(שם);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, ערך;
            while ((ערך = זרם_ערך.read()) != -1) { if (수 == 임시.length) throw new קלט_פלט_חריגה("קובץ גודל 제한"); 임시[수++] = (byte)ערך; }
            byte[] תוצאה = new byte[수]; System.arraycopy(임시, 0, תוצאה, 0, 수); return תוצאה;
        } finally { זרם_ערך.close(); }
        } catch (java.io.IOException שגיאה) { throw המר_חריגה.קלט_פלט(שגיאה); }
        catch (RuntimeException שגיאה) { throw המר_חריגה.לבצע_פקודה(שגיאה); }
    }
    public static void כתיבה_בית_ערך(String שם, byte[] תוכן_ערך) throws קלט_פלט_חריגה {
        try {
        FileOutputStream זרם_ערך = new FileOutputStream(שם);
        try { for (int לולאה_מדד = 0; לולאה_מדד < תוכן_ערך.length; לולאה_מדד++) זרם_ערך.write(תוכן_ערך[לולאה_מדד] & 255); } finally { זרם_ערך.close(); }
        } catch (java.io.IOException שגיאה) { throw המר_חריגה.קלט_פלט(שגיאה); }
        catch (RuntimeException שגיאה) { throw המר_חריגה.לבצע_פקודה(שגיאה); }
    }
    public static String קרא(String שם) throws קלט_פלט_חריגה {
        try { return 문자.פענח_נתונים(바이트읽기(שם));
        } catch (java.io.IOException שגיאה) { throw המר_חריגה.קלט_פלט(שגיאה); }
        catch (RuntimeException שגיאה) { throw המר_חריגה.לבצע_פקודה(שגיאה); }
    }
    public static void כתוב(String שם, String תוכן_ערך) throws קלט_פלט_חריגה {
        try { כתיבה_בית_ערך(שם, 문자.לקדד(תוכן_ערך));
        } catch (java.io.IOException שגיאה) { throw המר_חריגה.קלט_פלט(שגיאה); }
        catch (RuntimeException שגיאה) { throw המר_חריגה.לבצע_פקודה(שגיאה); }
    }
}
