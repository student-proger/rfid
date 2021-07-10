/**************************************************************************/
/*!
 * For Arduino STM32!!!
 * Only for 48 MHz!
 * 
    This example attempts to dump the contents of a Mifare Classic 1K card

    Note that you need the baud rate to be 115200 because we need to print
    out the data and read from the card at the same time!

    To enable debug message, define DEBUG in PN532/PN532_debug.h
*/
/**************************************************************************/

#define DEVICE_VID 0x1EAF
#define DEVICE_PID 0x0030
#define DEVICE_MANUFACTURER "R0WBH"
#define DEVICE_PRODUCT "RFIDCARD_RW"
#define DEVICE_SERIAL "00001"

#include <SPI.h>
#include <PN532_SPI.h>
#include "PN532.h"

#include <USBComposite.h>

//Размеры буферов приёма/передачи USB HID
#define TXSIZE 17
#define RXSIZE 18

PN532_SPI pn532spi(SPI, PA4);
PN532 nfc(pn532spi);

USBHID HID;
HIDRaw<TXSIZE,RXSIZE> raw(HID);
uint8_t rxbuf[RXSIZE];
uint8_t txbuf[TXSIZE];

uint8_t success;                          // Flag to check if there was an error with the PN532
uint8_t uid[] = { 0, 0, 0, 0, 0, 0, 0 };  // Buffer to store the returned UID
uint8_t uidLength;                        // Length of the UID (4 or 7 bytes depending on ISO14443A card type)
uint8_t currentblock;                     // Counter to keep track of which block we're on
bool authenticated = false;               // Flag to indicate if the sector is authenticated
uint8_t data[16];                         // Array to store block data during reads

bool recEnabled = false;  //Запись разрешена

// Keyb on NDEF and Mifare Classic should be the same
uint8_t keyuniversal[6] = { 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF };

const uint8_t reportDescription[] = {
   HID_RAW_REPORT_DESCRIPTOR(TXSIZE,RXSIZE)
};


void setup(void)
{
  USBComposite.setVendorId(DEVICE_VID);
  USBComposite.setProductId(DEVICE_PID);
  USBComposite.setManufacturerString(DEVICE_MANUFACTURER);
  USBComposite.setProductString(DEVICE_PRODUCT);
  USBComposite.setSerialString(DEVICE_SERIAL);

  HID.begin(reportDescription, sizeof(reportDescription));  
  raw.begin();

  // has to be fast to dump the entire memory contents!
  delay(3000);

  nfc.begin();

  uint32_t versiondata = nfc.getFirmwareVersion();
  if (! versiondata) {
    //Serial.print("Didn't find PN53x board");
    while (1)
    {
      if (raw.getOutput(rxbuf))
      {
        for (int i=0;i<TXSIZE;i++) txbuf[i]=0x00;
        txbuf[0] = 0xFB;
        raw.send(txbuf,TXSIZE);
      }
    }
  }
  // Got ok data, print it out!
  //Serial.print("Found chip PN5"); Serial.println((versiondata>>24) & 0xFF, HEX);
  //Serial.print("Firmware ver. "); Serial.print((versiondata>>16) & 0xFF, DEC);
  //Serial.print('.'); Serial.println((versiondata>>8) & 0xFF, DEC);

  // configure board to read RFID tags
  nfc.SAMConfig();

  //Serial.println("Waiting for an ISO14443A Card ...");
  pinMode(PC13, OUTPUT);
}


