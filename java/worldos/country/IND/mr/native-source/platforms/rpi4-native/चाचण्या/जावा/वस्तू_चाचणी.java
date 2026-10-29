// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface शक्य_गणनाकरा { int मूल्य(); }
class वॉलपेपर_मूल्य { static int तयार_करणे = 7; int संख्या; String नाव; वॉलपेपर_मूल्य(int संख्या) { this.संख्या = संख्या; नाव = "वॉलपेपर_मूल्य"; } int मूल्य() { return संख्या; } }
class शाखा_मूल्य extends वॉलपेपर_मूल्य implements शक्य_गणनाकरा { शाखा_मूल्य(int संख्या) { super(संख्या); नाव = "शाखा_मूल्य"; } public int मूल्य() { return संख्या * तयार_करणे; } }
public class वस्तू_चाचणी {
    static int प्रारंभिक_राज्य = वॉलपेपर_मूल्य.तयार_करणे + 2;
    static int शाखा(int संख्या) { switch (संख्या) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int विरळ_मूल्य(int संख्या) { switch (संख्या) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] बाबी) {
        शाखा_मूल्य दुसरे_संकार्य = new शाखा_मूल्य(6); वॉलपेपर_मूल्य तिसरे_संकार्य = दुसरे_संकार्य; शक्य_गणनाकरा चौथे_संकार्य = दुसरे_संकार्य;
        System.out.println(प्रारंभिक_राज्य + ":" + दुसरे_संकार्य.नाव + ":" + तिसरे_संकार्य.मूल्य() + ":" + चौथे_संकार्य.मूल्य());
        System.out.println((तिसरे_संकार्य instanceof शाखा_मूल्य) + ":" + (तिसरे_संकार्य instanceof शक्य_गणनाकरा) + ":" + शाखा(2) + ":" + विरळ_मूल्य(100));
        Object[] ऍरे_मूल्य = new Object[3]; ऍरे_मूल्य[0] = दुसरे_संकार्य; ऍरे_मूल्य[1] = "한글😀"; System.gc();
        System.out.println(((शाखा_मूल्य)ऍरे_मूल्य[0]).मूल्य()); System.out.println((String)ऍरे_मूल्य[1]);
        int[] संख्या_यादी_1801bec3 = {1, 2, 3, 4}; System.arraycopy(संख्या_यादी_1801bec3, 0, संख्या_यादी_1801bec3, 1, 3); System.out.println(संख्या_यादी_1801bec3[3]);
        byte[] बाइट_मूल्य = new byte[1]; बाइट_मूल्य[0] = (byte)255; char[] वर्ण = {'한'}; short[] आहे_लघु = {(short)65535}; boolean[] तर्कमूल्य_मूल्य = {true};
        System.out.println(बाइट_मूल्य[0] + ":" + वर्ण[0] + ":" + आहे_लघु[0] + ":" + तर्कमूल्य_मूल्य[0]);
    }
}
