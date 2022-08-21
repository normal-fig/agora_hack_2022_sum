# agora_hack_2022_sum

## Запуск приложения

### ```docker-compose up --build```

### Запрос

POST localhost:8100/match_products

Тело запроса - JSON
```
[
  {
    "id": "some_id_1",
    "name": "Название товара1",
    "props": [...]
  },
  {
    "id": "some_id_2",
    "name": "Название товара2",
    "props": [...]
  },
  {
    "id": "some_id_3",
    "name": "Название товара3",
    "props": [...]
  }
]
```


Тело ответа
```
[
  {
    "id": "some_id_1",
    "reference_id": "reference_4_id"
  },
  {
    "id": "some_id_2",
    "reference_id": "reference_8_id"
  },
  {
    "id": "some_id_3",
    "reference_id": null
  }
]
```
<br>

### Добавление новых эталонов

POST localhost:8100/match_products

Тело запроса - JSON
```
[
  {
    "id": "some_id_1",
    "name": "Название товара1",
    "props": [...]
  },
  {
    "id": "some_id_2",
    "name": "Название товара2",
    "props": [...]
  },
  {
    "id": "some_id_3",
    "name": "Название товара3",
    "props": [...]
  }
]
```
<br>
