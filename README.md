![](assets/logo.png)

# Disecto : Backend Dev Assignment

- [Setup](#setup)
- [Urls](#urls)
- [Models](#models)
- [Assumptions](#assumptions)
- [Task 2](#task-2)

## setup

- clone the repository

```
git clone https://github.com/gurbaaz27/disecto-backdev-task.git
cd disecto-backdev-task
```

- create virtual environment using `venv` or `conda`

```
conda create -n venv python -y
conda activate venv
```

- install the dependencies

```
pip install -r requirement.txt
```

- setup your models and database

```
python manage.py makemigrations
python manage.py migrate
```

- to explore admin dashboard, create a superuser

```
python manage.py createsuperuser
```

- fire up your server 

```
python manage.py runserver
```

## urls

- GET: get the list of available items with details such as (name, price, description).
```
http://127.0.0.1:8000/api/items
```

- POST: to send the list of items to buy with corresponding quantities.
- PUT: to update the list of items in the purchase list.
- GET: get the invoice for the purchase in pdf format as per the above format but with all the necessary details filled dynamically

```
http://127.0.0.1:8000/api/customer-purchase/<int:customer-id>
```

- apart from this, we have some utility apis

```
# view/add details of customers with get/post
http://127.0.0.1:8000/api/customers/ 
# add details of new items with post
http://127.0.0.1:8000/api/items/
```


## models

- Customer (Name, Phone No., Address)
- Item (Description, Price)
- Invoice (Customer, Timestamp)
- InvoiceItems (Invoice, Item, Quantity)


## assumptions

- `PUT` method either creates request for new items and/or update requests of previous items. Items not included in a `PUT` request, if they exist in invoice earlier, do not get deleted. 
- if `POST` method is called for an item that is already in invoice, it would result in error. the task of updation is solely via `PUT` method 
- if there is error for even one item in `POST` or `PUT` (i.e. due to insufficient stocks, item id does not exist etc), entire request fails
- each invoice is one-to-one mapped to customer. practically there could be many invoices per customer and it should be many-to-one mapped. but keeping things simple here (as then one would also need to provide some sort of invoice `id` apart from customer `id` while testing) 


## task 2

```
python manage.py generate_stock_list --help

usage: manage.py generate_stock_list [-h] [--version] [-v {0,1,2,3}] [--settings SETTINGS] [--pythonpath PYTHONPATH] [--traceback] [--no-color]
                                     [--force-color] [--skip-checks]

Auto generate a list of products/items with low stock/expiry from the inventory database.
```

below command can be scheduled via `cron` to run 12 AM daily on the server side

```
python manage.py generate_stock_list
```
