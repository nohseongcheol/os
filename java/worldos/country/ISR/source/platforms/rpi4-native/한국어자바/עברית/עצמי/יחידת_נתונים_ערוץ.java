// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package עברית.עצמי;

/** יחידת_נתונים(電文)·ערוץ_ערך_a3973059(通路): 경계를 가진 UDP 자료를 주고받는 משתתף. */
public final class יחידת_נתונים_ערוץ {
    private final java.net.DatagramSocket תקן_משתתף;
    private יחידת_נתונים_ערוץ(int מספר_יציאה) throws קלט_פלט_חריגה {
        try { תקן_משתתף = 통신.פתח(מספר_יציאה);
        } catch (java.io.IOException שגיאה) { throw המר_חריגה.קלט_פלט(שגיאה); }
        catch (RuntimeException שגיאה) { throw המר_חריגה.לבצע_פקודה(שגיאה); }
    }
    public static יחידת_נתונים_ערוץ פתח(int מספר_יציאה) throws קלט_פלט_חריגה {
        try { return new יחידת_נתונים_ערוץ(מספר_יציאה);
        } catch (java.io.IOException שגיאה) { throw המר_חריגה.קלט_פלט(שגיאה); }
        catch (RuntimeException שגיאה) { throw המר_חריגה.לבצע_פקודה(שגיאה); }
    }
    public void שלח(String למען, int מספר_יציאה, String נתונים) throws קלט_פלט_חריגה {
        try { 통신.שלח(תקן_משתתף, למען, מספר_יציאה, נתונים);
        } catch (java.io.IOException שגיאה) { throw המר_חריגה.קלט_פלט(שגיאה); }
        catch (RuntimeException שגיאה) { throw המר_חריגה.לבצע_פקודה(שגיאה); }
    }
    public String לקבל() throws קלט_פלט_חריגה {
        try { return 통신.לקבל(תקן_משתתף);
        } catch (java.io.IOException שגיאה) { throw המר_חריגה.קלט_פלט(שגיאה); }
        catch (RuntimeException שגיאה) { throw המר_חריגה.לבצע_פקודה(שגיאה); }
    }
    public void פסק_זמן(int 밀리초) throws קלט_פלט_חריגה {
        try { 통신.פסק_זמן(תקן_משתתף, 밀리초);
        } catch (java.io.IOException שגיאה) { throw המר_חריגה.קלט_פלט(שגיאה); }
        catch (RuntimeException שגיאה) { throw המר_חריגה.לבצע_פקודה(שגיאה); }
    }
    public int מספר_יציאה() { return תקן_משתתף.getLocalPort(); }
    public boolean מערכות_מידע_נסגר() { return תקן_משתתף.isClosed(); }
    public void סגירה() { 통신.סגירה(תקן_משתתף); }
}
