// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package עברית.עצמי;

/** חיבור(連結)·ערוץ_ערך_a3973059(通路): 상대와 이어진 TCP בית_ערך 흐름의 משתתף. */
public final class קשר {
    private final java.net.Socket תקן_ספריה_גשר;
    קשר(java.net.Socket תקן_ספריה_גשר) { this.תקן_ספריה_גשר = תקן_ספריה_גשר; }
    public static קשר פתח(String למען, int מספר_יציאה) throws קלט_פלט_חריגה {
        try {
            return new קשר(new java.net.Socket(למען, מספר_יציאה));
        } catch (java.io.IOException שגיאה) { throw המר_חריגה.קלט_פלט(שגיאה); }
        catch (RuntimeException שגיאה) { throw המר_חריגה.לבצע_פקודה(שגיאה); }
    }
    public זרימת_קלט קלט_ערך() throws קלט_פלט_חריגה {
        try { return new זרימת_קלט(תקן_ספריה_גשר.getInputStream());
        } catch (java.io.IOException שגיאה) { throw המר_חריגה.קלט_פלט(שגיאה); }
        catch (RuntimeException שגיאה) { throw המר_חריגה.לבצע_פקודה(שגיאה); }
    }
    public זרימת_פלט פלטטקסט() throws קלט_פלט_חריגה {
        try { return new זרימת_פלט(תקן_ספריה_גשר.getOutputStream());
        } catch (java.io.IOException שגיאה) { throw המר_חריגה.קלט_פלט(שגיאה); }
        catch (RuntimeException שגיאה) { throw המר_חריגה.לבצע_פקודה(שגיאה); }
    }
    public void פסק_זמן(int 밀리초) throws קלט_פלט_חריגה {
        try { תקן_ספריה_גשר.setSoTimeout(밀리초);
        } catch (java.io.IOException שגיאה) { throw המר_חריגה.קלט_פלט(שגיאה); }
        catch (RuntimeException שגיאה) { throw המר_חריגה.לבצע_פקודה(שגיאה); }
    }
    public int מספר_יציאה() { return תקן_ספריה_גשר.getPort(); }
    public int מקומי_מספר_יציאה() { return תקן_ספריה_גשר.getLocalPort(); }
    public boolean מערכות_מידע_נסגר() { return תקן_ספריה_גשר.isClosed(); }
    public boolean 연결됨() { return תקן_ספריה_גשר.isConnected(); }
    public void סגירה() throws קלט_פלט_חריגה {
        try { תקן_ספריה_גשר.close();
        } catch (java.io.IOException שגיאה) { throw המר_חריגה.קלט_פלט(שגיאה); }
        catch (RuntimeException שגיאה) { throw המר_חריגה.לבצע_פקודה(שגיאה); }
    }
}
