import json
import os
import random
import datetime

os.system("cls")

menu = """ 
\033[1;34m▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
♻ Green Lantern Corps AEWMS ♻               
▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

\033[1;31m [Main Menu]
\033[33m
[ 1 ] Add New E-Waste Item
[ 2 ] View All E-Waste Items
[ 3 ] Update Item Details
[ 4 ] Remove Item
[ 5 ] Storage & Safety Alerts
[ 6 ] Generate Reports
[ 7 ] Exit\033[0m
"""
# Get Total Storage Weight of items Sum from the items.json
def get_total_storage():
    total = 0
    try:
        with open("items.json", "r") as file:
            for line in file:
                if line.strip():
                    item = json.loads(line)
                    if item["status"].lower() == "stored":
                        total += item["item_weight"]
    except FileNotFoundError:
        pass
    return total
# Get the storage capacity from config.json
def load_storage_capacity():
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
            return config.get("storage_capacity", 1000)
    except:
        return 1000

# Checking for Hazard items stored more than 30 days
def check_hazard_alerts():
    alerts = []
    overdue = datetime.datetime.now() - datetime.timedelta(days=30)
    try:
        with open("items.json", "r") as file:
            for line in file:
                if line.strip():
                    item = json.loads(line)
                    if item["status"].lower() == "stored" and item["item_category"] == "Hazardous":
                        timestamp = datetime.datetime.strptime(item["timestamp"], "%Y-%m-%d %H:%M:%S")
                        if timestamp < overdue:
                            alerts.append(item)
    except FileNotFoundError:
        pass
    return alerts


# Checking ID already exist
def id_exists(item_id):
    try:
        with open("items.json", "r") as file:
            for line in file:
                if line.strip():
                    item = json.loads(line)
                    if item["item_id"] == item_id:
                        return True
    except FileNotFoundError:
        pass
    return False

# Display All items as a table
def display_items(items):
    print(f"\033[1;32m{'ID':<10}{'NAME':<20}{'CATEGORY':<20}{'WEIGHT(kg)':<15}{'FEE/KG(LKR)':<15}{'STATUS':<15}\033[0m")
    print("-" * 95)
    for item in items:
        print(
            f"\033[33m{item['item_id']:<10}\033[0m"
            f"\033[33m{item['item_name']:<20}\033[0m"
            f"\033[33m{item['item_category']:<20}\033[0m"
            f"\033[33m{item['item_weight']:<15}\033[0m"
            f"\033[33m{item['recycling_fee']:<15}\033[0m"
            f"\033[33m{item['status']:<15}\033[0m"
        )

