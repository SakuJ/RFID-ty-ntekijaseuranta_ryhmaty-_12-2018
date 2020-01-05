#include <QCoreApplication>
#include <QSerialPort>
#include <QSerialPortInfo>
#include <QDebug>
#include <stdio.h>
#include <iostream>
#include <windows.h>
#include <unistd.h>
#include <sys/stat.h>
#include <time.h>
using namespace std;

//copy paht to DummyDataBase.txt
#define paht "../DummyDataBase.txt"
#define tempPaht "../DummyDataBase_temp.txt"
#define lpaht "../Log.txt"

QSerialPort serial;
FILE * fPointer, *ftemp, *flog;
char rfid[255];
char timeWR[80];
char com[] = "COM3";
const int workers = 5;
int logged[workers];
int getTime = 0;
int oneLog = 0;
int lines = 1;
int numN = 0;
int num = 0;
int er = 0;
QByteArray sender = "0";
QByteArray resiveRfid;
QString id;
char linec;

//open serialport
void serialopen()
{
    //name from ArduinoIDE, ex: COM3 COM7 COM8
    serial.setPortName(com);
    serial.open(QIODevice::ReadWrite);
    serial.setBaudRate(QSerialPort::Baud9600);
    serial.setFlowControl(QSerialPort::NoFlowControl);
    serial.setDataBits(QSerialPort::Data8);
    serial.setParity(QSerialPort::NoParity);
    serial.setStopBits(QSerialPort::OneStop);
}

//Time
void timeWrite(){
    flog = fopen(lpaht, "a");
    time_t rawtime;
    time (&rawtime);

    struct tm * timeIn;
    timeIn = localtime (&rawtime);

    strftime (timeWR,80,"%A %d.%m.%y %H:%M",timeIn);
    printf(timeWR);
    printf("\n");
    fprintf(flog, "%s\n", timeWR);
    fclose(flog);
}

//Logfile
void log(){
    flog = fopen(lpaht, "a");

    if (getTime == 0){
        fprintf(flog, "%s",rfid);
        oneLog++;
        if (oneLog == 4){
            oneLog = 0;
        }
        fclose(flog);
    }
    else{
        timeWrite();
        getTime = 0;
    }
}

//write byte to arduino
void write(){
    //checks if arduino can read data, if not goes to loop untill it can
    while (!serial.isWritable()){
    }
    //executed when arduino is available to read
    serial.write(sender);
    //qDebug() << "\nWrite numeber: " << sender;
    //waits 1 clock cycle
    usleep(96000);

}

//loggin, loggout/no id
void loggio(){

    int changeline = (lines - numN);

    if(strcmp(rfid, "LOGGED IN\n") == 0){

        fPointer = fopen(paht, "r");
        ftemp = fopen(tempPaht, "w");

        for (int i = 0; i < lines; i++){

            fgets(rfid, sizeof(rfid), fPointer);
            if (changeline == i){

                fprintf(ftemp, "LOGGED OUT\n");
            }
            else{
                fprintf(ftemp, rfid);
            }
        }

        fclose(ftemp);
        fclose(fPointer);
        remove(paht);
        rename(tempPaht, paht);

        flog = fopen(lpaht, "a");
        printf("LOGGED OUT...\n");
        fprintf(flog, "LOGGED OUT...\n");
        fclose(flog);

        sender = "2";
        //go to function
        write();
    }
    else if (strcmp(rfid, "LOGGED OUT\n") == 0){

        fPointer = fopen(paht, "r");
        ftemp = fopen(tempPaht, "w");

        for (int i = 0; i < lines; i++){

            fgets(rfid, sizeof(rfid), fPointer);
            if (changeline == i){

                fprintf(ftemp, "LOGGED IN\n");
            }
            else{
                fprintf(ftemp, rfid);
            }
        }

        fclose(ftemp);
        fclose(fPointer);
        remove(paht);
        rename(tempPaht, paht);

        flog = fopen(lpaht, "a");
        printf("LOGGED IN...\n");
        fprintf(flog, "LOGGED IN...\n");
        fclose(flog);

        sender = "1";
        //go to function
        write();
    }
    else{

        printf("ERROR No ID found\nERROR: ID001C");
        sender = "3";
        //go to function
        write();
    }
}

