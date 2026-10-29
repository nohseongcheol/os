// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package English.Native;

/** Converts standard Java errors at the local API boundary without changing the meaning of standard catch clauses. */
final class convertException {
    private convertException() {}
    public static InputOutputException inputOutput(java.io.IOException error) {
        if (error instanceof InputOutputException) return (InputOutputException)error;
        if (error instanceof java.net.SocketTimeoutException) return new WaitTimeoutException("The network operation timed out.");
        if (error instanceof java.net.UnknownHostException) return new AddressLookupException("Cannot resolve the address. Use a numeric IPv4 address for now.");
        if (error instanceof java.io.FileNotFoundException) return new MissingFileException("Cannot open the file.");
        if (error instanceof java.net.SocketException) return new CommunicationException("Connection operation failed: " + error.getMessage());
        return new InputOutputException("Input/output operation failed: " + error.getMessage());
    }
    public static RuntimeException executeCommand(RuntimeException error) {
        if (error instanceof java.lang.NumberFormatException) return new NumberFormatFailure("Check the number format and range.");
        if (error instanceof java.lang.IllegalArgumentException) return new InvalidArgumentException("Check the argument value and range.");
        if (error instanceof java.lang.ArrayIndexOutOfBoundsException) return new ArrayBoundsException("Array index is out of bounds.");
        if (error instanceof java.lang.StringIndexOutOfBoundsException) return new StringBoundsException("String index is out of bounds.");
        if (error instanceof java.lang.IndexOutOfBoundsException) return new BoundsException("The permitted range was exceeded.");
        if (error instanceof java.lang.NullPointerException) return new NullReferenceException("The reference is null.");
        return new ExecutionException(error.getMessage());
    }
}
