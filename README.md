# rfid
RFID reader/writer

## Протокол USB-HID для ридера RFID

На любой запрос:    
Ответ: FB - если не найден RFID модуль


**Чтение UID карты:**    
01    
Ответ: AA {длина UID} {UID} / FA

**Аутентификация блока:**    
02 {номер ключа 00/01} {ключ 6 байт} {номер блока}    
Ответ: AB / FA

**Чтение блока:**    
03 {номер блока}    
Ответ: AC {данные 16 байт} / FA

**Запись блока:**    
04 {номер блока} {данные 16 байт}    
Ответ: AD / FA / EA (запись не разрешена)

**Разрешение записи:**    
AA CC FC E8 1A B0 EE 57

**Очистка переменных:**    
05

# Подключение

PB11 - переключатель    
PB10 - зуммер    

# TODO

* Обработка ошибок
* Окно настроек
* Запись блока
* Форматирование карты
* Сохранение дампа в файл
* Запись дампа на карту
* Сравнение с дампом
* Автоматическое определение карты при прикладывании
