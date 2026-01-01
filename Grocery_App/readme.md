****🛒 Grocery Tracker Application****

**📌 Project Overview**

The Grocery Tracker is a full-stack web application designed to help users manage their monthly grocery purchases. Users can add, update, delete, mark groceries as bought, and analyze purchase patterns through interactive analytics.

The application demonstrates:

1. Clean backend API design
2. Database abstraction
3. Streamlit UI state management
4. Real-world CRUD + analytics use cases

**🏗️ Architecture**

1. Streamlit UI
   |
   |  (REST API calls using requests)


2. FastAPI Backend
   |
   |  (Database helper functions)
   

3. MySQL Database

**Project Architecture**

    grocery_app/
    
    │
    ├── app.py                     # Main Streamlit entry point
    
    ├── add_update_groceries.py    # Grocery CRUD UI logic
    
    ├── grocery_analytics.py       # Analytics & visualizations
    
    │
    ├── server.py                  # FastAPI backend
    
    ├── db_helper.py               # Database access layer
    
    │
    └── README.md

**⚙️ Features**

**🧾 Grocery Management**

1. Add groceries

2. Update grocery details

3. Delete groceries

4. Mark groceries as bought

5. Month & year-based filtering

**📊 Analytics**

1. Total / Bought / Pending items

2. Bought percentage

3. Unique products & places

4. Top 5 frequently bought items

5. Place-wise breakdown

6. Monthly item trends

## ⚠️ Limitations

While the Grocery Tracker project demonstrates end-to-end development, there are a few limitations to be aware of:

1. **Single-user design**
   - The current app does not support multiple users or authentication.
   - All data is stored in a single database without role-based access.

2. **Local deployment**
   - Both FastAPI and Streamlit need to run locally.
   - Not yet optimized for cloud deployment or production scalability.

3. **No category-wise analytics**
   - Analytics are limited to total counts, percentage bought, and place/item frequency.
   - Product categories (e.g., fruits, dairy, snacks) are not considered.

4. **Basic UI design**
   - Streamlit UI is functional but lacks advanced interactive features or mobile-specific optimizations beyond CSS tweaks.

5. **Performance with large datasets**
   - Designed for moderate data sizes.
   - May slow down with very large grocery histories or heavy analytics computation.

6. **No notifications/reminders**
   - The app cannot notify users of pending items or weekly grocery trends.

9. **No cloud DB integration**
   - Currently uses local MySQL only.
   - Migrating to cloud DB (AWS RDS, etc.) would require configuration changes.
