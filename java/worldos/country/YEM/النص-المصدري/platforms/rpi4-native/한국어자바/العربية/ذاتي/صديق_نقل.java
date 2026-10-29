// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package العربية.ذاتي;
import java.net.*;
public final class صديق_نقل {
    private صديق_نقل() {}
    public static صديق فتح(String عنوان, int رقم_المنفذ) throws إدخال_إخراج_استثناء {
        try { return صديق.فتح(عنوان, رقم_المنفذ);
        } catch (java.io.IOException خطأ) { throw تحويل_استثناء.إدخال_إخراج(خطأ); }
        catch (RuntimeException خطأ) { throw تحويل_استثناء.ينفذ_أمر(خطأ); }
    }
    public static يستلم_منفذ 수신열기(int رقم_المنفذ) throws إدخال_إخراج_استثناء {
        try { return يستلم_منفذ.فتح(رقم_المنفذ);
        } catch (java.io.IOException خطأ) { throw تحويل_استثناء.إدخال_إخراج(خطأ); }
        catch (RuntimeException خطأ) { throw تحويل_استثناء.ينفذ_أمر(خطأ); }
    }
    public static Socket اتصال(String عنوان, int منفذ_قيمة) throws إدخال_إخراج_استثناء {
        try { return new Socket(عنوان, منفذ_قيمة);
        } catch (java.io.IOException خطأ) { throw تحويل_استثناء.إدخال_إخراج(خطأ); }
        catch (RuntimeException خطأ) { throw تحويل_استثناء.ينفذ_أمر(خطأ); }
    }
    public static ServerSocket انصات_المشارك(int منفذ_قيمة) throws إدخال_إخراج_استثناء {
        try { return new ServerSocket(منفذ_قيمة);
        } catch (java.io.IOException خطأ) { throw تحويل_استثناء.إدخال_إخراج(خطأ); }
        catch (RuntimeException خطأ) { throw تحويل_استثناء.ينفذ_أمر(خطأ); }
    }
    public static Socket يستلم(ServerSocket خادم_قيمة) throws إدخال_إخراج_استثناء {
        try { return خادم_قيمة.accept();
        } catch (java.io.IOException خطأ) { throw تحويل_استثناء.إدخال_إخراج(خطأ); }
        catch (RuntimeException خطأ) { throw تحويل_استثناء.ينفذ_أمر(خطأ); }
    }
}
