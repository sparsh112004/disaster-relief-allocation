import math
import matplotlib.pyplot as plt 
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

    def merge_sort(self, warehouses, location):
        """Merge Sort to sort warehouses by nearest distance"""
        if len(warehouses) <= 1:
            return warehouses

        mid = len(warehouses) // 2
        left_half = self.merge_sort(warehouses[:mid], location)
        right_half = self.merge_sort(warehouses[mid:], location)

        return self.merge(left_half, right_half, location)

    def merge(self, left, right, location):
        sorted_list = []
        while left and right:
            self.comparisons += 1  # Count comparison
            if haversine(location[0], location[1], left[0].lat, left[0].lon) <= haversine(location[0], location[1], right[0].lat, right[0].lon):
                sorted_list.append(left.pop(0))
                self.swaps += 1  # Count swap
            else:
                sorted_list.append(right.pop(0))
                self.swaps += 1  # Count swap
        
        # Count remaining elements as swaps
        self.swaps += len(left) + len(right)
        sorted_list.extend(left if left else right)
        return sorted_list

    def allocate_resources(self, request):
        """Allocate resources from multiple warehouses and display distances"""
        # Reset counters before sorting
        self.comparisons = 0
        self.swaps = 0
        
        warehouses_copy = self.warehouses.copy()
        sorted_wh = self.merge_sort(warehouses_copy, request["location"])
        
        # Print sorting statistics
        print(f"\n📊 Sorting Statistics:")
        print(f"Number of comparisons: {self.comparisons}")
        print(f"Number of swaps: {self.swaps}")
        print(f"Time Complexity: O(n log n)")
        
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
        """Use binary search to find nearest warehouse with sufficient resource"""
        # First, calculate distances to all warehouses
        warehouses_with_distances = []
        for wh in self.warehouses:
            distance = haversine(location[0], location[1], wh.lat, wh.lon)
            if resource in wh.inventory and wh.inventory[resource] >= min_quantity:
                warehouses_with_distances.append((wh, distance))
        
        # Sort warehouses by distance
        warehouses_with_distances.sort(key=lambda x: x[1])
        
        # Binary search for first warehouse with sufficient resource
        if not warehouses_with_distances:
            return None
        
        return warehouses_with_distances[0][0]  # Return the nearest warehouse

