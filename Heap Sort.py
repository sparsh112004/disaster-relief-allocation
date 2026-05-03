import math
import matplotlib.pyplot as plt 
import hashlib  # For password hashing
from datetime import datetime  # For activity logging

# Location Mapping
location_mapping = {
    "New Delhi, Delhi": (28.6139, 77.2090),
    "Mumbai, Maharashtra": (19.0760, 72.8777),
    "Kolkata, West Bengal": (22.5726, 88.3639),
    "Chennai, Tamil Nadu": (13.0827, 80.2707),
    "Bangalore, Karnataka": (12.9716, 77.5946),
    "Hyderabad, Telangana": (17.3850, 78.4867),
    "Ahmedabad, Gujarat": (23.0225, 72.5714),
    "Pune, Maharashtra": (18.5204, 73.8567),
    "Jaipur, Rajasthan": (26.9124, 75.7873),
    "Lucknow, Uttar Pradesh": (26.8467, 80.9462),
}

# Haversine formula for distance calculation
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth's radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)  # Round to 2 decimal places

class Admin:
    def __init__(self, admin_id, username, password_hash, name, contact, role="admin"):
        self.id = admin_id
        self.username = username
        self.password_hash = password_hash
        self.name = name
        self.contact = contact
        self.role = role  # Can be "super_admin", "admin", or "coordinator"
        self.last_login = None
        self.created_at = datetime.now()
        self.is_active = True

