// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package العربية.ذاتي;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 فضاء_المستخدم 용어를 보존한다. حديث_عنصر 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class ملف {
    private ملف() {}
    public static byte[] يقرأ_بايت_قيمة(String اسم) throws إدخال_إخراج_استثناء {
        try {
        FileInputStream بث_قيمة = new FileInputStream(اسم);
        try {
            byte[] 임시 = new byte[16384]; int رقم = 0, قيمة;
            while ((قيمة = بث_قيمة.read()) != -1) { if (رقم == 임시.length) throw new إدخال_إخراج_استثناء("ملف حجم 제한"); 임시[رقم++] = (byte)قيمة; }
            byte[] نتيجة = new byte[رقم]; System.arraycopy(임시, 0, نتيجة, 0, رقم); return نتيجة;
        } finally { بث_قيمة.close(); }
        } catch (java.io.IOException خطأ) { throw تحويل_استثناء.إدخال_إخراج(خطأ); }
        catch (RuntimeException خطأ) { throw تحويل_استثناء.ينفذ_أمر(خطأ); }
    }
    public static void كتابة_بايت_قيمة(String اسم, byte[] محتوى_قيمة) throws إدخال_إخراج_استثناء {
        try {
        FileOutputStream بث_قيمة = new FileOutputStream(اسم);
        try { for (int يكرر_فهرس = 0; يكرر_فهرس < محتوى_قيمة.length; يكرر_فهرس++) بث_قيمة.write(محتوى_قيمة[يكرر_فهرس] & 255); } finally { بث_قيمة.close(); }
        } catch (java.io.IOException خطأ) { throw تحويل_استثناء.إدخال_إخراج(خطأ); }
        catch (RuntimeException خطأ) { throw تحويل_استثناء.ينفذ_أمر(خطأ); }
    }
    public static String قراءة(String اسم) throws إدخال_إخراج_استثناء {
        try { return 문자.يفك_التشفير_بيانات(يقرأ_بايت_قيمة(اسم));
        } catch (java.io.IOException خطأ) { throw تحويل_استثناء.إدخال_إخراج(خطأ); }
        catch (RuntimeException خطأ) { throw تحويل_استثناء.ينفذ_أمر(خطأ); }
    }
    public static void كتابة(String اسم, String محتوى_قيمة) throws إدخال_إخراج_استثناء {
        try { كتابة_بايت_قيمة(اسم, 문자.يرمّز(محتوى_قيمة));
        } catch (java.io.IOException خطأ) { throw تحويل_استثناء.إدخال_إخراج(خطأ); }
        catch (RuntimeException خطأ) { throw تحويل_استثناء.ينفذ_أمر(خطأ); }
    }
}
