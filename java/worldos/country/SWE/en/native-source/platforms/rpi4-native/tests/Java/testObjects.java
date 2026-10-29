// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface canCalculate { int value(); }
class backgroundValue { static int prepare = 7; int number; String name; backgroundValue(int number) { this.number = number; name = "backgroundValue"; } int value() { return number; } }
class branchValue extends backgroundValue implements canCalculate { branchValue(int number) { super(number); name = "branchValue"; } public int value() { return number * prepare; } }
public class testObjects {
    static int initialState = backgroundValue.prepare + 2;
    static int branch(int number) { switch (number) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int sparseValue(int number) { switch (number) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] arguments) {
        branchValue secondOperand = new branchValue(6); backgroundValue thirdOperand = secondOperand; canCalculate fourthOperand = secondOperand;
        System.out.println(initialState + ":" + secondOperand.name + ":" + thirdOperand.value() + ":" + fourthOperand.value());
        System.out.println((thirdOperand instanceof branchValue) + ":" + (thirdOperand instanceof canCalculate) + ":" + branch(2) + ":" + sparseValue(100));
        Object[] arrayValue = new Object[3]; arrayValue[0] = secondOperand; arrayValue[1] = "한글😀"; System.gc();
        System.out.println(((branchValue)arrayValue[0]).value()); System.out.println((String)arrayValue[1]);
        int[] countList = {1, 2, 3, 4}; System.arraycopy(countList, 0, countList, 1, 3); System.out.println(countList[3]);
        byte[] byteValue = new byte[1]; byteValue[0] = (byte)255; char[] Characters = {'한'}; short[] isShort = {(short)65535}; boolean[] booleanValue = {true};
        System.out.println(byteValue[0] + ":" + Characters[0] + ":" + isShort[0] + ":" + booleanValue[0]);
    }
}