# [ Function 1 ]  To Add New Waste Items
def add_new_waste_item():
    global storage_capacity
    os.system("cls")
    total_weight = 0
    total_fee = 0
    output = []
    process_storage = 0
    while True:
        print("\033[34m▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\033[0m")
        print("\033[1;34mADD NEW E-WASTE ITEM\033[0m")
        print("\033[34m▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\033[0m")
        print("")
        current_storage = get_total_storage()
        remaining = storage_capacity - current_storage - process_storage
        print(f"\033[1;33mAvailable Storage: {remaining} kg / {storage_capacity} kg\033[0m")

        if remaining <= 0:
            print("\033[1;31mStorage capacity is full! Cannot add more items.\033[0m")
            input("\nPress Enter...")
            break
        while True:
            try:
                item_id = random.randint(100000, 999999)
                if id_exists(item_id) or any(item["item_id"] == item_id for item in output):
                    continue
                item_name = input("\033[1;35mEnter Item name(Least 3 Letters): \033[0m")
                if len(item_name) > 2:
                    break
                else:
                    print("\033[1;31m! Enter At least 3 Letters\033[0m")
            except ValueError:
                print("\033[1;31mInvalid Input\033[0m")
        print("\033[1;32mItem Categories\n[ 1 ] Recyclable\n[ 2 ] Hazardous\n[ 3 ] Non-Recyclable\033[0m")
        while True:
            try:
                item_category = int(input("\033[1;35mEnter a Item category: \033[0m"))
                if item_category == 1:
                    item_category = "Recyclable"
                    break
                elif item_category == 2:
                    item_category = "Hazardous"
                    break
                elif item_category == 3:
                    item_category = "Non-Recyclable"
                    break
                else:
                    print("\033[1;31mInvalid input. Enter [ 1 ],[ 2 ] or [ 3 ]\033[0m")
            except ValueError:
                print("\033[1;31mInvalid Input\033[0m")
        while True:
            try:
                item_weight = float(input("\033[1;35mEnter Item weight (kg): \033[0m"))
                process_storage += item_weight
                if item_weight <= 0:
                    print("\033[1;31mWeight cannot be negative or zero!\033[0m")
                    continue
                if item_weight > remaining or process_storage > remaining:
                    print(f"\033[1;31mNot enough space! Only {remaining} kg available.\033[0m")
                    continue
                break
            except ValueError:
                print("\033[1;31mInvalid input\033[0m")
        while True:
            try:
                recycling_fee = float(input("\033[1;35mEnter recycling fee per kg (LKR): \033[0m"))
                if recycling_fee < 0:
                    print("\033[1;31mFee cannot be negative!\033[0m")
                    continue
                break
            except ValueError:
                print("\033[1;31mInvalid input\033[0m")

        status = "stored"
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        device_output = {
            "item_id": item_id,
            "item_name": item_name,
            "item_category": item_category,
            "item_weight": item_weight,
            "recycling_fee": recycling_fee,
            "status": status,
            "timestamp": timestamp
        }
        output.append(device_output)
        total_weight += item_weight
        total_fee += item_weight * recycling_fee
        while True:
            continue_or_not = input("Add More Items? (yes/no): ").lower()
            if continue_or_not == "yes":
                os.system("cls")
                break
            elif continue_or_not == "no":
                os.system("cls")
                print("\033[1;33m---------Billing Summary---------\033[0m\n")
                for item in output:
                    print(
                        f"\033[1;32mITEM_NAME: \033[1;35m{item['item_name']} (\033[1;32mID: \033[1;35m{item['item_id']})\033[1;32m | CATEGORY: \033[1;35m{item['item_category']}\033[1;32m | WEIGHT: \033[1;35m{item['item_weight']}kg\033[1;32m | FEE_PER_KG: LKR \033[1;35m{item['recycling_fee']}\033[1;32m | TIMESTAMP: \033[1;35m{item['timestamp']}\033[0m")
                print(f"\nTotal weight: {total_weight}kg")
                print(f"Total fee: LKR {total_fee}")
                if total_weight > 50:
                    bulk_discount = total_fee * 0.05
                    print(f"Bulk discount: LKR {bulk_discount:.2f}")
                    print(f"FINAL TOTAL: {total_fee - bulk_discount:.2f}")
                print("\033[1;32mItem(s) Added Successfully ✓\033[0m")
                try:
                    with open("items.json", "r") as file:
                        existing = [json.loads(line) for line in file if line.strip()]
                except FileNotFoundError:
                    existing = []
                existing.extend(output)
                with open("items.json", "w") as file:
                    for item in existing:
                        json.dump(item, file)
                        file.write("\n")
                input("\nPress Enter to return to menu...")
                break
            else:
                print("Invalid Input. Type yes or no.")
        if continue_or_not == "no":
            break


