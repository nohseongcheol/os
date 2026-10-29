// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package עברית.עצמי;

/** קלט_ערך(入力)과 זרם_ערך: 순서대로 들어오는 바이트를 읽는 ערוץ_ערך_a3973059. */
public final class זרימת_קלט {
    private final java.io.InputStream תקן_זרם;
    זרימת_קלט(java.io.InputStream תקן_זרם) { this.תקן_זרם = תקן_זרם; }
    public int קרא() throws קלט_פלט_חריגה {
        try { return תקן_זרם.read();
        } catch (java.io.IOException שגיאה) { throw המר_חריגה.קלט_פלט(שגיאה); }
        catch (RuntimeException שגיאה) { throw המר_חריגה.לבצע_פקודה(שגיאה); }
    }
    public int קרא(byte[] נתונים) throws קלט_פלט_חריגה {
        try { return תקן_זרם.read(נתונים);
        } catch (java.io.IOException שגיאה) { throw המר_חריגה.קלט_פלט(שגיאה); }
        catch (RuntimeException שגיאה) { throw המר_חריגה.לבצע_פקודה(שגיאה); }
    }
    public int קרא(byte[] נתונים, int הפעלה, int 길이) throws קלט_פלט_חריגה {
        try { return תקן_זרם.read(נתונים, הפעלה, 길이);
        } catch (java.io.IOException שגיאה) { throw המר_חריגה.קלט_פלט(שגיאה); }
        catch (RuntimeException שגיאה) { throw המר_חריגה.לבצע_פקודה(שגיאה); }
    }
    public void סגירה() throws קלט_פלט_חריגה {
        try { תקן_זרם.close();
        } catch (java.io.IOException שגיאה) { throw המר_חריגה.קלט_פלט(שגיאה); }
        catch (RuntimeException שגיאה) { throw המר_חריגה.לבצע_פקודה(שגיאה); }
    }
}
