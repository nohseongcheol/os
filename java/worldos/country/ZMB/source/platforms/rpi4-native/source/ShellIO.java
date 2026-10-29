// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Pipes execute sequentially in 16 KiB units. This does not emulate processes or concurrent pipelines. */
public final class ShellIO {
    static int[] inputData = new int[16384], outputData = new int[16384];
    static int inputLength, inputPosition, outputLength, inputFile = -1, outputFile = -1;
    static boolean pipeInput, pipeOutput;
    static int failureValue;
    static boolean allowInteractive = true;
    public static int isInteractive() { return allowInteractive && inputFile < 3 && outputFile < 3 && !pipeInput && !pipeOutput ? 1 : 0; }
    public static int Output(int channelValue, int value) {
        if (channelValue != 1) return 0;
        if (outputFile >= 3) { int processedValue = MemoryFiles.write(outputFile, value); if (processedValue < 0) failureValue = processedValue; return 1; }
        if (!pipeOutput) return 0;
        if (outputLength == outputData.length) failureValue = -28;
        else outputData[outputLength++] = value;
        return 1;
    }
    public static int inputValue() {
        if (inputFile >= 3) { int processedValue = MemoryFiles.read(inputFile); return processedValue == 256 ? -2 : processedValue; }
        if (pipeInput) return inputPosition < inputLength ? inputData[inputPosition++] : -2;
        return -3; // Forward to UART.
    }
    static void run(boolean leadingPipe, boolean trailingPipe) {
        pipeInput = leadingPipe; pipeOutput = trailingPipe;
        inputPosition = 0; outputLength = 0; inputFile = -1; outputFile = -1; failureValue = 0;
    }
    static void ending() {
        Board.switchIo(0);
        if (inputFile >= 3) MemoryFiles.close(inputFile);
        if (outputFile >= 3) MemoryFiles.close(outputFile);
        if (pipeOutput) { inputLength = outputLength; for (int loopIndex = 0; loopIndex < outputLength; loopIndex++) inputData[loopIndex] = outputData[loopIndex]; }
        inputFile = -1; outputFile = -1; pipeInput = false; pipeOutput = false;
    }
}
