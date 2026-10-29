// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package العربية.ذاتي;

/** رزمةمستقلة(電文)·قناة_إدخال(通路): 경계를 가진 UDP 자료를 주고받는 المشارك. */
public final class مخطط_بيانات_قناة {
    private final java.net.DatagramSocket قياسي_المشارك;
    private مخطط_بيانات_قناة(int رقم_المنفذ) throws إدخال_إخراج_استثناء {
        try { قياسي_المشارك = 통신.فتح(رقم_المنفذ);
        } catch (java.io.IOException خطأ) { throw تحويل_استثناء.إدخال_إخراج(خطأ); }
        catch (RuntimeException خطأ) { throw تحويل_استثناء.ينفذ_أمر(خطأ); }
    }
    public static مخطط_بيانات_قناة فتح(int رقم_المنفذ) throws إدخال_إخراج_استثناء {
        try { return new مخطط_بيانات_قناة(رقم_المنفذ);
        } catch (java.io.IOException خطأ) { throw تحويل_استثناء.إدخال_إخراج(خطأ); }
        catch (RuntimeException خطأ) { throw تحويل_استثناء.ينفذ_أمر(خطأ); }
    }
    public void يرسل(String عنوان, int رقم_المنفذ, String بيانات) throws إدخال_إخراج_استثناء {
        try { 통신.يرسل(قياسي_المشارك, عنوان, رقم_المنفذ, بيانات);
        } catch (java.io.IOException خطأ) { throw تحويل_استثناء.إدخال_إخراج(خطأ); }
        catch (RuntimeException خطأ) { throw تحويل_استثناء.ينفذ_أمر(خطأ); }
    }
    public String يستلم() throws إدخال_إخراج_استثناء {
        try { return 통신.يستلم(قياسي_المشارك);
        } catch (java.io.IOException خطأ) { throw تحويل_استثناء.إدخال_إخراج(خطأ); }
        catch (RuntimeException خطأ) { throw تحويل_استثناء.ينفذ_أمر(خطأ); }
    }
    public void 대기시간(int 밀리초) throws إدخال_إخراج_استثناء {
        try { 통신.대기시간(قياسي_المشارك, 밀리초);
        } catch (java.io.IOException خطأ) { throw تحويل_استثناء.إدخال_إخراج(خطأ); }
        catch (RuntimeException خطأ) { throw تحويل_استثناء.ينفذ_أمر(خطأ); }
    }
    public int رقم_المنفذ() { return قياسي_المشارك.getLocalPort(); }
    public boolean أنظمة_المعلومات_مغلق() { return قياسي_المشارك.isClosed(); }
    public void إغلاق() { 통신.إغلاق(قياسي_المشارك); }
}
