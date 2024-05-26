# Product Sheets for eCommerce in WordPress using WooCommerce

This project generates product sheets in PDF format from CSV data and uploads them to a WordPress website, creating a new tab called "Documentation" that links to the product sheets.

## Requirements

- Python 3.x
- pip

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/JMViJi/woocommerce-product-sheets.git
    cd woocommerce-product-sheets
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1. Rename the `.env2` file to `.env` and edit the WooCommerce and WordPress credentials with your own credentials:
    ```bash
    mv .env2 .env
    ```

2. Open the `.env` file in a text editor and update the following variables:
    ```plaintext
    WOO_URL=https://your-woocommerce-url.com
    CONSUMER_KEY=your_consumer_key
    CONSUMER_SECRET=your_consumer_secret
    WORDPRESS_URL=https://your-woocommerce-url.com/wp-json/wp/v2/media
    WORDPRESS_USER=your_wordpress_user
    WORDPRESS_PASSWORD=your_wordpress_password
    ```

## Usage

Ensure you have the product data in a CSV file located in the `data` folder. You also need a `template.svg` file in the `templates` folder to style the product sheet, and desired fonts in the `fonts` folder.

Run the main script to generate and upload the product sheets:

```bash
python main.py
