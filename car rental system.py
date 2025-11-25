class CarManager:
    def __init__(self):
        self.inventory = {
            1: {"make": "Toyota", "model": "Corolla", "available": True},
            2: {"make": "Honda", "model": "Civic", "available": True},
            3: {"make": "Ford", "model": "Mustang", "available": False},
            4: {"make": "BMW", "model": "X5", "available": True},
        }
        self.next_car_id = 5

    def add_car(self, make, model):
        self.inventory[self.next_car_id] = {"make": make, "model": model, "available": True}
        print(f"✅ Added Car ID {self.next_car_id}: {make} {model}")
        self.next_car_id += 1

    def display_available_cars(self):
        available_cars = [
            (car_id, data["make"], data["model"])
            for car_id, data in self.inventory.items()
            if data["available"]
        ]

        if not available_cars:
            print("😔 No cars currently available for rent.")
            return

        print("\n--- 🚘 Available Cars ---")
        for car_id, make, model in available_cars:
            print(f"ID: {car_id} | Make: {make} | Model: {model}")
        print("--------------------------")
        
        return available_cars

    def check_availability(self, car_id):
        try:
            car_id = int(car_id)
            if car_id in self.inventory:
                return self.inventory[car_id]["available"]
            return False
        except ValueError:
            return False

    def get_car_info(self, car_id):
        try:
            car_id = int(car_id)
            if car_id in self.inventory:
                return f"{self.inventory[car_id]['make']} {self.inventory[car_id]['model']}"
            return "Unknown Car"
        except ValueError:
            return "Unknown Car"


    def update_availability(self, car_id, is_available):
        try:
            car_id = int(car_id)
            if car_id in self.inventory:
                self.inventory[car_id]["available"] = is_available
                return True
            return False
        except ValueError:
            return False


class RentalManager:
    DAILY_RATE = 50 

    def __init__(self, car_manager):
        self.car_manager = car_manager
        self.active_rentals = {}

    def rent_car(self, customer_name, car_id, rental_days):
        try:
            car_id = int(car_id)
            rental_days = int(rental_days)
        except ValueError:
            print("❌ Error: Car ID and Days must be valid numbers.")
            return False

        if customer_name in self.active_rentals:
            print(f"❌ Error: {customer_name} already has an active rental.")
            return False
            
        if self.car_manager.check_availability(car_id):
            self.car_manager.update_availability(car_id, False)

            self.active_rentals[customer_name] = (car_id, rental_days)

            cost = rental_days * self.DAILY_RATE
            car_info = self.car_manager.get_car_info(car_id)
            print(f"🎉 Success! {customer_name} rented a {car_info} for {rental_days} days.")
            print(f"💰 Total estimated cost: ${cost}")
            return True
        else:
            car_info = self.car_manager.get_car_info(car_id)
            if car_info != "Unknown Car":
                print(f"❌ Error: The {car_info} (ID: {car_id}) is not available.")
            else:
                print(f"❌ Error: Car ID {car_id} not found in inventory.")
            return False

    def return_car(self, customer_name):
        if customer_name not in self.active_rentals:
            print(f"❌ Error: No active rental found for {customer_name}.")
            return False

        car_id, days = self.active_rentals.pop(customer_name)
        
        if self.car_manager.update_availability(car_id, True):
            car_info = self.car_manager.get_car_info(car_id)
            print(f"✅ Success! {car_info} (ID: {car_id}) returned by {customer_name}.")
            print("Car is now available for the next customer.")
            return True
        else:
            print("⚠️ Warning: Car was returned, but an error occurred updating its availability.")
            return False

    def display_rentals(self):
        if not self.active_rentals:
            print("No cars currently out on rent.")
            return

        print("\n--- 📝 Active Rentals ---")
        for customer, (car_id, days) in self.active_rentals.items():
            car_info = self.car_manager.get_car_info(car_id)
            print(f"Customer: {customer:<15} | Car: {car_info:<15} | ID: {car_id} | Days: {days}")
        print("--------------------------")


class UserInterface:
    def __init__(self):
        self.car_manager = CarManager()
        self.rental_manager = RentalManager(self.car_manager)
        self.running = True

    def display_menu(self):
        print("\n" + "="*30)
        print("🚗 **Car Rental Service Menu** 🚗")
        print("="*30)
        print("1. View Available Cars")
        print("2. Rent a Car")
        print("3. Return a Car")
        print("4. View Active Rentals")
        print("5. Add a New Car (Admin)")
        print("6. Exit")
        print("="*30)

    def run(self):
        print("Welcome to the Python Car Rental Service!")
        while self.running:
            self.display_menu()
            choice = input("Enter your choice (1-6): ").strip()
            print()

            if choice == '1':
                self.car_manager.display_available_cars()
            elif choice == '2':
                self._handle_rent_car()
            elif choice == '3':
                self._handle_return_car()
            elif choice == '4':
                self.rental_manager.display_rentals()
            elif choice == '5':
                self._handle_add_car()
            elif choice == '6':
                self.running = False
                print("Thank you for using the Car Rental Service. Goodbye! 👋")
            else:
                print("❌ Invalid choice. Please enter a number between 1 and 6.")
    
    def _handle_rent_car(self):
        print("--- Rent a Car ---")
        customer = input("Enter your name: ").strip()
        car_id = input("Enter the Car ID you wish to rent: ").strip()
        days = input("Enter number of days for rental: ").strip()
        
        if customer and car_id and days.isdigit() and int(days) > 0:
            self.rental_manager.rent_car(customer, car_id, days)
        else:
            print("❌ Invalid input. Please ensure all fields are filled correctly and days is a positive number.")

    def _handle_return_car(self):
        print("--- Return a Car ---")
        customer = input("Enter the name used for the rental: ").strip()
        if customer:
            self.rental_manager.return_car(customer)
        else:
            print("❌ Customer name cannot be empty.")

    def _handle_add_car(self):
        print("--- Add New Car ---")
        make = input("Enter the car's Make (e.g., Tesla): ").strip()
        model = input("Enter the car's Model (e.g., Model 3): ").strip()
        if make and model:
            self.car_manager.add_car(make, model)
        else:
            print("❌ Car Make and Model cannot be empty.")

if __name__ == "__main__":
    app = UserInterface()
    app.run()