from octos.handler.command import Command
from faker import Faker

fake = Faker()

class SeedDB(Command):
    """Command to seed the database with fake data."""

    def handle(self):
        # Import models inside the handle method to ensure apps are ready
        from app.user.models import User
        from app.products.models import Product
        from app.sales.models import SalesOrder
        from app.purchases.models import PurchaseOrder

        self.seed_users(User)
        self.seed_products(Product)
        self.seed_sales(SalesOrder, User, Product)
        self.seed_purchases(PurchaseOrder, Product, User)

    def seed_users(self, User):
        """Seed user data"""
        for _ in range(10):  # Create 10 fake users
            user = User.objects.create(
                name=fake.name(),
                email=fake.email(),
                role=User.CUSTOMER  # or any other role
            )
            user.set_password(fake.password())  # Ensure password is hashed
            user.save()
        print("Users seeded successfully.")

    def seed_products(self, Product):
        """Seed product data"""
        for _ in range(20):  # Create 20 fake products
            Product.objects.create(
                sku=fake.unique.ean(length=8),
                name=fake.word(),
                description=fake.text(),
                price=fake.random_number(digits=2),
                stock=fake.random_number(digits=2, fix_len=True)  # Ensure stock is positive
            )
        print("Products seeded successfully.")

    def seed_sales(self, SalesOrder, User, Product):
        """Seed sales data"""
        users = User.objects.filter(role=User.CUSTOMER)
        products = Product.objects.all()

        if not users.exists():
            print("No users with customer role found.")
            return

        if not products.exists():
            print("No products found.")
            return

        for _ in range(15):  # Create 15 fake sales orders
            product = fake.random_element(products)
            quantity = fake.random_number(digits=1)

            # Ensure quantity is at least 1
            quantity = max(quantity, 1)

            if product.stock >= quantity:  # Ensure there's enough stock
                SalesOrder.objects.create(
                    customer=fake.random_element(users),
                    product=product,
                    quantity=quantity,
                    price=product.price,  # Use product price
                    created_by=fake.random_element(users),
                )
        print("Sales orders seeded successfully.")

    def seed_purchases(self, PurchaseOrder, Product, User):
        """Seed purchase data"""
        products = Product.objects.all()

        if not products.exists():
            print("No products available to create purchase orders.")
            return

        for _ in range(10):  # Create 10 fake purchase orders
            PurchaseOrder.objects.create(
                product=fake.random_element(products),
                quantity=fake.random_number(digits=2, fix_len=False),
                supplier_name=fake.company(),
                created_by=fake.random_element(User.objects.all()),
            )
        print("Purchase orders seeded successfully.")
