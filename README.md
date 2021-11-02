![](assets/logo.png)

# Disecto : Backend Dev Assignment

- [Setup](#setup)
- [Urls](#urls)
- [Models](#models)
- [Assumptions](#assumptions)

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
http://127.0.0.1:8000/api/customer-purchase/<customer-id>
```


## models

- Customer (Name, Phone No., Address)
- Item (Description, Price)
- Invoice (Customer, Timestamp)
- InvoiceItems (Invoice, Item, Quantity)


## assumptions

- `PUT` method created request for new items and/or update requests of previous items. Items not included in a PUT request, if they exist in Invoice earlier, do not get deleted. 

