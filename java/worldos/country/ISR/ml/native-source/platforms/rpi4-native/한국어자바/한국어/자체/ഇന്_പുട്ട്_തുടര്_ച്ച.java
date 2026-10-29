// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 입력(入力)과 സ്ട്രീം_മൂല്യം: 순서대로 들어오는 바이트를 읽는 ചാനല്_എന്_ട്രി. */
public final class ഇന്_പുട്ട്_തുടര്_ച്ച {
    private final java.io.InputStream 표준흐름;
    ഇന്_പുട്ട്_തുടര്_ച്ച(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int വായന() throws ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്_ഒഴിവാക്കൽ {
        try { return 표준흐름.read();
        } catch (java.io.IOException പിശക്) { throw 예외변환.ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്(പിശക്); }
        catch (RuntimeException പിശക്) { throw 예외변환.നടപ്പാക്കുക_കമാന്_ഡ്(പിശക്); }
    }
    public int വായന(byte[] ഡാറ്റാ) throws ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്_ഒഴിവാക്കൽ {
        try { return 표준흐름.read(ഡാറ്റാ);
        } catch (java.io.IOException പിശക്) { throw 예외변환.ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്(പിശക്); }
        catch (RuntimeException പിശക്) { throw 예외변환.നടപ്പാക്കുക_കമാന്_ഡ്(പിശക്); }
    }
    public int വായന(byte[] ഡാറ്റാ, int നടപ്പിലാക്കുക, int ദൈര്_ഘ്യം_മൂല്യം) throws ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്_ഒഴിവാക്കൽ {
        try { return 표준흐름.read(ഡാറ്റാ, നടപ്പിലാക്കുക, ദൈര്_ഘ്യം_മൂല്യം);
        } catch (java.io.IOException പിശക്) { throw 예외변환.ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്(പിശക്); }
        catch (RuntimeException പിശക്) { throw 예외변환.നടപ്പാക്കുക_കമാന്_ഡ്(പിശക്); }
    }
    public void അടയ്ക്കു() throws ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്_ഒഴിവാക്കൽ {
        try { 표준흐름.close();
        } catch (java.io.IOException പിശക്) { throw 예외변환.ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്(പിശക്); }
        catch (RuntimeException പിശക്) { throw 예외변환.നടപ്പാക്കുക_കമാന്_ഡ്(പിശക്); }
    }
}
