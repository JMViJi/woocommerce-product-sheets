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
### Obtaining WooCommerce API Keys

To obtain the API keys for your WooCommerce store, follow these steps:

1. Log in to your WooCommerce store's WordPress admin dashboard.
2. Go to **WooCommerce > Settings**.
3. Click on the **Advanced** tab, then select **REST API**.
4. Click the **Add Key** button.
5. Fill in the **Description** (e.g., "Product Manager Script").
6. Select the **User** you want to generate the key for in the **User** field.
7. Set **Permissions** to **Read/Write**.
8. Click the **Generate API Key** button.
9. You will be shown a **Consumer Key** and a **Consumer Secret**. Copy these keys and paste them into your `.env` file as `CONSUMER_KEY` and `CONSUMER_SECRET`, respectively.

### Obtaining WordPress Application Passwords

To obtain the application passwords for your WordPress site, follow these steps:

1. Log in to your WordPress admin dashboard.
2. Go to **Users > Profile**.
3. Scroll down to the **Application Passwords** section.
4. Enter a name for the new application password (e.g., "Product Manager Script") and click **Add New Application Password**.
5. A new password will be generated (Example: XXXX XXXX XXXX XXXX XXXX XXXX). Copy this password and use it as `WORDPRESS_PASSWORD` in your `.env` file.
6. Your WordPress username should be used as `WORDPRESS_USER` in the `.env` file.
   
## Usage

Ensure you have the product data in a CSV file located in the `data` folder. You also need a `template.svg` file in the `templates` folder to style the product sheet, and desired fonts in the `fonts` folder.

Run the main script to generate and upload the product sheets:

```bash
python main.py
