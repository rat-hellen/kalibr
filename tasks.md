## common tasks
1. Убрать из кода проекта все, что не используется на текущий момент. Весь тестовый и експериментальный код перенести в папку test.
2. Приемом, обработкой и хранением меток должен заниматься объект Zmq_Sub. Соответственно, нужно перенести в этот класс lastSubReadLabel_lfm. сanWriteToDB должен быть методом этого класса, который анализирует уже разобранные метки. Объект этого класса должен быть параметром для Reader_Async а не наоборот.
## driver_module_lfm.py
... Ok
## drv_reader_async_lfm.py
1. Сделать lastReadLine параметром функции getFrequency. Убрать его из свойств объекта. lastReadLine не используется нигде кроме этой функции. 
2. Сделать db_client свойством объекта. Не надо создавать соединение на каждую запись - это дорого. Соединение с базой устанавливать после соединения с компортом в процедуре чтения порта.
3. Использовать dataclass для инициализации свойств объекта Reader_Async. Избежать трехкратного повторения десятка параметров в коде.

## drv_db_client.py
1. выделить коннект к базе отдельным методом

## drv_zmq_sub_lfm.py
1. использовать recv_json для приема меток