//null values
void nullvalues(){
    //reset values
    num = 0;
    numN = lines;
    sender = "0";
    QByteArray resiveRfid = "";
    fseek(fPointer, 0, SEEK_SET);
}

//error codes
void errors(){
    //ERROR BG
    //SX001P
    if(!serial.isOpen()){

        printf("Serial Port (COM*): ");
        char ser[3];
        scanf("%s", ser);
        strcpy(com, ser);
        system ("cls");
        serialopen();
        if(!serial.isOpen())
        {

            printf("Serial Port connection ERROR!!!\nCheck the connection!\nERROR: SX001P\n");
            er = 1;
        }
    }
    //LX001G
    flog = fopen(lpaht, "r");
    if(fPointer == NULL){
        flog = fopen(lpaht, "w");
        printf("created Log File");
    }

    fclose(flog);

    if(fPointer == NULL){
        printf("ERROR Openig the database!!!\nERROR: DX001B");
        er = 1;
    }

    while (EOF != (linec =getc(fPointer))){
        if(linec == '\n'){
            lines++;
        }
    }
    lines -= 1;
    numN = lines;

    //DX002B
    if(lines <= 1){
        printf("ERROR No data in Database\nERROR: DX002B");
        er = 1;
    }
    //DX003B
    else if(lines <= 3 || (lines % 4) != 0){
        printf("ERROR No valid data in Database\nERROR: DX003B");
        er = 1;
    }
    fclose(fPointer);
    //ERROR END
}

int main(int argc, char *argv[])
{
    QCoreApplication a(argc, argv);
    fPointer = fopen(paht, "r");

    serialopen();
    //check any errors
    errors();
    if (er == 1){
        goto END;
    }
    //infinete loop
    while (1){

        //start point
        newread:
        //null values
        nullvalues();
        sleep(3);

        //check comm for any bytes
        while(!serial.canReadLine())
        {
            serial.waitForReadyRead(-1);
        }
        //wait untill 10 bytes
        while (serial.waitForReadyRead(10))
        {
            //write serialdata to Qbytearray
            fPointer = fopen(paht, "r");
            resiveRfid = serial.readAll();
            system ("cls");

            //loops every line on database
            for(int i = 0; i < lines; i++)
            {
                //write 1 line to charArray, and writes cA to QString
                fgets(rfid, sizeof(rfid), fPointer);
                id = rfid;
                //parses characters after '/n' character
                id.truncate(id.lastIndexOf(QChar('\n')));

                //executed every 4 lines
                if((i % 4) == 0)
                {
                    //checks if Qbytearray contais QString
                    if (resiveRfid.contains(id.toUtf8()))
                    {
                        //prints workers info
                        for (int i = 0; i < 4; i++)
                        {
                            if(i <= 0){
                                //go to function
                                getTime = 1;
                                log();

                            }
                            if (i >= 3){
                                fclose(fPointer);
                                loggio();
                                //printf("%s",rfid);
                                goto newread;
                            }
                            else{
                                printf("%s",rfid);
                                log();
                            }
                            numN--;
                            fgets(rfid, sizeof(rfid), fPointer);
                        }
                    }
                    //ID001C
                    else
                    {
                        //numN--;
                        //if workersID is not in the line
                        num++;
                        // if ID does not match any line
                        if(num >= workers)
                        {
                            getTime = 1;
                            fclose(fPointer);
                            //go to function
                            loggio();
                            //printf(resiveRfid);
                            //back to start
                            goto newread;
                        }
                    }
                }
            numN--;
            }
        }
    }
    END:
    return a.exec();
}
