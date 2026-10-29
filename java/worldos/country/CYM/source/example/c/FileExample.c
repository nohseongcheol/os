#include "ExampleABI.h"
int main(void) {
    const char data[]="C file: English 😀\n";
    int file=openFile("c.txt",ReadWrite|CreateIfMissing|TruncateContents,0600);
    if(file<0)return 1;
    if(writeFileData(file,data,sizeof(data)-1)!=sizeof(data)-1)return 2;
    if(seekFile(file,0,FromBeginning)!=0)return 3;
    char readTextValue[128]={0};int lengthValue=readFileData(file,readTextValue,sizeof(readTextValue)-1);
    closeFile(file);
    if(lengthValue!=sizeof(data)-1)return 4;
    for(int number=0;number<lengthValue;number++)if(data[number]!=readTextValue[number])return 5;
    return Output(readTextValue);
}