void loop(void) {
  


  if (raw.getOutput(rxbuf))
  {
    for (int i=0;i<TXSIZE;i++) txbuf[i]=0x00;

    if (rxbuf[0] == 0x01) //Чтение UID карты
    {
      success = nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A, uid, &uidLength);
      if (success)
      {
        txbuf[0] = 0xAA;
        txbuf[1] = uidLength;
        for (uint8_t i = 0; i < uidLength; i++)
        {
          txbuf[i+2] = uid[i];
        }
      }
      else
      {
        txbuf[0] = 0xFA;
      }
    }

    if (rxbuf[0] == 0x02) //Аутентификация блока
    {
      currentblock = rxbuf[8];
      keyuniversal[0] = rxbuf[2];
      keyuniversal[1] = rxbuf[3];
      keyuniversal[2] = rxbuf[4];
      keyuniversal[3] = rxbuf[5];
      keyuniversal[4] = rxbuf[6];
      keyuniversal[5] = rxbuf[7];
      if (uidLength == 4)
      {
        success = nfc.mifareclassic_AuthenticateBlock (uid, uidLength, currentblock, rxbuf[1], keyuniversal);
      }
      if (success)
      {
        txbuf[0] = 0xAB;
      }
      else
      {
        txbuf[0] = 0xFA;
      }

    }

    if (rxbuf[0] == 0x03) //Чтение блока
    {
      currentblock = rxbuf[1];
      success = nfc.mifareclassic_ReadDataBlock(currentblock, data);

      if (success)
      {
        txbuf[0] = 0xAC;
        for (int i=0; i<16; i++)
        {
          txbuf[i+1] = data[i];
        }
      }
      else
      {
        txbuf[0] = 0xFA;
      }
    }

    if (rxbuf[0] == 0xAA) //Разрешение записи
    {
      //AA CC FC E8 1A B0 EE 57
      uint8_t recEnableTemplate[8] = {0xAA, 0xCC, 0xFC, 0xE8, 0x1A, 0xB0, 0xEE, 0x57};
      bool ok = true;
      for (int i=0; i<8; i++)
      {
        if (rxbuf[i] != recEnableTemplate[i])
        {
          ok = false;
        }
      }
      if (ok)
      {
        recEnabled = true;
      }

    }

    if (rxbuf[0] == 0x04) //Запись блока
    {
      if (recEnabled)
      {
        currentblock = rxbuf[1];
        for (int i=0; i<8; i++)
        {
          data[i] = rxbuf[i+1];
        }

        success = nfc.mifareclassic_WriteDataBlock(currentblock, data);

        if (success)
        {
          txbuf[0] = 0xAD;
        }
        else
        {
          txbuf[0] = 0xFA;
        }
      }
      else
      {
        txbuf[0] = 0xEA;
      }
    }

    raw.send(txbuf,TXSIZE);
  }


  /*
  // Wait for an ISO14443A type cards (Mifare, etc.).  When one is found
  // 'uid' will be populated with the UID, and uidLength will indicate
  // if the uid is 4 bytes (Mifare Classic) or 7 bytes (Mifare Ultralight)
  success = nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A, uid, &uidLength);

  if (success) {
    // Display some basic information about the card
    //Serial.println("Found an ISO14443A card");
    //Serial.print("  UID Length: ");Serial.print(uidLength, DEC);Serial.println(" bytes");
    //Serial.print("  UID Value: ");
    for (uint8_t i = 0; i < uidLength; i++) {
      //Serial.print(uid[i], HEX);
      //Serial.print(' ');
    }
    //Serial.println("");

    if (uidLength == 4)
    {
      // We probably have a Mifare Classic card ...
      //Serial.println("Seems to be a Mifare Classic card (4 byte UID)");

      // Now we try to go through all 16 sectors (each having 4 blocks)
      // authenticating each sector, and then dumping the blocks
      for (currentblock = 0; currentblock < 64; currentblock++)
      {
        // Check if this is a new block so that we can reauthenticate
        if (nfc.mifareclassic_IsFirstBlock(currentblock)) authenticated = false;

        // If the sector hasn't been authenticated, do so first
        if (!authenticated)
        {
          // Starting of a new sector ... try to to authenticate
          Serial.print("------------------------Sector ");Serial.print(currentblock/4, DEC);Serial.println("-------------------------");
          if (currentblock == 0)
          {
              // This will be 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF for Mifare Classic (non-NDEF!)
              // or 0xA0 0xA1 0xA2 0xA3 0xA4 0xA5 for NDEF formatted cards using key a,
              // but keyb should be the same for both (0xFF 0xFF 0xFF 0xFF 0xFF 0xFF)
              success = nfc.mifareclassic_AuthenticateBlock (uid, uidLength, currentblock, 1, keyuniversal);
          }
          else
          {
              // This will be 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF for Mifare Classic (non-NDEF!)
              // or 0xD3 0xF7 0xD3 0xF7 0xD3 0xF7 for NDEF formatted cards using key a,
              // but keyb should be the same for both (0xFF 0xFF 0xFF 0xFF 0xFF 0xFF)
              success = nfc.mifareclassic_AuthenticateBlock (uid, uidLength, currentblock, 1, keyuniversal);
          }
          if (success)
          {
            authenticated = true;
          }
          else
          {
            //Serial.println("Authentication error");
          }
        }
        // If we're still not authenticated just skip the block
        if (!authenticated)
        {
          //Serial.print("Block ");Serial.print(currentblock, DEC);Serial.println(" unable to authenticate");
        }
        else
        {
          // Authenticated ... we should be able to read the block now
          // Dump the data into the 'data' array
          success = nfc.mifareclassic_ReadDataBlock(currentblock, data);
          if (success)
          {
            // Read successful
            //Serial.print("Block ");Serial.print(currentblock, DEC);
            if (currentblock < 10)
            {
              //Serial.print("  ");
            }
            else
            {
              //Serial.print(" ");
            }
            // Dump the raw data
            nfc.PrintHexChar(data, 16);
          }
          else
          {
            // Oops ... something happened
            //Serial.print("Block ");Serial.print(currentblock, DEC);
            //Serial.println(" unable to read this block");
          }
        }
      }
    }
    else
    {
      //Serial.println("Ooops ... this doesn't seem to be a Mifare Classic card!");
    }
  
  // Wait a bit before trying again
  //Serial.println("\n\nSend a character to run the mem dumper again!");
  delay(3000);
  //Serial.flush();
  //while (!Serial.available());
  //while (Serial.available()) {
  //Serial.read();
  //}
  }
  //Serial.flush();*/
}
