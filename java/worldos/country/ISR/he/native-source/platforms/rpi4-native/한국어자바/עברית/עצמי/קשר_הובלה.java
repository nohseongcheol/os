// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package עברית.עצמי;
import java.net.*;
public final class קשר_הובלה {
    private קשר_הובלה() {}
    public static קשר פתח(String למען, int מספר_יציאה) throws קלט_פלט_חריגה {
        try { return קשר.פתח(למען, מספר_יציאה);
        } catch (java.io.IOException שגיאה) { throw המר_חריגה.קלט_פלט(שגיאה); }
        catch (RuntimeException שגיאה) { throw המר_חריגה.לבצע_פקודה(שגיאה); }
    }
    public static לקבל_הסב 수신열기(int מספר_יציאה) throws קלט_פלט_חריגה {
        try { return לקבל_הסב.פתח(מספר_יציאה);
        } catch (java.io.IOException שגיאה) { throw המר_חריגה.קלט_פלט(שגיאה); }
        catch (RuntimeException שגיאה) { throw המר_חריגה.לבצע_פקודה(שגיאה); }
    }
    public static Socket חיבור(String למען, int הסב_ערך) throws קלט_פלט_חריגה {
        try { return new Socket(למען, הסב_ערך);
        } catch (java.io.IOException שגיאה) { throw המר_חריגה.קלט_פלט(שגיאה); }
        catch (RuntimeException שגיאה) { throw המר_חריגה.לבצע_פקודה(שגיאה); }
    }
    public static ServerSocket להאזין_משתתף(int הסב_ערך) throws קלט_פלט_חריגה {
        try { return new ServerSocket(הסב_ערך);
        } catch (java.io.IOException שגיאה) { throw המר_חריגה.קלט_פלט(שגיאה); }
        catch (RuntimeException שגיאה) { throw המר_חריגה.לבצע_פקודה(שגיאה); }
    }
    public static Socket לקבל(ServerSocket שרת_ערך) throws קלט_פלט_חריגה {
        try { return שרת_ערך.accept();
        } catch (java.io.IOException שגיאה) { throw המר_חריגה.קלט_פלט(שגיאה); }
        catch (RuntimeException שגיאה) { throw המר_חריגה.לבצע_פקודה(שגיאה); }
    }
}
