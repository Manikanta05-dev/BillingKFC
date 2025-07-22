# KFC Restaurant Billing System

A modern, KFC-branded restaurant billing system built with **Flask**, **SQLite**, and pure **CSS** (no Bootstrap). This project provides a beautiful, responsive, and fully functional billing and menu management web app for restaurants, themed after KFC.

![KFC Banner](static/D-PR00002167-prod.webp)

## Features

- **KFC-Themed UI/UX**: Custom CSS, KFC colors, fonts, and real KFC food images.
- **Menu Management**: Add, view, and display menu items with images and prices.
- **Bill Creation**: Create bills with customer info, table number, and select menu items in a grid layout.
- **Bill Summary**: Real-time calculation of subtotal, tax, and total using JavaScript.
- **Bill List & View**: View all bills and detailed bill breakdowns.
- **Admin Dashboard**: See today's bills, revenue, and active menu items.
- **No Bootstrap**: 100% custom CSS for layout, buttons, cards, and tables.
- **Local Images**: All food images are stored in the `static/` directory for fast, reliable loading.

## Screenshots

![Menu Page](static/CHKZINGER.jpeg)

## Setup Instructions

1. **Clone the repository:**
   ```sh
   git clone https://github.com/Manikanta05-dev/BillingKFC.git
   cd BillingKFC
   ```
2. **Create a virtual environment (optional but recommended):**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Run the app:**
   ```sh
   python app.py
   ```
5. **Open in your browser:**
   Visit [http://localhost:5000](http://localhost:5000)

## Project Structure

```
BillingKFC/
├── app.py
├── config.py
├── requirements.txt
├── restaurant.db
├── static/
│   ├── CHKZINGER.jpeg
│   ├── BIGSAVE.jpeg
│   ├── D-PR00002167-prod.webp
│   ├── ...
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── menu.html
│   ├── create_bill.html
│   ├── bill_list.html
│   ├── bill_view.html
│   ├── admin.html
└── README.md
```

## Credits
- KFC branding and food images are for demonstration purposes only. This project is **not affiliated with KFC Corporation**.
- Built with [Flask](https://flask.palletsprojects.com/) and [SQLite](https://www.sqlite.org/).

## License
This project is for educational/demo use only. Not for commercial use. 