// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package עברית.עצמי;

/** לקבל_ערך_cef4d8ab(受信)·הסב_ערך(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class לקבל_הסב {
    private final java.net.ServerSocket תקן_הסב;
    private לקבל_הסב(int מספר_יציאה) throws קלט_פלט_חריגה {
        try { תקן_הסב = new java.net.ServerSocket(מספר_יציאה);
        } catch (java.io.IOException שגיאה) { throw המר_חריגה.קלט_פלט(שגיאה); }
        catch (RuntimeException שגיאה) { throw המר_חריגה.לבצע_פקודה(שגיאה); }
    }
    public static לקבל_הסב פתח(int מספר_יציאה) throws קלט_פלט_חריגה {
        try { return new לקבל_הסב(מספר_יציאה);
        } catch (java.io.IOException שגיאה) { throw המר_חריגה.קלט_פלט(שגיאה); }
        catch (RuntimeException שגיאה) { throw המר_חריגה.לבצע_פקודה(שגיאה); }
    }
    public קשר לקבל() throws קלט_פלט_חריגה {
        try { return new קשר(תקן_הסב.accept());
        } catch (java.io.IOException שגיאה) { throw המר_חריגה.קלט_פלט(שגיאה); }
        catch (RuntimeException שגיאה) { throw המר_חריגה.לבצע_פקודה(שגיאה); }
    }
    public int מספר_יציאה() { return תקן_הסב.getLocalPort(); }
    public void פסק_זמן(int 밀리초) throws קלט_פלט_חריגה {
        try { תקן_הסב.setSoTimeout(밀리초);
        } catch (java.io.IOException שגיאה) { throw המר_חריגה.קלט_פלט(שגיאה); }
        catch (RuntimeException שגיאה) { throw המר_חריגה.לבצע_פקודה(שגיאה); }
    }
    public boolean מערכות_מידע_נסגר() { return תקן_הסב.isClosed(); }
    public void סגירה() throws קלט_פלט_חריגה {
        try { תקן_הסב.close();
        } catch (java.io.IOException שגיאה) { throw המר_חריגה.קלט_פלט(שגיאה); }
        catch (RuntimeException שגיאה) { throw המר_חריגה.לבצע_פקודה(שגיאה); }
    }
}