# [ Function 2 ] To View, Sort, and Search Waste Items
def view_and_search_items():
    os.system("cls")
    all_items = []
    try:
        print("\033[34m▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\033[0m")
        print("\033[1;34mVIEW ALL E-WASTE ITEMS\033[0m")
        print("\033[34m▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\033[0m\n")
        with open("items.json", "r") as file:
            for line in file:
                if line.strip():
                    all_items.append(json.loads(line))
        if len(all_items) == 0:
            print("\033[1;31mNo items found.\033[0m")
            input("\nPress Enter...")
        else:
            display_items(all_items)
            print("")
            print("\033[1;33m[ 1 ] Sort Items\033[0m")
            print("\033[1;33m[ 2 ] Search Items\033[0m")
            while True:
                try:
                    option = int(input("\n\033[1;34mEnter Option: \033[0m"))
                    break
                except ValueError:
                    print("\033[1;31mInvalid Input! Enter 1 or 2 only.\033[0m")
            if option == 1:
                print("\n\033[1;35m[ 1 ] Sort Weight High to Low\033[0m")
                print("\033[1;35m[ 2 ] Sort Weight Low to High\033[0m")
                print("\033[1;35m[ 3 ] Sort By Category\033[0m")
                while True:
                    try:
                        sort_choice = int(input("\n\033[1;34mEnter Sort Option: \033[0m"))
                        break
                    except ValueError:
                        print("\033[1;31mInvalid Input!\033[0m")
                if sort_choice == 1:
                    sorted_items = sorted(all_items, key=lambda x: x['item_weight'], reverse=True)
                    os.system("cls")
                    print("\033[1;34mSORTED: HIGH TO LOW\033[0m\n")
                    display_items(sorted_items)
                    input("\n\n\033[1;31mPress Enter to exit...\033[0m")
                elif sort_choice == 2:
                    sorted_items = sorted(all_items, key=lambda x: x['item_weight'])
                    os.system("cls")
                    print("\033[1;34mSORTED: LOW TO HIGH\033[0m\n")
                    display_items(sorted_items)
                    input("\n\n\033[1;31mPress Enter to exit...\033[0m")
                elif sort_choice == 3:
                    sorted_items = sorted(all_items, key=lambda x: x['item_category'])
                    os.system("cls")
                    print("\033[1;34mSORTED BY CATEGORY\033[0m\n")
                    display_items(sorted_items)
                    input("\n\n\033[1;31mPress Enter to exit...\033[0m")
                else:
                    print("\033[1;31mInvalid Sort Option\033[0m")
                    input("\nPress Enter...")
            elif option == 2:
                print("\n\033[1;33m[ 1 ] Search By ID\033[0m")
                print("\033[1;33m[ 2 ] Search By Name\033[0m")
                while True:
                    try:
                        search_choice = int(input("\n\033[1;34mEnter Search Option: \033[0m"))
                        break
                    except ValueError:
                        print("\033[1;31mInvalid Input! Enter 1 or 2 only.\033[0m")
                if search_choice == 1:
                    while True:
                        try:
                            search_id = int(input("\033[34mEnter Item ID: \033[0m"))
                            break
                        except ValueError:
                            print("\033[1;31mInvalid ID! Enter numbers only.\033[0m")
                    found_items = [item for item in all_items if item['item_id'] == search_id]
                    if found_items:
                        os.system("cls")
                        print("\033[1;34mSEARCH RESULT\033[0m\n")
                        display_items(found_items)
                        input("\n\n\033[1;31mPress Enter to exit...\033[0m")
                    else:
                        print("\033[1;31mItem Not Found\033[0m")
                        input("\n\n\033[1;31mPress Enter to exit...\033[0m")
                elif search_choice == 2:
                    search_name = input("\033[1;34mEnter Item Name: \033[0m").lower()
                    found_items = [item for item in all_items if search_name in item['item_name'].lower()]
                    if found_items:
                        os.system("cls")
                        print("\033[1;34mSEARCH RESULT\033[0m\n")
                        display_items(found_items)
                        input("\n\n\033[1;31mPress Enter to exit...\033[0m")
                    else:
                        print("\033[1;31mItem Not Found\033[0m")
                        input("\n\n\033[1;31mPress Enter to exit...\033[0m")
                else:
                    print("\033[1;31mInvalid Search Option\033[0m")
    except FileNotFoundError:
        print("\033[1;31mFile not found.\033[0m")
        input("\nPress Enter...")


