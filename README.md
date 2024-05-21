# easyText

## Запуск
```bash
git clone https://github.com/MonkeyProd/easyText.git
cd easyText
docker system prune -fa --volumes # удалить прошлые билды
docker compose up --build --force-recreate # создать новый билд
Ctrl-C # после запуска закрыть
docker compose up # запустить заново
# сделать один запрос чтобы установились адблоки
```

## Схема БД
![](readme_assets/database-entity-relation-diagram.jpg)