class DisasterReliefSystem:
    def __init__(self):
        self.warehouse_manager = WarehouseManager()
        self.requester_manager = RequesterManager()
        self.requests = []
        self.display_greeting()  # Add greeting display
        
    def display_greeting(self):
        """Display welcome message and system information"""
        print("\n" + "="*50)
        print("🚨 Welcome to Disaster Relief Management System 🚨")
        print("="*50)
        print("\nSystem Information:")
        print(f"📦 Active Warehouses: {len(self.warehouse_manager.warehouses)}")
        print(f"👥 Registered Requesters: {len(self.requester_manager.requesters)}")
        print(f"🏢 Available Locations: {len(location_mapping)}")
        print("\nThis system uses Merge Sort algorithm to efficiently")
        print("coordinate disaster relief efforts by finding nearest warehouses.")
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
        
        # # Display available requesters for reference
        # print("\nAvailable Requesters:")
        # for requester in self.requester_manager.requesters:
        #     print(f"ID: {requester.id}, Name: {requester.name}")
        
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

    def admin_add_requester(self):
        """Admin function to add a new requester with auto-incremented ID"""
        print("\n--- Add New Requester (Admin) ---")
        
        # Show existing requesters for reference
        print("\nExisting Requesters:")
        for requester in self.requester_manager.requesters:
            print(f"ID: {requester.id}, Name: {requester.name}, Contact: {requester.contact}")
        
        # Get and validate new requester information
        requester_name = self.get_validated_input(
            "\nEnter requester name: ",
            self.validate_requester_name,
            "Invalid name. Name must contain only letters and spaces."
        )
        
        requester_contact = self.get_validated_input(
            "Enter contact number: ",
            self.validate_contact_number,
            "Invalid contact number. It must contain exactly 10 digits."
        )
        
        # Add the new requester with auto-generated ID
        new_requester = self.requester_manager.add_requester(requester_name, requester_contact)
        
        if new_requester:
            print("\n✅ New requester added successfully:")
            print(f"ID: {new_requester.id}, Name: {new_requester.name}, Contact: {new_requester.contact}")
        else:
            print("\n❌ Failed to add requester. Please try again.")
        
        input("\nPress Enter to continue...")
    
    def binary_search_request(self, requester_id):
        """Use binary search to find a request by requester ID"""
        # First sort requests by requester ID
        sorted_requests = sorted(self.requests, key=lambda x: x["id"])
        
        left, right = 0, len(sorted_requests) - 1
        result = []
        
        # Binary search for the first occurrence
        while left <= right:
            mid = (left + right) // 2
            if sorted_requests[mid]["id"] == requester_id:
                result.append(sorted_requests[mid])
                # Check for other requests with the same ID
                i = mid - 1
                while i >= 0 and sorted_requests[i]["id"] == requester_id:
                    result.append(sorted_requests[i])
                    i -= 1
                i = mid + 1
                while i < len(sorted_requests) and sorted_requests[i]["id"] == requester_id:
                    result.append(sorted_requests[i])
                    i += 1
                return result
            elif sorted_requests[mid]["id"] < requester_id:
                left = mid + 1
            else:
                right = mid - 1
        
        return result  # Empty list if no requests found
            
    def plot_latest_request(self):
        """Display graph for the most recent request"""
        if not self.requests:
            print("\n❌ No requests available to display. Please book a request first.")
            input("\nPress Enter to continue...")
            return

        # Get the most recent request
        latest_request = self.requests[-1]

        # Extract required data
        request_location = latest_request["location"]
        allocated_warehouses = latest_request.get("allocated_warehouse", {})

        # Calculate distances for all warehouses
        warehouse_distances = {}
        for wh in self.warehouse_manager.warehouses:
            warehouse_distances[wh.id] = haversine(
                request_location[0], 
                request_location[1], 
                wh.lat,
                wh.lon
            )

        # Call the plotting function
        self.plot_warehouse_map(request_location, warehouse_distances, allocated_warehouses)
        # Added a pause to keep user in the graph view
        input("\nPress Enter to continue...")

    def plot_warehouse_map(self, request_location, warehouse_distances, allocated_warehouses):
        """
        Creates a visualization of warehouses and their distances from the request location.
        """
        plt.figure(figsize=(12, 7))
        req_lat, req_lon = request_location
    
        # Define colors and styles
        requester_color = 'red'      # Requester (X)
        allocated_color = 'black'   # Allocated warehouses (Square)
        warehouse_color = 'darkblue'     # Regular warehouses (Circle)
        line_color = 'black'             # Distance lines
        city_bg_color = 'lightgray'      # Background for city labels
    
        # Plot all warehouses
        for wh in self.warehouse_manager.warehouses:
            lat, lon = wh.lat, wh.lon
            
            # Plot allocated warehouses with dark orange squares
            if wh.id in allocated_warehouses:
                plt.scatter(lon, lat, color=allocated_color, s=200, marker='s', 
                            label='Allocated Warehouse' if 'Allocated Warehouse' not in plt.gca().get_legend_handles_labels()[1] else "")
            else:
                plt.scatter(lon, lat, color=warehouse_color, s=100, marker='o',
                            label='Warehouse' if 'Warehouse' not in plt.gca().get_legend_handles_labels()[1] else "")
    
            # Add city label above the marker
            plt.text(lon, lat + 0.6, f"{wh.city}\n({wh.id})", fontsize=9, ha='center', va='bottom', color='black', 
                     bbox=dict(facecolor=city_bg_color, alpha=0.8, edgecolor='none'))
    
        # Plot requester location with red text, slightly below the marker
        plt.scatter(req_lon, req_lat, color=requester_color, marker='X', s=150, label='Requester')
    
        # Draw distance lines for allocated warehouses
        for wh_id in allocated_warehouses:
            warehouse = self.warehouse_manager.get_warehouse_by_id(wh_id)  # Using binary search
            if warehouse:
                wh_lat, wh_lon = warehouse.lat, warehouse.lon
                if (req_lat == wh_lat) and (req_lon == wh_lon):
                    continue  # No line, no distance label
                
                plt.plot([req_lon, wh_lon], [req_lat, wh_lat], color=line_color, linestyle='dotted')
                
                # Add distance labels at the midpoint, slightly above the line
                mid_lon = (req_lon + wh_lon) / 2
                mid_lat = (req_lat + wh_lat) / 2
                plt.text(mid_lon, mid_lat + 0.03, f"{warehouse_distances[wh_id]:.1f} km", 
                         fontsize=9, color='black', fontweight='bold', ha='center', va='bottom',
                         bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
    
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.title("Warehouse Distance Visualization")
        plt.legend()
        plt.grid(True)
        plt.show()
    
    def search_request_by_id(self):
        """Search for requests by requester ID using binary search"""
        print("\n--- Search Request by ID ---")
        requester_id = input("Enter requester ID to search: ")
        
        matching_requests = self.binary_search_request(requester_id)
        
        if matching_requests:
            print(f"\n✅ Found {len(matching_requests)} request(s) for ID: {requester_id}")
            for i, req in enumerate(matching_requests, 1):
                print(f"\n🔹 Request {i}:")
                print(f"👤 Name: {req['name']}")
                print(f"📍 Location: {req['location']}")
                print(f"👥 Population Affected: {req['population']}")
                
                # Show resources requested
                print("📦 Resources:")
                for res, qty in req["requirements"].items():
                    print(f"   - {res.capitalize()}: {qty}")
        else:
            print(f"\n❌ No requests found for ID: {requester_id}")
            
        input("\nPress Enter to continue...")
        
    def display_request(self):
        """Displays all disaster relief requests and their status."""
        if not self.requests:
            print("⚠️ No requests available.")
            input("\nPress Enter to continue...")
            return

        print("\n=== 📋 Disaster Relief Requests ===")
        for i, request in enumerate(self.requests, 1):
            print(f"\n🔹 **Request {i}**")
            print(f"🆔 ID: {request['id']}")
            print(f"👤 Name: {request['name']}")
            print(f"📍 Location: {request['location']}")
            print(f"👥 Population Affected: {request['population']}")

            print("\n📌 **Resources Needed:**")
            for res, qty in request["requirements"].items():
                print(f"   - {res.capitalize()}: {qty}")

            # Get allocated warehouse details
            allocated_wh = request.get("allocated_warehouse", None)

            # Check and display allocated warehouses
            if allocated_wh and isinstance(allocated_wh, dict) and len(allocated_wh) > 0:
                print("\n✅ **Allocated Warehouses:**")
                for wh, res in allocated_wh.items():
                    print(f"   - 📦 {wh}: {res}")
            else:
                print("\n⚠️ No warehouse allocated yet.")

        print("\n===================================")
        input("\nPress Enter to continue...")

    def display_requesters(self):
        """Display all registered requesters"""
        print("\n=== 👤 Registered Requesters ===")
        for i, requester in enumerate(self.requester_manager.requesters, 1):
            print(f"{i}. ID: {requester.id}, Name: {requester.name}, Contact: {requester.contact}")
        print("\n===================================")
        input("\nPress Enter to continue...")

    def display_warehouses(self):
        """Display all warehouses and their current inventory"""
        if not self.warehouse_manager.warehouses:
            print("\n⚠️ No warehouses available.")
            input("\nPress Enter to continue...")
            return

        print("\n=== 📦 Warehouse Inventory ===")
        for warehouse in self.warehouse_manager.warehouses:
            print(f"\n🏢 Warehouse {warehouse.id} ({warehouse.city})")
            print("📦 **Current Inventory:**")

            if not warehouse.inventory:
                print("   - ⚠️ No stock available.")
            else:
                for item, quantity in warehouse.inventory.items():
                    print(f"   - {item.capitalize()}: {quantity} units")

        print("\n===================================")
        input("\nPress Enter to continue...")
            
    def update_warehouse_units(self):
        """Update units for a specific warehouse"""
        print("\n=== Update Warehouse Units ===")
        
        # Display all warehouses first
        print("\nAvailable Warehouses:")
        for wh in self.warehouse_manager.warehouses:
            print(f"\n🏢 Warehouse {wh.id} ({wh.city})")
            print("Current Inventory:")
            for item, quantity in wh.inventory.items():
                print(f"   - {item.capitalize()}: {quantity} units")
        
        # Get warehouse ID
        while True:
            wh_id = input("\nEnter Warehouse ID (e.g., WH1): ").strip().upper()
            warehouse = self.warehouse_manager.get_warehouse_by_id(wh_id)
            if warehouse:
                break
            print("❌ Invalid warehouse ID. Please try again.")
        
        # Show current inventory of selected warehouse
        print(f"\nCurrent inventory for {wh_id}:")
        for item, quantity in warehouse.inventory.items():
            print(f"- {item.capitalize()}: {quantity} units")
        
        # Get resource to update
        while True:
            resource = input("\nEnter resource name to update: ").lower().strip()
            if resource in warehouse.inventory:
                break
            print("❌ Invalid resource name. Available resources:", ", ".join(warehouse.inventory.keys()))
        
        # Get new quantity
        while True:
            try:
                new_quantity = int(input(f"Enter new quantity for {resource}: "))
                if new_quantity >= 0:
                    break
                print("❌ Quantity must be non-negative.")
            except ValueError:
                print("❌ Please enter a valid number.")
        
        # Update the inventory
        old_quantity = warehouse.inventory[resource]
        warehouse.inventory[resource] = new_quantity
        
        print(f"\n✅ Successfully updated {resource} in {wh_id}")
        print(f"Old quantity: {old_quantity}")
        print(f"New quantity: {new_quantity}")
        
        input("\nPress Enter to continue...")

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
            print("7. Update Warehouse Units")  # New option
            print("8. Return to Main Menu")
            
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
                self.update_warehouse_units()  # New method call
            elif choice == '8':
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
        """Main menu for choosing user or admin operations."""
        while True:
            print("\n=== Disaster Relief Management System ===")
            print("1. User (Requester)")
            print("2. Admin")
            print("3. Exit")
            
            choice = input("Enter your choice: ")
            if choice == "1":
                self.user_menu()
            elif choice == "2":
                self.admin_menu()
            elif choice == "3":
                print("Exiting. Stay safe!")
                break
            else:
                print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    DisasterReliefSystem().main_menu()