# [ Function 3 ] To Update Item Details
def update_item_details():
    os.system("cls")
    while True:
        try:
            print("\033[34m▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\033[0m")
            print("\033[1;34mUPDATE ITEM DETAILS\033[0m")
            print("\033[34m▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\033[0m")
            print("\033[1;33m[ 1 ] Search Item to update By ID\033[0m")
            print("\033[1;33m[ 2 ] Search Item to update By Name\033[0m")
            print("\033[1;33m[ 0 ] Exit to Main Menu\033[0m")
            search_choice = int(input("\n\033[1;34mEnter Option: \033[0m"))
            if search_choice == 0:
                break
            try:
                with open("items.json", "r") as file:
                    devices = [json.loads(line) for line in file if line.strip()]
            except FileNotFoundError:
                print("\033[1;31mNo items found.\033[0m")
                input("\nPress Enter...")
                break
            found_item = None
            if search_choice == 1:
                search_id = int(input("\033[1;34mEnter Item ID: \033[0m"))
                for item in devices:
                    if item["item_id"] == search_id:
                        found_item = item
                        break
            elif search_choice == 2:
                search_name = input("\033[1;34mEnter Item Name: \033[0m").lower()
                results = [item for item in devices if search_name in item["item_name"].lower()]
                if not results:
                    print("\033[1;31mNo matching items found.\033[0m")
                    input("\nPress Enter...")
                    continue
                display_items(results)
                search_id = int(input("\n\033[1;34mEnter Item ID to update: "))
                for item in devices:
                    if item["item_id"] == search_id:
                        found_item = item
                        break
            else:
                print("\033[1;31mInvalid Option\033[0m")
                input("\nPress Enter...")
                continue
            if not found_item:
                print("\033[1;31mItem not found.\033[0m")
                input("\nPress Enter...")
                continue
            while True:
                os.system("cls")
                print("\n\033[34mItem Details:\033[0m\n")
                display_items([found_item])
                print("\n\n\033[1;33m[ 1 ] Update Storage Status\033[0m")
                print("\033[1;33m[ 2 ] Update Weight\033[0m")
                print("\033[1;33m[ 3 ] Update Category\033[0m")
                print("\033[1;33m[ 4 ] Update Recycling Fee per kg\033[0m")
                print("\033[1;33m[ 0 ] Back to Update Menu\033[0m")
                update_choice = int(input("\n\033[1;34mEnter Option: \033[0m"))
                if update_choice == 0:
                    break
                elif update_choice == 1:
                    new_status = input("\nEnter Status (Recycled/Disposed): ").lower()
                    if new_status == "recycled":
                        found_item["status"] = "Recycled"
                    elif new_status == "disposed":
                        found_item["status"] = "Disposed"
                    else:
                        print("\033[1;31mInvalid Status\033[0m")
                        continue
                elif update_choice == 2:
                    new_weight = float(input("\nEnter Weight (kg): "))
                    found_item["item_weight"] = new_weight
                elif update_choice == 3:
                    print("\n\033[1;33m[ 1 ] Recyclable\033[0m")
                    print("\033[1;33m[ 2 ] Hazardous\033[0m")
                    print("\033[1;33m[ 3 ] Non-Recyclable\033[0m")
                    new_category = int(input("\nEnter Category: "))
                    if new_category == 1:
                        found_item["item_category"] = "Recyclable"
                    elif new_category == 2:
                        found_item["item_category"] = "Hazardous"
                    elif new_category == 3:
                        found_item["item_category"] = "Non-Recyclable"
                elif update_choice == 4:
                    new_fee = float(input("\nEnter Recycling Fee per kg (LKR): "))
                    found_item["recycling_fee"] = new_fee
                else:
                    print("\033[1;31mInvalid Option\033[0m")
                    continue
                with open("items.json", "w") as file:
                    for item in devices:
                        json.dump(item, file)
                        file.write("\n")
                print("\033[1;32mUpdated successfully.\033[0m")
                input("\nPress Enter...")
        except ValueError:
            print("\033[1;31mInvalid Input\033[0m")
            input("\nPress Enter...")


