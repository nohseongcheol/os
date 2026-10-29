// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package العربية.ذاتي;

/** إدخال_قيمة(入力)과 بث_قيمة: 순서대로 들어오는 바이트를 읽는 قناة_إدخال. */
public final class تدفق_المدخلات {
    private final java.io.InputStream قياسي_بث;
    تدفق_المدخلات(java.io.InputStream قياسي_بث) { this.قياسي_بث = قياسي_بث; }
    public int قراءة() throws إدخال_إخراج_استثناء {
        try { return قياسي_بث.read();
        } catch (java.io.IOException خطأ) { throw تحويل_استثناء.إدخال_إخراج(خطأ); }
        catch (RuntimeException خطأ) { throw تحويل_استثناء.ينفذ_أمر(خطأ); }
    }
    public int قراءة(byte[] بيانات) throws إدخال_إخراج_استثناء {
        try { return قياسي_بث.read(بيانات);
        } catch (java.io.IOException خطأ) { throw تحويل_استثناء.إدخال_إخراج(خطأ); }
        catch (RuntimeException خطأ) { throw تحويل_استثناء.ينفذ_أمر(خطأ); }
    }
    public int قراءة(byte[] بيانات, int تشغيل, int 길이) throws إدخال_إخراج_استثناء {
        try { return قياسي_بث.read(بيانات, تشغيل, 길이);
        } catch (java.io.IOException خطأ) { throw تحويل_استثناء.إدخال_إخراج(خطأ); }
        catch (RuntimeException خطأ) { throw تحويل_استثناء.ينفذ_أمر(خطأ); }
    }
    public void إغلاق() throws إدخال_إخراج_استثناء {
        try { قياسي_بث.close();
        } catch (java.io.IOException خطأ) { throw تحويل_استثناء.إدخال_إخراج(خطأ); }
        catch (RuntimeException خطأ) { throw تحويل_استثناء.ينفذ_أمر(خطأ); }
    }
}
