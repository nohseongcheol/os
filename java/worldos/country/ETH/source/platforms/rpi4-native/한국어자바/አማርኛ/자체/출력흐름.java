// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package አማርኛ.자체;

/** ውጤት(出力)과 ልቀቅ_እሴት: 순서를 보존해 내보내는 바이트의 ሰርጥ_ምዝግብ. */
public final class 출력흐름 {
    private final java.io.OutputStream 표준흐름;
    출력흐름(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void መጻፊያ(int እሴት) throws ግቤት_ውጤት_ልዩነት {
        try { 표준흐름.write(እሴት);
        } catch (java.io.IOException ስህተት) { throw 예외변환.ግቤት_ውጤት(ስህተት); }
        catch (RuntimeException ስህተት) { throw 예외변환.ፈጽም_ትእዛዝ(ስህተት); }
    }
    public void መጻፊያ(byte[] ውሂብ) throws ግቤት_ውጤት_ልዩነት {
        try { 표준흐름.write(ውሂብ);
        } catch (java.io.IOException ስህተት) { throw 예외변환.ግቤት_ውጤት(ስህተት); }
        catch (RuntimeException ስህተት) { throw 예외변환.ፈጽም_ትእዛዝ(ስህተት); }
    }
    public void መጻፊያ(byte[] ውሂብ, int ማስኬጃ, int ርዝመት_እሴት) throws ግቤት_ውጤት_ልዩነት {
        try { 표준흐름.write(ውሂብ, ማስኬጃ, ርዝመት_እሴት);
        } catch (java.io.IOException ስህተት) { throw 예외변환.ግቤት_ውጤት(ስህተት); }
        catch (RuntimeException ስህተት) { throw 예외변환.ፈጽም_ትእዛዝ(ስህተት); }
    }
    public void 내보내기() throws ግቤት_ውጤት_ልዩነት {
        try { 표준흐름.flush();
        } catch (java.io.IOException ስህተት) { throw 예외변환.ግቤት_ውጤት(ስህተት); }
        catch (RuntimeException ስህተት) { throw 예외변환.ፈጽም_ትእዛዝ(ስህተት); }
    }
    public void መዝጊያ() throws ግቤት_ውጤት_ልዩነት {
        try { 표준흐름.close();
        } catch (java.io.IOException ስህተት) { throw 예외변환.ግቤት_ውጤት(ስህተት); }
        catch (RuntimeException ስህተት) { throw 예외변환.ፈጽም_ትእዛዝ(ስህተት); }
    }
}