# [ Function 4 ] To Remove Items
def remove_e_waste_item():
    os.system("cls")
    while True:
        try:
            print("\033[34m▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\033[0m")
            print("\033[1;34mREMOVE ITEM\033[0m")
            print("\033[34m▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\033[0m")
            print("\033[1;33m[ 1 ] Remove All Recycled and Disposed Items\033[0m")
            print("\033[1;33m[ 2 ] Search & Remove By ID / Name\033[0m")
            print("\033[1;33m[ 3 ] View All & Remove by ID\033[0m")
            print("\033[1;33m[ 0 ] Back to Main Menu\033[0m")
            remove_choice = int(input("\n\033[1;34mEnter Option: \033[0m"))
            if remove_choice == 0:
                break
            with open("items.json", "r") as file:
                devices = [json.loads(line) for line in file if line.strip()]
            if remove_choice == 1:
                recycled_items = [item for item in devices if item["status"].lower() in ["recycled", "disposed"]]
                if len(recycled_items) == 0:
                    print("\033[1;31mNo Recycled or Disposed Items Found.\033[0m")
                    input("\nPress Enter...")
                    break
                display_items(recycled_items)
                confirm = input("\n\033[1;31mDelete ALL recycled items? (yes/no): \033[0m").lower()
                if confirm == "yes":
                    devices = [item for item in devices if item["status"].lower() not in ["recycled", "disposed"]]
                    with open("items.json", "w") as file:
                        for item in devices:
                            json.dump(item, file)
                            file.write("\n")
                    print("\033[1;32mAll Recycled and Disposed Items Removed.\033[0m")
                else:
                    print("\033[1;33mCancelled.\033[0m")
                input("\nPress Enter...")
                break
            elif remove_choice == 2 or remove_choice == 3:
                found_items = []
                if remove_choice == 3:
                    print("\n\033[1;34mAll Items:\033[0m")
                    found_items = devices
                else:
                    print("\033[1;33m[ 1 ] Search By ID\033[0m")
                    print("\033[1;33m[ 2 ] Search By Name\033[0m")
                    search_choice = int(input("\n\033[1;34mEnter Search Option: \033[0m"))
                    if search_choice == 1:
                        search_id = int(input("\033[1;34mEnter Item ID: \033[0m"))
                        found_items = [item for item in devices if item["item_id"] == search_id]
                    elif search_choice == 2:
                        search_name = input("\033[1;34mEnter Item Name: \033[0m").lower()
                        found_items = [item for item in devices if search_name in item["item_name"].lower()]
                    else:
                        print("\033[1;31mInvalid Option\033[0m")
                        input("\nPress Enter...")
                        continue
                if not found_items:
                    print("\033[1;31mNo items found.\033[0m")
                    input("\nPress Enter...")
                    continue
                if remove_choice == 2:
                    print("\n\033[1;34mMatching Items:\033[0m")
                display_items(found_items)
                try:
                    delete_id = int(input("\n\033[1;31mEnter ID of item to delete: \033[0m"))
                    found_index = None
                    for index, item in enumerate(devices):
                        if item["item_id"] == delete_id:
                            found_index = index
                            break
                    if found_index is not None:
                        display_items([devices[found_index]])
                        confirm = input("\n\033[1;31mDelete this item? (yes/no): \033[0m").lower()
                        if confirm == "yes":
                            devices.pop(found_index)
                            with open("items.json", "w") as file:
                                for item in devices:
                                    json.dump(item, file)
                                    file.write("\n")
                            print("\033[1;32mItem Removed Successfully.\033[0m")
                        else:
                            print("\033[1;33mCancelled.\033[0m")
                    else:
                        print("\033[1;31mInvalid ID.\033[0m")
                except ValueError:
                    print("\033[1;31mInvalid Input\033[0m")
                input("\nPress Enter to return to Remove Menu...")
                os.system("cls")
                continue
            else:
                print("\033[1;31mInvalid Option\033[0m")
        except ValueError:
            print("\033[1;31mInvalid Input\033[0m")
        input("\nPress Enter to return to Remove Menu...")

# [ Function 5 ] To Handle Storage Capacity and Hazard Alerts
def view_storage_and_safety_alerts():
    global storage_capacity
    os.system("cls")
    print("\033[34m▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\033[0m")
    print("\033[1;34mSTORAGE & SAFETY ALERTS\033[0m")
    print("\033[34m▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\033[0m\n")

    total = get_total_storage()
    print(f"Current Storage Used: {total} kg / {storage_capacity} kg")
    if total > storage_capacity * 0.8:
        print("\033[1;31mWARNING: Storage exceeds 80% capacity!\033[0m")
    if total >= storage_capacity:
        print("\033[1;31mCRITICAL: Storage is FULL!\033[0m")

    alerts = check_hazard_alerts()
    if alerts:
        print("\n\033[1;31mHAZARDOUS ITEMS STORED LONGER THAN 30 DAYS:\033[0m")
        display_items(alerts)
    else:
        print("\n\033[1;32mNo urgent hazard alerts.\033[0m")

    print("\n\033[1;33m[ 1 ] Change Storage Capacity\033[0m")
    print("\033[1;33m[ 2 ] Back to Main Menu\033[0m")
    while True:
        try:
            sub_choice = int(input("\n\033[1;34mEnter Option: \033[0m"))
            if sub_choice == 1:
                new_capacity = int(input("\nEnter new storage capacity (kg): "))
                if new_capacity > 0:
                    storage_capacity = new_capacity
                    try:
                        with open("config.json", "w") as f:
                            json.dump({"storage_capacity": new_capacity}, f)
                    except:
                        pass
                    print("\033[1;32mStorage capacity updated successfully.\033[0m")
                else:
                    print("\033[1;31mCapacity must be positive!\033[0m")
            elif sub_choice == 2:
                break
            else:
                print("\033[1;31mInvalid Option\033[0m")
        except ValueError:
            print("\033[1;31mInvalid Input\033[0m")
    input("\nPress Enter to return...")

