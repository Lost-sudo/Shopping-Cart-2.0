import sqlite3

conn = sqlite3.connect('shoppingcart.db')

c = conn.cursor()

# c.execute("""CREATE TABLE "users" (
#             "ID" INTEGER NOT NULL,
#             "username" VARCHAR(50) NOT NULL,
#             "password" VARCHAR(50) NOT NULL,
#             "shoppingcart" TEXT NOT NULL,
#             PRIMARY KEY("ID" AUTOINCREMENT)
#             )""")

# c.execute("""CREATE TABLE "items" (
#             "ITEMS_ID" INTEGER NOT NULL,
#             "item_name" VARCHAR(100) NOT NULL,
#             "item_price" VARCHAR(100) NOT NULL,
#             PRIMARY KEY ("ITEMS_ID" AUTOINCREMENT)
#             )""")

c.execute("""CREATE TABLE "purchase_history" (
            "SOLD_ID" INTEGER NOT NULL,
            "item_name" VARCHAR(100) NOT NULL,
            "item_price" FLOAT NOT NULL,
            PRIMARY KEY ("SOLD_ID" AUTOINCREMENT)  
            )""")

# items = [
#     ("T-shirt", "19.99"),
#     ("Jeans", "39.99"),
#     ("Sneakers", "59.99"),
#     ("Dress", "29.99"),
#     ("Watch", "99.99"),
#     ("Sunglasses", "24.99"),
#     ("Backpack", "34.99"),
#     ("Hoodie", "44.99"),
#     ("Shorts", "14.99"),
#     ("Boots", "69.99"),
#     ("Skirt", "27.99"),
#     ("Hat", "12.99"),
#     ("Jacket", "54.99"),
#     ("Sandals", "19.99"),
#     ("Blouse", "24.99"),
#     ("Socks", "4.99"),
#     ("Scarf", "9.99"),
#     ("Pants", "34.99"),
#     ("Belt", "14.99"),
#     ("Gloves", "7.99"),
#     ("Shirt", "19.99"),
#     ("Earrings", "29.99"),
#     ("Necklace", "39.99"),
#     ("Ring", "49.99"),
#     ("Purse", "59.99"),
#     ("Wallet", "24.99"),
#     ("Tie", "14.99"),
#     ("Coat", "74.99"),
#     ("Umbrella", "9.99"),
#     ("Suit", "99.99"),
#     ("Trousers", "44.99"),
#     ("Blazer", "64.99"),
#     ("Vest", "29.99"),
#     ("Bowtie", "8.99"),
#     ("Dress shoes", "49.99"),
#     ("Running shoes", "54.99"),
#     ("High heels", "39.99"),
#     ("Flats", "29.99"),
#     ("Flip flops", "9.99"),
#     ("Swimsuit", "34.99"),
#     ("Tunic", "24.99"),
#     ("Leggings", "19.99"),
#     ("Cardigan", "44.99"),
#     ("Pajamas", "29.99"),
#     ("Slippers", "14.99"),
#     ("Sweater", "39.99"),
#     ("Handbag", "49.99"),
#     ("Messenger bag", "54.99"),
#     ("Tote bag", "39.99"),
#     ("Shoulder bag", "29.99"),
#     ("Clutch", "19.99"),
#     ("Crossbody bag", "34.99"),
#     ("Briefcase", "59.99"),
#     ("Laptop bag", "44.99"),
#     ("Travel bag", "69.99"),
#     ("Duffel bag", "49.99"),
#     ("Weekender bag", "64.99"),
#     ("Satchel", "54.99"),
#     ("Bucket bag", "39.99"),
#     ("Hobo bag", "34.99"),
#     ("Trolley bag", "79.99"),
#     ("Wristlet", "19.99"),
#     ("Backpack purse", "44.99"),
#     ("Fanny pack", "29.99"),
#     ("Bum bag", "24.99"),
#     ("Tennis shoes", "49.99"),
#     ("Clogs", "34.99"),
#     ("Loafers", "39.99"),
#     ("Moccasins", "29.99"),
#     ("Oxfords", "54.99"),
#     ("Espadrilles", "44.99"),
#     ("Mules", "39.99"),
#     ("Platform shoes", "59.99"),
#     ("Wedge sandals", "49.99"),
#     ("Ankle boots", "39.99"),
#     ("Chelsea boots", "69.99"),
#     ("Combat boots", "54.99"),
#     ("Cowboy boots", "79.99"),
#     ("Rain boots", "34.99"),
#     ("Snow boots", "59.99"),
#     ("Hiking boots", "74.99"),
#     ("Work boots", "89.99"),
#     ("Dress boots", "64.99"),
#     ("Chukka boots", "49.99"),
#     ("Lace-up boots", "54.99"),
#     ("Riding boots", "59.99"),
#     ("Thigh-high boots", "69.99"),
#     ("Over-the-knee boots", "79.99"),
#     ("Peep-toe boots", "49.99"),
#     ("Stiletto boots", "69.99"),
#     ("Pointed-toe boots", "54.99"),
#     ("Round-toe boots", "59.99"),
#     ("Square-toe boots", "64.99"),
#     ("Almond-toe boots", "54.99")
# ]
#
# for item in items:
#     c.execute("INSERT INTO items (item_name, item_price) VALUES (?, ?)", item)
#
# conn.commit()
#
# conn.close()
