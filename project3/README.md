# Project 3

A django app that implements an online store for a imaginary pizza restaurant. Customers can add items to their shopping cart and checkout with their order. The website admin can alter the menu, see orders come in, and check off completed orders. Uses django ORM database and django''s form models and verification.

## Description of files

### orders 

- <div>admin.py</div>
	- registering models for django admin site

- <div>forms.py</div>
	- Forms for login, registration, pizza and sub toppings. Form options for toppings and Extras draw from the database. Pizza form checks for the correct number of toppings.

- <div>models.py</div> 
	- database objects and __str__ methods. 

- <div>views.py</div>
	- handles login and logout, rendering of forms, rendering of menu based on database adding and deleting items in cart, calculating totals, placing orders, displaying orders to admin, and marking orders complete. 

#### static/orders

- home.js
	- javascript for menu page. Ajax requests for forms, changing shopping cart badge for items added

- checkout.js 
	- ajax for deleting items from cart and placing order. Returns to shopping after deleting all items.

- admin.js 
	- ajax for marking orders complete and fading them out on the page

#### templates/orders

- All the html for the site. Base.html is template for other pages to inherit. Forms rendered with crispy_forms.
 