# [ Function 6 ] To Generate Report
def generate_summary_report():
    global storage_capacity
    os.system("cls")
    print("\033[34m▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\033[0m")
    print("\033[1;34mGENERATING REPORT...\033[0m")
    print("\033[34m▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\033[0m\n")

    all_items = []
    try:
        with open("items.json", "r") as file:
            for line in file:
                if line.strip():
                    all_items.append(json.loads(line))
    except FileNotFoundError:
        print("\033[1;31mNo data found.\033[0m")
        input("\nPress Enter...")
        return
    total_weight_all = sum(item["item_weight"] for item in all_items)
    total_fee_all = sum(item["item_weight"] * item["recycling_fee"] for item in all_items)
    processed = len([item for item in all_items if item["status"].lower() != "stored"])

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
    report_filename = f"AEWMS_Report_{timestamp}.txt"

    report = f"""GREEN LANTERN CORPS AEWMS REPORT
    Generated on: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    ======================================
    Total Items: {len(all_items)}       
    Total Weight Collected: {total_weight_all} kg
    Total Recycling Fees: LKR {total_fee_all:.2f}
    Processed Items: {processed}
    Current Storage Capacity: {storage_capacity} kg
    ======================================
    """
    # Generating Report as TXT file
    with open(report_filename, "w") as f:
        f.write(report)
    print(f"\033[1;32mReport generated successfully as {report_filename}\033[0m")
    input("\nPress Enter...")

# STARTUP ALERTS !
storage_capacity = load_storage_capacity()
alerts = check_hazard_alerts()
total_storage = get_total_storage()
storage_warning = total_storage > storage_capacity * 0.8

if alerts or storage_warning:
    os.system("cls")
    print("\033[1;31m▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\033[0m")
    print("\033[1;31m      WARNING ! ! ! \033[0m")
    print("\033[1;31m▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\033[0m")
    if alerts:
        print("\033[1;31mWARNING: HAZARDOUS ITEMS OLDER THAN 30 DAYS DETECTED!\033[0m")
        print("Please check Storage & Safety Alerts menu.")
        display_items(alerts)
        print("")
    if storage_warning:
        print("\033[1;31mWARNING: STORAGE EXCEEDS 80% CAPACITY!\033[0m")
        print(f"Current Usage: {total_storage} kg / {storage_capacity} kg")
        print("Please manage storage to avoid adding new items.")
        print("")
    input("\nPress Enter to continue to menu...")

# MAIN MENU
while True:
    os.system("cls")
    print(menu)

    # Live inline alerts calculation inside main loop
    total_storage = get_total_storage()
    if total_storage > storage_capacity * 0.8:
        print("\033[1;31mWARNING: Storage exceeds 80% capacity! (" + str(total_storage) + "/" + str(
            storage_capacity) + " kg)\033[0m")

    hazard_alerts = check_hazard_alerts()
    if hazard_alerts:
        print("\033[1;31mWARNING: Hazardous items stored longer than 30 days detected!\033[0m")
        print("\033[1;31mGo to menu [5] for details.\033[0m")

    try:
        choice = int(input("\033[1;35mEnter a number: \033[0m"))
        if choice == 1: # For Add new E-waste Items Menu
            add_new_waste_item()
        elif choice == 2: # For View ALl E-waste Items Menu
            view_and_search_items()
        elif choice == 3: # For Update E-waste Item Details Menu
            update_item_details()
        elif choice == 4: # For Remove E-Waste Items Menu
            remove_e_waste_item()
        elif choice == 5: # For Storage Alerts Menu
            view_storage_and_safety_alerts()
        elif choice == 6: # For Generate Reports Menu
            generate_summary_report()
        elif choice == 7: # For Exit The Program
            print("\033[1;32mThank you for using Green Lantern Corps AEWMS. Data saved.\033[0m")
            break
        else:
            os.system("cls")
            print("\033[1;31mInvalid Input! Enter a choice between 1 and 7.\033[0m")
            input("\nPress Enter...")
    except ValueError:
        print("\033[1;31mInvalid Input\033[0m")
        input("\nPress Enter...")