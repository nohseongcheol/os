// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package العربية.ذاتي;

/** اتصال(連結)·قناة_إدخال(通路): 상대와 이어진 TCP بايت_قيمة 흐름의 المشارك. */
public final class صديق {
    private final java.net.Socket قياسي_مكتبة_جسر;
    صديق(java.net.Socket قياسي_مكتبة_جسر) { this.قياسي_مكتبة_جسر = قياسي_مكتبة_جسر; }
    public static صديق فتح(String عنوان, int رقم_المنفذ) throws إدخال_إخراج_استثناء {
        try {
            return new صديق(new java.net.Socket(عنوان, رقم_المنفذ));
        } catch (java.io.IOException خطأ) { throw تحويل_استثناء.إدخال_إخراج(خطأ); }
        catch (RuntimeException خطأ) { throw تحويل_استثناء.ينفذ_أمر(خطأ); }
    }
    public تدفق_المدخلات إدخال_قيمة() throws إدخال_إخراج_استثناء {
        try { return new تدفق_المدخلات(قياسي_مكتبة_جسر.getInputStream());
        } catch (java.io.IOException خطأ) { throw تحويل_استثناء.إدخال_إخراج(خطأ); }
        catch (RuntimeException خطأ) { throw تحويل_استثناء.ينفذ_أمر(خطأ); }
    }
    public تدفق_الإنتاج مخرجات() throws إدخال_إخراج_استثناء {
        try { return new تدفق_الإنتاج(قياسي_مكتبة_جسر.getOutputStream());
        } catch (java.io.IOException خطأ) { throw تحويل_استثناء.إدخال_إخراج(خطأ); }
        catch (RuntimeException خطأ) { throw تحويل_استثناء.ينفذ_أمر(خطأ); }
    }
    public void 대기시간(int 밀리초) throws إدخال_إخراج_استثناء {
        try { قياسي_مكتبة_جسر.setSoTimeout(밀리초);
        } catch (java.io.IOException خطأ) { throw تحويل_استثناء.إدخال_إخراج(خطأ); }
        catch (RuntimeException خطأ) { throw تحويل_استثناء.ينفذ_أمر(خطأ); }
    }
    public int رقم_المنفذ() { return قياسي_مكتبة_جسر.getPort(); }
    public int محلي_رقم_المنفذ() { return قياسي_مكتبة_جسر.getLocalPort(); }
    public boolean أنظمة_المعلومات_مغلق() { return قياسي_مكتبة_جسر.isClosed(); }
    public boolean 연결됨() { return قياسي_مكتبة_جسر.isConnected(); }
    public void إغلاق() throws إدخال_إخراج_استثناء {
        try { قياسي_مكتبة_جسر.close();
        } catch (java.io.IOException خطأ) { throw تحويل_استثناء.إدخال_إخراج(خطأ); }
        catch (RuntimeException خطأ) { throw تحويل_استثناء.ينفذ_أمر(خطأ); }
    }
}
