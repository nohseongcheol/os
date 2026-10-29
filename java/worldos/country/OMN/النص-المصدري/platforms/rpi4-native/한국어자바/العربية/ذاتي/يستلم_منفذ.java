// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package العربية.ذاتي;

/** يستلم_قيمة(受信)·منفذ_قيمة(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class يستلم_منفذ {
    private final java.net.ServerSocket قياسي_منفذ;
    private يستلم_منفذ(int رقم_المنفذ) throws إدخال_إخراج_استثناء {
        try { قياسي_منفذ = new java.net.ServerSocket(رقم_المنفذ);
        } catch (java.io.IOException خطأ) { throw تحويل_استثناء.إدخال_إخراج(خطأ); }
        catch (RuntimeException خطأ) { throw تحويل_استثناء.ينفذ_أمر(خطأ); }
    }
    public static يستلم_منفذ فتح(int رقم_المنفذ) throws إدخال_إخراج_استثناء {
        try { return new يستلم_منفذ(رقم_المنفذ);
        } catch (java.io.IOException خطأ) { throw تحويل_استثناء.إدخال_إخراج(خطأ); }
        catch (RuntimeException خطأ) { throw تحويل_استثناء.ينفذ_أمر(خطأ); }
    }
    public صديق يستلم() throws إدخال_إخراج_استثناء {
        try { return new صديق(قياسي_منفذ.accept());
        } catch (java.io.IOException خطأ) { throw تحويل_استثناء.إدخال_إخراج(خطأ); }
        catch (RuntimeException خطأ) { throw تحويل_استثناء.ينفذ_أمر(خطأ); }
    }
    public int رقم_المنفذ() { return قياسي_منفذ.getLocalPort(); }
    public void 대기시간(int 밀리초) throws إدخال_إخراج_استثناء {
        try { قياسي_منفذ.setSoTimeout(밀리초);
        } catch (java.io.IOException خطأ) { throw تحويل_استثناء.إدخال_إخراج(خطأ); }
        catch (RuntimeException خطأ) { throw تحويل_استثناء.ينفذ_أمر(خطأ); }
    }
    public boolean أنظمة_المعلومات_مغلق() { return قياسي_منفذ.isClosed(); }
    public void إغلاق() throws إدخال_إخراج_استثناء {
        try { قياسي_منفذ.close();
        } catch (java.io.IOException خطأ) { throw تحويل_استثناء.إدخال_إخراج(خطأ); }
        catch (RuntimeException خطأ) { throw تحويل_استثناء.ينفذ_أمر(خطأ); }
    }
}
