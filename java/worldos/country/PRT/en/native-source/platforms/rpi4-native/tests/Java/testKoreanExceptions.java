// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import English.Native.*;

public class testKoreanExceptions {
    static void defaultTimeout() throws java.io.IOException {
        throw new java.net.SocketTimeoutException("원래 exception");
    }
    public static void main(String[] arguments) throws InputOutputException {
        try { throw new WaitTimeoutException("waitState ending"); }
        catch (WaitTimeoutException error) { Output.writeLine(error.description()); }
        try { throw new AddressLookupException("address failureValue"); }
        catch (InputOutputException error) { Output.writeLine(error.description()); }
        try { throw new MissingFileException("file failureValue"); }
        catch (java.io.IOException error) { Output.writeLine("표준 상위 exception 호환"); }
        try { defaultTimeout(); }
        catch (WaitTimeoutException wasCaughtIncorrectly) { Output.writeLine("잘못된 alternateName"); }
        catch (java.io.IOException originalError) { Output.writeLine("English 예외의 독립된 typeCategory"); }
        try { file.read("없는한글파일"); }
        catch (MissingFileException error) { Output.writeLine("file error English convertValue"); }
        try { Characters.parseInteger("숫자가아님"); }
        catch (NumberFormatFailure error) { Output.writeLine("digitValue error English convertValue"); }
        try { Checks.require(false, "Checks failureValue"); }
        catch (InvalidArgumentException error) { Output.writeLine(error.description()); }
        try { throw new ArrayBoundsException("clip failureValue"); }
        catch (BoundsException error) { Output.writeLine(error.description()); }
        try { throw new NullReferenceException("빈 reference"); }
        catch (java.lang.RuntimeException error) { Output.writeLine("executeCommand exception 호환"); }
        try { throw new exception("직접 정의한 description"); }
        catch (exception error) { Output.writeLine(error.description()); }
        try { throw new ThreadStateException("ThreadStateException"); }
        catch (ThreadStateException error) { Output.writeLine(error.description()); }
        try { throw new WaitTimeoutException("WaitTimeoutException"); }
        catch (WaitTimeoutException error) { Output.writeLine(error.description()); }
        try { throw new WaitInterruptedException("WaitInterruptedException"); }
        catch (WaitInterruptedException error) { Output.writeLine(error.description()); }
        try { throw new StringBoundsException("StringBoundsException"); }
        catch (StringBoundsException error) { Output.writeLine(error.description()); }
        try { throw new ArrayBoundsException("ArrayBoundsException"); }
        catch (ArrayBoundsException error) { Output.writeLine(error.description()); }
        try { throw new ArrayStoreFailure("ArrayStoreFailure"); }
        catch (ArrayStoreFailure error) { Output.writeLine(error.description()); }
        try { throw new BoundsException("BoundsException"); }
        catch (BoundsException error) { Output.writeLine(error.description()); }
        try { throw new NullReferenceException("NullReferenceException"); }
        catch (NullReferenceException error) { Output.writeLine(error.description()); }
        try { throw new ArithmeticFailure("ArithmeticFailure"); }
        catch (ArithmeticFailure error) { Output.writeLine(error.description()); }
        try { throw new StateException("StateException"); }
        catch (StateException error) { Output.writeLine(error.description()); }
        try { throw new NumberFormatFailure("NumberFormatFailure"); }
        catch (NumberFormatFailure error) { Output.writeLine(error.description()); }
        try { throw new ExecutionException("ExecutionException"); }
        catch (ExecutionException error) { Output.writeLine(error.description()); }
        try { throw new exception("exception"); }
        catch (exception error) { Output.writeLine(error.description()); }
        try { throw new NegativeArraySizeFailure("NegativeArraySizeFailure"); }
        catch (NegativeArraySizeFailure error) { Output.writeLine(error.description()); }
        try { throw new InputOutputException("InputOutputException"); }
        catch (InputOutputException error) { Output.writeLine(error.description()); }
        try { throw new InvalidArgumentException("InvalidArgumentException"); }
        catch (InvalidArgumentException error) { Output.writeLine(error.description()); }
        try { throw new AddressLookupException("AddressLookupException"); }
        catch (AddressLookupException error) { Output.writeLine(error.description()); }
        try { throw new CommunicationException("CommunicationException"); }
        catch (CommunicationException error) { Output.writeLine(error.description()); }
        try { throw new MissingFileException("MissingFileException"); }
        catch (MissingFileException error) { Output.writeLine(error.description()); }
        try { throw new TypeCastException("TypeCastException"); }
        catch (TypeCastException error) { Output.writeLine(error.description()); }
        Output.writeLine("English exception processValueEntry isComplete");
    }
}
