## FASTAPI BLOG PROJECT 
```
 uvicorn main:app --reload
```

# Fast API Dependancy injection 
* fast api denpendce on dependancy injection Design pattern

# Fast api dependence on Model View Controll (MVC) Design Pattern 
* this enapls us to seprate logic from businss and make code easy to extend and maintain 

# Fastapi websocket (Realtime Cummnication  )
* fastapi allowing realtime connection throug WebSocket  

# fast api using async for better performance 
* fastapi using aysnc orm sqlachemy database for better performance and handling alot of database requests asysyencronously for better performance, how do we can applay this 
1- using sutiple database driver for asyncronous request handling 
2- using async and await 
3- using Async seesion 
4- for crud ops uing select function querying and sclaer for get and delete for daeleting datapase object this all dependce on project needs 

# integrating celery 
* celery is used for heavy task that takes toolong time to process such as sending Email image processing database pooling 
1- this good for scalabilty 
2- user experience 
3- ``` celery -A celery_worker.celery_app worker --pool=solo --loglevel=info ```

# interating flower 
* flower is monitoring tool for celery tasks with good ui for developers montoring tasks 
1- ```  celery -A celery_worker.celery_app flower --port=5555```



# iintegrating alemic 
* alemebic is database migration tool for fastapi apps and flask ,
1- save diffrent versioon for your database changes this is good for contrllling your database 
2- init alembic ``` alembic init alembic```
3- making migrations ```  alembic -c blog/alembic.ini revision --autogenerate -m "Databse created  "```
4- applay migrations ``` alembic -c blog/alembic.ini upgrade head``` 
