"""Terminal functions module."""
from datetime import datetime

from ipet.ext.auth.models import User
from ipet.ext.customer.models import AssocProductCustomer, Customer
from ipet.ext.db import db
from ipet.ext.product.models import Product


def create_db():
    """Create the table structure.

    Returns:
        str: Error or success message.
    """
    try:
        db.create_all()
        return "Banco criado com sucesso!"
    except Exception as exp:
        return f"Erro: {exp.args[0]}"


def populate_db():
    """Insert data into database.

    Returns:
        str: Error or success message.
    """
    user = User(username="admin", password="admin")
    customer1 = Customer(cpf=38164206572, full_name="Kelmer Souza Passos")
    customer2 = Customer(cpf=48154206554, full_name="Gabriele Pinheiro Passos")
    customer3 = Customer(cpf=48154202154, full_name="Randall Heller")
    customer4 = Customer(cpf=48155465259, full_name="Brooke Champlin")
    customer5 = Customer(cpf=48154289518, full_name="Andres Franecki")
    customer6 = Customer(cpf=48154106556, full_name="Dr. Mable O'Kon")
    product1=Product(
            full_name="Biscoito",
            full_description="Biscoito de Chocolate",
            brand="Vitarela",
            price=14.25,
        )
    product2=Product(
        full_name="Macarrão",
        full_description="Macarrão parafuso",
        brand="Vitarela",
        price=14.25,)

    product3=Product(
        full_name="Macarrão integral",
        full_description="Macarrão parafuso",
        brand="Vitarela",
        price=14.25,)

    product4=Product(
        full_name="Macarrão Miojo",
        full_description="Macarrão parafuso",
        brand="Vitarela",
        price=14.25,)
    
    # assoc_product1 = AssocProductCustomer(
    #     product=Product(
    #         full_name="Biscoito",
    #         full_description="Biscoito de Chocolate",
    #         brand="Vitarela",
    #         price=14.25,
    #     ),
    #     created_at=datetime.now(),
    # )
    # assoc_product2 = AssocProductCustomer(
    #     product=Product(
    #         full_name="Macarrão",
    #         full_description="Macarrão parafuso",
    #         brand="Vitarela",
    #         price=14.25,
    #     ),
    #     created_at=datetime.now(),
    # )
    # customer1.products.append(assoc_product1)
    # customer1.products.append(assoc_product2)
    db.session.add(user)
    db.session.add(customer1)
    db.session.add(customer2)
    db.session.add(customer3)
    db.session.add(customer4)
    db.session.add(customer5)
    db.session.add(customer6)
    db.session.add(product1)
    db.session.add(product2)
    db.session.add(product3)
    db.session.add(product4)
    try:
        db.session.commit()
        return "Registros criados com sucesso!"
    except Exception as exp:
        return f"Erro: {exp.args[0]}"