class AdminManager:
    def __init__(self):
        self.admins = []
        self.last_id_num = 0
        self.activity_log = []
        self.load_default_admin()
        
    def load_default_admin(self):
        """Load default admin account"""
        default_password = "admin123"  # Default password
        password_hash = hashlib.sha256(default_password.encode()).hexdigest()
        self.admins.append(Admin("ADM001", "admin", password_hash, "System Administrator", "9999999999", "super_admin"))
        self.last_id_num = 1
    
    def log_activity(self, admin_id, action, details):
        """Log admin activity"""
        timestamp = datetime.now()
        log_entry = {
            "timestamp": timestamp,
            "admin_id": admin_id,
            "action": action,
            "details": details
        }
        self.activity_log.append(log_entry)
    
    def generate_next_id(self):
        """Generate the next admin ID"""
        self.last_id_num += 1
        return f"ADM{self.last_id_num:03d}"
    
    def hash_password(self, password):
        """Hash the password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def add_admin(self, username, password, name, contact, role="admin"):
        """Add a new admin to the system"""
        # Check if username already exists
        if any(admin.username == username for admin in self.admins):
            return None
            
        # Generate new admin ID
        new_id = self.generate_next_id()
        
        # Hash the password
        password_hash = self.hash_password(password)
        
        # Create new admin
        new_admin = Admin(new_id, username, password_hash, name, contact, role)
        self.admins.append(new_admin)
        
        # Log the activity
        self.log_activity(new_id, "account_created", f"New admin account created: {username}")
        
        return new_admin
    
    def authenticate_admin(self, username, password):
        """Authenticate admin using username and password"""
        password_hash = self.hash_password(password)
        for admin in self.admins:
            if admin.username == username and admin.password_hash == password_hash and admin.is_active:
                admin.last_login = datetime.now()
                self.log_activity(admin.id, "login", "Successful login")
                return admin
        return None
    
    def get_admin_by_id(self, admin_id):
        """Get admin by ID"""
        for admin in self.admins:
            if admin.id == admin_id:
                return admin
        return None
    
    def get_admin_by_username(self, username):
        """Get admin by username"""
        for admin in self.admins:
            if admin.username == username:
                return admin
        return None
    
    def delete_admin(self, admin_id):
        """Delete an admin by ID"""
        # Don't allow deletion of the default admin
        if admin_id == "ADM001":
            return False
            
        admin = self.get_admin_by_id(admin_id)
        if admin:
            self.admins.remove(admin)
            self.log_activity(admin_id, "account_deleted", f"Admin account deleted: {admin.username}")
            return True
        return False
    
    def change_password(self, admin_id, old_password, new_password):
        """Change admin password"""
        admin = self.get_admin_by_id(admin_id)
        if not admin:
            return False
            
        # Verify old password
        old_hash = self.hash_password(old_password)
        if admin.password_hash != old_hash:
            return False
            
        # Update password
        admin.password_hash = self.hash_password(new_password)
        self.log_activity(admin_id, "password_changed", "Password updated successfully")
        return True
    
    def update_admin_info(self, admin_id, name=None, contact=None, role=None):
        """Update admin information"""
        admin = self.get_admin_by_id(admin_id)
        if not admin:
            return False
            
        changes = []
        if name and name != admin.name:
            admin.name = name
            changes.append("name")
        if contact and contact != admin.contact:
            admin.contact = contact
            changes.append("contact")
        if role and role != admin.role:
            admin.role = role
            changes.append("role")
            
        if changes:
            self.log_activity(admin_id, "info_updated", f"Updated: {', '.join(changes)}")
            return True
        return False
    
    def display_admins(self):
        """Display all registered admins"""
        print("\n=== 👨‍💼 Registered Administrators ===")
        for admin in self.admins:
            print(f"ID: {admin.id}")
            print(f"Username: {admin.username}")
            print(f"Name: {admin.name}")
            print(f"Contact: {admin.contact}")
            print(f"Role: {admin.role}")
            print(f"Status: {'Active' if admin.is_active else 'Inactive'}")
            if admin.last_login:
                print(f"Last Login: {admin.last_login.strftime('%Y-%m-%d %H:%M:%S')}")
            print("-" * 30)
        print("\n===================================")
    
    def display_activity_log(self, admin_id=None):
        """Display activity log for an admin or all admins"""
        print("\n=== 📋 Activity Log ===")
        filtered_log = self.activity_log
        if admin_id:
            filtered_log = [log for log in self.activity_log if log["admin_id"] == admin_id]
            
        if not filtered_log:
            print("No activity logs found.")
        else:
            for log in filtered_log:
                print(f"\nTimestamp: {log['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"Admin ID: {log['admin_id']}")
                print(f"Action: {log['action']}")
                print(f"Details: {log['details']}")
                print("-" * 30)
        print("\n===================================")

class Requester:
    def __init__(self, requester_id, name, contact):
        self.id = requester_id
        self.name = name
        self.contact = contact

class RequesterManager:
    def __init__(self):
        self.requesters = []
        self.last_id_num = 0  # Track the last ID number
        self.load_requesters()
        self.sort_requesters_by_id()  # Sort requesters by ID for binary search
        
    def load_requesters(self):
        """Pre-loads requesters into the system"""
        requester_data = [
            ("REQ001", "Amit Kumar", "9876543210"),
            ("REQ002", "Priya Sharma", "8765432109"),
            ("REQ003", "Rahul Singh", "7654321098"),
            ("REQ004", "Deepika Patel", "6543210987"),
            ("REQ005", "Vikram Malhotra", "5432109876"),
        ]
        for r_id, name, contact in requester_data:
            self.requesters.append(Requester(r_id, name, contact))
            
        # Set the last_id_num based on existing IDs
        self.update_last_id_num()
    
    def sort_requesters_by_id(self):
        """Sort requesters by ID to enable binary search"""
        self.requesters.sort(key=lambda x: x.id)
    
    def update_last_id_num(self):
        """Update the last_id_num based on existing requesters"""
        max_num = 0
        for requester in self.requesters:
            # Extract numeric part from ID
            if requester.id.startswith("REQ"):
                try:
                    id_num = int(requester.id[3:])
                    max_num = max(max_num, id_num)
                except ValueError:
                    pass
        self.last_id_num = max_num
    
    def generate_next_id(self):
        """Generate the next requester ID"""
        self.last_id_num += 1
        return f"REQ{self.last_id_num:03d}"  # Format: REQ001, REQ002, etc.
    
    def binary_search_requester(self, requester_id):
        """Find a requester by ID using binary search"""
        left, right = 0, len(self.requesters) - 1
        
        while left <= right:
            mid = (left + right) // 2
            if self.requesters[mid].id == requester_id:
                return self.requesters[mid]
            elif self.requesters[mid].id < requester_id:
                left = mid + 1
            else:
                right = mid - 1
                
        return None  # Requester not found
    
    def is_valid_requester(self, requester_id, name):
        """Check if requester ID and name match using binary search"""
        requester = self.binary_search_requester(requester_id)
        if requester and requester.name == name:
            return True
        return False
    
    def get_requester_by_id(self, requester_id):
        """Get a requester by ID using binary search"""
        return self.binary_search_requester(requester_id)
    
    def add_requester(self, name, contact):
        """Add a new requester to the system with auto-generated ID"""
        # Generate new requester ID
        new_id = self.generate_next_id()
        
        # Add new requester
        new_requester = Requester(new_id, name, contact)
        self.requesters.append(new_requester)
        # Re-sort the list to maintain binary search functionality
        self.sort_requesters_by_id()
        return new_requester

class Warehouse:
    def __init__(self, warehouse_id, city_name, inventory):
        self.id = warehouse_id
        self.city = city_name
        self.lat, self.lon = location_mapping[city_name]
        self.inventory = inventory  # {resource: quantity}

class WarehouseManager:
    def __init__(self):
        self.warehouses = []
        self.comparisons = 0  # Add counter for comparisons
        self.swaps = 0       # Add counter for swaps
        self.load_warehouses()
        self.sort_warehouses_by_id()

    def load_warehouses(self):
        """Pre-loads warehouses into the system"""
        warehouse_data = {
            "WH1": ("New Delhi, Delhi", {"food": 120, "water": 180, "medicine": 70, "doctor team": 5}),
            "WH2": ("Mumbai, Maharashtra", {"food": 150, "water": 200, "medicine": 90, "doctor team": 4}),
            "WH3": ("Kolkata, West Bengal", {"food": 100, "water": 140, "medicine": 60, "doctor team": 3}),
            "WH4": ("Chennai, Tamil Nadu", {"food": 130, "water": 170, "medicine": 80, "doctor team": 6}),
            "WH5": ("Bangalore, Karnataka", {"food": 140, "water": 190, "medicine": 85, "doctor team": 7}),
        }
        for wid, (city, inventory) in warehouse_data.items():
            self.warehouses.append(Warehouse(wid, city, inventory))
    
    def sort_warehouses_by_id(self):
        """Sort warehouses by ID to enable binary search"""
        self.warehouses.sort(key=lambda x: x.id)

    def binary_search_warehouse(self, warehouse_id):
        """Find a warehouse by ID using binary search"""
        left, right = 0, len(self.warehouses) - 1
        
        while left <= right:
            mid = (left + right) // 2
            if self.warehouses[mid].id == warehouse_id:
                return self.warehouses[mid]
            elif self.warehouses[mid].id < warehouse_id:
                left = mid + 1
            else:
                right = mid - 1
                
        return None  # Warehouse not found
    
    def get_warehouse_by_id(self, warehouse_id):
        """Get a warehouse by ID using binary search"""
        return self.binary_search_warehouse(warehouse_id)

    # Heap Sort implementation for sorting warehouses by distance
    def heapify(self, arr, n, i, location):
        """
        Heapify subtree rooted at index i in array arr of size n
        """
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        
        # Compare with left child
        if left < n:
            self.comparisons += 1
            if haversine(location[0], location[1], arr[left].lat, arr[left].lon) > haversine(location[0], location[1], arr[largest].lat, arr[largest].lon):
                largest = left
            
        # Compare with right child
        if right < n:
            self.comparisons += 1
            if haversine(location[0], location[1], arr[right].lat, arr[right].lon) > haversine(location[0], location[1], arr[largest].lat, arr[largest].lon):
                largest = right
            
        # Change root if needed
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]  # Swap
            self.swaps += 1
            self.heapify(arr, n, largest, location)
            
    def heap_sort(self, arr, location):
        """
        Sort array using heap sort - sort warehouses by distance (closest first)
        """
        self.comparisons = 0  # Reset counters
        self.swaps = 0
        
        n = len(arr)
        
        # Build a maxheap
        for i in range(n // 2 - 1, -1, -1):
            self.heapify(arr, n, i, location)
            
        # Extract elements one by one
        for i in range(n-1, 0, -1):
            arr[0], arr[i] = arr[i], arr[0]  # Swap
            self.swaps += 1
            self.heapify(arr, i, 0, location)

        # Print sorting statistics
        print(f"\n📊 Sorting Statistics:")
        print(f"Number of comparisons: {self.comparisons}")
        print(f"Number of swaps: {self.swaps}")
        print(f"Time Complexity: O(n log n)")
        
        return arr[::-1]

    def allocate_resources(self, request):
        """Allocate resources from multiple warehouses and display distances"""
        # Create a copy of warehouses to avoid modifying the original list during sorting
        warehouses_copy = self.warehouses.copy()
        sorted_wh = self.heap_sort(warehouses_copy, request["location"])
        allocated = {}
        warehouse_distances = {}

        for resource, qty_needed in request["requirements"].items():
            remaining_qty = qty_needed

            for wh in sorted_wh:
                if remaining_qty == 0:
                    break

                available_qty = wh.inventory.get(resource, 0)
                allocated_qty = min(available_qty, remaining_qty)

                if allocated_qty > 0:
                    if wh.id not in allocated:
                        allocated[wh.id] = {}
                    allocated[wh.id][resource] = allocated_qty
                    wh.inventory[resource] -= allocated_qty
                    remaining_qty -= allocated_qty

        for wh in sorted_wh:
            warehouse_distances[wh.id] = haversine(request["location"][0], request["location"][1], wh.lat, wh.lon)

        return allocated, warehouse_distances, sorted_wh

    def find_nearest_warehouse_with_resource(self, location, resource, min_quantity):
        """Find nearest warehouse with sufficient resource using heap sort"""
        # First, calculate distances to all warehouses
        warehouses_with_resource = []
        for wh in self.warehouses:
            if resource in wh.inventory and wh.inventory[resource] >= min_quantity:
                warehouses_with_resource.append(wh)
        
        # Sort warehouses by distance using heap sort
        sorted_warehouses = self.heap_sort(warehouses_with_resource, location)
        
        if not sorted_warehouses:
            return None
        
        return sorted_warehouses[0]  # Return the nearest warehouse

class DisasterReliefSystem:
    def __init__(self):
        self.warehouse_manager = WarehouseManager()
        self.requester_manager = RequesterManager()
        self.admin_manager = AdminManager()  # Add admin manager
        self.requests = []
        self.current_admin = None  # Track current logged-in admin
        self.display_greeting()

    def display_greeting(self):
        """Display welcome message and system information"""
        print("\n" + "="*50)
        print("🚨 Welcome to Disaster Relief Management System 🚨")
        print("="*50)
        print("\nSystem Information:")
        print(f"📦 Active Warehouses: {len(self.warehouse_manager.warehouses)}")
        print(f"👥 Registered Requesters: {len(self.requester_manager.requesters)}")
        print(f"🏢 Available Locations: {len(location_mapping)}")
        print("\nThis system helps coordinate disaster relief efforts")
        print("by efficiently managing resources and warehouse allocations.")
        print("="*50 + "\n")

    # Input validation methods
    def validate_requester_id(self, requester_id):
        """Validate requester ID - can be string or integer"""
        return len(str(requester_id).strip()) > 0  # Just check it's not empty
    
    def validate_requester_name(self, name):
        """Validate name - must be non-empty string containing only letters and spaces"""
        if not name or not isinstance(name, str):
            return False
        # Check if name contains only letters and spaces
        return all(c.isalpha() or c.isspace() for c in name.strip())
    
    def validate_contact_number(self, contact):
        """Validate contact number - must be exactly 10 digits"""
        if not contact:
            return False
        contact = contact.strip()
        return contact.isdigit() and len(contact) == 10
    
    def validate_integer_input(self, value, min_value=0):
        """Validate an integer input is valid and >= min_value"""
        try:
            val = int(value)
            return val >= min_value
        except (ValueError, TypeError):
            return False
    
    def get_validated_input(self, prompt, validation_func, error_message):
        """Get input from user with validation"""
        while True:
            value = input(prompt)
            if validation_func(value):
                return value
            print(f"❌ {error_message}")
    
    def get_integer_input(self, prompt, min_value=0):
        """Get validated integer input"""
        while True:
            value = input(prompt)
            try:
                val = int(value)
                if val >= min_value:
                    return val
                print(f"❌ Value must be at least {min_value}.")
            except ValueError:
                print("❌ Invalid input. Please enter a valid integer.")
    
    def binary_search_location(self, location_name):
        """Use binary search to find if a location exists in our mapping"""
        # Convert the dictionary keys to a sorted list
        locations = sorted(location_mapping.keys())
        left, right = 0, len(locations) - 1
        
        while left <= right:
            mid = (left + right) // 2
            if locations[mid] == location_name:
                return locations[mid]
            elif locations[mid] < location_name:
                left = mid + 1
            else:
                right = mid - 1
                
        return None  # Location not found
    
    def plot_warehouse_distances(self, request_location, warehouse_distances, allocated_wh):
        plt.figure(figsize=(10, 6))

        # Plot all warehouses in blue
        for wh in self.warehouse_manager.warehouses:
            city = wh.city
            lat, lon = location_mapping[city]
            
            if wh.id in allocated_wh:
                plt.scatter(lon, lat, color='orange', s=100, label='Allocated Warehouse' if 'Allocated Warehouse' not in plt.gca().get_legend_handles_labels()[1] else "")
            else:
                plt.scatter(lon, lat, color='blue', label='Warehouse' if 'Warehouse' not in plt.gca().get_legend_handles_labels()[1] else "")
            plt.text(lon, lat, city, fontsize=9, ha='right', color='black')

        # Plot requester location in red
        req_lat, req_lon = request_location
        plt.scatter(req_lon, req_lat, color='red', marker='X', s=100, label='Requester')

        # Draw lines to warehouses
        for wh_id, distance in warehouse_distances.items():
            warehouse = self.warehouse_manager.get_warehouse_by_id(wh_id)
            if warehouse:
                wh_lat, wh_lon = warehouse.lat, warehouse.lon
                plt.plot([req_lon, wh_lon], [req_lat, wh_lat], 'gray', linestyle='dotted')
                plt.text((req_lon + wh_lon) / 2, (req_lat + wh_lat) / 2, f"{distance} km", fontsize=8, color='black')

        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.title("Warehouse Distance Visualization")
        plt.legend()
        plt.grid(True)
        plt.show()

    def book_request(self):
        """User menu for disaster relief request with input validation."""
        print("\n--- User Request Menu ---")
        
        # Validate requester ID
        requester_id = self.get_validated_input(
            "\nEnter requester ID: ",
            self.validate_requester_id,
            "Invalid requester ID. It cannot be empty."
        )
        
        # Validate requester name
        requester_name = self.get_validated_input(
            "Enter requester name: ",
            self.validate_requester_name,
            "Invalid name. Name must contain only letters and spaces."
        )
        
        # Check if requester ID and name match our predefined data using binary search
        if not self.requester_manager.is_valid_requester(requester_id, requester_name):
            print("❌ Requester ID and name do not match our records. Request cannot be processed.")
            input("\nPress Enter to continue...")
            return  # Return immediately without proceeding
        
        # Get the requester using binary search
        requester = self.requester_manager.get_requester_by_id(requester_id)
        if not requester:  # Additional check to prevent continuing with invalid ID
            print("❌ Requester ID not found. Request cannot be processed.")
            input("\nPress Enter to continue...")
            return  # Return immediately without proceeding
            
        requester_no = requester.contact
        
        print(f"✅ Requester verified. Contact: {requester_no}")
        
        # Validate location using binary search
        while True:
            loc_name = input("Enter your location name (e.g., New Delhi, Delhi): ")
            location_found = self.binary_search_location(loc_name)
            if location_found:
                location = location_mapping[location_found]
                break
            print("❌ Invalid location. Try again.")
        
        # Validate population affected
        population_affected = self.get_integer_input(
            "Enter the number of people affected: ",
            min_value=1
        )

        # Define valid resources
        valid_resources = ["food", "water", "medicine", "doctor team"]
        
        # Resource validation loop
        while True:
            print(f"Valid resources: {', '.join(valid_resources)}")
            resources_needed = input("Enter required resources (comma-separated): ")
            resource_list = [r.strip().lower() for r in resources_needed.split(",")]
            
            # Check for invalid resources using binary search
            invalid_resources = []
            for res in resource_list:
                if res and res not in valid_resources:
                    invalid_resources.append(res)
            
            if invalid_resources:
                print(f"❌ Invalid resource(s): {', '.join(invalid_resources)}. Please re-enter all resources.")
                continue
            
            # Check for empty list
            if not any(resource_list):
                print("❌ Please enter at least one resource.")
                continue
                
            # All resources are valid, proceed
            break
        
        requirements = {}
                
        # Ask for quantities for each valid resource
        for res in resource_list:
            if res:  # Skip empty entries
                requirements[res] = self.get_integer_input(
                    f"{res.capitalize()}: ",
                    min_value=0
                )

        request = {
            "id": requester_id,
            "name": requester_name,
            "contact": requester_no,
            "location": location,
            "requirements": requirements,
            "population": population_affected
        }
        self.requests.append(request)

        allocated_wh, warehouse_distances, sorted_wh = self.warehouse_manager.allocate_resources(request)
        
        request["allocated_warehouse"] = allocated_wh
        
        print("\n📍 **Warehouse Distances from Requester's Location**:")
        for wh in sorted_wh:
            print(f"📦 Warehouse {wh.id} in {wh.city} ➡️ {warehouse_distances[wh.id]} km")

        print("\n✅ **Resource Allocation:**")
        for wh, res in allocated_wh.items():
            print(f"📦 Warehouse {wh} ({warehouse_distances[wh]} km away): {res}")
            
        # Added a pause to keep user in the request menu
        input("\nPress Enter to continue...")

    def admin_login(self):
        """Handle admin login"""
        print("\n=== Admin Login ===")
        username = input("Enter username: ")
        password = input("Enter password: ")
        
        admin = self.admin_manager.authenticate_admin(username, password)
        if admin:
            self.current_admin = admin
            print(f"\n✅ Welcome, {admin.name}!")
            return True
        else:
            print("\n❌ Invalid username or password.")
            return False

    def add_new_admin(self):
        """Add a new admin user"""
        if not self.current_admin:
            print("\n❌ Please login as admin first.")
            return

        # Only super_admin can add new admins
        if self.current_admin.role != "super_admin":
            print("\n❌ Only super administrators can add new admins.")
            input("\nPress Enter to continue...")
            return

        print("\n=== Add New Administrator ===")
        
        # Get and validate new admin information
        username = self.get_validated_input(
            "Enter username: ",
            lambda x: len(x.strip()) > 0 and not any(c.isspace() for c in x),
            "Username cannot be empty or contain spaces."
        )
        
        password = self.get_validated_input(
            "Enter password: ",
            lambda x: len(x.strip()) >= 6,
            "Password must be at least 6 characters long."
        )
        
        name = self.get_validated_input(
            "Enter full name: ",
            self.validate_requester_name,
            "Invalid name. Name must contain only letters and spaces."
        )
        
        contact = self.get_validated_input(
            "Enter contact number: ",
            self.validate_contact_number,
            "Invalid contact number. It must contain exactly 10 digits."
        )
        
        # Get role
        print("\nAvailable roles:")
        print("1. super_admin (Full system access)")
        print("2. admin (Standard administrative access)")
        print("3. coordinator (Limited access)")
        
        role_choice = input("\nSelect role (1-3): ").strip()
        role_map = {
            "1": "super_admin",
            "2": "admin",
            "3": "coordinator"
        }
        
        if role_choice not in role_map:
            print("\n❌ Invalid role selection.")
            input("\nPress Enter to continue...")
            return
            
        role = role_map[role_choice]
        
        # Add the new admin
        new_admin = self.admin_manager.add_admin(username, password, name, contact, role)
        
        if new_admin:
            print("\n✅ New administrator added successfully!")
            print(f"ID: {new_admin.id}")
            print(f"Username: {new_admin.username}")
            print(f"Name: {new_admin.name}")
            print(f"Role: {new_admin.role}")
        else:
            print("\n❌ Failed to add administrator. Username may already exist.")
        
        input("\nPress Enter to continue...")

    def manage_admins(self):
        """Manage administrator accounts"""
        while True:
            print("\n=== Administrator Management ===")
            print("1. Display All Administrators")
            print("2. Add New Administrator")
            print("3. Delete Administrator")
            print("4. Change Admin Password")
            print("5. Update Admin Information")
            print("6. Return to Admin Menu")
            
            choice = input("Enter your choice: ")
            if choice == '1':
                self.admin_manager.display_admins()
            elif choice == '2':
                self.add_new_admin()
            elif choice == '3':
                self.delete_admin()
            elif choice == '4':
                self.change_admin_password()
            elif choice == '5':
                self.update_admin_info()
            elif choice == '6':
                break
            else:
                print("❌ Invalid choice. Please try again.")

    def delete_admin(self):
        """Delete an administrator"""
        if not self.current_admin:
            print("\n❌ Please login as admin first.")
            return

        print("\n=== Delete Administrator ===")
        self.admin_manager.display_admins()
        
        admin_id = input("\nEnter the ID of the admin to delete: ").strip().upper()
        
        # Don't allow self-deletion
        if admin_id == self.current_admin.id:
            print("\n❌ You cannot delete your own account.")
            input("\nPress Enter to continue...")
            return
            
        # Confirm deletion
        confirm = input(f"Are you sure you want to delete admin {admin_id}? (yes/no): ").lower()
        if confirm != 'yes':
            print("Deletion cancelled.")
            input("\nPress Enter to continue...")
            return
            
        if self.admin_manager.delete_admin(admin_id):
            print("\n✅ Administrator deleted successfully!")
        else:
            print("\n❌ Failed to delete administrator. ID may be invalid or it's the default admin.")
            
        input("\nPress Enter to continue...")

    def change_admin_password(self):
        """Change administrator password"""
        if not self.current_admin:
            print("\n❌ Please login as admin first.")
            return

        print("\n=== Change Administrator Password ===")
        
        # Get old password
        old_password = input("Enter current password: ")
        
        # Get new password
        new_password = self.get_validated_input(
            "Enter new password: ",
            lambda x: len(x.strip()) >= 6,
            "Password must be at least 6 characters long."
        )
        
        # Confirm new password
        confirm_password = input("Confirm new password: ")
        if new_password != confirm_password:
            print("\n❌ Passwords do not match.")
            input("\nPress Enter to continue...")
            return
            
        if self.admin_manager.change_password(self.current_admin.id, old_password, new_password):
            print("\n✅ Password changed successfully!")
        else:
            print("\n❌ Failed to change password. Current password may be incorrect.")
            
        input("\nPress Enter to continue...")

    def update_admin_info(self):
        """Update administrator information"""
        if not self.current_admin:
            print("\n❌ Please login as admin first.")
            return

        print("\n=== Update Administrator Information ===")
        print("Leave blank to keep current value.")
        
        # Get new name
        new_name = input(f"Enter new name [{self.current_admin.name}]: ").strip()
        if new_name and not self.validate_requester_name(new_name):
            print("\n❌ Invalid name format. Name must contain only letters and spaces.")
            input("\nPress Enter to continue...")
            return
            
        # Get new contact
        new_contact = input(f"Enter new contact number [{self.current_admin.contact}]: ").strip()
        if new_contact and not self.validate_contact_number(new_contact):
            print("\n❌ Invalid contact number. Must be exactly 10 digits.")
            input("\nPress Enter to continue...")
            return
            
        # Only super_admin can change roles
        new_role = None
        if self.current_admin.role == "super_admin":
            print("\nAvailable roles:")
            print("1. super_admin (Full system access)")
            print("2. admin (Standard administrative access)")
            print("3. coordinator (Limited access)")
            
            role_choice = input("\nSelect new role (1-3) or press Enter to keep current: ").strip()
            if role_choice:
                role_map = {
                    "1": "super_admin",
                    "2": "admin",
                    "3": "coordinator"
                }
                if role_choice in role_map:
                    new_role = role_map[role_choice]
                else:
                    print("\n❌ Invalid role selection.")
                    input("\nPress Enter to continue...")
                    return
            
        # Update information
        if self.admin_manager.update_admin_info(
            self.current_admin.id,
            name=new_name if new_name else None,
            contact=new_contact if new_contact else None,
            role=new_role
        ):
            print("\n✅ Administrator information updated successfully!")
            # Update current admin object
            if new_name:
                self.current_admin.name = new_name
            if new_contact:
                self.current_admin.contact = new_contact
            if new_role:
                self.current_admin.role = new_role
        else:
            print("\n❌ Failed to update administrator information.")
            
        input("\nPress Enter to continue...")

    def display_activity_log(self):
        """Display activity log for an admin or all admins"""
        self.admin_manager.display_activity_log()

    def admin_menu(self):
        """Admin menu that keeps the user in the admin interface until they choose to return to main menu"""
        while True:
            print("\n=== Admin Menu ===")
            print("1. Display Requesters Data")
            print("2. Display all Warehouses")
            print("3. Visual Representation of Requester and Warehouses")
            print("4. Display Registered Coordinators")
            print("5. Add New Requester")
            print("6. Search Request by ID")
            print("7. Update Warehouse Units")
            print("8. Manage Administrators")
            print("9. Display Activity Log")
            print("10. Return to Main Menu")
            
            choice = input("Enter your choice: ")
            if choice == '1':
                self.display_request()
            elif choice == '2':
                self.display_warehouses()
            elif choice == '3':
                self.plot_latest_request()
            elif choice == '4':
                self.display_requesters()
            elif choice == '5':
                self.admin_add_requester()
            elif choice == '6':
                self.search_request_by_id()
            elif choice == '7':
                self.update_warehouse_units()
            elif choice == '8':
                self.manage_admins()
            elif choice == '9':
                self.display_activity_log()
            elif choice == '10':
                print("Returning to main menu...")
                break
            else:
                print("❌ Invalid choice. Please try again.")

    def user_menu(self):
        """User menu that keeps the user in the user interface until they choose to return to main menu"""
        while True:
            print("\n=== User Menu ===")
            print("1. Book Request")
            print("2. Display Graph")
            print("3. Return to Main Menu")
            
            choice = input("Enter your choice: ")
            if choice == '1':
                self.book_request()
                # Do NOT return to main menu after booking, stay in user menu
            elif choice == '2':
                self.plot_latest_request()
            elif choice == '3':
                print("Returning to main menu...")
                break
            else:
                print("❌ Invalid choice. Please try again.")

    def main_menu(self):
        """Main menu that keeps the user in the system until they choose to exit"""
        while True:
            print("\n=== Disaster Relief Management System ===")
            print("1. Book a Request")
            print("2. Admin Login")
            print("3. Exit")
            
            choice = input("Enter your choice: ")
            if choice == '1':
                self.book_request()
            elif choice == '2':
                if self.admin_login():
                    self.admin_menu()
            elif choice == '3':
                print("\nThank you for using Disaster Relief Management System!")
                break
            else:
                print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    DisasterReliefSystem().main_menu()
        