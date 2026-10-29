// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package العربية.ذاتي;

/** مخرجات(出力)과 بث_قيمة: 순서를 보존해 내보내는 바이트의 قناة_إدخال. */
public final class تدفق_الإنتاج {
    private final java.io.OutputStream قياسي_بث;
    تدفق_الإنتاج(java.io.OutputStream قياسي_بث) { this.قياسي_بث = قياسي_بث; }
    public void كتابة(int قيمة) throws إدخال_إخراج_استثناء {
        try { قياسي_بث.write(قيمة);
        } catch (java.io.IOException خطأ) { throw تحويل_استثناء.إدخال_إخراج(خطأ); }
        catch (RuntimeException خطأ) { throw تحويل_استثناء.ينفذ_أمر(خطأ); }
    }
    public void كتابة(byte[] بيانات) throws إدخال_إخراج_استثناء {
        try { قياسي_بث.write(بيانات);
        } catch (java.io.IOException خطأ) { throw تحويل_استثناء.إدخال_إخراج(خطأ); }
        catch (RuntimeException خطأ) { throw تحويل_استثناء.ينفذ_أمر(خطأ); }
    }
    public void كتابة(byte[] بيانات, int تشغيل, int 길이) throws إدخال_إخراج_استثناء {
        try { قياسي_بث.write(بيانات, تشغيل, 길이);
        } catch (java.io.IOException خطأ) { throw تحويل_استثناء.إدخال_إخراج(خطأ); }
        catch (RuntimeException خطأ) { throw تحويل_استثناء.ينفذ_أمر(خطأ); }
    }
    public void 내보내기() throws إدخال_إخراج_استثناء {
        try { قياسي_بث.flush();
        } catch (java.io.IOException خطأ) { throw تحويل_استثناء.إدخال_إخراج(خطأ); }
        catch (RuntimeException خطأ) { throw تحويل_استثناء.ينفذ_أمر(خطأ); }
    }
    public void إغلاق() throws إدخال_إخراج_استثناء {
        try { قياسي_بث.close();
        } catch (java.io.IOException خطأ) { throw تحويل_استثناء.إدخال_إخراج(خطأ); }
        catch (RuntimeException خطأ) { throw تحويل_استثناء.ينفذ_أمر(خطأ); }
    }
}
