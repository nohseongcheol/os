// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package עברית.עצמי;

/** פלטטקסט(出力)과 זרם_ערך: 순서를 보존해 내보내는 바이트의 ערוץ_ערך_a3973059. */
public final class זרימת_פלט {
    private final java.io.OutputStream תקן_זרם;
    זרימת_פלט(java.io.OutputStream תקן_זרם) { this.תקן_זרם = תקן_זרם; }
    public void כתוב(int ערך) throws קלט_פלט_חריגה {
        try { תקן_זרם.write(ערך);
        } catch (java.io.IOException שגיאה) { throw המר_חריגה.קלט_פלט(שגיאה); }
        catch (RuntimeException שגיאה) { throw המר_חריגה.לבצע_פקודה(שגיאה); }
    }
    public void כתוב(byte[] נתונים) throws קלט_פלט_חריגה {
        try { תקן_זרם.write(נתונים);
        } catch (java.io.IOException שגיאה) { throw המר_חריגה.קלט_פלט(שגיאה); }
        catch (RuntimeException שגיאה) { throw המר_חריגה.לבצע_פקודה(שגיאה); }
    }
    public void כתוב(byte[] נתונים, int הפעלה, int 길이) throws קלט_פלט_חריגה {
        try { תקן_זרם.write(נתונים, הפעלה, 길이);
        } catch (java.io.IOException שגיאה) { throw המר_חריגה.קלט_פלט(שגיאה); }
        catch (RuntimeException שגיאה) { throw המר_חריגה.לבצע_פקודה(שגיאה); }
    }
    public void 내보내기() throws קלט_פלט_חריגה {
        try { תקן_זרם.flush();
        } catch (java.io.IOException שגיאה) { throw המר_חריגה.קלט_פלט(שגיאה); }
        catch (RuntimeException שגיאה) { throw המר_חריגה.לבצע_פקודה(שגיאה); }
    }
    public void סגירה() throws קלט_פלט_חריגה {
        try { תקן_זרם.close();
        } catch (java.io.IOException שגיאה) { throw המר_חריגה.קלט_פלט(שגיאה); }
        catch (RuntimeException שגיאה) { throw המר_חריגה.לבצע_פקודה(שגיאה); }
    }
}
