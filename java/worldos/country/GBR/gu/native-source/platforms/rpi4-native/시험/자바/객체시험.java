// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int મૂલ્ય(); }
class વૉલપેપર_મૂલ્ય { static int તૈયાર_કરો = 7; int 수; String નામ; વૉલપેપર_મૂલ્ય(int 수) { this.수 = 수; નામ = "વૉલપેપર_મૂલ્ય"; } int મૂલ્ય() { return 수; } }
class શાખા_મૂલ્ય extends વૉલપેપર_મૂલ્ય implements 계산가능 { શાખા_મૂલ્ય(int 수) { super(수); નામ = "શાખા_મૂલ્ય"; } public int મૂલ્ય() { return 수 * તૈયાર_કરો; } }
public class 객체시험 {
    static int 초기 = વૉલપેપર_મૂલ્ય.તૈયાર_કરો + 2;
    static int શાખા(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] દલીલો) {
        શાખા_મૂલ્ય 나 = new શાખા_મૂલ્ય(6); વૉલપેપર_મૂલ્ય 다 = 나; 계산가능 라 = 나;
        System.out.println(초기 + ":" + 나.નામ + ":" + 다.મૂલ્ય() + ":" + 라.મૂલ્ય());
        System.out.println((다 instanceof શાખા_મૂલ્ય) + ":" + (다 instanceof 계산가능) + ":" + શાખા(2) + ":" + 띄엄(100));
        Object[] અરે_મૂલ્ય = new Object[3]; અરે_મૂલ્ય[0] = 나; અરે_મૂલ્ય[1] = "한글😀"; System.gc();
        System.out.println(((શાખા_મૂલ્ય)અરે_મૂલ્ય[0]).મૂલ્ય()); System.out.println((String)અરે_મૂલ્ય[1]);
        int[] 수들 = {1, 2, 3, 4}; System.arraycopy(수들, 0, 수들, 1, 3); System.out.println(수들[3]);
        byte[] બાઇટ_મૂલ્ય = new byte[1]; બાઇટ_મૂલ્ય[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] 참거짓 = {true};
        System.out.println(બાઇટ_મૂલ્ય[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + 참거짓[0]);
    }
}
